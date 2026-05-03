import os
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

EMBEDING_MODEL = os.getenv("OPENAI_MODEL","text-embedding-3-small")
PG_VECTOR_COLLECTION = os.getenv("PGVECTOR_COLLECTION")
DATABASE_URL = os.getenv("DATABASE_URL")

model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.5)

def search_prompt(question: str):
    embeddings = OpenAIEmbeddings(model=EMBEDING_MODEL)
    
    store = PGVector(
      embeddings=embeddings,
      collection_name=PG_VECTOR_COLLECTION,
      connection=DATABASE_URL,
      use_jsonb=True,
    )
    results = store.similarity_search_with_score(question, k=10)
    
    context = ""
    for doc, _score in results:
        page = doc.metadata.get("page_label")
        source = doc.metadata.get("source")

        context += "--- CONTEXTO ---\n"
        context += f"METADADOS: page: {page}, source: {source}\n"
        context += f"CONTEÚDO: {doc.page_content}\n\n"


    print("contexto", context)
    prompt = ChatPromptTemplate.from_messages([
        ("system", PROMPT_TEMPLATE),
        ("human", question)
    ])

    chain = prompt | model

    res = chain.invoke({ "pergunta": question, "contexto": context })
   
    return res.content
