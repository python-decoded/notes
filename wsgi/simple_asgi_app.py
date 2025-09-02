
async def asgi_app(scope: dict, receive, send):

    body = b''
    while True:
        message = await receive()
        body += message.get('body', b'')
        if not message.get('more_body', False):
            break

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [('content-type', 'text/plain')]
    })

    response_body = f"""
        Hi there!!!
        {'\n'.join(str(i) for i in scope.items())}
        {body}
    """

    await send({
        'type': 'http.response.body',
        'body': response_body.encode("utf-8")
    })
