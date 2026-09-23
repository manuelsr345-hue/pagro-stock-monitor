import urllib.request

PAGRO_URL = "https://www.pagro.at/pokemon-30-jahre-sammelkartenspiel-top-trainer-box-196214144842.html"

JINA_URL = "https://r.jina.ai/" + PAGRO_URL

print("Teste Jina Reader...")
print("URL:", JINA_URL)

request = urllib.request.Request(
    JINA_URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

try:
    with urllib.request.urlopen(request, timeout=60) as response:

        status = response.status
        content = response.read().decode(
            "utf-8",
            errors="ignore"
        )

        print("HTTP Status:", status)
        print("Antwort-Länge:", len(content))
        print()
        print("ERSTE 3000 ZEICHEN:")
        print(content[:3000])

except Exception as e:
    print("FEHLER:", e)
