import audioread
import numpy as np
import torch
from IPython.display import Audio
from hifi_gan_bwe import BandwidthExtender
import soundfile as sf
import os
import subprocess


# 適用するモデルの選択
# https://github.com/brentspell/hifi-gan-bwe#pretrained-models
model = BandwidthExtender.from_pretrained("hifi-gan-bwe-05-cd9f4ca-vctk-48kHz")
input_path = './output_no_silence.mp3'

def convert_audio(input_file):
    # 入力ファイルの拡張子を取得
    original_extension = os.path.splitext(input_file)[1]

    # ファイル名 (拡張子なし)
    base_name = os.path.splitext(input_file)[0]

    # .mov フォーマットに変換
    mov_file = f"{base_name}.wav"
    cmd = ["ffmpeg", "-i", input_file, mov_file, "-y"]
    subprocess.run(cmd, check=True)
    return base_name, original_extension

def reconvert_audio(base_name, original_extension):
    converted_file = f"output{original_extension}"
    cmd = ["ffmpeg", "-i", f"{base_name}.wav", converted_file, "-y"]
    subprocess.run(cmd, check=True)

base_name, original_extension = convert_audio(input_path)

print(base_name, original_extension)
# 音声の読み込み
with audioread.audio_open(f"{base_name}.wav") as f:
    print(f.channels, f.samplerate, f.duration)
    sample_rate = f.samplerate
    x = (np.hstack([np.frombuffer(b, dtype=np.int16) for b in f]).reshape([-1, f.channels]).astype(np.float32) / 32767.0)

# モデルの適用
with torch.no_grad():
    y = np.stack([model(torch.from_numpy(x), sample_rate) for x in x.T]).T

sf.write(f"{base_name}.wav", y, samplerate=int(model.sample_rate))

reconvert_audio(base_name, original_extension)