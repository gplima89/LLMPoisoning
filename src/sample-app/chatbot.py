"""
LLM Poisoning Workshop - Sample RAG Application

This is a deliberately vulnerable application for educational purposes.
It demonstrates common security issues in RAG-based LLM systems.

WARNING: DO NOT use this code in production!
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import VectorizedQuery

load_dotenv()


class HRChatbot:
    """
    HR Chatbot using RAG (Retrieval-Augmented Generation)
    
    This chatbot answers employee questions by:
    1. Retrieving relevant documents from Azure AI Search
    2. Using retrieved context to generate answers with Azure OpenAI
    
    VULNERABILITIES (intentional for workshop):
    - No input validation
    - No output sanitization
    - No document verification
    - No access control on search index
    """
    
    def __init__(self):
        """Initialize the chatbot with Azure services"""
        
        # Azure OpenAI setup
        self.openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt4-deployment")
        
        # Azure AI Search setup
        self.search_client = SearchClient(
            endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
            index_name=os.getenv("AZURE_SEARCH_INDEX_NAME", "documents-index"),
            credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_API_KEY"))
        )
        
        # System prompt (intentionally vulnerable to injection)
        self.system_prompt = """You are a helpful HR assistant for the company.
        Answer employee questions based on the provided context from company documents.
        Always cite your sources using the document titles.
        Be professional and helpful."""
    
    def retrieve_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from Azure AI Search
        
        VULNERABILITY: No verification of document authenticity
        
        Args:
            query: User's question
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents with metadata
        """
        try:
            results = self.search_client.search(
                search_text=query,
                top=top_k,
                select=["id", "title", "content", "metadata"]
            )
            
            documents = []
            for result in results:
                documents.append({
                    "id": result.get("id"),
                    "title": result.get("title"),
                    "content": result.get("content"),
                    "metadata": result.get("metadata", {}),
                    "score": result.get("@search.score", 0)
                })
            
            return documents
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def generate_answer(self, query: str, context_docs: List[Dict[str, Any]]) -> str:
        """
        Generate answer using Azure OpenAI with retrieved context
        
        VULNERABILITY: Context injection - malicious docs can manipulate output
        
        Args:
            query: User's question
            context_docs: Retrieved documents
            
        Returns:
            Generated answer
        """
        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document: {doc['title']}\n{doc['content']}"
            for doc in context_docs
        ])
        
        # Create messages for GPT-4
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"""Context from company documents:
{context}

Question: {query}

Please answer the question based on the context provided. Cite specific documents."""}
        ]
        
        try:
            # VULNERABILITY: No output filtering
            response = self.openai_client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {e}"
    
    def ask(self, question: str) -> Dict[str, Any]:
        """
        Main method to ask a question to the chatbot
        
        Args:
            question: User's question
            
        Returns:
            Dictionary with answer and sources
        """
        # VULNERABILITY: No input validation or sanitization
        print(f"\n[DEBUG] Processing question: {question}")
        
        # Step 1: Retrieve relevant documents
        context_docs = self.retrieve_context(question)
        print(f"[DEBUG] Retrieved {len(context_docs)} documents")
        
        if not context_docs:
            return {
                "answer": "I don't have enough information to answer that question.",
                "sources": [],
                "confidence": 0.0
            }
        
        # Step 2: Generate answer
        answer = self.generate_answer(question, context_docs)
        
        # Step 3: Extract sources
        sources = [doc["title"] for doc in context_docs]
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": sum(doc["score"] for doc in context_docs) / len(context_docs),
            "documents": context_docs
        }


def main():
    """Demo the chatbot"""
    print("=" * 60)
    print("HR Chatbot - LLM Poisoning Workshop Demo")
    print("=" * 60)
    
    # Initialize chatbot
    chatbot = HRChatbot()
    
    # Example questions
    questions = [
        "What is the company password policy?",
        "Is MFA required?",
        "How should I handle sensitive credentials?",
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")
        
        response = chatbot.ask(question)
        
        print(f"\nAnswer: {response['answer']}")
        print(f"\nSources: {', '.join(response['sources'])}")
        print(f"Confidence: {response['confidence']:.2f}")


if __name__ == "__main__":
    main()
