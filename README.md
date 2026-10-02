# 🎓 Student Counselling AI Chatbot

An AI-powered student counselling chatbot designed to provide accurate information about university courses, admissions, eligibility, fees, duration, seats, and other course-related details.

The chatbot uses a Retrieval-Augmented Generation (RAG) architecture to retrieve relevant information from university course data before generating an answer with a local Large Language Model.

---

## 📌 Project Overview

Students often need to search through different sources to find information about university courses and admissions.

This project provides a conversational interface where students can simply ask questions such as:

* What courses are available?
* What is the eligibility for BBA?
* What is the fee for B.Tech?
* What is the admission process for MBA?
* How many seats are available?
* Who is the HOD of a particular course?

The chatbot retrieves relevant information from the university's course dataset and uses an LLM to generate a natural-language response.

---

## ✨ Features

* 🎓 Course information
* 📚 Course eligibility details
* 💰 Semester-wise fee information
* 📝 Admission process
* ⏳ Course duration
* 🪑 Total seats
* 👨‍🏫 HOD / Chairperson information
* 📞 Contact and helpline information
* 🔎 RAG-based information retrieval
* 🤖 Local LLM using Ollama
* ⚡ Cached embeddings and retriever
* 🧪 Automated testing
* 🚫 No external LLM API required

---

## 🧠 RAG Architecture

The chatbot follows a Retrieval-Augmented Generation pipeline:

```text
                    User Question
                         │
                         ▼
                  FastAPI Backend
                         │
                         ▼
                 Question Processing
                         │
                         ▼
              ┌─────────────────────┐
              │     ChromaDB        │
              │  Vector Retrieval   │
              └─────────────────────┘
                         │
                         ▼
              Relevant Course Context
                         │
                         ▼
                  Prompt Generation
                         │
                         ▼
                 Ollama / Llama 3.2
                         │
                         ▼
                  Generated Answer
                         │
                         ▼
                     Frontend
```

### Retrieval Flow

1. User submits a question.
2. The backend processes the question.
3. Relevant course information is retrieved from ChromaDB.
4. Retrieved context is added to the prompt.
5. Llama 3.2 generates the final response.
6. The response is returned to the frontend.

---

## 🛠️ Tech Stack

### Frontend

* React
* Vite
* JavaScript
* HTML
* CSS

### Backend

* Python
* FastAPI
* LangChain

### RAG

* ChromaDB
* HuggingFace Embeddings
* `sentence-transformers/all-MiniLM-L6-v2`

### LLM

* Ollama
* Llama 3.2

### Data

* CSV
* Pandas

### Testing

* Pytest

### Version Control

* Git
* GitHub

---

## 📂 Project Structure

```text
student-counselling-ai/
│
├── backend/
│   ├── app/
│   │   ├── rag/
│   │   │   ├── embeddings.py
│   │   │   ├── retriever.py
│   │   │   ├── pipeline.py
│   │   │   └── ...
│   │   │
│   │   └── llm/
│   │       ├── model.py
│   │       ├── prompts.py
│   │       └── ...
│   │
│   └── main.py
│
├── data/
│   └── raw/
│       └── courses.csv
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 📊 Current Dataset

The chatbot currently uses university course information containing details such as:

* Course Name
* Department
* Duration
* Total Seats
* Admission Mode
* Eligibility Criteria
* First Semester Fee
* Second Semester Fee
* Chairperson / HOD
* Contact & Helpline
* Admission Process

The current dataset contains information for **18 courses**.

---

## ⚡ Performance

The project includes performance monitoring for the RAG pipeline.

### Warm Request Performance

After the embedding model and retriever are initialized:

```text
🔧 Retriever Creation: 0.0000 sec
🔎 Retrieval:          ~0.03 sec
📝 Prompt Build:       ~0.00 sec
🤖 LLM:                ~2.5 sec
⏱️ Total:              ~2.6 sec
```

### Optimization

Embedding and retriever initialization are cached so that expensive initialization does not happen for every request.

The first request may take longer because the embedding model and vector store need to be initialized.

Subsequent requests reuse the cached components.

---

## 🧪 Testing

The project currently has an automated test suite.

```text
49 passed
```

Tests are used to verify the chatbot's responses and core functionality.

Run the tests with:

```bash
pytest -v
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/niteshjind/Student-Counselling-Ai-chatbot.git
cd Student-Counselling-Ai-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows Git Bash

```bash
source .venv/Scripts/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🤖 Ollama Setup

Install Ollama and make sure it is running.

Pull the required model:

```bash
ollama pull llama3.2
```

Check the installed model:

```bash
ollama list
```

The chatbot uses the local Llama 3.2 model through Ollama.

No external LLM API key is required for the current setup.

---

## ▶️ Running the Backend

From the project directory:

```bash
cd backend
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The backend will be available locally through the FastAPI server.

---

## ▶️ Running the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Vite will provide the local frontend development URL.

---

## 🔌 API

The backend provides a chat endpoint:

```text
POST /chat
```

The endpoint accepts a user's question and returns the chatbot response.

Example request:

```json
{
  "question": "What is the eligibility for BBA?"
}
```

---

## 🔐 Privacy & API Usage

The current chatbot architecture is designed to run the LLM locally using Ollama.

Therefore, the project does not depend on an external paid LLM API for generating responses.

The university course information is stored locally and retrieved through the project's RAG pipeline.

---

## 🚀 Future Improvements

Planned improvements include:

* 🌐 Production deployment
* 💬 Improved chatbot UI
* 🎓 Integration with the university portal
* 📱 Responsive mobile interface
* 🔎 Improved retrieval and ranking
* 📚 Support for additional university documents
* 🧠 Better conversational context
* 📊 Usage and performance analytics

---

## 👨‍💻 Project Status

```text
RAG Pipeline        ✅
Vector Database     ✅
Local LLM           ✅
Course Dataset      ✅
FastAPI Backend     ✅
React Frontend      🚧
Automated Testing   ✅
Performance Tuning  ✅
Deployment          🚧
```

---

## 📄 License

This project is developed as an academic minor project.

---

## 👨‍💻 Author

**Nitesh Yadav**

B.Tech — Artificial Intelligence & Machine Learning

GitHub: [niteshjind](https://github.com/niteshjind)
