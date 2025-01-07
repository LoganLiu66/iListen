import hashlib
import logging
import numpy as np
import spaces
import torch
import whisperx
import yt_dlp
from pathlib import Path
from pydub import AudioSegment
from tn.english.normalizer import Normalizer

device = "cuda" if torch.cuda.is_available() else "cpu"
batch_size = 8
sr = 16000
asr_model = whisperx.load_model("base.en", device=device, compute_type="float32", download_root="models")
tn_model = Normalizer(cache_dir="models/tn")
align_model, metadata = whisperx.load_align_model(language_code='en', device=device, model_dir="models")


@spaces.GPU
def extract_audios(url, upload):
    # download audio
    if upload:
        audio_file = upload
    else:
        success, reason, audio_file = download_audio(url)
        if not success:
            return False, reason, []

    audio = whisperx.load_audio(audio_file)

    id = Path(audio_file).stem
    logging.info("Transcribing...")
    # Each element in result['segments'] including multiple sentences, depended on the vad model
    result = asr_model.transcribe(audio, batch_size=batch_size)
    segments = result["segments"]
    logging.info("Normalizing...")
    for segment in segments:
        segment['text'] = tn_model.normalize(segment['text'])
    logging.info("Aligning...")
    # After align, each element in result['segments'] including only one sentence
    result = whisperx.align(segments, align_model, metadata, audio, device, return_char_alignments=False)
    segments = result["segments"]

    output_dir = f'output/downloaded_audios/{id}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    audio_infos = []
    for i, segment in enumerate(segments):
        logging.info(segment)
        begin = segment['start']
        end = segment['end']
        text = segment['text']
        segment_audio = audio[int(begin * sr): int(end * sr)]
        segment_audio = (segment_audio * 32767).astype(np.int16)
        audio_segment = AudioSegment(
            segment_audio.tobytes(), 
            frame_rate=sr,
            sample_width=2,
            channels=1
        )
        audio_path = f'{output_dir}/{id}_{str(i).zfill(4)}.mp3'
        audio_segment.export(audio_path, format="mp3")
        audio_infos.append((audio_path, text))
        logging.info(f'Successfully exported {audio_path}')
    return True, "Successfully extracted", audio_infos


def download_audio(url):
    """
    Can be used for downloading audio from youtube、bilibili or wave url.
    """
    id = hashlib.sha256(url.encode()).hexdigest()[:20]
    ydl_opts = {
        'outtmpl': f'output/downloaded_audios/{id}.%(ext)s',
        'format': 'bestaudio[ext=m4a]/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            output_file = f'output/downloaded_audios/{id}.m4a'
            open('output/logs/downloaded_audios.txt', 'a').write(f"{id}|{url}\n")
            logging.info(f"Successfully downloaded {url} and saved to {output_file}")
            return True, "Successfully downloaded", output_file
    except Exception as e:
        logging.info(f"Error downloading audio: {e}")
        return False, f"Error downloading audio: {e}", None


def setup_logger():
    Path('output/logs').mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename='output/logs/gradio.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def test():
    extract_audios('https://www.youtube.com/watch?v=Yv_S7KrOlfk', None)

if __name__ == '__main__':
    test()