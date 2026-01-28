# File path: doc_intel_backend/quick_check.py
import sys
import os

# 1. Setup path so Python finds your 'app' folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.indexing_agent import IndexingAgent
from app.services.qa_agent import QAAgent

def test_agents():
    print("\n--- 🚀 Starting Quick Check ---")

    # 1. Dummy Data
    file_id = "quick_test_001"
    sample_text = """
    LangChain Expression Language (LCEL) is a declarative way to easily compose chains together.
    It was designed from day 1 to support putting prototypes in production, with no code changes.
    """
    
    # 2. Test Indexing
    print(f"\n[1] Indexing data for ID: {file_id}...")
    try:
        indexer = IndexingAgent()
        path = indexer.index_document(sample_text, file_id)
        print(f"✅ Indexing Success! Saved to: {path}")
    except Exception as e:
        print(f"❌ Indexing Failed: {e}")
        return

    # 3. Test QA (with new LCEL logic)
    print(f"\n[2] Asking Question...")
    try:
        qa = QAAgent()
        question = "What is LCEL designed for?"
        result = qa.answer_question(question, file_id)
        
        print(f"\n🤖 AI Answer: {result['answer']}")
        print(f"📄 Sources: {result['sources']}")
        
        if result['answer'] and "prototypes" in result['answer']:
            print("\n✅ SUCCESS: The Agents are working perfectly.")
        else:
            print("\n⚠️ WARNING: Answer received but looked unexpected. Check LLM.")
            
    except Exception as e:
        print(f"❌ QA Failed: {e}")

if __name__ == "__main__":
    test_agents()