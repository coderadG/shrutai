import numpy as np 
import soundfile as sf
from scipy.signal import butter, lfilter
import subprocess
import noisereduce as nr
import io

# def decode_mp4_with_ffmpeg(mp4_path):
#     command = [
#         "ffmpeg",
#         "-i", mp4_path,
#         "-vn",           # Disable video (extra safety)
#         "-f", "wav",     # Force WAV container
#         "-ac", "1",      # Mono
#         "-ar", "16000",  # 16kHz
#         "pipe:1"         # Output to stdout
#     ]

#     # Use run() instead of Popen to ensure the buffer is fully captured
#     result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
#     if result.returncode != 0:
#         raise RuntimeError(f"FFmpeg failed: {result.stderr.decode()}")

#     # result.stdout now contains the full WAV file in bytes
#     audio, sr = sf.read(io.BytesIO(result.stdout))
#     return audio, sr

def bandpass_filter(audio,sr,low=300,high=3400):
    nyq = 0.5 * sr
    low /= nyq
    high /= nyq
    b, a = butter(4, [low, high], btype="band")
    return lfilter(b, a, audio)
# 1. Load
#audio, sr = decode_mp4_with_ffmpeg(r"C:\Users\user\Desktop\PROJECTS\ShrutAI\shrutai\ml\noise_filter\noisy_audio.mp4")

# 2. Pre-filter (The 'Broom')
# This removes sub-bass engine rumble that makes the audio "heavy"
filtered_basic = bandpass_filter(audio, sr)

# 3. Smart Noise Reduction (The 'Vacuum')
# This targets the traffic/static sitting behind the voice
cleaned_audio = nr.reduce_noise(y=filtered_basic, sr=sr, prop_decrease=0.85)

# 4. Save
sf.write("shrutai_final_output.wav", cleaned_audio, sr)