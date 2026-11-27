# 📄 PDF Question-Answering RAG App

A simple web app that lets you **upload a PDF and ask questions about it in plain English**. It reads your document, understands its content, and answers your questions using an AI language model — no manual searching through pages required.

---

## 📌 What Problem Does This Solve?

Imagine you have a long PDF — a research paper, a manual, a contract, or a report — and you just want quick answers instead of reading the whole thing. This app lets you:

1. Upload the PDF.
2. Ask a question like *"What is the main conclusion of this paper?"* or *"What are the payment terms?"*
3. Get an AI-generated answer based only on the content of that document.

This approach is called **RAG (Retrieval-Augmented Generation)**. Instead of asking an AI model a question "blind," the app first *retrieves* the most relevant parts of your document, then feeds those parts to the AI so it can *generate* an accurate, grounded answer.

---

## 🛠️ Technology Used

| Tool / Library | Role in the App |
|---|---|
| **[Streamlit](https://streamlit.io/)** | Powers the simple web interface (file upload box, text box, buttons) |
| **[LangChain](https://www.langchain.com/)** | Framework that connects all the RAG pieces together (loading, splitting, retrieving, answering) |
| **Unstructured** (`UnstructuredPDFLoader`) | Reads and extracts text from your PDF file |
| **Hugging Face Embeddings** | Converts chunks of text into numerical "meaning vectors" so similar content can be found later |
| **[Chroma](https://www.trychroma.com/)** | A vector database that stores those text chunks and lets the app quickly find the most relevant ones |
| **[Groq](https://groq.com/) + GPT-OSS 120B** | The large language model that reads the relevant text chunks and writes the final answer |
| **python-dotenv** | Loads your secret API key from a `.env` file instead of hardcoding it |

### How it works, step by step

1. **Upload** — You upload a PDF through the Streamlit interface.
2. **Load & Split** — The app reads the PDF's text and splits it into small overlapping chunks (about 2,000 characters each) so the AI can process them effectively.
3. **Embed & Store** — Each chunk is converted into a numerical vector (an "embedding") and saved in a local Chroma database.
4. **Ask** — When you type a question, the app searches the Chroma database for the chunks most related to your question.
5. **Answer** — Those relevant chunks, along with your question, are sent to the GPT-OSS 120B model (via Groq), which writes a natural-language answer.

---

## ✅ Prerequisites

Before you start, make sure you have:

- **Python 3.9 or higher** installed ([download here](https://www.python.org/downloads/))
- A free **Groq API key** ([sign up here](https://console.groq.com/)) — this is what lets the app use the GPT-OSS 120B model
- Basic comfort using a terminal / command prompt

---

## 📦 Installation

1. **Get the project files** onto your computer (clone the repo or download the folder), then open a terminal in that folder.

2. **Create a virtual environment** (recommended, keeps dependencies isolated):

   ```bash
   python -m venv venv
   ```

   Activate it:

   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

   > This installs Streamlit, LangChain, Chroma, the PDF reader, and everything else the app needs. It may take a few minutes the first time.

4. **Set up your API key:**

   - Rename `env_template.txt` to `.env`
   - Open `.env` and replace the placeholder with your real Groq API key:

     ```
     GROQ_API_KEY=your_actual_groq_api_key_here
     ```

   > ⚠️ Never share your `.env` file or commit it to a public GitHub repo — it contains your private API key.

---

## ▶️ Running the App

With your virtual environment activated and `.env` set up, run:

```bash
streamlit run app.py
```

This will open the app automatically in your web browser (usually at `http://localhost:8501`).

### Using the app

1. Click **"Upload a PDF file"** and choose a document.
2. Wait for the **"Document Processed Successfully"** message.
3. Type your question in the **"Ask your question about the document"** box.
4. Click **"Answer"** and read the AI's response below.

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `app.py` | The Streamlit web interface — handles file uploads and displays answers |
| `rag_utility.py` | The "engine" — loads PDFs, creates embeddings, stores them, and generates answers |
| `requirements.txt` | List of Python packages the project depends on |
| `env_template.txt` | Template for your `.env` file (holds your Groq API key) |

---

## 💡 Tips & Troubleshooting

- **First run is slower** — the embedding model and dependencies download the first time you use them.
- **Large PDFs take longer** to process since they're split into more chunks.
- **"Answer" button seems to ignore a new PDF?** Make sure you see the "Document Processed Successfully" message before asking a question — this confirms the new document has replaced the old one in the database.
- **Getting API errors?** Double-check that your `.env` file is named exactly `.env` (not `.env.txt`) and that your Groq API key is correct and active.

---

## 🚀 Possible Improvements (Ideas for Later)

- Support multiple PDFs at once
- Show which part of the PDF an answer came from (source citations)
- Add a chat-style conversation history
- Support other file types (Word docs, text files, etc.)
