import base64
import hashlib
import os
import urllib.parse
import urllib.request

client_id = ""
client_secret = ""
redirect_uri = ""
scopes = ["tweet.read", "tweet.write", "users.read", "offline.access"]


def validate_credentials():
    """認証情報が設定されているか確認する"""
    if not client_id or not client_secret or not redirect_uri:
        print("エラー: client_id、client_secret、redirect_uriが設定されていません")
        return False
    return True


def get_authorization_url(code_challenge):
    """認証URLを生成する"""
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "state": "state",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    return "https://x.com/i/oauth2/authorize?" + urllib.parse.urlencode(params)


def get_authorization_code(authorization_response):
    """リダイレクトURLから認証コードを抽出する"""
    parsed_url = urllib.parse.urlparse(authorization_response)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    code = query_params.get("code", [None])[0]

    if not code:
        print("エラー: 認証コードが見つかりません")
        return
    return code


def main():
    if not validate_credentials():
        return

    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").replace("=", "")
    )

    challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(challenge).decode("utf-8").replace("=", "")
    )

    auth_url = get_authorization_url(code_challenge)
    print(f"認証 URL: {auth_url}")

    auth_response = input("認証後にリダイレクトされたURLを入力してください: ")

    code = get_authorization_code(auth_response)
    if not code:
        return

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

    request = urllib.request.Request(
        "https://api.x.com/2/oauth2/token", encoded_data, headers
    )

    try:
        with urllib.request.urlopen(request) as response:
            body = response.read()
            print(body)
            return
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Response body: {e.read().decode('utf-8')}")
        return


if __name__ == "__main__":
    main()
