from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "1F500A879AFD19B13118"

@app.route("/webhook", methods=["GET"])
def verificar_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Erro na verificação", 403

@app.route("/", methods=["GET"])
def index():
    return "Servidor ativo", 200

if __name__ == "__main__":
    app.run(debug=True)

