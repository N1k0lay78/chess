import csv


def change_config(param, edited_value):
    data = []
    with open('user/settings.config', 'r', newline='') as csvfile:
        csv_data = csv.reader(csvfile, delimiter=':', quotechar='\n')
        for key, value in csv_data:
            data.append([key, value])

    with open('user/settings.config', 'w', newline='') as csvfile:
        csv_data = csv.writer(csvfile, delimiter=':', quotechar='\n',
                                quoting=csv.QUOTE_MINIMAL)
        for key, value in data:
            if key == param:
                csv_data.writerow([key, edited_value])
            else:
                csv_data.writerow([key, value])
