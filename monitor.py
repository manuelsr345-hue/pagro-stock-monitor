import os
import urllib.request
import urllib.parse

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8397288901")


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }).encode()

    request = urllib.request.Request(
        url,
        data=data,
        method="POST"
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        result = response.read().decode()

    print("Telegram Antwort:")
    print(result)


def main():

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN fehlt!")

    send_telegram(
        "✅ PAGRO-MONITOR TEST\n\n"
        "Telegram funktioniert! 🚀"
    )


if __name__ == "__main__":
    main()
