# AI Document Intelligence Backend

This project is a backend system that lets you upload a PDF and ask questions about it. It uses FastAPI for the web server, LangChain for the logic, and Google Gemini to answer questions.

## System Architecture

The system is split into three main "Agents" that handle different jobs. A central controller (Orchestrator) manages them so the code stays clean.

graph TD

    User -->|POST /upload| API
    User -->|POST /query| API
    
    API -->|Calls| Controller[Orchestrator]
    
    subgraph "Agents"
        Controller -->|1. Extract Text| AgentA[Ingestion Agent]
        Controller -->|2. Create Index| AgentB[Indexing Agent]
        Controller -->|3. Answer| AgentC[QA Agent]
    end
    
    AgentA -->|Reads| Files[Local Storage]
    AgentB -->|Writes| Database[FAISS Vector DB]
    AgentC -->|Reads| Database
    AgentC -->|Asks| Gemini[Google Gemini API]


## Agent Responsibilities

1. Ingestion Agent: Its only job is to open the PDF file and pull out the text.

2. Indexing Agent: It takes that text, chops it into small pieces, and turns it into numbers (vectors) using HuggingFace. It saves these to a local folder so we can search them later.

3. QA Agent: When you ask a question, this agent finds the relevant text in the database and sends it to Google Gemini to write an answer.

4. Orchestrator: This connects everything. It handles the API requests and runs the heavy AI work in the background so the server doesn't freeze.

## Docker Setup(Preferred)

Run the app in a container without installing Python manually.

1. Build the Image:
```
docker build -t doc-backend .
```

2. Run the Container:
```
docker run -p 8000:8000 --env-file .env doc-backend
```
3. Visit this URL:
   ```
   http://127.0.0.1:8000/docs
   ```
## Setup Instructions

Clone the repo and set up Python:
```
git clone [https://github.com/UzairHassan-code/ai-doc-backend.git](https://github.com/UzairHassan-code/ai-doc-backend.git)
cd ai-doc-backend
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
```
## Install libraries:
```
pip install -r requirements.txt
```

Set your API Key:
Create a file named .env in the main folder and add your key:

GOOGLE_API_KEY=your_google_api_key_here


Run the server:
```
uvicorn app.main:app --reload
```

You can now open http://localhost:8000/docs to see the API.

API Examples

You can test these using curl or Postman.

1. Upload a Document

This uploads the file and starts the AI processing.

curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@sample.pdf;type=application/pdf'


2. Ask a Question

Take the file_id you got from the upload step and use it here.

curl -X 'POST' \
  'http://127.0.0.1:8000/api/v1/query/0f0dcd14-9846-4014-8e31-5fc9f2f99f0a' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "question": "What is this document about?"
}'

# (You can use SwaggerUI for testing the APIs)

## Trade-offs and Improvements

Here are a few decisions I made to keep things simple, and how I would improve them later:

1. Local Storage vs Cloud

I am saving files and the database directly to the project folder. 
Improvement: In a real app, I would save files to DB and use a cloud vector database like Pinecone.

2. PDF Parsing

I used a simple library (pypdf) that extracts text. It works well for digital PDFs but fails on scanned images.
Improvement: I would add an OCR step to read text from images.
