from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def logar_em_google_sheets(mensagem, resposta):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1RJJUBdYE0pnFPOnCHF4AdE6Lqoo3sSrVkXmYEHfQ5C8").sheet1

    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        sheet.append_row([data_hora, mensagem, resposta])
        print("✅ Registro salvo:", data_hora, mensagem, resposta)
    except Exception as e:
        print("❌ Erro ao gravar no Google Sheets:", e)

