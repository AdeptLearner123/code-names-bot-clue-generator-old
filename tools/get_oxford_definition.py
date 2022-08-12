import sys
import requests
import json

def main():
    term = sys.argv[1]

    app_id = "16ac7881"
    app_key = "70911ba7775224cbe7a2980d3027f628"

    url = f"https://od-api.oxforddictionaries.com/api/v2/entries/en-us/{term}"
    r = requests.get(url, headers = { "app_id": app_id, "app_key": app_key })

    print("Code", r.status_code)
    print("Text", r.text)
    print("Json", json.dumps(r.json()))

if __name__ == "__main__":
    main()
