import random

params = {
    "mode": "online",  # online/offline/fog of war
    "board_name": "test2",
    "log_level": "",
    "debug": False,
    "online_host_ip": "192.168.1.13",  # "192.168.1.13" "26.238.243.152"
    "online_host_port": 8080,
    "nickname": "",  # if empty use input
    "screen_size": (600, 600),
    "app_name": "Chess Fog of War",
    "app_icon": "Source/Image/icon.png",
    "max_fps": 30,
    "is_on_rotation": True,
    "start_window": "Test",  # "Load" for production
    "is_flip_screen": False,
    "code": 0,
}

# is_on_fog_of_war = False
# name_board_to_play = "test2"
# is_online = True
# # debug = False
# # online_host_ip = "192.168.1.71"  # "192.168.1.13" "26.238.243.152"
# # online_host_port = 8080
# debug = True
# online_host_ip = "192.168.1.13"  # "26.238.243.152"
# online_host_port = 5050
# nickname = ""  # if empty use input

nicknames = ["NIKI", "RJKZ", "RJKZAVR", "NIKOLAUSUS", "NIKNIKSHAM", "TSAR", "N1K0LAY78", "NIKTV_78"]


def set_random_nickname():
    params["nickname"] = random.choice(nicknames) + "_" + str(random.choice(range(1, 100001)))
    return params["nickname"]