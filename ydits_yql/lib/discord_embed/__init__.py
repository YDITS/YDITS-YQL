from discord import Embed


class DiscordEmbed(Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if kwargs.get("author"):
            self.author = kwargs["author"]

        if kwargs.get("fields"):
            self.fields = kwargs["fields"]

        if kwargs.get("footer"):
            self.footer = kwargs["footer"]

        if kwargs.get("image"):
            self.image = kwargs["image"]

        if kwargs.get("video"):
            self.video = kwargs["video"]
