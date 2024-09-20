def on_message(self, *, message):
    print(f"[LOG  ] Message from {message.author}: {message.content}")
