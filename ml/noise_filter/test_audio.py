import soundfile as sf
import numpy as np

# Check the input file
audio, sr = sf.read("raw_mic_output.wav")
print(f"Input file stats:")
print(f"  Sample rate: {sr}")
print(f"  Duration: {len(audio)/sr:.2f} seconds")
print(f"  Data type: {audio.dtype}")
print(f"  Min value: {audio.min()}")
print(f"  Max value: {audio.max()}")
print(f"  Mean absolute value: {np.abs(audio).mean()}")
print(f"  Shape: {audio.shape}")

if np.abs(audio).max() < 0.01:
    print("\ WARNING: Input audio is too quiet or silent!")
else:
    print("\n✓ Input audio has signal")