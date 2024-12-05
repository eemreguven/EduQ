
# RAG System with Ollama and ChromaDB

This application implements a Retrieval-Augmented Generation (RAG) system using Ollama's large language models and ChromaDB for document storage and similarity search.

---

## Prerequisites

Before running the application, ensure the following prerequisites are met:

1. **Python Environment**:
   - Install Python 3.11 or later.
   - Set up a virtual environment (recommended).

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

2. **Dependencies**:
   - Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Ollama CLI**:
   - Install the Ollama CLI from the [Ollama website](https://ollama.ai).
   - Verify the installation by running:

   ```bash
   ollama --version
   ```

4. **ChromaDB Setup**:
   - No additional setup is needed for ChromaDB, as it will initialize automatically during runtime.

---

## Fetch Necessary Models

Before the first run of the application, you must fetch the required models using the `ollama pull` command.

1. Pull the base language model for question generation:

   ```bash
   ollama pull llama3.2:3b
   ```

2. Pull the embedding model for similarity search:

   ```bash
   ollama pull nomic-embed-text
   ```

---

## Running the Application

1. Start the Flask application:

   ```bash
   python app.py
   ```

2. Open the application in your browser at:

   ```
   http://127.0.0.1:5000
   ```

---

## Development and Debugging

1. **Clearing the Database**:
   To reset the Chroma database, run the `populate_database.py` script with the `--reset` flag:

   ```bash
   python rag-system/populate_database.py --reset
   ```

2. **Fetching Updated Models**:
   If newer versions of the models are released, pull them again using `ollama pull`.

---

## Support

For issues or questions, feel free to open a discussion or raise an issue on the repository.
