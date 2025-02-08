import tkinter as tk
from tkinter import scrolledtext
import threading
import ollama
from typing import Any, Dict, List
from frontend import ChatFrontend
from backend import build_conversation_prompt, generate_response, choose_mode, choose_model

def main_cli(client: ollama.Client, model: str) -> None:
    """
    Run an interactive CLI chat session.
    """
    print("Interactive Deepseek‑R1 Chat (CLI Mode). Type 'exit' to quit.\n")
    conversation_history: List[str] = []
    while True:
        question: str = input("Your question: ")
        if question.lower() in ("exit", "quit"):
            print("Exiting interactive chat.")
            break
        prompt: str = build_conversation_prompt(conversation_history, question)
        print("\nFetching response...\n")
        response: str = generate_response(client, model, prompt)
        print("Response:")
        print(response + "\n")
        conversation_history.append(f"User: {question}")
        conversation_history.append(f"Assistant: {response}")

def main() -> None:
    """
    Main entry point: ask for conversation mode and model choice, then start the appropriate interface.
    """
    print("Welcome to Deepseek‑R1 Chat!")
    mode: str = choose_mode()
    client = ollama.Client()
    selected_model_name: str = choose_model(client)
    
    if mode == "cli":
        main_cli(client, selected_model_name)
    else:
        root = tk.Tk()
        app = ChatFrontend(root, client, selected_model_name)
        root.mainloop()

if __name__ == "__main__":
    main() 