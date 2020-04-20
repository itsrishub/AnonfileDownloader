import os

class Var(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

class Development(Var):
    LOGGER = True
    # Here for later purposes
