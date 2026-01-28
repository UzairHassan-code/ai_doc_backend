# File path: doc_intel_backend/app/services/orchestrator.py

import logging
from app.services.ingestion_agent import IngestionAgent
from app.services.indexing_agent import IndexingAgent
from app.services.qa_agent import QAAgent

# Configure logging to see what's happening in the console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Orchestrator:
    """
    The Controller that coordinates the three agents.
    It ensures data flows smoothly from Upload -> Ingestion -> Indexing -> QA.
    """
    
    def __init__(self):
        self.ingestion_agent = IngestionAgent()
        self.indexing_agent = IndexingAgent()
        self.qa_agent = QAAgent()

    def run_pipeline(self, file_path: str, file_id: str):
        """
        Executes the full ingestion and indexing pipeline.
        This is designed to be run as a Background Task.
        """
        logger.info(f"🚀 Starting pipeline for file: {file_id}")
        
        try:
            # Step 1: Ingestion (Extract Text)
            text_content = self.ingestion_agent.process(file_path)
            
            if not text_content or len(text_content.strip()) == 0:
                logger.warning(f"⚠️ No text extracted for file {file_id}. Stopping pipeline.")
                return False

            logger.info(f"✅ Text extracted for {file_id} ({len(text_content)} chars).")

            # Step 2: Indexing (Vector Store)
            index_path = self.indexing_agent.index_document(text_content, file_id)
            logger.info(f"✅ Successfully indexed file {file_id} at {index_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Pipeline failed for {file_id}: {str(e)}")
            return False

    def ask(self, question: str, file_id: str):
        """
        Delegates the question to the QA Agent.
        """
        logger.info(f"❓ Asking question for file {file_id}: {question}")
        return self.qa_agent.answer_question(question, file_id)