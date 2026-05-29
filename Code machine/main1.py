import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

duration = 5 
sample_rate = 44100

print("Говорите...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
sd.wait()

print(">>> Запись завершена, теперь распознаём...")
wav.write("output.wav", sample_rate, recording)

print("-" * 30)
print("Выберите язык перевода:")
print("en - Английский")
print("es - Испанский")
print("it - Итальянский")
print("pl - Польский")
print("pt - Португальский")
print("-" * 30)

user_input = input("Введите код языка или название: ").strip().lower()

languages = {
    "английский": "en", "en": "en", "english": "en",
    "испанский": "es", "es": "es", "spanish": "es",
    "итальянский": "it", "it": "it", "italian": "it",
    "польский": "pl", "pl": "pl", "polish": "pl",
    "португальский": "pt", "pt": "pt", "portuguese": "pt"
}

target_lang = languages.get(user_input, "en")

recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio, language="ru-RU")
    print(f"Вы сказали: {text}")

    translator = Translator()
    translated = translator.translate(text, dest=target_lang)
    
    print(f"Перевод ({target_lang}): {translated.text}")

except sr.UnknownValueError:
    print("Ошибка: Речь не распознана")
except sr.RequestError:
    print("Ошибка: Проблемы с интернетом")
except Exception as e:
    print(f"Произошла ошибка: {e}")


