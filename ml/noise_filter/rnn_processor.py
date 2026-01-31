import numpy as np
import soundfile as sf
from pyrnnoise import RNNoise
import wave

def process_with_rnn(input_path, output_path):
    # 1. Load the recording
    audio, sample_rate = sf.read(input_path)
    
    print(f"Original: dtype={audio.dtype}, range=[{audio.min()}, {audio.max()}]")
    
    # 2. Convert to int16
    audio_int16 = (audio * 32767).astype(np.int16)
    
    print(f"Converted: dtype={audio_int16.dtype}, range=[{audio_int16.min()}, {audio_int16.max()}]")
    
    # 3. Initialize RNN
    denoiser = RNNoise(sample_rate=sample_rate)
    
    print(f"RNN is analyzing {input_path}...")
    
    # 4. Process chunks
    denoised_chunks = []
    for speech_prob, denoised_frame in denoiser.denoise_chunk(audio_int16):
        denoised_chunks.append(denoised_frame)
    
    # 5. Combine
    cleaned_audio = np.concatenate(denoised_chunks)
    
    print(f"Output BEFORE amplification: range=[{cleaned_audio.min()}, {cleaned_audio.max()}]")
    
    # 6. AMPLIFY the output (this is the key fix!)
    # Calculate how much to amplify
    max_val = np.abs(cleaned_audio).max()
    if max_val > 0:
        amplification = 32767 / max_val * 0.8  # 0.8 to prevent clipping
        cleaned_audio = (cleaned_audio * amplification).astype(np.int16)
    
    print(f"Output AFTER amplification: range=[{cleaned_audio.min()}, {cleaned_audio.max()}]")
    
    # 7. Save as proper WAV
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(cleaned_audio.tobytes())
    
    print(f"✓ Success! Cleaned audio saved to {output_path}")

if __name__ == "__main__":
    process_with_rnn("raw_mic_output.wav", "shrutai_rnn_cleaned.wav")