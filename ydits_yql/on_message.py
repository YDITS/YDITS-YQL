def on_message(self, *, message):
    if is_me(self, message=message):
        return

    if is_bot(message=message):
        return


def is_me(self, *, message):
    return message.author == self.user


def is_bot(*, message):
    return message.author.bot
