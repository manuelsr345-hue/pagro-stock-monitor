import urllib.request

URLS = [
    "https://www.pagro.at/store-api/product",
    "https://www.pagro.at/api/product",
    "https://www.pagro.at/api/search",
]

for url in URLS:
    print()
    print("Teste:", url)

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json"
            }
        )

        with urllib.request.urlopen(request, timeout=20) as response:
            print("HTTP:", response.status)
            print("Content-Type:", response.headers.get("Content-Type"))
            print("Antwort:", response.read(500).decode("utf-8", errors="ignore"))

    except Exception as e:
        print("Fehler:", e)
