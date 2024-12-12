
from qdrant_client import QdrantClient
import google.generativeai as genai
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from qdrant_client import QdrantClient


def chat_with_rag(query: str):
    """
    Simple RAG-enhanced chat function using Gemini
    """
    try:
        # Initialize constants
        GEMINI_API_KEY = "AIzaSyCtO7jsR7sT-riZYuCJa69-qdjblR0qez0"
        QDRANT_URL = "https://f60408b9-0739-40b1-885d-56e57ef88ee5.us-east4-0.gcp.cloud.qdrant.io"
        QDRANT_API_KEY = "IhyblpSTqHUICu2hXDXQbSTw1yNRdvQj1BXmmKkI0VCb_Na4B-ImxA"
        COLLECTION_NAME = "digitalex_vectors"

        # Initialize Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        #model = genai.GenerativeModel("gemini-1.5-flash")

        # Initialize embeddings and Qdrant
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GEMINI_API_KEY
        )
        qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

        # Get relevant context from Qdrant
        query_embedding = embeddings.embed_query(query)
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=11
        )
        
        # Combine context
        context = "\n".join([hit.payload['page_content'] for hit in search_results])

        
        return context

    except Exception as e:
        return f"An error occurred: {str(e)}"