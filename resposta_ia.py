from openai import OpenAI
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Inicializa o cliente OpenAI com a chave da API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_resposta(mensagem_usuario):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensagem_usuario}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Erro ao gerar resposta: {e}"