from twilio.rest import Client

# Your Account SID and Auth Token from console.twilio.com


client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+91 9510123175",
    from_="+12015590637",
    body="Lodu Lalit")

print(message.sid)