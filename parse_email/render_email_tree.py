from email.parser import BytesParser
from email.message import Message


def show_email_tree(message: Message, level: int = 0, show_headers=False):

    print("---" * level + f"Type: {message.get_content_type()}, {len(message)}")

    if show_headers:
        for h in message.items():
            print("   " * level + str(h))

    for payload in message.get_payload():
        if isinstance(payload, Message):
            show_email_tree(payload, level=level + 1, show_headers=show_headers)


def render_email(path):
    with open(path, "rb") as f:
        message = BytesParser().parse(f)

    print()
    show_email_tree(message)


if __name__ == "__main__":
    render_email("email.eml")
