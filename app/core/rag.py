from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings
from app.core.logger import logger
import time

# Embedding model
embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)

# Init Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Check if index exists
if settings.PINECONE_INDEX_NAME not in [i["name"] for i in pc.list_indexes()]:
    pc.create_index(
        name=settings.PINECONE_INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    # Wait until the index is ready
    while not pc.describe_index(settings.PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

# Connect to the index
index = pc.Index(settings.PINECONE_INDEX_NAME)


# Create pinecone vectorstore
def get_vectorstore() -> PineconeVectorStore:
    return PineconeVectorStore(index=index, embedding=embeddings)

# Store resume in pinecone vectorstore
def store_resume(text: str, metadata: dict = None):
    try:
        vectorstore = get_vectorstore()
        vectorstore.add_texts([text], metadatas=[metadata] if metadata else [{}])
        logger.info("Stored resume in Pinecone")
        return {"status": "stored"}
    except Exception as e:
        logger.error(f"Pinecone store failed: {e}")
        return {"error": str(e)}

# Search for resumes
def search_resumes(query: str, k: int = 3):
    try:
        vectorstore = get_vectorstore()
        results = vectorstore.similarity_search(query, k=k)
        return [{"text": r.page_content, "metadata": r.metadata} for r in results]
    except Exception as e:
        logger.error(f"Pinecone search failed: {e}")
        return {"error": str(e)}
    
# Delete a resume vector by email
def delete_resume_by_email(email: str):
    try:
        # Use the Pinecone client (index)
        response = index.delete(filter={"email": {"$eq": email}})
        logger.info(f"Deleted previous resume for {email} from Pinecone")
        return {"status": "deleted", "response": response}
    except Exception as e:
        logger.error(f"Failed to delete resume for {email}: {e}")
        return {"error": str(e)}