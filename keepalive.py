from flask import Flask
from threading import Thread

web_server = Flask("")


@web_server.route("/")
def respond():
    return "Bot running."


def keep_alive():
    """
    Run a minimal web server to make REPL.IT keep the bot running
    """
    Thread(target=web_server.run, args=("0.0.0.0", 8080)).start()
