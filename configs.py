from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "1669750"))
    API_HASH = getenv("API_HASH", "0f53ee8c576281995d621194aec588d8")
    BOT_TOKEN = getenv("BOT_TOKEN", "6560312984:AAG7iIu0DnpO3jpwHRgQV3jxY1QTklAc-us")
    FSUB = getenv("FSUB", "KCHDMOVIES2023")
    CHID = int(getenv("CHID", "-1001914958042"))#update channel
    SUDO = list(map(int, getenv("SUDO", "718979130").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://sudoscreen:5kEOBvPKpRoCCfyy@cluster0.swh5syh.mongodb.net/?retryWrites=true&w=majority")
    WEB_SERVER = getenv("WEB_SERVER", False)
    PORT = int(getenv("PORT", 8080))
cfg = Config()
