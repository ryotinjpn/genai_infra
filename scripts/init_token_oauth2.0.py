import base64
import hashlib
import os
import urllib.parse
import urllib.request

client_id = ""
client_secret = ""
redirect_uri = ""
scopes = ["tweet.read", "tweet.write", "users.read", "offline.access"]

code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
code_verifier = code_verifier.replace("=", "")

code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
code_challenge = code_challenge.replace("=", "")

params = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": " ".join(scopes),
    "state": "state",
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
}

authorization_url = "https://x.com/i/oauth2/authorize?" + urllib.parse.urlencode(params)
print(f"認証 URL: {authorization_url}")

authorization_response = input("認証後にリダイレクトされたURLを入力してください: ")

parsed_url = urllib.parse.urlparse(authorization_response)
query_params = urllib.parse.parse_qs(parsed_url.query)
code = query_params.get("code", [None])[0]

data = {
    "code": code,
    "grant_type": "authorization_code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "code_verifier": code_verifier,
}
encoded_data = urllib.parse.urlencode(data).encode()

auth = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/x-www-form-urlencoded",
}
req = urllib.request.Request("https://api.x.com/2/oauth2/token", encoded_data, headers)

try:
    with urllib.request.urlopen(req) as res:
        body = res.read()
        print(body)
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print(f"Response body: {e.read().decode('utf-8')}")
