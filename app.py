from flask import Flask, request, jsonify
from resposta_ia import gerar_resposta
from logger import logar_em_google_sheets
import requests
import os

app = Flask(__name__)

VERIFY_TOKEN = "1F500A879AFD19B13118"
PAGE_ACCESS_TOKEN = "IGAAZAtNznD6MpBZAE4wX3B5aE52elB3VTM4aFdGOG5hVTFHSm1YQU5CQVFtajFqMnJiVHJ4YmpXTXBRYzBBMkxJQmxBS1htbG1LWHBya1pEQ2tOX01LZAncwTEZAFaUxkejd6eUlkWUN5QzNYVXBXQkdZAZAEgxeUFlbV9UODQwZAWFrQQZDZD"  # <-- Substitua pelo seu token de página válido

@app.route("/", methods=["GET"])
def index():
    return "Servidor está ativo!", 200

# ✅ Verificação inicial do webhook
@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
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

# ✅ Envio da resposta automática ao Instagram
def enviar_resposta(id_usuario, mensagem):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": id_usuario},
        "message": {"text": mensagem}
    }
    headers = {"Content-Type": "application/json"}
    resposta = requests.post(url, json=payload, headers=headers)
    print("📤 Resposta enviada:", resposta.json())

# ✅ Escuta a porta correta no ambiente da Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
