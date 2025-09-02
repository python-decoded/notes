from typing import Iterable


def wsgi_app(environ: dict, start_response: callable) -> Iterable[bytes]:

    response_status = "200 OK"
    response_headers = [("Content-type", "text/plain")]
    start_response(response_status, response_headers)

    body = environ["wsgi.input"].read().decode("utf-8")

    return [
        b"Hi There!!!\n",
        "\n".join(str(i) for i in environ.items()).encode("utf-8"),
        b"\n",
        body.encode("utf-8")
    ]






