from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from qdrant_client.models import Distance, VectorParams
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
import PyPDF2
def load_pdf(file_path):
    """Load PDF content using PyPDF2"""
    text = ""
    with open(file_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Get the number of pages
        num_pages = len(pdf_reader.pages)
        
        # Extract text from each page
        for page_num in range(num_pages):
            # Get the page object
            page = pdf_reader.pages[page_num]
            
            # Extract text from the page
            text += page.extract_text() + "\n"
    
    return text


def process_pdf(file_path):
    """Process PDF file and store embeddings in Qdrant"""
    try:
        # Initialize constants
        GEMINI_API_KEY = "AIzaSyBpcmD6usZZUOvoty0GflZzk_uE_EH3E28"
        COLLECTION_NAME = "digitalex_vectors"
        EMBEDDING_DIMENSION = 768  # Google's embedding dimension
        QDRANT_API_KEY = "IhyblpSTqHUICu2hXDXQbSTw1yNRdvQj1BXmmKkI0VCb_Na4B-ImxA"
        QDRANT_URL = "https://f60408b9-0739-40b1-885d-56e57ef88ee5.us-east4-0.gcp.cloud.qdrant.io"
        qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
        # Load PDF content
        print("Loading PDF...")
        text_content = load_pdf(file_path)
        document = Document(page_content=text_content, metadata={"source": file_path})
        
        # Split text into chunks
        print("Splitting text...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, 
            chunk_overlap=200
        )
        final_documents = text_splitter.split_documents([document])
        print(f"Created {len(final_documents)} chunks")
        
        # Initialize Google's embeddings
        print("Initializing embeddings...")
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=GEMINI_API_KEY
        )
        
        # Recreate Qdrant collection
        print("Setting up Qdrant collection...")
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                distance=Distance.COSINE
            )
        )

        # Initialize Qdrant with Google embeddings
        print("Initializing Qdrant database...")
        qdrant_db = Qdrant(
            client=qdrant_client, 
            collection_name=COLLECTION_NAME, 
            embeddings=embeddings
        )

        # Add documents in batches
        print("Adding documents to database...")
        batch_size = 25
        for i in range(0, len(final_documents), batch_size):
            batch = final_documents[i:i + batch_size]
            qdrant_db.add_documents(documents=batch)
            print(f"Processed batch {i//batch_size + 1}/{(len(final_documents) + batch_size - 1)//batch_size}")

        print("PDF processing completed successfully")
        return qdrant_db

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        raise e
    
process_pdf(file_path=r"C:\Users\user\Downloads\MCX-080824-090552.pdf")