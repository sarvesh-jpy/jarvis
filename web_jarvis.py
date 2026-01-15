import streamlit as st
import speech_recognition as sr
import pywhatkit
import pyautogui
import time
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

# Custom CSS to make it look futuristic
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #00FF00;
    }
    .stButton>button {
        background-color: #00FF00;
        color: black;
        border-radius: 12px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. VOICE FUNCTIONS (Reuse your logic) ---
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_placeholder.info("🎤 Listening... Speak now!")
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            status_placeholder.warning("⏳ Processing...")
            command = recognizer.recognize_google(audio).lower()
            return command
        except:
            return ""

def execute(command):
    response = ""
    if "play" in command:
        song = command.replace("play", "")
        response = f"🎵 Playing **{song}** on YouTube..."
        pywhatkit.playonyt(song)
        
    elif "open cmd" in command or "command prompt" in command:
        response = "💻 Opening **Command Prompt**..."
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write('cmd')
        time.sleep(0.5)
        pyautogui.press('enter')
        
    elif "open google" in command:
        response = "🌐 Opening **Google**..."
        pywhatkit.search("Google")

    else:
        response = f"❓ Command '{command}' not recognized."
    
    return response

# --- 3. THE USER INTERFACE ---
st.title("🤖 Jarvis Voice Commander")
st.write("Control your PC with your voice.")

# Create placeholders for dynamic updates
status_placeholder = st.empty()
result_placeholder = st.empty()

# The Big Button
if st.button("🎙️ TAP TO SPEAK"):
    # 1. Listen
    user_command = listen()
    
    if user_command:
        # 2. Show what you said
        st.success(f"🗣️ You said: **{user_command}**")
        
        # 3. Execute
        ai_response = execute(user_command)
        result_placeholder.markdown(f"### {ai_response}")
    else:
        status_placeholder.error("❌ Didn't catch that. Try again.")

# Footer
st.markdown("---")
st.caption("Powered by Python & Streamlit")