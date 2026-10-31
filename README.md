# Chatbot Faculdade - Pipeline RAG com Gemini e ChromaDB

## Sobre o Projeto

Este projeto consiste em um protótipo de chatbot inteligente baseado em **RAG (Retrieval Augmented Generation)** para consulta de informações institucionais da faculdade.

O sistema utiliza documentos como:

- Currículos Lattes dos professores
- Regulamentos institucionais
- Informações dos cursos
- Documentos acadêmicos
- Arquivos de texto do portal da faculdade

Ao invés de depender exclusivamente do conhecimento do modelo de IA, o chatbot realiza uma busca semântica nos documentos armazenados e utiliza essas informações como contexto para gerar respostas mais precisas e confiáveis.

---

# Arquitetura

```text
Documentos
(PDF/TXT)

      ↓

Ingestão

      ↓

Embeddings
(BGE-M3)

      ↓

ChromaDB

      ↓

Busca Vetorial

      ↓

Gemini 2.5 Flash

      ↓

Resposta ao Usuário
```

---

# Tecnologias Utilizadas

## Backend

- Python 3.12+
- FastAPI

## Inteligência Artificial

- Gemini 2.5 Flash
- Sentence Transformers

## Embeddings

- BAAI/bge-m3

## Banco Vetorial

- ChromaDB

## Containers

- Docker
- Docker Compose

---

# Estrutura do Projeto

```text
chatbot-faculdade/

├── app/
│   └── rag/
│       ├── rag.py
│       └── main.py
│
├── data/
│   ├── faculdade/
│   │   └── BCC.txt
│   │
│   └── professores/
│       ├── Curriculo Professor 01.pdf
│       ├── Curriculo Professor 02.pdf
│       └── Curriculo Professor 03.pdf
│
├── docker/
│   ├── docker-compose.yml
│   └── Dockerfile
│
├── web_scraping/
│   └── app.py
│
├── ingest.py
│
├── .env
│
├── requirements.txt
│
└── README.md
```

---

# Funcionamento do Sistema

## Etapa 1 - Ingestão

O script:

```bash
ingest.py
```

é responsável por:

1. Ler todos os documentos da pasta `data`
2. Extrair o conteúdo dos PDFs
3. Gerar embeddings utilizando BGE-M3
4. Armazenar os vetores no ChromaDB

---

## Etapa 2 - Busca Semântica

Quando o usuário envia uma pergunta:

```text
Quem possui experiência em Inteligência Artificial?
```

O sistema:

1. Converte a pergunta em embedding
2. Busca os documentos semanticamente mais próximos
3. Retorna os documentos mais relevantes

---

## Etapa 3 - Geração da Resposta

O contexto recuperado é enviado ao Gemini:

```text
Pergunta
+
Contexto Recuperado
=
Prompt
```

O Gemini gera uma resposta baseada exclusivamente nas informações encontradas.

---

# Requisitos

## Software

- Python 3.12+
- Docker
- Docker Compose

---

# Instalação

## Clonar repositório

```bash
git clone <repositorio>

cd chatbot-faculdade
```

---

## Criar ambiente virtual

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Instalar dependências

```bash
pip install -r requirements.txt
```

---

# Configuração do Gemini

## Criar API Key

Acessar:

https://aistudio.google.com

Criar uma API Key.

---

## Configurar arquivo .env

```env
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

---

# Subindo o ChromaDB

## Docker Compose

Entrar na pasta docker:

```bash
cd docker
```

Subir container:

```bash
docker compose up -d
```

Verificar:

```bash
docker ps
```

Resultado esperado:

```text
chromadb
```

---

## Porta utilizada

```text
8001
```

A API do Chroma ficará disponível em:

```text
http://localhost:8001
```

---

# Preparação dos Dados

## Documentos Institucionais

Adicionar arquivos em:

```text
data/faculdade/
```

Exemplo:

```text
BCC.txt
ADS.txt
Regulamento.txt
Calendario.txt
```

---

## Currículos dos Professores

Adicionar PDFs em:

```text
data/professores/
```

Exemplo:

```text
Professor_Joao.pdf
Professor_Maria.pdf
Professor_Carlos.pdf
```

---

# Executando a Ingestão

Após adicionar os documentos:

```bash
python ingest.py
```

Resultado esperado:

```text
Documentos indexados.
```

---

# Executando a API

Executar:

```bash
uvicorn app.rag.main:app --reload
```

Resultado:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

# Swagger

Acessar:

```text
http://localhost:8000/docs
```

Interface disponível para testes da API.

---

# Endpoint Principal

## POST /chat

### Request

```json
{
  "pergunta": "Quem possui experiência em Inteligência Artificial?"
}
```

### Response

```json
{
  "resposta": "O professor João Silva possui experiência em Inteligência Artificial..."
}
```

---

# Fluxo Completo

```text
Usuário

    ↓

FastAPI

    ↓

Retriever

    ↓

ChromaDB

    ↓

Contexto

    ↓

Gemini

    ↓

Resposta
```

---

# Como Adicionar Novos Documentos

Adicionar o arquivo:

```text
data/faculdade/
```

ou

```text
data/professores/
```

Executar novamente:

```bash
python ingest.py
```

Os documentos serão reindexados.

---

# Melhorias Futuras

## Chunking Inteligente

Atualmente:

```text
1 PDF = 1 Documento
```

Melhoria:

```text
1 PDF = vários chunks
```

Benefícios:

- Busca mais precisa
- Menor consumo de tokens
- Melhor recuperação semântica

---

## Metadados

Adicionar:

```json
{
  "nome": "João Silva",
  "tipo": "professor",
  "curso": "BCC"
}
```

Permite filtros avançados.

---

## Histórico de Conversa

Manter contexto entre perguntas.

Exemplo:

```text
Usuário:
Quem é especialista em IA?

Bot:
Professor João Silva.

Usuário:
Qual sua formação?
```

O chatbot entenderá a referência ao professor mencionado anteriormente.

---

## Frontend React

Implementar interface web semelhante ao ChatGPT.

Stack sugerida:

- React
- Vite
- TailwindCSS

---

## Busca Híbrida

Combinar:

```text
Busca Vetorial
+
Busca por Palavra-Chave
```

Ferramentas:

- BM25
- Elasticsearch
- OpenSearch

---

## Web Scraping

A pasta:

```text
web_scraping/
```

poderá ser utilizada para:

- Notícias
- Eventos
- Cursos
- Portal da faculdade

Atualizando automaticamente a base de conhecimento.

---

# Solução de Problemas

## Erro de conexão com ChromaDB

Verifique:

```bash
docker ps
```

Confirme que o container:

```text
chromadb
```

está em execução.

---

## Erro de API Key

Verifique:

```env
GEMINI_API_KEY=
```

A chave deve estar válida.

---

## Nenhum documento encontrado

Verifique:

```text
data/
```

e execute novamente:

```bash
python ingest.py
```

---

# Roadmap

## MVP

- [x] FastAPI
- [x] ChromaDB
- [x] Gemini
- [x] Ingestão de PDFs
- [x] Busca Vetorial

## Versão 2

- [ ] Chunking
- [ ] Metadados
- [ ] Frontend React
- [ ] Histórico de Conversa

## Versão 3

- [ ] Busca Híbrida
- [ ] PostgreSQL + pgvector
- [ ] Agente IA
- [ ] Integração com Portal Acadêmico

---

# Autor

Projeto desenvolvido como estudo de:

- Inteligência Artificial Generativa
- Retrieval Augmented Generation (RAG)
- Embeddings
- Busca Vetorial
- Engenharia de Prompt
- Desenvolvimento Backend com Python