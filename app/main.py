from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
import os

from app.rag.rag import retrieve

load_dotenv()

# The client automatically detects the GEMINI_API_KEY environment variable
client = genai.Client()

app = FastAPI()

class ChatRequest(BaseModel):
    pergunta: str

@app.post("/chat")
def chat(req: ChatRequest):
    contexto = retrieve(req.pergunta)

    prompt = f"""
Você é um administrador de um fablab.

Sua função é responder com clareza, profundidade e organização,
sempre com base EXCLUSIVA nas informações recuperadas pelo pipeline RAG).

Diretrizes obrigatórias:
1. Use somente o contexto recuperado abaixo.
2. Entregue respostas completas, explicativas e bem estruturadas.
3. Não invente fatos, nomes, datas ou detalhes não presentes no contexto.
4. Se o contexto for insuficiente, diga explicitamente o que não foi encontrado.
5. Quando útil, apresente a resposta em tópicos para facilitar a leitura.

Contexto RAG:

{contexto}

Pergunta do usuário:

{req.pergunta}
"""

    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt
    )

    return {
        "resposta": response.text
    }