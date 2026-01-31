import numpy as np
import soundfile as sf
from pyrnnoise import RNNoise

# 1. Load audio
audio, sr = sf.read("raw_mic_output.wav")
print(f"Input: {audio.dtype}, range=[{audio.min():.4f}, {audio.max():.4f}]")

# 2. Convert to int16
audio_int16 = (audio * 32767).astype(np.int16)
print(f"Converted: {audio_int16.dtype}, range=[{audio_int16.min()}, {audio_int16.max()}]")

# Save this to test it plays
sf.write("test_before_rnn.wav", audio_int16, sr, subtype='PCM_16')
print("Saved test_before_rnn.wav - TRY PLAYING THIS FIRST")

# 3. Process with RNN
denoiser = RNNoise(sample_rate=sr)
denoised_chunks = []

print("\nProcessing chunks...")
chunk_count = 0
for speech_prob, denoised_frame in denoiser.denoise_chunk(audio_int16):
    chunk_count += 1
    if chunk_count <= 5:  # Print first 5 chunks
        # Handle speech_prob as array
        prob_mean = np.mean(speech_prob) if hasattr(speech_prob, 'mean') else speech_prob
        print(f"  Chunk {chunk_count}: speech_prob_mean={prob_mean:.3f}, "
              f"output_range=[{denoised_frame.min()}, {denoised_frame.max()}]")
    denoised_chunks.append(denoised_frame)

print(f"Total chunks processed: {chunk_count}")

# 4. Combine
cleaned = np.concatenate(denoised_chunks)
print(f"\nFinal output: {cleaned.dtype}, range=[{cleaned.min()}, {cleaned.max()}]")

# Check if output is basically silence
max_amplitude = np.abs(cleaned).max()
print(f"Max amplitude: {max_amplitude}")
if max_amplitude < 200:
    print("⚠️ WARNING: RNN output is too quiet - essentially silence!")

# Save without amplification first
sf.write("test_after_rnn_no_amp.wav", cleaned, sr, subtype='PCM_16')
print("Saved test_after_rnn_no_amp.wav")