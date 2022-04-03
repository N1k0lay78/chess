from flask import Flask, render_template, redirect
import config
import socket
from core.online.Server import Server
from Source.settings import params

self_ip = socket.gethostbyname(socket.gethostname())
server = Server(self_ip, 51600)
have_game = False
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
app = Flask(__name__)
app.config.from_object(config)


def get_render_template(template_name, title, **kwargs):
    return render_template(template_name, title=title, **kwargs)


def main(port=8000):
    if params["debug"]:
        global have_game
        if not have_game:
            server.create_game(1234, 4)
            have_game = True
    else:
        app.run(port=port)


# Стартовая страница
@app.route("/")
def website_main_page():
    return redirect("/create_game")


@app.route("/create_game")
def create_game():
    global have_game
    self_ip = socket.gethostbyname(socket.gethostname())
    if not have_game:
        server.create_game(1234, 4)
        have_game = True
    return f"""{self_ip}"""


@app.route("/restart_game")
def restart_game():
    # global have_game
    # have_game = False
    return redirect("/create_game")


if __name__ == '__main__':
    main(port=8000)
