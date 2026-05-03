import os
from dotenv import load_dotenv
from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
MODEL = os.getenv("OPENAI_MODEL","text-embedding-3-small")
PG_VECTOR_COLLECTION = os.getenv("PGVECTOR_COLLECTION")
DATABASE_URL = os.getenv("DATABASE_URL")

def ingest_pdf():
    docs = PyPDFLoader(PDF_PATH).load()
    
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False
    ).split_documents(docs)
    if not splits:
        raise SystemExit(0)
    
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]
    embeddings = OpenAIEmbeddings(model=MODEL)

    store = PGVector(
        embeddings=embeddings,
        collection_name=PG_VECTOR_COLLECTION,
        connection=DATABASE_URL,
        use_jsonb=True
    )

    store.add_documents(documents=enriched, ids=ids)



if __name__ == "__main__":
    ingest_pdf()