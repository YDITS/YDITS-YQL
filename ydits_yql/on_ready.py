def on_ready(self, *, init_channels):
    print(f"[INFO ] Logged in as {self.user}.")
    channels = {}
    channels["vxww50"] = self.get_channel(self.channels_id["vxww50"])
    init_channels(channels)
