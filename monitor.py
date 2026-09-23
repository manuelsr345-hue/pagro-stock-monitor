import os
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

PRODUCT_URL = "https://www.pagro.at/pokemon-30-jahre-sammelkartenspiel-top-trainer-box-196214144842.html"

STATE_FILE = Path("stock_state.json")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "8397288901")


def send_telegram(message):
    import urllib.request
    import urllib.parse

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
        return response.read().decode()


def load_state():
    if not STATE_FILE.exists():
        return None

    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return None


def save_state(state):
    STATE_FILE.write_text(
        json.dumps(state, indent=2)
    )


def check_product():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            viewport={
                "width": 390,
                "height": 844
            },
            user_agent=(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) "
                "AppleWebKit/605.1.15 "
                "(KHTML, like Gecko) "
                "Version/18.0 Mobile/15E148 Safari/604.1"
            ),
            locale="de-AT"
        )

        print("Öffne PAGRO...")

        response = page.goto(
            PRODUCT_URL,
            wait_until="domcontentloaded",
            timeout=60000
        )

        print(
            "HTTP Status:",
            response.status if response else "unknown"
        )

        # Warten, damit die Seite vollständig laden kann
        page.wait_for_timeout(5000)

        title = page.title()

        print("Seitentitel:", title)

        body_text = page.locator("body").inner_text().lower()

        availability_terms = [
            "in den warenkorb",
            "jetzt kaufen",
            "verfügbar",
            "lieferbar",
            "auf lager",
            "lagernd"
        ]

        unavailable_terms = [
            "nicht verfügbar",
            "nicht lieferbar",
            "ausverkauft",
            "out of stock"
        ]

        available_hits = [
            term
            for term in availability_terms
            if term in body_text
        ]

        unavailable_hits = [
            term
            for term in unavailable_terms
            if term in body_text
        ]

        # Buttons auslesen
        buttons = page.locator("button")

        button_texts = []

        for i in range(min(buttons.count(), 100)):

            try:
                text = buttons.nth(i).inner_text().strip()

                if text:
                    button_texts.append(text)

            except Exception:
                pass

        print()
        print("Buttons:")

        for button in button_texts:
            print(" -", button)

        available = False

        # Textprüfung
        if available_hits and not unavailable_hits:
            available = True

        # Buttonprüfung
        for button in button_texts:

            normalized = button.lower()

            if (
                "warenkorb" in normalized
                or "kaufen" in normalized
            ):

                if (
                    "nicht" not in normalized
                    and "ausverkauft" not in normalized
                ):
                    available = True

        print()
        print(
            "Verfügbarkeits-Treffer:",
            available_hits
        )

        print(
            "Nicht-verfügbar-Treffer:",
            unavailable_hits
        )

        print(
            "ERKANNT ALS VERFÜGBAR:",
            available
        )

        # Debug-Datei speichern
        debug = {
            "title": title,
            "http_status": (
                response.status
                if response
                else None
            ),
            "available": available,
            "available_hits": available_hits,
            "unavailable_hits": unavailable_hits,
            "buttons": button_texts
        }

        Path("debug.json").write_text(
            json.dumps(
                debug,
                indent=2,
                ensure_ascii=False
            )
        )

        browser.close()

        return available


def main():

    if not TELEGRAM_BOT_TOKEN:

        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN fehlt."
        )

    available = check_product()

    old_state = load_state()

    old_available = None

    if old_state:
        old_available = old_state.get(
            "available"
        )

    new_state = {
        "available": available
    }

    save_state(new_state)

    # Nur bei Wechsel von NICHT verfügbar
    # zu verfügbar Telegram senden
    if available and old_available is not True:

        message = (
            "🚨 PAGRO STOCK ALERT 🚨\n\n"
            "Pokémon 30 Jahre Sammelkartenspiel "
            "Top-Trainer-Box ist möglicherweise verfügbar!\n\n"
            "💰 55 €\n\n"
            f"{PRODUCT_URL}"
        )

        send_telegram(message)

        print(
            "🚨 TELEGRAM-ALARM GESENDET!"
        )

    elif available:

        print(
            "Produkt weiterhin verfügbar – "
            "kein neuer Alarm."
        )

    else:

        print(
            "Produkt nicht verfügbar."
        )


if __name__ == "__main__":
    main()
