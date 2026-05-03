# Desafio MBA Engenharia de Software com IA - Full Cycle

Projeto de ingestao e busca semantica em documentos PDF usando LangChain, OpenAI Embeddings, PostgreSQL e pgvector.

A aplicacao carrega um PDF, divide o conteudo em chunks, gera embeddings, grava os vetores no PostgreSQL com pgvector e permite fazer perguntas via terminal. As respostas sao geradas com base no contexto recuperado do banco vetorial.

## Tecnologias

- Python 3.12
- LangChain
- OpenAI
- PostgreSQL 17
- pgvector
- Docker Compose

## Estrutura

- `src/ingest.py`: realiza a ingestao do PDF no banco vetorial.
- `src/search.py`: busca trechos similares no pgvector e monta o prompt de resposta.
- `src/chat.py`: interface de chat no terminal.
- `docker-compose.yml`: sobe o PostgreSQL com pgvector e cria a extensao `vector`.
- `requirements.txt`: dependencias Python do projeto.
- `.env.example`: exemplo das variaveis de ambiente necessarias.
- `document.pdf`: PDF usado como fonte de dados por padrao.

## Pre-requisitos

- Docker e Docker Compose instalados
- Python 3.12 instalado
- Chave de API da OpenAI

## Configuracao

1. Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

2. Edite o `.env` e preencha a chave da OpenAI:

```env
OPENAI_API_KEY=sua_chave_openai
OPENAI_MODEL=text-embedding-3-small
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag
PGVECTOR_COLLECTION=documents
PDF_PATH=document.pdf
```

Se quiser ingerir outro PDF, altere `PDF_PATH` para o caminho do arquivo desejado.

## Execucao

1. Suba o banco PostgreSQL com pgvector:

```bash
docker compose up -d
```

2. Crie e ative um ambiente virtual Python:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependencias:

```bash
pip install -r requirements.txt
```

4. Execute a ingestao do PDF:

```bash
python src/ingest.py
```

Esse comando le o arquivo definido em `PDF_PATH`, gera embeddings com o modelo definido em `OPENAI_MODEL` e salva os documentos vetorizados na colecao definida em `PGVECTOR_COLLECTION`.

5. Inicie o chat no terminal:

```bash
python src/chat.py
```

No menu interativo:

- Digite `1` para fazer uma pergunta.
- Digite a pergunta sobre o conteudo do PDF ingerido.
- Digite `2` para sair.

## Fluxo esperado

1. O `docker-compose.yml` inicia o PostgreSQL e habilita a extensao `vector`.
2. O `src/ingest.py` carrega o PDF, quebra o texto em chunks e persiste os embeddings no banco.
3. O `src/chat.py` recebe perguntas no terminal.
4. O `src/search.py` busca os trechos mais similares no pgvector e envia o contexto para o modelo de chat.
5. A resposta deve usar apenas as informacoes recuperadas do PDF.

## Comandos uteis

Parar os containers:

```bash
docker compose down
```

Parar os containers e remover o volume do banco:

```bash
docker compose down -v
```

Reexecutar a ingestao depois de trocar o PDF:

```bash
python src/ingest.py
```

## Observacoes

- A ingestao depende de `OPENAI_API_KEY`; sem ela, a geracao de embeddings falha.
- O banco precisa estar em execucao antes de rodar `src/ingest.py` ou `src/chat.py`.
- Se o volume do Docker for removido, sera necessario executar a ingestao novamente.
- O chat responde adequadamente apenas sobre documentos que ja foram ingeridos no banco vetorial.
