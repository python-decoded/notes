from requests import session


class ApiClient:
    def __init__(self):
        self.session = session()

    @property
    def token(self):
        return self.session.headers.get("Authorization", "").removeprefix("Bearer ") or None

    @token.setter
    def token(self, token):
        self.session.headers["Authorization"] = f"Bearer {token}"

    @token.deleter
    def token(self):
        self.session.headers.pop("Authorization", None)

    def request(self, *args, **kwargs):
        return self.session.request(*args, **kwargs)


api_client = ApiClient()

# api_client.set_token("FOO")
# api_client.get_token()
# api_client.delete_token()

api_client.token = "FOO"
api_client.token
del api_client.token
