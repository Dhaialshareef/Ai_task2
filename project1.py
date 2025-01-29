import speech_recognition as sr
import openai
import pyttsx3
import os

# إعداد مفتاح API
openai.api_key = os.getenv("OPENAI_API_KEY")

# دالة لتحويل النص إلى صوت
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1)
    engine.say(text)
    engine.runAndWait()


def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak now...")
        try:
            # تحديد وقت الاستماع (مثلاً 5 ثوانٍ)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="en-US")
            print(f"User input: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


def chat_with_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error during API communication: {e}")
        return None


if __name__ == "__main__":
    user_input = speech_to_text()
    if user_input:
        chat_response = chat_with_gpt(user_input)
        if chat_response:
            print(f"Model response: {chat_response}")
            text_to_speech(chat_response)

