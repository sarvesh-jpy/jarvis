import customtkinter as ctk
import speech_recognition as sr
import pywhatkit
import pyautogui
import threading
import time

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class SARVESH(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. WINDOW SETUP
        self.title("SARVESH AI ")
        self.geometry("400x500")
        self.resizable(False, False)

        # 2. UI ELEMENTS
        # Title
        self.title_label = ctk.CTkLabel(self, text="🤖 SARVESH assistant", font=("Roboto Medium", 24))
        self.title_label.pack(pady=20)

        # Status Display
        self.status_label = ctk.CTkLabel(self, text="Ready to help.", font=("Arial", 14), text_color="gray")
        self.status_label.pack(pady=10)

        # The Big Mic Button
        self.listen_btn = ctk.CTkButton(self, text="🎙️ TAP TO SPEAK", height=50, width=200, 
                                        font=("Arial", 16, "bold"), command=self.start_listening)
        self.listen_btn.pack(pady=20)

        # Log Box (Scrollable)
        self.log_box = ctk.CTkTextbox(self, width=350, height=200)
        self.log_box.pack(pady=10)
        self.log_box.insert("0.0", ">> System Initialized...\n")
        self.log_box.configure(state="disabled") # Make read-only

    def log_message(self, message):
        """Updates the text box safely"""
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f">> {message}\n")
        self.log_box.see("end") # Auto-scroll to bottom
        self.log_box.configure(state="disabled")

    def start_listening(self):
        """Starts the listening process in a separate background thread"""
        self.listen_btn.configure(state="disabled", text="👂 Listening...")
        self.status_label.configure(text="Listening...", text_color="#00FF00")
        
        # Start thread so window doesn't freeze
        threading.Thread(target=self.run_voice_command, daemon=True).start()

    def run_voice_command(self):
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                
                # Update UI to show processing
                self.status_label.configure(text="Processing...", text_color="orange")
                
                command = recognizer.recognize_google(audio).lower()
                self.log_message(f"You said: '{command}'")
                
                # EXECUTE COMMANDS
                self.execute_command(command)
                
            except sr.WaitTimeoutError:
                self.log_message("Timeout: No speech detected.")
            except sr.UnknownValueError:
                self.log_message("Error: Could not understand audio.")
            except Exception as e:
                self.log_message(f"Error: {e}")
            finally:
                # Reset UI buttons
                self.listen_btn.configure(state="normal", text="🎙️ TAP TO SPEAK")
                self.status_label.configure(text="Ready.", text_color="gray")

    def execute_command(self, command):
        if "play" in command:
            song = command.replace("play", "")
            self.log_message(f"Playing {song} on YouTube...")
            pywhatkit.playonyt(song)
            
        elif "open cmd" in command or "command prompt" in command:
            self.log_message("Opening Command Prompt...")
            pyautogui.press('win')
            time.sleep(1)
            pyautogui.write('cmd')
            time.sleep(0.5)
            pyautogui.press('enter')
            
        elif "open google" in command:
             self.log_message("Opening Google...")
             pywhatkit.search("Google")

        elif "open setting" in command or "windows" in command:
            self.log_message(" opening setting")
            pyautogui.press('win')
            time.sleep(1)
            pyautogui.write('setting')
            time.sleep(0.5)
            pyautogui.press('enter')
             
        else:
            self.log_message("Command not recognized.")

# --- RUN THE APP ---
if __name__ == "__main__":
    app = SARVESH()
    app.mainloop()