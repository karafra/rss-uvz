import multiprocessing
import os
import threading
from time import sleep
from src.Bot import Bot
from flask import Flask
from flask import render_template
from flask_apscheduler import APScheduler
#from src import listen_for_updates
from dotenv import load_dotenv

'''
class FlaskConfig(object):
    JOBS = [
        {
            "id": "Update RSS",
            "func": "app:test",
        }
    ]


class App(Flask):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(__name__, *args, **kwargs)


app: App = App()
app.config.from_object(FlaskConfig)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def default(path):
    full_path = os.path.join("static", "images", "ouroboros.gif")
    return render_template("ouroboros.html", user_image=full_path)

'''
if __name__ == '__main__':
    
    def test():
        bot: Bot = Bot()
        bot.start()
        while True: ...
    test()