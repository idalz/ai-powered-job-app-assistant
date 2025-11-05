from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings
from app.core.logger import logger
import time

# Embedding model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=settings.OPENAI_API_KEY
)

# Init Pinecone client
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Connect to the index (must be created manually in Pinecone dashboard)
index = pc.Index(settings.PINECONE_INDEX_NAME)


# Create pinecone vectorstore with namespace
def get_vectorstore() -> PineconeVectorStore:
    return PineconeVectorStore(
        index=index,
        embedding=embeddings,
        namespace=settings.PINECONE_NAMESPACE
    )

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
        results = vectorstore.similarity_search_with_score(query, k=k)
        return [{"text": r[0].page_content, "metadata": r[0].metadata, "score": r[1]} for r in results]
    except Exception as e:
        logger.error(f"Pinecone search failed: {e}")
        return {"error": str(e)}
    
# Delete a resume vector by email
def delete_resume_by_email(email: str):
    try:
        # Use the Pinecone client (index) with namespace
        response = index.delete(
            filter={"email": {"$eq": email}},
            namespace=settings.PINECONE_NAMESPACE
        )
        logger.info(f"Deleted previous resume for {email} from Pinecone namespace {settings.PINECONE_NAMESPACE}")
        return {"status": "deleted", "response": response}
    except Exception as e:
        logger.error(f"Failed to delete resume for {email}: {e}")
        return {"error": str(e)}