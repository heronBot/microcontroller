import numpy as np
import pyaudio
import threading
import time

volume = 1.0
fs = 44100
duration = 0.02
frequency = 200

new = time.time()
running = True
note = 200

t = np.linspace(0, duration, int(fs * duration), endpoint=False)  # Time array
samples = (np.sin(2 * np.pi * note * t) * volume).astype(np.float32)

stereo_samples = np.zeros((samples.size * 2,), dtype=np.float32)
stereo_samples[0::2] = samples
stereo_samples[1::2] = samples

p = pyaudio.PyAudio()  # Initialize PyAudio
stream = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True)

def digitalOne():
    global running,p,stream
    running = True
    
    p = pyaudio.PyAudio()  # Initialize PyAudio
    stream = p.open(format=pyaudio.paFloat32,
                    channels=2,
                    rate=fs,
                output=True)

    threading.Thread(target=on).start()

def digitalZero():
    global running
    running = False
    # Ensure the stream is stopped and closed properly
    stream.stop_stream()
    stream.close()
    p.terminate()

def on():
    while running:
        stream.write(stereo_samples.tobytes())


