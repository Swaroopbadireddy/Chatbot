import streamlit as st
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import time

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
player = pyttsx3.init()

# Configure the Google Generative AI API
API_KEY = "AIzaSyD8qE6ACuvl5Gpd3Dw5IKiB-hkrLQDCHFU"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# Streamlit UI
st.title("Continuous Voice Bot with Generative AI")

if "listening" not in st.session_state:
    st.session_state.listening = False

# Button to start/stop listening
if st.button("Start Listening"):
    st.session_state.listening = not st.session_state.listening

if st.session_state.listening:
    st.write("Listening... (Say 'stop' to end)")
    
    # Continuous listening loop
    while st.session_state.listening:
        with sr.Microphone() as input_device:
            try:
                # Listen for the user's command
                voice_content = listener.listen(input_device, timeout=3, phrase_time_limit=3)
                text_command = listener.recognize_google(voice_content)
                st.write("You said:", text_command)

                if text_command.lower() in ["stop", "quit", "exit", "bye"]:
                    st.write("Thank you, have a nice day... Bye!")
                    talk("Thank you and have a nice day.")
                    st.session_state.listening = False  # Stop listening
                else:
                    reply = voice_bot(text_command)
                    st.write("Voice Bot:", reply)
                    talk(reply)

            except sr.UnknownValueError:
                st.write("Sorry, I could not understand the audio.")
            except sr.RequestError:
                st.write("Request to Google API failed.")
            except sr.WaitTimeoutError:
                st.write("Listening timed out, please try again.")

            # Streamlit requires a small delay to avoid freezing the UI
            time.sleep(1)
else:
    st.write("Click 'Start Listening' to begin.")

def voice_bot(prompt):
    response = model.generate_content(prompt)
    truncated_response = truncate_response(response.text, max_tokens=50)  # Truncate to 50 tokens
    return truncated_response

def truncate_response(text, max_tokens):
    tokens = text.split()
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return ' '.join(tokens)

def talk(text):
    player.say(text)
    player.runAndWait()
