import speech_recognition as sr 
from googletrans import Translator
import random
import time

words_db = {
    "easy": ["кот", "собака", "яблоко", "мама", "дом", "рыба", "чай", "лес"],
    "medium": ["школа", "банан", "дорога", "погода", "птица", "компьютер", "музыка"],
    "hard": ["технология", "произношение", "воображение", "путешествие", "библиотека"]
}

translator = Translator()
recognizer = sr.Recognizer()

def main_game_loop():
    """ 
    Основная логика игры 
    Счетчик очков и жизней добавлен вручную
    """
    points = 0
    lives = 5
    
    print("--- 🎮 STARTING THE TRANSLATION GAME 🎮 ---")
    print("--- Добро пожаловать в игру, я тебе говорю слово , а ты должен перевести на ангийский! ---")
    level = input("Выбери уровень сложности (easy/medium/hard): ").lower().strip()
    
    if level not in words_db:
        print("⚠️ Ошибка! Ставим легкий уровень по умолчанию.")
        level = "easy"

    words_list = words_db[level].copy()
    random.shuffle(words_list)

    while lives > 0 and words_list:
        target_word = words_list.pop()
        
        try:
            translation = translator.translate(target_word, src='ru', dest='en')
            correct_answer = translation.text.lower().strip()
        except Exception as e:
            print(f"🌐 Ошибка сети: {e}")
            continue

        print(f"\n👉 ТВОЕ СЛОВО: {target_word.upper()}")
        print("🎤 У тебя 5 секунд, говори...")

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio_data = recognizer.listen(source, timeout=5)
                
                user_say = recognizer.recognize_google(audio_data, language="en-EN").lower().strip()
                print(f"👂 Ты сказал: '{user_say}'")

                if user_say == correct_answer:
                    points += 10
                    print(f"✅ В точку! +10 очков! Текущий счет: {points} ⭐️")
                else:
                    lives -= 1
                    print(f"❌ Мимо! Правильно: {correct_answer}. Жизней: {lives} 💔")

            except sr.UnknownValueError:
                lives -= 1
                print(f"🤷‍♂️ Не понял тебя. Минус жизнь. Осталось: {lives}")
            except Exception as e:
                print(f"🧨 Упс, что-то пошло не так: {e}")

    print("\n" + "="*40)
    if lives > 0:
        print(f"🏆 ПОБЕДА! Ты набрал {points} очков! 😎")
    else:
        print(f"💀 GAME OVER. Твой результат: {points} 🕹")
    print("="*40)

if __name__ == "__main__":
    main_game_loop() 