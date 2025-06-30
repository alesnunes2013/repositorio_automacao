import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Função para logar a interação no Google Sheets
def logar_em_google_sheets(mensagem, resposta):
    # Define o escopo de acesso à API
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Autenticação com a conta de serviço
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "/etc/secrets/credentials.json", scope
    )
    client = gspread.authorize(creds)

    # Acessa a planilha e a primeira aba
    planilha = client.open("log_ia_dm_instagram").sheet1

    # Prepara e envia o log (data/hora, mensagem, resposta)
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    planilha.append_row([data_hora, mensagem, resposta])
