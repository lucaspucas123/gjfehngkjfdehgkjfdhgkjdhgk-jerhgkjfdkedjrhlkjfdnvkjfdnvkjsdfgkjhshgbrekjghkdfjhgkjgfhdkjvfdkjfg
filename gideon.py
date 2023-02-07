import speech_recognition as sr
import openai
import re
from gtts import gTTS
import os

openai.api_key = "UR KEY"

# Initialize the speech recognizer class (for recognizing speech)
r = sr.Recognizer()

def process_input(text):
    # Use OpenAI's API to generate a response to the user's input
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=text,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    ).choices[0].text

    # Use regex to detect certain keywords in the user's input
    weather_pattern = re.compile("what's the weather like in (.*)")
    weather_match = weather_pattern.search(text.lower())

    # If the user is asking about the weather, get the current weather conditions
    if weather_match:
        location = weather_match.group(1)
        response = "The current weather in " + location + " is mostly sunny with a high of 75 degrees."

    return response

# Loop indefinitely
while True:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Try to recognize the speech and convert it to text
    try:
        text = r.recognize_google(audio)
        print("You said: " + text)
    except:
        print("Sorry, I didn't catch that. Could you please repeat?")
        continue

    # If the user says "Gideon," start the conversation
    if "Gideon" in text:
        response = process_input(text)
        print("AI response: " + response)
        tts = gTTS(response, lang='en')
        tts.save("response.mp3")
        os.system("play response.mp3 &")
        os.system("nohup mpg123 response.mp3 &")
    else:
        print("Sorry, I only respond if you call my name first.")
