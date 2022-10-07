import csv

initializer = {
    "max_fps": lambda x: int(x),
    "debug": lambda x: x == '1',
    "host_ip": lambda x: x,
    "host_port": lambda x: int(x),
    "nickname": lambda x: x,
    "screen_size": lambda x: list(map(int, x.split(','))),
    "flip_board": lambda x: x == '1',
}


def config_initializer(config_dict):
    config_dict['is_online'] = False
    config_dict['debug'] = False
    config_dict['log_level'] = ""
    config_dict['app_name'] = "Chees Fog of War"
    config_dict['app_icon'] = "Source/Image/icon.png"
    config_dict['start_window'] = "Load"
    config_dict['debug'] = False
    config_dict['loading_window_time'] = 12
    with open('user/settings.config', 'r', newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=':', quotechar='\n')
        for key, value in csv_data:
            config_dict[key] = initializer[key](value)
