import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def logar_em_google_sheets(mensagem, resposta):
    # Define escopo
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    # Autentica com a conta de serviço
    creds = ServiceAccountCredentials.from_json_keyfile_name("/etc/secrets/credentials.json", scope)
    client = gspread.authorize(creds)

    # Acessa a planilha via ID e a aba 1
    sheet = client.open_by_key("1RJUBdYE0pnFP0nCHF4dE6Lqoo3SrVkXmYEfHQScC8").sheet1

    # Loga (data/hora, mensagem recebida, resposta gerada)
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([data_hora, mensagem, resposta])
