import speech_recognition as sr
import pywhatkit
import pyautogui
import time

def listen_to_voice():
    # 1. SETUP MICROPHONE
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n🎤 LISTENING... (Speak now!)")
        
        # Adjust for background noise automatically
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            # Listen for 5 seconds max
            audio = recognizer.listen(source, timeout=5)
            print("⏳ Processing...")
            
            # Convert Voice to Text
            command = recognizer.recognize_google(audio).lower()
            print(f"🗣️ You said: '{command}'")
            return command
            
        except sr.UnknownValueError:
            print("❌ I didn't catch that.")
            return ""
        except sr.RequestError:
            print("❌ Internet error for voice recognition.")
            return ""
        except Exception as e:
            print(f"❌ Error: {e}")
            return ""

def execute_command(command):
    if "play" in command:
        # LOGIC: Remove the word "play" and search the rest
        song = command.replace("play", "")
        print(f"🎵 Playing {song} on YouTube...")
        pywhatkit.playonyt(song)
        
    elif "open cmd" in command or "command prompt" in command:
        print("💻 Opening Command Prompt...")
        # AUTOMATION: Press Windows Key -> Type 'cmd' -> Press Enter
        pyautogui.press('win')
        time.sleep(1) # Wait for menu to pop up
        pyautogui.write('cmd')
        time.sleep(0.5)
        pyautogui.press('enter')
        
    elif "exit" in command or "stop" in command:
        print("👋 Goodbye!")
        return False
    
    else:
        print("❓ Command not recognized. Try 'Play Believer' or 'Open CMD'")
        
    return True

# --- MAIN LOOP ---
if __name__ == "__main__":
    print("🤖 JARVIS ACTIVATED")
    print("-------------------------")
    print("Try saying: 'Play Believer' or 'Open Command Prompt'")
    
    running = True
    while running:
        command = listen_to_voice()
        if command:
            running = execute_command(command)