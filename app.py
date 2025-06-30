from flask import Flask, render_template, request
from resposta_ia import gerar_resposta
import csv
from datetime import datetime

app = Flask(__name__)

LOG_FILE = 'log.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    resposta = None
    if request.method == 'POST':
        mensagem = request.form['mensagem']
        resposta = gerar_resposta(mensagem)
        with open(LOG_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now(), mensagem, resposta])
    return render_template('index.html', resposta=resposta)

if __name__ == '__main__':
    app.run(debug=True)