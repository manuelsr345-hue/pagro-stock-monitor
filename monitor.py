import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8397288901")

PRODUCT_URL = "https://www.pagro.at/pokemon-30-jahre-sammelkartenspiel-top-trainer-box-196214144842.html"

# Öffentliche PAGRO-Kategorieseite
CHECK_URL = "https://www.pagro.at/spielen"


def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "disable_web_page_preview": False
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


def check_pagro():
    print("Prüfe PAGRO-Kategorieseite...")

    request = urllib.request.Request(
        CHECK_URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/140.0 Safari/537.36"
            ),
            "Accept-Language": "de-AT,de;q=0.9"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8", errors="ignore")

            print("HTTP Status:", response.status)
            print("HTML Länge:", len(html))

    except Exception as e:
        print("Fehler beim PAGRO-Abruf:", e)
        return False

    # Produkt-ID und Produktname suchen
    product_found = (
        "196214144842" in html
        or "pokemon-30-jahre-sammelkartenspiel-top-trainer-box" in html.lower()
    )

    print("Top-Trainer-Box gefunden:", product_found)

    return product_found


def main():

    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN fehlt!")

    available = check_pagro()

    if available:
        print("Produkt auf PAGRO-Seite gefunden.")

    else:
        print("Produkt nicht gefunden.")

    print("Noch KEIN Alarm – wir testen zunächst nur die Erkennung.")


if __name__ == "__main__":
    main()
