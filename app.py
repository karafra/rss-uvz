import os
import requests
from random import randint
from time import sleep
from src.Bot import Bot
from flask import Flask
from flask import render_template
from multiprocessing import Process
from flask_apscheduler import APScheduler

def keep_dyno_awake() -> None:
    url: str = os.environ["BASE_URL"]
    while True:
        requests.get(url)
        sleep(randint(0, 55))
            

def bot() -> None:
    Process(target=keep_dyno_awake).start()
    bot: Bot = Bot()
    bot.start()
    try:
        while True: ...
    except KeyboardInterrupt:
        bot.stop_service("email")
        bot.stop_service("rss")
        bot.stop_service("tweet")

class FlaskConfig(object):
    JOBS = [
        {
            "id": "Update RSS",
            "func": "app:bot",
        }
    ]

app: Flask = Flask(__name__)
app.config.from_object(FlaskConfig)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def default(path):
    full_path = os.path.join("static", "images", "ouroboros.gif")
    return render_template("ouroboros.html", user_image=full_path)


if __name__ == '__main__':
    app.run()