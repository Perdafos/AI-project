import speech_recognition as sr
import asyncio
from edge_tts import Communicate
from playsound import playsound
from datetime import datetime
import random
import requests
import uuid
import os
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

# ========== TTS ==========
async def speak_async(text, voice="en-US-AriaNeural"):
    """Function to output speech with a specified voice"""
    output_file = f"output_{uuid.uuid4()}.mp3"
    tts = Communicate(text, voice=voice)
    await tts.save(output_file)
    try:
        playsound(output_file)
    finally:
        # Ensure the file is deleted immediately after playback
        try:
            os.remove(output_file)
        except Exception as e:
            print(f"Could not delete temp file: {e}")
        
def speak(text, voice="en-US-AriaNeural"):
    """Function to output speech with a specified voice"""
    asyncio.run(speak_async(text, voice))

# ========== LM Studio ==========
def ask_lmstudio(prompt):
    url = "http://localhost:1234/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "model": "lmstudio",  # Biarkan LM Studio pilih model yang aktif
        "messages": [
            {"role": "system", "content": "You are a helpful voice assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        print("LM Studio response:", result)
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error contacting LM Studio: {e}"

# ========== LISTEN ==========
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        
        try:
            command = r.recognize_google(audio, language="en-US")
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
            return ""
        except sr.RequestError:
            speak("Unable to connect to the speech recognition service.")
            return ""

# ========== NEWS ==========
def get_news():
    api_key = os.getenv("NEWSAPI_API_KEY")  # Load API key from environment variable
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_data = response.json()
        articles = news_data.get("articles", [])
        
        if articles:
            top_article = articles[0]
            title = top_article.get("title", "No title")
            desc = top_article.get("description", "No description")
            return f"Here is the latest news: {title}. {desc}"
        else:
            return "Sorry, I couldn't find any news at the moment."
    except Exception as e:
        return f"An error occurred while fetching the news: {str(e)}"
    
# ========== WEATHER ==========
def get_weather():
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")  # Load API key from environment variable
    city = "Malang,ID"  # Lokasi: Malang, Indonesia
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=id"

    try:
        response = requests.get(url)
        
        # Mengecek error 401 jika terjadi masalah dengan API Key
        if response.status_code == 401:
            return "Error: API Key tidak valid. Silakan cek API Key Anda."
        elif response.status_code != 200:
            return f"Error {response.status_code}: Terjadi masalah saat mengambil data cuaca."
        
        data = response.json()
        main_weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Mengambil nama kota dan cuaca saat ini
        weather_report = f"Cuaca di Malang saat ini: {main_weather}, suhu {temp}°C, kelembapan {humidity}%, kecepatan angin {wind_speed} m/s."
        
        return weather_report
    except requests.exceptions.RequestException as e:
        return f"Terjadi kesalahan saat mengambil data cuaca: {e}"

# Panggil fungsi untuk melihat hasil cuaca
print(get_weather())

# ========== MAIN ==========
def main():
    speak("Welcome Sir!.")

    while True:
        command = listen()

        if "hello" in command:
            speak("Hello! How can I assist you today?")
        
        elif "weather" in command:
            speak("Fetching the weather for Malang, Jawa Timur...")
            weather_info = get_weather()
            speak(weather_info, voice="id-ID-ArdiNeural")  # Use Indonesian voice for weather info
        
        elif "time" in command:
            current_time = datetime.now().strftime("%H:%M")
            speak(f"The current time is {current_time}.")
        
        elif "date" in command:
            current_date = datetime.now().strftime("%A, %d %B %Y")
            speak(f"Today is {current_date}.")
        
        elif "joke" in command:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "Why don't skeletons fight each other? They don't have the guts!"
            ]
            speak(random.choice(jokes))
        
        elif "calculate" in command:
            speak("Please say the calculation you want to perform.")
            calc_command = listen()
            try:
                result = eval(calc_command)
                speak(f"The result is {result}.")
            except Exception:
                speak("Sorry, I couldn't perform the calculation.")
        
        elif "news" in command:
            speak("Fetching the latest news...")
            news = get_news()
            speak(news)
        
        elif "motivation" in command:
            quotes = [
                "The only way to do great work is to love what you do. - Steve Jobs",
                "Success is not the key to happiness. Happiness is the key to success. - Albert Schweitzer",
                "Believe you can and you're halfway there. - Theodore Roosevelt"
            ]
            speak(random.choice(quotes))
        
        elif "write" in command:
            speak("What should I write?")
            text_to_write = listen()
            if text_to_write:
                speak("The text has been noted.")
            else:
                speak("I didn't catch what you want me to write.")
                
        elif "chat" in command or "question" in command or "ask" in command:
            speak("What would you like to ask?")
            user_input = listen()
            if user_input:
                speak("Okay, let me check that for you.")
                response = ask_lmstudio(user_input)
                speak(response)

        elif "turn off now" in command:
            speak("Goodbye!")
            break
        
        elif "thanks" in command:
            speak("You're welcome!")

if __name__ == "__main__":
    main()
