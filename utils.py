import os
from typing import BinaryIO

from pydub import AudioSegment


def save_audio(record_id: str, file: BinaryIO):
    if not os.path.exists('audio_files'):
        os.makedirs('audio_files')

    wav_path = f"audio_files/{record_id}.wav"

    with open(wav_path, "wb") as audio_file:
        audio_file.write(file.read())

    return wav_path


def convert_wav_to_mp3(record_id: str, wav_path: str):
    mp3_filename = f"{record_id}.mp3"
    mp3_path = f"audio_files/{mp3_filename}"

    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")

    return mp3_filename
