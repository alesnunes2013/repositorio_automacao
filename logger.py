from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def logar_em_google_sheets(mensagem, resposta):
    # Escopos necessários para acesso ao Sheets e Drive
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        # Autenticação com o arquivo JSON
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
        client = gspread.authorize(creds)

        # Abertura da planilha pelo ID
        sheet = client.open_by_key("1RJJUBdYE0pnFPOnCHF4AdE6Lqoo3sSrVkXmYEHfQ5C8").sheet1

        # Geração da data/hora atual
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Envio para o Google Sheets
        sheet.append_row([data_hora, mensagem, resposta])
        print("✅ Registro salvo:", data_hora, mensagem, resposta)

    except Exception as e:
        print("❌ Erro ao gravar no Google Sheets:", e)


