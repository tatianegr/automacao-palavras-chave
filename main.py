import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests

# Autenticação com Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Abra a planilha (altere o nome se necessário)
spreadsheet = client.open("Gerador de Palavras-chave")
aba_termos = spreadsheet.worksheet("Entrada")
aba_resultados = spreadsheet.worksheet("Resultados")

# Leia os termos
termos = aba_termos.col_values(1)[1:]  # pula cabeçalho

def buscar_sugestoes(term):
    url = f"https://suggestqueries.google.com/complete/search?client=firefox&q={term}"
    response = requests.get(url)
    if response.status_code == 200:
        sugestoes = response.json()[1]
        return sugestoes
    return []

# Escreve os resultados na aba 'Resultados'
aba_resultados.clear()
aba_resultados.update("A1", [["Termo", "Sugestões"]])

linhas = []
for termo in termos:
    sugestoes = buscar_sugestoes(termo)
    linhas.append([termo, ", ".join(sugestoes)])

aba_resultados.update(f"A2", linhas)

print("Sugestões adicionadas com sucesso!")
