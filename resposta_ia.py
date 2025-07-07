import openai
import os

# Define a chave da API diretamente do ambiente Render (não precisa do .env)
openai.api_key = os.getenv("OPENAI_API_KEY")

def gerar_resposta(mensagem_usuario):
    try:
        print(f"🔍 Gerando resposta para: {mensagem_usuario}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensagem_usuario}],
            temperature=0.7
        )

        resposta = response.choices[0].message["content"].strip()
        print(f"✅ Resposta gerada: {resposta}")
        return resposta

    except Exception as e:
        erro = f"Erro ao gerar resposta: {e}"
        print(f"❌ {erro}")
        return erro

