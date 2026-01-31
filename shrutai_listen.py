import whisper
import pyaudio
import numpy as np
import warnings
import os

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU")

# UPGRADE: 'base' is better for noisy rooms than 'tiny'
print("Upgrading ShrutAi's brain to 'Base' model...")
model = whisper.load_model("base") 

def start_listening():
    CHUNK = 2048
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    THRESHOLD = 1000 # Keep this at 1000 for iPhone

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=0, frames_per_buffer=CHUNK)
    
    print("\n>>> ShrutAi is listening via iPhone...")
    
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            rms = np.sqrt(np.mean(np.square(np.frombuffer(data, dtype=np.int16).astype(np.float32))))
            
            if rms < THRESHOLD:
                continue 

            audio_frames = [np.frombuffer(data, dtype=np.int16)]
            for _ in range(0, int(RATE / CHUNK * 2.0)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_frames.append(np.frombuffer(data, dtype=np.int16))
            
            audio_data = np.concatenate(audio_frames).astype(np.float32) / 32768.0
            result = model.transcribe(audio_data, language="en", fp16=False)
            text = result['text'].lower().strip()

            # THE 'CALIBRATED' LIST
            triggers = ["shrut", "shroud a.i", "a.i" "shrutai", "sure they", "true day", "should they", "show it", "shrut ai"]

            if any(word in text for word in triggers):
                print(f"\n✨ [WAKE WORD DETECTED]: '{text}'")
                os.system('say "Yes Smera?"') # Mac will talk back
                # This is where we will eventually put the 'Brain' logic
                print(">>> Waiting for your command...")
            else:
                if len(text) > 3:
                    print(f"Heard but ignored: ({text})")

        except Exception as e:
            continue

if __name__ == "__main__":
    start_listening()