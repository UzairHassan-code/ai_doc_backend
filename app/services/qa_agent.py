# File path: doc_intel_backend/app/services/qa_agent.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.core.config import settings
from app.services.indexing_agent import IndexingAgent

class QAAgent:
    """
    Agent responsible for answering questions using explicit LCEL pipes.
    """
    
    def __init__(self):
        # Initialize Gemini Model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2
        )
        self.indexing_agent = IndexingAgent()

    def _format_docs(self, docs):
        """Helper to combine document chunks into a single string."""
        return "\n\n".join(doc.page_content for doc in docs)

    def answer_question(self, question: str, file_id: str) -> dict:
        """
        Answers a question using a transparent LCEL pipeline.
        """
        # 1. Load the specific vector store
        try:
            vector_store = self.indexing_agent.load_index(file_id)
        except Exception:
            return {"answer": "Document not found or not indexed yet.", "sources": []}
            
        # 2. Create Retriever
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        
        # 3. Define the Prompt
        template = """Answer the question based only on the following context:

        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)

        # 4. Build the Chain (The "Pipe" Syntax)
        # This is the Raw LCEL. It says:
        # "Take input. Send 'context' to retriever+formatter. Send 'question' through unchanged."
        # "Then pass both to prompt."
        # "Then pass prompt to Gemini."
        # "Then make the output a string."
        rag_chain = (
            {"context": retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        # 5. Run it
        try:
            answer = rag_chain.invoke(question)
            
            # 6. Retrieve sources manually (since StrOutputParser only gives text)
            # We do a quick separate fetch just to populate the UI 'sources' field
            source_docs = retriever.invoke(question)
            sources = [doc.page_content[:200] + "..." for doc in source_docs]

            return {
                "answer": answer,
                "sources": sources
            }
        except Exception as e:
            return {"answer": f"Error during generation: {str(e)}", "sources": []}