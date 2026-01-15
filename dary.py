import customtkinter as ctk
import speech_recognition as sr
import pywhatkit
import pyautogui
import threading
import time

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

# THE NEW NAME TO WAKE IT UP
WAKE_WORD = "dary"

class DaryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. WINDOW SETUP
        self.title("DARY AI - Ultimate")
        self.geometry("400x600")
        self.resizable(False, False)
        
        # Variables
        self.is_listening = False
        self.always_on_mode = False

        # 2. UI ELEMENTS
        # Title
        self.title_label = ctk.CTkLabel(self, text="🤖 DARY", font=("Roboto Medium", 24))
        self.title_label.pack(pady=20)

        # Status Display
        self.status_label = ctk.CTkLabel(self, text="System Offline", font=("Arial", 14), text_color="gray")
        self.status_label.pack(pady=10)

        # Log Box (Scrollable)
        self.log_box = ctk.CTkTextbox(self, width=350, height=250)
        self.log_box.pack(pady=10)
        self.log_box.insert("0.0", ">> DARY System Initialized...\n")
        self.log_box.configure(state="disabled")

        # TOGGLE: Always On Mode
        self.switch_var = ctk.StringVar(value="off")
        self.mode_switch = ctk.CTkSwitch(self, text=f"Hands-Free Mode ('{WAKE_WORD}')", 
                                         command=self.toggle_mode, variable=self.switch_var, onvalue="on", offvalue="off")
        self.mode_switch.pack(pady=20)

        # Manual Button
        self.listen_btn = ctk.CTkButton(self, text="🎙️ TAP TO SPEAK", height=50, width=200, 
                                        font=("Arial", 16, "bold"), command=self.manual_listen)
        self.listen_btn.pack(pady=10)

    def log_message(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f">> {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def toggle_mode(self):
        if self.switch_var.get() == "on":
            self.always_on_mode = True
            self.status_label.configure(text=f"Listening for '{WAKE_WORD}'...", text_color="#00FF00")
            self.log_message(f"🟢 Hands-Free Enabled. Say '{WAKE_WORD}...'")
            # Start the infinite listening loop in background
            threading.Thread(target=self.background_listener, daemon=True).start()
        else:
            self.always_on_mode = False
            self.status_label.configure(text="Manual Mode", text_color="gray")
            self.log_message("🔴 Hands-Free Disabled.")

    def background_listener(self):
        """Infinite loop that listens for the Wake Word"""
        recognizer = sr.Recognizer()
        
        while self.always_on_mode:
            with sr.Microphone() as source:
                try:
                    # Quick listen
                    recognizer.adjust_for_ambient_noise(source, duration=0.5)
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    
                    # Convert to text
                    command = recognizer.recognize_google(audio).lower()
                    
                    # CHECK FOR WAKE WORD "DARY"
                    if WAKE_WORD in command:
                        self.log_message(f"⚡ Wake Word Detected: '{command}'")
                        # Remove "dary" and execute the rest
                        clean_command = command.replace(WAKE_WORD, "").strip()
                        self.execute_command(clean_command)
                    else:
                        print(f"Ignored: {command}") 
                        
                except sr.WaitTimeoutError:
                    pass 
                except sr.UnknownValueError:
                    pass 
                except Exception as e:
                    print(f"Error: {e}")

    def manual_listen(self):
        """Click-to-speak function"""
        self.listen_btn.configure(state="disabled", text="👂 Listening...")
        threading.Thread(target=self.run_single_voice_command, daemon=True).start()

    def run_single_voice_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                self.log_message(f"You said: '{command}'")
                self.execute_command(command)
            except:
                self.log_message("❌ Could not understand.")
            finally:
                self.listen_btn.configure(state="normal", text="🎙️ TAP TO SPEAK")

    def execute_command(self, command):
        if not command:
            return

        if "play" in command:
            song = command.replace("play", "")
            self.log_message(f"🎵 DARY is playing {song}...")
            pywhatkit.playonyt(song)
            
        elif "open cmd" in command or "command prompt" in command:
            self.log_message("💻 DARY is opening Command Prompt...")
            pyautogui.press('win')
            time.sleep(1)
            pyautogui.write('cmd')
            time.sleep(0.5)
            pyautogui.press('enter')

        elif "open setting" in command or "windows" in command:
            self.log_message(" DARY is opening setting")
            pyautogui.press('win')
            time.sleep(1)
            pyautogui.write('setting')
            time.sleep(0.5)
            pyautogui.press('enter')
            
        elif "open google" in command:
             self.log_message("🌐 DARY is opening Google...")
             pywhatkit.search("Google")
             
        elif "shutdown" in command:
            self.log_message("👋 DARY Shutting down...")
            self.quit()

# --- RUN ---
if __name__ == "__main__":
    app = DaryApp()
    app.mainloop()