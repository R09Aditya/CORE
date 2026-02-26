import customtkinter as ctk
import time
import subprocess
import pyttsx3
from PIL import Image
from customtkinter import CTkImage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def speak(text):
    def _speak():
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for v in voices:
            if "male" in v.name.lower():
                engine.setProperty('voice', v.id)
                break
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()

import threading

app = ctk.CTk()
app.geometry("520x470")
app.title("Initializing CORE")
app.resizable(False, False)
app.attributes('-topmost', True)

border_frame = ctk.CTkFrame(app, width=500, height=470, corner_radius=10, border_color="#751fd7", border_width=2)
border_frame.pack(padx=10, pady=(15, 0))
border_frame.pack_propagate(False)

image = Image.open("CORE.png")
image = image.resize((320, 320), Image.Resampling.LANCZOS)
logo_image = CTkImage(light_image=image, dark_image=image, size=(320, 320))
logo = ctk.CTkLabel(border_frame, image=logo_image, text="")
logo.pack(pady=(20, 0))

title = ctk.CTkLabel(border_frame, text="Initializing CORE...", font=("Arial", 28, "bold"))
title.pack(pady=(10, 4))

progress = ctk.CTkProgressBar(border_frame, width=420)
progress.pack(pady=(10, 4))
progress.set(0)

status_label_var = ctk.StringVar()
status_label_var.set("Starting systems...")
status_label = ctk.CTkLabel(border_frame, textvariable=status_label_var, font=("Arial", 20))
status_label.pack(pady=(10, 4))

loading_steps = [
    "Loading CORE modules...",
    "Initializing quantum encryptors...",
    "Verifying zero-knowledge protocols...",
    "Launching virtual ignition chamber...",
    "Connecting to YubiKey driver...",
    "Calibrating launch sequence...",
    "Encrypting telemetry data..."
]

def is_yubikey_inserted():
    try:
        result = subprocess.run(['ykman', 'info'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return "Serial number" in result.stdout
    except Exception:
        return False

def show_countdown_screen():
    for widget in border_frame.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(border_frame, text="Initiating Launch Countdown", font=("Arial", 28, "bold"))
    title.pack(pady=(20, 10))

    countdown_label = ctk.CTkLabel(border_frame, text="T-10", font=("Arial", 48, "bold"), text_color="red")
    countdown_label.pack(pady=(10, 20))

    status = ctk.CTkLabel(border_frame, text="All systems nominal.", font=("Arial", 18))
    status.pack(pady=(0, 20))

    def run_countdown():
        for i in range(10, 0, -1):
            countdown_label.configure(text=f"T-{i}")
            speak(f"T minus {i}")
            app.update_idletasks()
            time.sleep(1)
        show_success_screen()

    app.after(100, run_countdown)

def show_success_screen():
    for widget in border_frame.winfo_children():
        widget.destroy()

    speak("Launch successful. Mission deployed.")

    ctk.CTkLabel(border_frame, text="Launch Successful!", font=("Arial", 32, "bold"), text_color="green").pack(pady=30)
    ctk.CTkLabel(border_frame, text="Mission has been authorized and deployed.", font=("Arial", 20)).pack(pady=10)
    ctk.CTkButton(border_frame, text="Exit", command=app.destroy, font=("Arial", 20), fg_color="#00aa00", hover_color="#006600", text_color="white", width=180, height=50).pack(pady=30)

def show_yubikey_verification_screen(name1, name2):
    for widget in border_frame.winfo_children():
        widget.destroy()

    speak("Final authentication required. Insert and tap both YubiKeys.")

    ctk.CTkLabel(border_frame, text="YubiKey Verification", font=("Arial", 28, "bold")).pack(pady=(15, 5))
    ctk.CTkLabel(border_frame, text="Insert & tap YubiKeys to continue", font=("Arial", 18)).pack(pady=(0, 15))

    status_var = ctk.StringVar()
    status_var.set("Awaiting YubiKey inputs...")
    status_label = ctk.CTkLabel(border_frame, textvariable=status_var, font=("Arial", 16), text_color="yellow")
    status_label.pack(pady=(0, 10))

    def check_taps():
        if is_yubikey_inserted():
            status_var.set("YubiKey detected! Access granted.")
            status_label.configure(text_color="green")
            show_countdown_screen()
        else:
            status_var.set("Insert your YubiKey to continue...")
            status_label.configure(text_color="orange")

    ctk.CTkButton(border_frame, text=f"Scan YubiKey - {name1.title()}", command=check_taps, font=("Arial", 18), width=240, height=50).pack(pady=10)
    ctk.CTkButton(border_frame, text=f"Scan YubiKey - {name2.title()}", command=check_taps, font=("Arial", 18), width=240, height=50).pack(pady=10)

    ctk.CTkButton(border_frame, text="Abort", command=app.destroy, font=("Arial", 18), fg_color="#684ba9", hover_color="#b30000", text_color="white", width=180, height=45).pack(pady=(10, 0))

def show_commander_prompt():
    for widget in border_frame.winfo_children():
        widget.destroy()

    speak("Please enter both commander identities to proceed.")

    title = ctk.CTkLabel(border_frame, text="Commander Identification", font=("Arial", 30, "bold"))
    title.pack(pady=(10, 5))

    subtitle = ctk.CTkLabel(border_frame, text="Secure Login Terminal", font=("Arial", 22))
    subtitle.pack(pady=(0, 10))

    name_entry_1 = ctk.CTkEntry(border_frame, width=340, font=("Arial", 18), placeholder_text="Commander 1 Name")
    name_entry_1.pack(pady=(5, 5))

    name_entry_2 = ctk.CTkEntry(border_frame, width=340, font=("Arial", 18), placeholder_text="Commander 2 Name")
    name_entry_2.pack(pady=(5, 10))

    error_label = ctk.CTkLabel(border_frame, text="", font=("Arial", 16), text_color="red")
    error_label.pack()

    info_label = ctk.CTkLabel(border_frame, text="Both identities are required to authorize control.\nPlease ensure correctness.", font=("Arial", 16), justify="center")
    info_label.pack(pady=(10, 10))

    def proceed():
        name1 = name_entry_1.get().strip().lower()
        name2 = name_entry_2.get().strip().lower()
        valid_names = {"akshat jain", "aditya sharma"}
        if name1 in valid_names and name2 in valid_names and name1 != name2:
            show_code_screen(name1, name2)
        else:
            error_label.configure(text="Invalid commander names. Access Denied.")
            speak("Access denied. Invalid commander names.")

    proceed_btn = ctk.CTkButton(border_frame, text="Authenticate", command=proceed, font=("Arial", 20), width=180, height=50)
    proceed_btn.pack(pady=(10, 10))

    abort_btn = ctk.CTkButton(border_frame, text="Abort", command=app.destroy, font=("Arial", 20), fg_color="#7843c3", hover_color="#b30000", text_color="white", width=180, height=50)
    abort_btn.pack(pady=(5, 0))

def show_code_screen(name1, name2):
    for widget in border_frame.winfo_children():
        widget.destroy()

    speak("Enter final access codes for both commanders.")

    label = ctk.CTkLabel(border_frame, text="Enter Access Codes", font=("Arial", 28, "bold"))
    label.pack(pady=(20, 10))

    code1 = ctk.CTkEntry(border_frame, width=300, font=("Arial", 18), placeholder_text=f"Access Code: {name1.title()}")
    code1.pack(pady=10)

    code2 = ctk.CTkEntry(border_frame, width=300, font=("Arial", 18), placeholder_text=f"Access Code: {name2.title()}")
    code2.pack(pady=10)

    status_info = ctk.CTkLabel(border_frame, text="Final authentication layer.", font=("Arial", 16))
    status_info.pack(pady=15)

    def verify():
        entered1 = code1.get().strip()
        entered2 = code2.get().strip()
        if (entered1 == "07012010" and entered2 == "21082008") or (entered1 == "21082008" and entered2 == "07012010"):
            show_yubikey_verification_screen(name1, name2)
        else:
            status_info.configure(text="Access Denied. Check your codes.", text_color="red")
            speak("Access denied. Incorrect codes.")

    auth_btn = ctk.CTkButton(border_frame, text="Verify Codes", command=verify, font=("Arial", 20), width=180, height=50)
    auth_btn.pack(pady=(5, 10))

    abort_btn = ctk.CTkButton(border_frame, text="Abort", command=app.destroy, font=("Arial", 20), fg_color="#6141b9", hover_color="#b30000", text_color="white", width=180, height=50)
    abort_btn.pack(pady=(0, 0))

def load_app():
    for i, step in enumerate(loading_steps):
        status_label_var.set(step)
        speak(step)
        progress.set((i + 1) / len(loading_steps))
        app.update_idletasks()
        time.sleep(1.2)
    show_commander_prompt()

app.after(100, load_app)
app.mainloop()
