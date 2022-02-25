from flask import Flask, render_template, redirect
import config
import socket
from core.online.Server import Server


server = Server()
have_game = False
ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg']
application = Flask(__name__)
application.config.from_object(config)


def get_render_template(template_name, title, **kwargs):
    return render_template(template_name, title=title, **kwargs)


def main(port=8000):
    application.run(port=port)


# Стартовая страница
@application.route("/")
def website_main_page():
    return redirect("/create_game")


@application.route("/create_game")
def create_game():
    global have_game
    self_ip = socket.gethostbyname(socket.gethostname())
    if not have_game:
        server.create_socket(8000, self_ip)
        have_game = True
    return f"""{self_ip}"""


@application.route("/restart_game")
def restart_game():
    global have_game
    have_game = False
    return redirect("/create_game")


if __name__ == '__main__':
    main(port=8000)
