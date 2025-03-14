import speech_recognition as sr
import numpy as np
import cv2
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
from tkinter import ttk
import string
import os

class SignLanguageApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sign Language Translator")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add image display
        self.image = "signlang.png"
        img = Image.open(self.image)
        img = img.resize((400, 200), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(img)
        
        # Logo display
        self.logo_label = ttk.Label(self.main_frame, image=self.logo)
        self.logo_label.pack(pady=10)
        
        # Title
        self.title_label = ttk.Label(
            self.main_frame,
            text="Sign Language Translator",
            font=("Britannic Bold", 36, "bold")  # Changed font family, size, and weight
        )
        self.title_label.pack(pady=20)
        
        # Status frame
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=10)
        
        self.status_label = ttk.Label(
            self.status_frame,
            text="Status: Ready",
            font=("Helvetica", 12)
        )
        self.status_label.pack()
        
        # Display frame for sign language output
        self.display_frame = ttk.Frame(self.main_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        # Load microphone icon
        mic_icon = Image.open("mic_icon.png")  # Make sure this image exists in your project directory
        mic_icon = mic_icon.resize((40, 40), Image.LANCZOS)
        self.mic_photo = ImageTk.PhotoImage(mic_icon)
        
        # Center-aligned button frame
        self.center_button_frame = ttk.Frame(self.button_frame)
        self.center_button_frame.pack(expand=True)
        
        self.start_button = ttk.Button(
            self.center_button_frame,
            image=self.mic_photo,
            command=self.start_translation
        )
        self.start_button.pack(pady=5)
        
        self.stop_button = ttk.Button(
            self.center_button_frame,
            text="All Done!",
            command=self.root.quit
        )
        self.stop_button.pack(pady=5)
        
        # Initialize recognizer
        self.recognizer = sr.Recognizer()
        
        # Initialize word list
        self.isl_gif=['let me sing a kutty story','any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
                'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
                'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
                'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
                'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing', 
                'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
                'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
                'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
                'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
                'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
                'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
                'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
                'where is the bathroom', 'where is the police station', 'you are wrong','address','agra','ahemdabad', 'all', 'april', 'assam', 'august', 
                'australia', 'badoda', 'banana', 'banaras', 'banglore', 'bihar','bridge','cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 
                'coconut', 'crocodile','dasara', 'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 
                'gujrat', 'hello', 'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
                'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
                'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
                'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
                'voice', 'wednesday', 'weight','please wait for sometime','what is your mobile number','what are you doing','are you busy']
        
        self.arr = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        
        # Pre-load letter images
        self.letter_images = {}
        for char in self.arr:
            img_path = f'letters/{char}.jpg'
            img = Image.open(img_path)
            img = img.resize((200, 200), Image.LANCZOS)
            self.letter_images[char] = ImageTk.PhotoImage(img)
        
    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        self.root.update()
        
    def display_gif(self, gif_path):
        if hasattr(self, 'gif_label'):
            self.gif_label.destroy()
            
        self.gif_label = ImageLabel(self.display_frame)
        self.gif_label.pack(fill=tk.BOTH, expand=True)
        self.gif_label.load(gif_path)
        self.root.update()

        
    def display_letter(self, char):
        if hasattr(self, 'gif_label'):
            self.gif_label.destroy()
            
        letter_label = ttk.Label(self.display_frame, image=self.letter_images[char])
        letter_label.image = self.letter_images[char]
        letter_label.pack(pady=5)
        self.root.after(300, letter_label.destroy)

    def start_translation(self):
        self.update_status("Listening...")
        self.translate_audio()

    def translate_audio(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
            print("I am Listening")
            self.update_status("Listening...")
            try:
                audio = self.recognizer.listen(source)
                text = self.recognizer.recognize_google(audio).lower()
                print('You Said: ' + text)
                self.update_status(f'You Said: {text}')

                # Remove punctuation
                for c in string.punctuation:
                    text = text.replace(c, "")

                if text in ['goodbye', 'good bye', 'bye']:
                    print("oops!Time To say good bye")
                    self.update_status("Goodbye!")
                    self.root.quit()
                    return

                elif text in self.isl_gif:
                    self.display_gif(f'ISL_Gifs/{text}.gif')
                else:
                    for char in text:
                        if char in self.arr:
                            self.display_letter(char)
                            self.root.update()
                            self.root.after(300)

            except sr.UnknownValueError:
                print(" ")
                self.update_status("Could not understand audio")
            except sr.RequestError:
                self.update_status("Could not request results")
            except Exception as e:
                self.update_status(f"Error: {str(e)}")
            
            # Reset status after translation
            self.root.after(2000, lambda: self.update_status("Ready"))

class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        self.running = True

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.running = False
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if not self.frames or not self.running:
            return
        
        self.loc += 1
        self.loc %= len(self.frames)
        self.config(image=self.frames[self.loc])
        self.after(self.delay, self.next_frame)

if __name__ == "__main__":
    app = SignLanguageApp()
    app.root.mainloop()
