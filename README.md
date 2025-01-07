# iListen

<div align="center">
    <img src="./images/iListen.png" alt="iListen" width="200">
</div>

<strong>iListen</strong>: A gradio app for English listening practice. Source audio can be any you interested in, like Youtube, Bilibili, or even your own audio files. This app will automatically download the audio using [yt-dlp](https://github.com/yt-dlp/yt-dlp) and split it into sentences using [whisperx](https://github.com/m-bain/whisperX). Then you can listen to the audio and practice your listening skills.
#### 👉🏻[iListen Demo on HuggingFace](https://huggingface.co/spaces/loganliu66/iListen)👈🏻 👉🏻[iListen Demo on GitHub](https://github.com/loganliu66/iListen)👈🏻 

## Usage

```bash
git clone https://github.com/loganliu66/iListen.git
cd iListen
pip install -r requirements.txt
python app.py
```

## Features

- [x] Download audio URL(Youtube, Bilibili, Wave URL) using [yt-dlp](https://github.com/yt-dlp/yt-dlp).
- [x] Sentence-level Segmentation using [whisperx](https://github.com/m-bain/whisperX).
- [x] Two listening modes: Random and Sequential.
- [x] CPU/GPU support.

## TODO

- [ ] Add more audio sources.

## Note

- The text from whisper is not always accurate.
- The audio and text may not be fully aligned.
- The audio is not always downloaded successfully due to blocked IP by Youtube or Bilibili.
- If you want to use this app on MacOS, please build [openfst1.8.3](https://www.openfst.org/twiki/bin/view/FST/WebHome) manually (refer to [mac_build_openfst.sh](mac_build_openfst.sh)) and install [pynini2.1.6](https://www.openfst.org/twiki/bin/view/GRM/Pynini) by `conda install -c conda-forge pynini` and then install [WeTextProcessing 1.0.4.1](https://github.com/WeTextProcessing/WeTextProcessing).

## Acknowledge

- [whisperx](https://github.com/m-bain/whisperX)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
