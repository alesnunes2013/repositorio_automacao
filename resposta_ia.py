import openai
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Define a chave da API
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta(mensagem_usuario):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensagem_usuario}],
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"

