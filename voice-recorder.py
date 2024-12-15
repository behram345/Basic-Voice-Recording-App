import pyaudio
import wave
import tkinter as tk
from tkinter import messagebox
import threading

# Ses kaydını başlatan fonksiyon
def start_recording():
    global recording
    recording = True
    messagebox.showinfo("Başlat", "Ses kaydı başladı...")
    # Ses kaydı için parametreler
    audio_format = pyaudio.paInt16  # Ses formatı
    channels = 1  # Mono ses
    rate = 44100  # 44.1kHz örnekleme oranı
    chunk = 1024  # Veri blok boyutu
    record_seconds = 10  # Kaydın süresi (saniye)

    # Pyaudio başlatma
    audio = pyaudio.PyAudio()
    stream = audio.open(format=audio_format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    frames = []

    for _ in range(0, int(rate / chunk * record_seconds)):
        if not recording:
            break
        data = stream.read(chunk)
        frames.append(data)

    # Kaydı bitir ve dosyaya kaydet
    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open("kayit.wav", 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(audio_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    messagebox.showinfo("Tamamlandı", "Ses kaydı tamamlandı ve kayit.wav dosyasına kaydedildi.")

# Ses kaydını durduran fonksiyon
def stop_recording():
    global recording
    recording = False
    messagebox.showinfo("Durduruldu", "Ses kaydı durduruldu.")

# GUI kısmı
def run_gui():
    root = tk.Tk()
    root.title("Ses Kayıt Uygulaması")

    global recording
    recording = False

    # Başlat butonu
    start_button = tk.Button(root, text="Kaydı Başlat", width=20, command=lambda: threading.Thread(target=start_recording).start())
    start_button.pack(pady=20)

    # Durdur butonu
    stop_button = tk.Button(root, text="Kaydı Durdur", width=20, command=stop_recording)
    stop_button.pack(pady=20)

    # GUI'yi başlat
    root.mainloop()

# Uygulamayı başlat
run_gui()
