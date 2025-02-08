import tkinter as tk
from tkinter import scrolledtext
import threading
import ollama
from typing import Any, Dict, List
from backend import build_conversation_prompt, generate_response  # Reuse the shared functions from backend.py

class ChatFrontend:
    """
    A simple tkinter‑based chat frontend.
    """
    def __init__(self, master: tk.Tk, client: ollama.Client, model: str) -> None:
        self.master = master
        self.client = client
        self.model = model
        master.title(f"Chat with {model}")  # Set the window title to the model name
        
        # Chat display area.
        self.chat_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', width=80, height=20)
        self.chat_area.pack(padx=10, pady=10)
        
        # Frame for input field and send button.
        input_frame = tk.Frame(master)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        self.entry = tk.Entry(input_frame, width=70)
        self.entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        self.conversation_history: List[str] = []
    
    def append_message(self, message: str) -> None:
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, message + "\n\n")  # Add an empty line between messages
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)
    
    def send_message(self, event: tk.Event = None) -> None:
        user_input: str = self.entry.get().strip()
        if not user_input:
            return
        self.append_message(f"You: {user_input}")
        self.entry.delete(0, tk.END)
        
        # Disable entry while waiting for a response.
        self.entry.configure(state='disabled')
        self.send_button.configure(state=tk.DISABLED)
        
        # Indicate that the AI is thinking
        self.append_message("Assistant is thinking...")
        
        prompt: str = build_conversation_prompt(self.conversation_history, user_input)
        threading.Thread(target=self.get_response, args=(user_input, prompt), daemon=True).start()
    
    def get_response(self, user_text: str, prompt: str) -> None:
        response: str = generate_response(self.client, self.model, prompt)
        self.master.after(0, self.update_response, user_text, response)
    
    def update_response(self, user_text: str, response: str) -> None:
        # Remove the "Assistant is thinking..." message
        self.chat_area.configure(state='normal')
        self.chat_area.delete("end-3l", "end-1l")
        self.chat_area.configure(state='disabled')
        
        self.append_message(f"Assistant: {response}")
        self.conversation_history.append(f"User: {user_text}")
        self.conversation_history.append(f"Assistant: {response}")
        self.entry.configure(state='normal')
        self.send_button.configure(state=tk.NORMAL)
        self.entry.focus_set() 