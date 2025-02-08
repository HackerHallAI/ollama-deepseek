# Ollama Chat Interface

This project is a tutorial on setting up Ollama to run on your local computer and creating a Python-based UI to interact with different models. The project includes both a command-line interface (CLI) and a graphical user interface (GUI) using Tkinter.

## Features

- **CLI Mode**: Interact with the AI models via a command-line interface.
- **UI Mode**: Use a simple Tkinter-based chat interface for a more visual interaction.
- **Model Selection**: Choose from available models to customize your chat experience.

## Prerequisites

- Python 3.7 or higher (I used 3.12)
- Pip (Python package manager)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Ollama**:
   - Follow the instructions on the [Ollama website](https://ollama.com) to set up and configure Ollama on your local machine.

## Usage

### Running the Application

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Choose the mode**:
   - **CLI**: Type `1` to start the command-line interface.
   - **UI**: Type `2` to start the graphical user interface.

3. **Select a model**:
   - You will be prompted to choose a model from the available list. You can either enter the number corresponding to the model or type the model name directly.

### CLI Mode

- Type your questions directly into the terminal.
- Type `exit` or `quit` to end the session.

### UI Mode

- Enter your questions in the input field and press `Enter` or click the `Send` button.
- The conversation history is displayed in the chat area.

## Project Structure

- `backend.py`: Contains functions for building conversation prompts and generating responses using Ollama.
- `frontend.py`: Implements the Tkinter-based chat interface.
- `main.py`: Entry point for the application, handles mode and model selection.
- `requirements.txt`: Lists the Python dependencies for the project.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Ollama](https://ollama.com) for providing the AI models and API.
- The Python community for the libraries and tools used in this project. 