from email.parser import BytesParser

with open("email.eml", "rb") as f:
    message = BytesParser().parse(f)

# headers
len(message)
dict(message)

message["From"]
message.get("Subject")
message.get_all("To")

# content-type
message.get("Content-Type")
message.get_content_type()
message.get_content_maintype()
message.get_content_subtype()

# payloads
payloads = message.get_payload()  # assume we have 2 payloads
len(payloads)

payload_1, payload_2 = payloads

payload_1.get_content_type()  # assume 1st is plain text
text = payload_1.get_payload()
text[:100]

payload_2.get_content_type()  # assume 2nd is html
html = payload_2.get_payload()
html[:100]
