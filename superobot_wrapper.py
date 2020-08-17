import superobot as sr
import json

if __name__ == "__main__":
    auth = None
    with open("./bot_auth.json") as f:
        auth = json.load(f)

    superobot = sr.SupeRo_Bot(auth["user"], auth["oauth"])
    for channel in auth["channels"]:
        superobot.join(channel, verbose=True)
    superobot.listen()
