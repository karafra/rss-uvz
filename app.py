import os
from src import errors
from flask import Flask
from flask import render_template
from flask_apscheduler import APScheduler, scheduler


class FlaskConfig(object):
    JOBS = [
        {
            "id": "Update RSS",
            "func": "src:listen_for_updates",
        }
    ]


app: Flask = Flask(__name__)
app.config.from_object(FlaskConfig)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

app.register_blueprint(errors)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def default(path):
    full_path = os.path.join("static", "images", "ouroboros.gif")
    return render_template("ouroboros.html", user_image=full_path)

if __name__ == '__main__':
    app.run()
