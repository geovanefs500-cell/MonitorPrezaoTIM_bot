from http.server import BaseHTTPRequestHandler
import json
import os
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
SITE = "https://prezaofree.com.br/"

def enviar(chat_id, texto, teclado=None):
    dados = {"chat_id": chat_id, "text": texto}
    if teclado:
        dados["reply_markup"] = teclado
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        json=dados,
        timeout=20
    )

def verificar_site():
    try:
        r = requests.get(
            SITE,
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        return "ONLINE" if r.status_code == 200 else f"INDISPONÍVEL (HTTP {r.status_code})"
    except requests.RequestException as erro:
        return f"SEM CONEXÃO ({erro})"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        dados = json.loads(self.rfile.read(tamanho) or b"{}")

        mensagem = dados.get("message", {})
        chat_id = mensagem.get("chat", {}).get("id")
        comando = mensagem.get("text", "").strip()

        if chat_id:
            if comando == "/start":
                teclado = {
                    "keyboard": [
                        [{"text": "📊 Consultar status"}],
                        [{"text": "🌐 Abrir site"}, {"text": "❓ Ajuda"}]
                    ],
                    "resize_keyboard": True
                }
                enviar(chat_id, "🤖 Monitor Prezão e TIM\n\nEscolha uma opção:", teclado)

            elif comando in ["/status", "📊 Consultar status"]:
                site = verificar_site()
                texto = (
                    "📊 STATUS DOS SERVIÇOS\n\n"
                    f"🌐 Site Prezão Free: {site}\n\n"
                    "📱 Aplicativo Prezão Free: NÃO VERIFICADO\n"
                    "📱 Aplicativo TIM Fun: NÃO VERIFICADO\n\n"
                    "Os aplicativos precisam de sinais públicos "
                    "confiáveis para confirmar indisponibilidade."
                )
                enviar(chat_id, texto)

            elif comando in ["/site", "🌐 Abrir site"]:
                enviar(chat_id, f"🌐 Acesse o Prezão Free:\n{SITE}")

            elif comando in ["/ajuda", "❓ Ajuda"]:
                enviar(
                    chat_id,
                    "Comandos disponíveis:\n"
                    "/start - Iniciar\n"
                    "/status - Consultar status\n"
                    "/site - Abrir site\n"
                    "/ajuda - Ajuda"
                )

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")