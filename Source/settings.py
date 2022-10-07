import random

params = {
    "mode": "online",  # online/offline/fog of war
    "board_name": "classic",
    "log_level": "",
    "debug": True,
    "online_host_ip": "192.168.42.174",  # "192.168.1.13" "26.238.243.152"
    "online_host_port": 8080,
    "nickname": "",  # if empty use input
    "screen_size": (600, 600),
    "app_name": "Chess Fog of War",
    "app_icon": "Source/Image/icon.png",
    "max_fps": 30,
    "is_on_rotation": True,
    "start_window": "Menu",  # "Load" for production
    "is_flip_screen": False,
    "code": 0,
    "game_exist": False,
    "have_answer": False,
    "loading_window_time": 12,
    "after_load": "Menu",
    "game_logs_dir": "\\user\\game_logs",
    "game_logs_new_file": True,
}

nicknames = ["NIKI", "RJKZ", "RJKZAVR", "NIKOLAUSUS", "NIKNIKSHAM", "TSAR", "N1K0LAY78", "NIKTV_78"]


def set_random_nickname():
    params["nickname"] = random.choice(nicknames) + "_" + str(random.choice(range(1, 100001)))
    return params["nickname"]
