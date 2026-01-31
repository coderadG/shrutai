import pyaudio
import wave

# --- SETTINGS ---
CHUNK = 1024            # How many samples to 'grab' at once
FORMAT = pyaudio.paInt16 # 16-bit resolution (standard)
CHANNELS = 1            # Mono audio
RATE = 16000            # Sample rate (16kHz is standard for AI)
RECORD_SECONDS = 10     # How long to record
OUTPUT_FILE = "raw_mic_output.wav"

# --- STARTUP ---
p = pyaudio.PyAudio()

# Open the 'Stream' (the live pipe to your mic)
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print(f"* Recording for {RECORD_SECONDS} seconds... SPEAK NOW!")

frames = [] # This is our temporary storage for the chunks

# --- THE CHUNKING LOOP ---
# We calculate how many chunks we need to read to hit our seconds limit
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK) # Grab one chunk of raw bytes
    frames.append(data)       # Add it to our list

print("* Done recording.")

# --- CLEANUP ---
stream.stop_stream()
stream.close()
p.terminate()

# --- SAVE TO FILE ---
wf = wave.open(OUTPUT_FILE, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames)) # Glue all chunks together and save
wf.close()

print(f"* File saved as {OUTPUT_FILE}")