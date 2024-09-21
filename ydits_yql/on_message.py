def on_message(self, *, message):
    print(f"[LOG  ] {message.author} からのメッセージ: {message.content}")
