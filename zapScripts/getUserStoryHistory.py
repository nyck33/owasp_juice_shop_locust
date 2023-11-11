from zapv2 import ZAPv2

# Initialize the ZAP API client with the address, port, and API key of your ZAP instance
zap = ZAPv2(apikey='3sddebkd6g80063kk45cgbvf31', proxies={'http': 'http://localhost:8080', 'https': 'http://localhost:8080'})


# Get the list of messages
messages = zap.core.messages()

print(messages[0] if messages else "No messages found")


# Filter messages for interactions with localhost:3000
filtered_messages = [msg for msg in messages if 'localhost:3000' in msg['requestHeader'].split(' ')[1]]

# Save the filtered messages to a file
with open('filtered_history.txt', 'w') as file:
    for msg in filtered_messages:
        file.write(f"Message ID: {msg['id']}\n")
        file.write(f"Request URL: {msg['requestHeader'].split(' ')[1]}\n")
        file.write(f"Request Header: {msg['requestHeader']}\n")
        file.write(f"Request Body: {msg['requestBody']}\n")
        file.write(f"Response Header: {msg['responseHeader']}\n")
        file.write(f"Response Body: {msg['responseBody']}\n")
        file.write('\n')
