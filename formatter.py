import main
import csv


def extract_csv_data(file):
    csv_list = []
    with open(file, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=' ')
        for row in reader:
            csv_list.append(row)
    usable_csv_list = []
    for line in csv_list:
        csv_item = main.separate_csv_items(line)
        usable_csv_list.append(csv_item)
    return usable_csv_list


def average_controls(imported_list):
    avg_list = []
    avg_var = 0
    csv_counter = 0

    for num in range(1, len(imported_list) - 1):
        avg_var += float(imported_list[num][3])
        csv_counter += 1
        if csv_counter == 6:
            csv_counter = 0
            avg_var = round(avg_var / 6.0)
            avg_list.append(avg_var)
            avg_var = 0
    return avg_list
