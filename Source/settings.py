params = {
    "mode": "offline",  # online/offline/fog of war
    "board_name": "classic",
    "log_level": "",
    "debug": False,
    "online_host_ip": "192.168.1.71",  # "192.168.1.13" "26.238.243.152"
    "online_host_port": 8080,
    "nickname": "",  # if empty use input
    "screen_size": (600, 600),
    "app_name": "Chess Fog of War",
    "app_icon": "Source/Image/icon.png",
    "max_fps": 30,
    "start_window": "Game",  # "Load" for production
    "is_flip_screen": False,
}

is_on_fog_of_war = False
name_board_to_play = "classic"
is_online = True
debug = False
online_host_ip = "192.168.1.71"  # "192.168.1.13" "26.238.243.152"
online_host_port = 8080
nickname = ""  # if empty use input


def set_param(param, value):
    params[param] = value


def get_param(param):
    return params[param]
