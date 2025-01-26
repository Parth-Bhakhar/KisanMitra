from twilio.rest import Client

# Your Account SID and Auth Token from console.twilio.com
account_sid = "ACfa186fc6fe8d62e038bd50b3546822b1"
auth_token  = "f2326e3d755f7528d05f223a89dc72a8"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+91 9510123175",
    from_="+12015590637",
    body="Lodu Lalit")

print(message.sid)