import hashlib
import logging
import numpy as np
import yt_dlp
from pathlib import Path
from pydub import AudioSegment
from pywhispercpp.model import Model

model = Model(models_dir='models/whisper', model='base.en')


def extract_audios(url, upload):
    # download audio
    if upload:
        audio_file = upload
    else:
        success, reason, audio_file = download_audio(url)
        if not success:
            return False, reason, []

    audio = AudioSegment.from_file(audio_file)
    audio.set_channels(1)

    id = Path(audio_file).stem
    logging.info("Transcribing...")
    segments = model.transcribe(audio_file)
    output_dir = f'output/downloaded_audios/{id}'
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    audio_infos = []
    for i, segment in enumerate(segments):
        logging.info(segment)
        begin = segment.t0
        end = segment.t1
        text = segment.text
        segment_audio = audio[begin * 10: end * 10 - 100]    
        audio_path = f'{output_dir}/{id}_{str(i).zfill(4)}.mp3'
        segment_audio.export(audio_path, format='mp3')
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