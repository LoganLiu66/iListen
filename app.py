import gradio as gr
import logging
import random
from utils import extract_audios, setup_logger


def download_audio(url_input, upload_input, mode, show_text):
    logging.info(f"Downloading audio from {url_input} or {upload_input} with mode {mode} and show_text {show_text}")
    success, status, audio_infos = extract_audios(url_input, upload_input)
    logging.info(f"Success: {success}, Status: {status}")

    if not success:
        return status, audio_infos, [], None, None, None, None, None, None, None, None
    
    if mode == "Random":
        shuffled_audio_infos = audio_infos.copy()
        random.shuffle(shuffled_audio_infos)
        batch_audio_list = [shuffled_audio_infos[i:i+3] for i in range(0, len(shuffled_audio_infos), 3)]
    else:
        batch_audio_list = [audio_infos[i:i+3] for i in range(0, len(audio_infos), 3)]
    
    batch_idx, audio1, audio2, audio3, text1, text2, text3 = obtain_audios(batch_audio_list, 0, show_text)
    logging.info(f"audio1: {audio1}, audio2: {audio2}, audio3: {audio3}, text1: {text1}, text2: {text2}, text3: {text3}")
    index = batch_idx * 3 + 1
    return f"Successfully extracted {len(audio_infos)} audios", audio_infos, batch_audio_list, index, len(audio_infos), audio1, audio2, audio3, text1, text2, text3


def obtain_audios(batch_audio_list, batch_idx, show_text):
    logging.info(f"Obtaining audios with show_text {show_text}, index: {batch_idx}")
    texts, audios = [""] * 3, [None] * 3
    batch_idx = batch_idx % len(batch_audio_list)
    batch_audios = batch_audio_list[batch_idx]
    logging.info(f"batch_audios: {batch_audios}")
    for i, audio_info in enumerate(batch_audios):
        audios[i] = audio_info[0]
        if show_text == "Yes":
            texts[i] = audio_info[1]
    return batch_idx, audios[0], audios[1], audios[2], texts[0], texts[1], texts[2]


def sample_audios(unvisited_audios, audio_infos, mode, show_text):
    logging.info(f"Sampling audios with mode {mode} and show_text {show_text}, unvisited_audios: {len(unvisited_audios)}")
    texts, audios = [""] * 3, [None] * 3
    if mode == "Random":
        sampled_audios = random.sample(list(unvisited_audios), min(3, len(unvisited_audios)))
        unvisited_audios = unvisited_audios - set(sampled_audios)
        for i, audio_idx in enumerate(sampled_audios):
            audios[i] = audio_infos[audio_idx][0]
            if show_text == "Yes":
                texts[i] = audio_infos[audio_idx][1]
            
    elif mode == "Sequential":
        sampled_audios = list(unvisited_audios)[:3]
        unvisited_audios = unvisited_audios - set(sampled_audios)
        for i, audio_idx in enumerate(sampled_audios):
            audios[i] = audio_infos[audio_idx][0]
            if show_text == "Yes":
                texts[i] = audio_infos[audio_idx][1]
    logging.info(f"sampled_audios: {sampled_audios}, unvisited_audios: {len(unvisited_audios)}")
    logging.info(f"audios: {audios}, texts: {texts}")
    return unvisited_audios, audios[0], audios[1], audios[2], texts[0], texts[1], texts[2]

def prev_audio(batch_audio_list, index, show_text):
    batch_idx = (int(index) - 1) // 3
    batch_idx, audio1, audio2, audio3, text1, text2, text3 = obtain_audios(batch_audio_list, batch_idx - 1, show_text)
    index = batch_idx * 3 + 1
    return index, audio1, audio2, audio3, text1, text2, text3

def next_audio(batch_audio_list, index, show_text):
    batch_idx = (int(index) - 1) // 3
    batch_idx, audio1, audio2, audio3, text1, text2, text3 = obtain_audios(batch_audio_list, batch_idx + 1, show_text)
    index = batch_idx * 3 + 1
    return index, audio1, audio2, audio3, text1, text2, text3


def index_reset(batch_audio_list, show_text):
    logging.info(f"Resetting with show_text {show_text}")
    batch_idx, audio1, audio2, audio3, text1, text2, text3 = obtain_audios(batch_audio_list, 0, show_text)
    index = batch_idx * 3 + 1
    return index, audio1, audio2, audio3, text1, text2, text3

def mode_reset(audio_infos, mode, show_text):
    logging.info(f"Resetting with mode {mode} and show_text {show_text}")
    if mode == "Random":
        shuffled_audio_infos = audio_infos.copy()
        random.shuffle(shuffled_audio_infos)
        batch_audio_list = [shuffled_audio_infos[i:i+3] for i in range(0, len(shuffled_audio_infos), 3)]
    else:
        batch_audio_list = [audio_infos[i:i+3] for i in range(0, len(audio_infos), 3)]
    batch_idx, audio1, audio2, audio3, text1, text2, text3 = obtain_audios(batch_audio_list, 0, show_text)
    index = batch_idx * 3 + 1
    return batch_audio_list, index, audio1, audio2, audio3, text1, text2, text3

def change_show_text(batch_audio_list, index, show_text):
    logging.info(f"Changing show_text to {show_text}, index: {index}")
    batch_idx = (int(index) - 1) // 3
    _, _, _, _, text1, text2, text3 = obtain_audios(batch_audio_list, batch_idx, show_text)
    return text1, text2, text3


def url_tab_select():
    return None


def upload_tab_select():
    return None


def main():
    with gr.Blocks() as demo:
        audio_infos = gr.State([])
        batch_audio_list = gr.State([])

        gr.Markdown("## iListen")
        gr.Markdown("A gradio app for English listening practice. Source audio can be any you interested in, like Youtube, Bilibili, or even your own audio files. This app will automatically download the audio using [yt-dlp](https://github.com/yt-dlp/yt-dlp) and split it into sentences using [whisperx](https://github.com/m-bain/whisperX). Then you can listen to the audio and practice your listening skills. 👉🏻[GitHub](https://github.com/loganliu66/iListen)👈🏻")
        gr.Markdown("NOTE: It's best to run this demo locally, as higging_face's ip may be blocked by YouTube to the point where it won't download the audio!")

        url_tab = gr.Tab("URL")
        upload_tab = gr.Tab("Upload")
        with url_tab:
            url_input = gr.Textbox(label="Audio URL", placeholder="Enter YouTube, Bilibili or direct audio URL")
            gr.Examples(
                examples=[
                    "https://paddlespeech.bj.bcebos.com/Parakeet/docs/demos/tacotron2_ljspeech_waveflow_samples_0.2/sentence_1.wav"
                ],
                inputs=[url_input]
            )
        with upload_tab:
            upload_input = gr.Audio(label="Upload Audio", type="filepath", sources="upload", format="mp3")
            gr.Examples(
                examples=[
                    "audios/cut_20250107_103715.wav"
                ],
                inputs=[upload_input]
            )

        extract_btn = gr.Button("Extract Audios")
        output_info = gr.Textbox(label="Output Info", value="")

        with gr.Row():
            mode = gr.Dropdown(label="Mode", choices=["Sequential", "Random"], value="Sequential")
            show_text = gr.Dropdown(label="Show Text", choices=["Yes", "No"], value="No")
        
        with gr.Row():
            prev_btn = gr.Button("Previous")
            next_btn = gr.Button("Next", variant="primary")
        with gr.Row():
            index = gr.Textbox(label="Index", value="")
            total_audios = gr.Textbox(label="Total Audios", value="")
            reset_btn = gr.Button("Reset")
        
        with gr.Row():
            audio1 = gr.Audio(label="Audio 1", type="filepath")
            audio2 = gr.Audio(label="Audio 2", type="filepath")
            audio3 = gr.Audio(label="Audio 3", type="filepath")
        
        with gr.Row():
            text1 = gr.Textbox(label="Text 1", type="text")
            text2 = gr.Textbox(label="Text 2", type="text")
            text3 = gr.Textbox(label="Text 3", type="text")
        
        extract_btn.click(
            fn=download_audio,
            inputs=[url_input, upload_input, mode, show_text],
            outputs=[output_info, audio_infos, batch_audio_list, index, total_audios, audio1, audio2, audio3, text1, text2, text3]
        )
        prev_btn.click(
            fn=prev_audio,
            inputs=[batch_audio_list, index, show_text],
            outputs=[index, audio1, audio2, audio3, text1, text2, text3]
        )
        next_btn.click(
            fn=next_audio,
            inputs=[batch_audio_list, index, show_text],
            outputs=[index, audio1, audio2, audio3, text1, text2, text3]
        )
        reset_btn.click(
            fn=index_reset,
            inputs=[batch_audio_list, show_text],
            outputs=[index, audio1, audio2, audio3, text1, text2, text3]
        )

        mode.change(
            fn=mode_reset,
            inputs=[audio_infos, mode, show_text],
            outputs=[batch_audio_list, index, audio1, audio2, audio3, text1, text2, text3]
        )

        show_text.change(
            fn=change_show_text,
            inputs=[batch_audio_list, index, show_text],
            outputs=[text1, text2, text3]
        )

        url_tab.select(
            fn=url_tab_select,
            inputs=[],
            outputs=[url_input]
        )

        upload_tab.select(
            fn=upload_tab_select,
            inputs=[],
            outputs=[upload_input]
        )
        
    demo.launch()

if __name__ == '__main__':
    setup_logger()
    main()