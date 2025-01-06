---
title: iListen
emoji: 🎧
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.9.1
app_file: app.py
pinned: false
license: other
---
# iListen

<div align="center">
    <img src="./images/iListen.png" alt="iListen" width="200">
</div>

<strong>iListen</strong>: A gradio app for English listening practice. Source audio can be any you interested in, like Youtube, Bilibili, or even your own audio files. This app will automatically download the audio using [yt-dlp](https://github.com/yt-dlp/yt-dlp) and split it into sentences using [faster-whisper](https://github.com/guillaumekln/faster-whisper). Then you can listen to the audio and practice your listening skills.
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
- [x] Sentence-level Segmentation using [faster-whisper](https://github.com/guillaumekln/faster-whisper).
- [x] Speech-to-Text with Whisper.
- [x] Two listening modes: Random and Sequential.

## TODO

- [ ] Add more audio sources.

## Note

- The text from whisper is not always accurate.
- The audio and text may not be fully aligned.
- The audio is not always downloaded successfully due to blocked IP by Youtube or Bilibili.

## Acknowledge

- [faster-whisper](https://github.com/guillaumekln/faster-whisper)
- [whisper](https://github.com/openai/whisper)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
