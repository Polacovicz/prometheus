from flask import Flask, request
import requests

TOKEN = "SEU_TOKEN_AQUI"
API_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

def send_message(chat_id, text):
    url = API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def index():
    return "Webhook do Oráculo está rodando!", 200

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    print("Recebendo atualização:", update)  # Log para depuração
    
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        print(f"Mensagem recebida: {text}")  # Log da mensagem recebida
        
        if text.lower() == "/status":
            send_message(chat_id, "Seu saldo atual é $10.000")
        elif text.lower().startswith("/comprar"):
            send_message(chat_id, "Ordem de compra recebida!")
        elif text.lower().startswith("/vender"):
            send_message(chat_id, "Ordem de venda recebida!")
        else:
            send_message(chat_id, "Comando não reconhecido. Use /status, /comprar ou /vender")
    
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
