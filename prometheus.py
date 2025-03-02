from flask import Flask, request
import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

def send_message(chat_id, text):
    url = API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    print(f"[LOG] Enviando mensagem para {chat_id}: {text}, Status: {response.status_code}")

@app.route("/", methods=["GET"])
def index():
    return "Webhook do Oráculo está rodando!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    update = request.get_json()
    print("[LOG] Recebendo atualização do Telegram:", update)  # Log completo
    
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "").strip()
        print(f"[LOG] Mensagem recebida: {text}")
        
        if text.lower() == "/status":
            send_message(chat_id, "Seu saldo atual é $10.000")
        elif text.lower().startswith("/comprar"):
            send_message(chat_id, "Ordem de compra recebida!")
        elif text.lower().startswith("/vender"):
            send_message(chat_id, "Ordem de venda recebida!")
        else:
            send_message(chat_id, "Comando não reconhecido. Use /status, /comprar ou /vender")
    else:
        print("[LOG] Nenhuma mensagem detectada no update.")
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
