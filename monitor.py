import os
import json
import requests
from datetime import datetime

SITE = "https://prezaofree.com.br/"
ARQUIVO = "status.json"

def verificar():
    try:
        r = requests.get(
            SITE,
            timeout=25,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        return "online" if r.status_code == 200 else "offline"
    except requests.RequestException:
        return "offline"

def avisar(mensagem):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat = os.environ["TELEGRAM_CHAT_ID"]

    requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat, "text": mensagem},
        timeout=20
    ).raise_for_status()

atual = verificar()

try:
    with open(ARQUIVO) as f:
        anterior = json.load(f)["status"]
except (OSError, ValueError, KeyError):
    anterior = None

if anterior is None:
    avisar(f"🤖 Monitor Prezão iniciado. Estado atual: {atual}")
elif anterior != atual:
    hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    avisar(
        f"🚨 Prezão Free mudou de estado!\n"
        f"Anterior: {anterior}\n"
        f"Atual: {atual}\n"
        f"Horário: {hora}\n{SITE}"
    )

with open(ARQUIVO, "w") as f:
    json.dump({"status": atual}, f)

print("Verificação concluída:", atual)