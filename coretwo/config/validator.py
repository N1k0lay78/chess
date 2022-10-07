import csv
import re

validations = {
    "max_fps": lambda x: int(x) in range(1, 120),
    "debug": lambda x: int(x) in range(2),
    "host_ip": lambda x: [0 <= int(x) < 256 for x in
                          re.split('\.', re.match(r'^\d+\.\d+\.\d+\.\d+$', x).group(0))].count(True) == 4,
    "host_port": lambda x: int(x) in range(20, 9000),
    "nickname": lambda x: len(x) < 15,
    "screen_size": lambda x: 600 <= int(x.split(',')[0]) and 600 <= int(x.split(',')[1]),
    "flip_board": lambda x: int(x) in range(2),
}


def config_validator():
    with open('user/settings.config', 'r', newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=':', quotechar='\n')
        for key, value in csv_data:
            if not key in validations:
                return f"Error at validate settings.config key '{key}' is't defined"
            elif not validations[key](value):
                return f"Error at validate settings.config param '{key}'"

    return ""
