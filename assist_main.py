import speech_recognition as sr
import joblib
import pandas as pd
from llm_response import get_response_from_llm
from ml_model_current import collect_data
from basic_input_handler import handle_basic_inputs
from range_query_handler import handle_range_query
import random

def listen_to_user():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    greetings = [
        "Hey there! How can I assist with your EV today?",
        "Hello! Hope you're doing well. What would you like to check about your EV?",
        "Hi! Let's optimize your EV ride. Ask away!"
    ]
    print(random.choice(greetings))

    with mic as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)

    try:
        query = recognizer.recognize_google(audio)
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return "I couldn't catch that. Could you please repeat?"
    except sr.RequestError as e:
        return f"Error with voice recognition: {e}"

def detect_intent(query):
    if any(word in query for word in ["range", "how far", "can i reach", "travel", "distance"]):
        return "range_query"
    elif any(word in query for word in ["ac", "air conditioner", "load", "weight", "passengers"]):
        return "basic_input"
    else:
        return "unknown"

def assistant_main():
    query = listen_to_user()

    if "repeat" in query or "error" in query:
        print(query)
        return

    intent = detect_intent(query)

    if intent == "basic_input":
        response = handle_basic_inputs(query)
        print(response)

    elif intent == "range_query":
        prediction, details = handle_range_query(query)
        llm_reply = get_response_from_llm(prediction, details, query)
        print(llm_reply)

    else:
        print("I'm here to help you with your EV range and setup. Try asking about range or vehicle settings.")