from flask import Flask, request, jsonify
from resposta_ia import gerar_resposta
from logger import logar_em_google_sheets
import requests
import os
from dotenv import load_dotenv

# ✅ Carrega variáveis do .env
load_dotenv()

# ✅ Tokens carregados de variáveis de ambiente
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("INSTAGRAM_TOKEN")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "Servidor está ativo!", 200

# ✅ Verificação do Webhook pelo Facebook
@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Verificação do webhook realizada com sucesso.")
        return challenge, 200
    else:
        print("❌ Verificação do webhook falhou.")
        return "Erro na verificação", 403

# ✅ Recebimento de mensagens do Instagram
@app.route("/webhook", methods=["POST"])
def receber_mensagem():
    payload = request.get_json()
    print("📩 Webhook recebido:", payload)

    try:
        for entry in payload.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event["sender"]["id"]

                if "message" in messaging_event and "text" in messaging_event["message"]:
                    texto_recebido = messaging_event["message"]["text"]
                    print("✉️ Texto recebido:", texto_recebido)

                    resposta = gerar_resposta(texto_recebido)
                    print("🤖 Resposta IA:", resposta)

                    enviar_resposta(sender_id, resposta)
                    logar_em_google_sheets(texto_recebido, resposta)

        return "Mensagem processada", 200

    except Exception as e:
        print("❌ Erro ao processar webhook:", e)
        return "Erro no processamento", 500

# ✅ Envio da resposta automática via API Graph
def enviar_resposta(id_usuario, mensagem):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": id_usuario},
        "message": {"text": mensagem}
    }
    headers = {"Content-Type": "application/json"}

    try:
        resposta = requests.post(url, json=payload, headers=headers)
        print("📤 Resposta enviada:", resposta.json())
    except Exception as e:
        print("❌ Falha ao enviar resposta:", e)

# ✅ Porta compatível com Render.com
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render define PORT automaticamente
    app.run(debug=True, host="0.0.0.0", port=port)


