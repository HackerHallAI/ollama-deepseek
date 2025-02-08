from typing import Any, Dict, List
import ollama
import re

def build_conversation_prompt(history: List[str], question: str) -> str:
    """
    Build a conversational prompt by combining conversation history with the current question.
    """
    if history:
        conversation_context = "\n".join(history)
        return f"{conversation_context}\nUser: {question}\nAssistant:"
    else:
        return f"User: {question}\nAssistant:"

def generate_response(client: ollama.Client, model: str, prompt: str) -> str:
    """
    Generate a response using the chosen model via the Ollama python package.
    Post-processes the output to remove any '<think>...</think>' portion.
    """
    try:
        # Prepare the messages for the chat
        messages = [{"role": "user", "content": prompt}]
        
        # Enable streaming
        response = client.chat(model=model, messages=messages, stream=True)
        
        # Collect the streamed response
        full_response = ""
        for chunk in response:
            # Extract the content from the message attribute
            if hasattr(chunk, 'message') and hasattr(chunk.message, 'content'):
                full_response += chunk.message.content
                print(chunk.message.content, end='', flush=True)  # Print each chunk as it arrives
        
        # Use regex to remove the portion between <think> and </think>
        full_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()
        
        return full_response
    except Exception as e:
        print(f"Error during model invocation: {e}")
        return f"Error: {e}"

def choose_mode() -> str:
    """
    Prompt the user to choose between CLI and UI modes using a numbered selection.
    """
    options = ["CLI", "UI"]
    print("Choose conversation mode:")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        choice = input("Enter the number of your choice (1 for CLI, 2 for UI): ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index].lower()
        print("Invalid choice. Please enter 1 for CLI or 2 for UI.")

def choose_model(client: ollama.Client) -> str:
    """
    List available models using ollama.list() and allow the user to choose one.
    Falls back to a default list if necessary.
    """
    model_list = []
    try:
        # Use ollama.list() to get the available models.
        models_resp = ollama.list()  # Expected to return a dict with a "models" key
        if models_resp is None:
            raise Exception("No models found")
        for model in models_resp["models"]:
            print("Model dict:", model)
            # First try to use "model" key; if not present, fall back to "name"
            if "model" in model:
                model_list.append(model["model"])
            elif "name" in model:
                model_list.append(model["name"])
            else:
                print("Warning: Model dict has neither 'model' nor 'name' keys.")
    except Exception as e:
        print(f"Error retrieving model list: {e}")
        model_list = []

    print(model_list)
    
    # Fallback to a default list if no models are found.
    if not model_list:
        model_list = ["deepseek-r1"]

    print("Available models:")
    for i, mod in enumerate(model_list, 1):
        print(f"{i}. {mod}")
    choice = input("Choose a model by number or name (default deepseek-r1): ").strip()
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(model_list):
            return model_list[index]
        else:
            print("Invalid choice. Defaulting to deepseek-r1.")
            return "deepseek-r1"
    elif choice:
        if choice in model_list:
            return choice
        else:
            print("Model not found in available list. Defaulting to deepseek-r1.")
            return "deepseek-r1"
    else:
        return "deepseek-r1"