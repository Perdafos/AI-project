Before running the program, make sure you have installed all the required dependencies, such as speech_recognition, edge_tts, playsound, requests, and other libraries as needed. Also, create a .env file in your project directory to store the API Key used. Add NEWSAPI_API_KEY to fetch news data, and OPENWEATHERMAP_API_KEY for weather information.

If you want to use the AI-based question and answer feature, make sure the LM Studio server is running and can be accessed via http://localhost:1234.

Once everything is ready, run the main Python file (project.py) via the terminal or IDE of your choice. The program will greet you with a voice and start listening to commands given via the microphone.

To use the available features, simply say commands such as: “Weather” to get weather information in Malang, “News” to find out the latest news, “Time” or “Date” to ask the current time or date, “Joke” to listen to jokes, “Calculate” to do calculations, and “Chat” or “Ask” to ask the AI ​​something. If you want to close the program, simply say “Turn off now”.

The AI ​​will respond to all your commands using Text-to-Speech (TTS) technology, so that the answers are given in the form of voice. Make sure your microphone is working properly, because the system relies on voice input to receive commands. If there is an error in the API Key or there is a connection problem, the AI ​​will provide an appropriate error message.
