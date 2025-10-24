# Gradio Video Processing App

## Project Overview

This project is a multi-tab Gradio application designed for video processing. The application will allow users to load a video, extract frames, and then pass a selected frame to different processing modules, each in its own tab.

The core technologies used will be Python and the Gradio library.

## Project Principles

*   **Maintainability:** The code will be modular and well-documented to be easily maintainable.
*   **Security:** We will pay attention to security best practices, especially when handling user inputs and files.
*   **Scalability:** The application will be designed to be scalable, with efficient processing functions.
*   **Demo-Friendly:** The code will be clear, well-commented, and the application easy to demonstrate, making it suitable for a YouTube video.

## Directory Structure

The project will be organized with the following directory structure:

```
.
├── .venv/            # uv virtual environment
├── ui/               # Main Gradio UI components
├── modules/          # Independent processing modules (tabs)
├── main.py           # Main application entry point
└── requirements.txt  # Project dependencies
```

## Modules (Tabs)

### Module 1: Video Frame Extractor

*   **Purpose:** Load a video and extract its frames.
*   **Functionality:**
    *   Input field to paste a video file path or a file browser to upload a video.
    *   A slider or number input to define the frame extraction interval (e.g., extract one frame every N frames).
    *   A gallery or a similar component to display the extracted frames.
    *   Ability to select a single frame from the gallery.
*   **Output:** The selected frame will be made available to other modules.

## Development Environment

*   **Virtual Environment:** We will use `uv` to create and manage a virtual environment.
*   **Hot Reloading:** The Gradio application will be launched in `debug` mode to enable hot reloading during development.

## Building and Running

1.  **Setup the environment:**
    ```bash
    # Create the virtual environment
    uv venv
    # Activate the environment
    # On Windows:
    .venv\Scripts\activate
    # On macOS/Linux:
    # source .venv/bin/activate
    ```
2.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    ```
3.  **Run the application:**
    ```bash
    # This will start the Gradio app with hot reloading
    # On Windows:
    start /b python main.py
    # On macOS/Linux:
    # python main.py &
    # This command starts the Gradio app with hot reloading.
    # The server will automatically restart when you save a file.
    gradio main.py
    ```

## Notes de Développement

*   **Lancement du serveur (Windows) :** La commande `start /b python main.py` lance le serveur en arrière-plan mais peut masquer sa sortie.
*   **URL par défaut :** Si l'URL ne s'affiche pas, l'application Gradio est généralement accessible à l'adresse [http://127.0.0.1:7860](http://127.0.0.1:7860).
*   **Redirection des logs :** Pour voir les messages du serveur (y compris les erreurs de débogage) dans un environnement sans console visible, lancez le serveur avec `start /b python main.py > server.log 2>&1`. Le fichier `server.log` contiendra alors toute la sortie.
*   **Gestion des processus "zombies" :** Si le serveur ne répond pas, il se peut qu'un ancien processus soit bloqué.
    *   Pour vérifier, utilisez `tasklist | findstr python`.
    *   Pour forcer l'arrêt d'un processus, utilisez `taskkill /F /PID <numéro_du_pid>`.
*   **Méthode recommandée :** Utiliser `gradio main.py` est la meilleure pratique. Cela garde le serveur au premier plan, affiche les logs et les erreurs en temps réel, et gère parfaitement le rechargement à chaud.
*   **URL par défaut :** L'application Gradio est généralement accessible à l'adresse http://127.0.0.1:7860.
*   **Arrêter le serveur :** Pour arrêter le serveur lancé avec `gradio`, retournez simplement dans le terminal et appuyez sur `Ctrl+C`.

## Development Conventions

*   **UI:** The main Gradio interface will be defined in the `ui/` directory.
*   **Modules:** Each processing module should be developed as a self-contained unit within the `modules/` directory. Each module will correspond to a tab in the Gradio interface.
*   **Dependencies:** All Python dependencies should be listed in `requirements.txt`.
