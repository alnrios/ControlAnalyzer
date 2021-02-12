from main import d1_list, d1_dict, d7_dict, d7_list
import os
from formatter import extract_csv_data, average_controls
import openpyxl
from math import ceil
import sys
# run this file


def control_avg_function(control_dict, cell_line_dict_ID):
    for result_sheet in directory:
        for tech in control_dict:
            for day in control_dict[tech]:
                for barcode in control_dict[tech][day]:
                    if barcode in result_sheet:
                        results_var = average_controls(extract_csv_data('results/{}'.format(result_sheet)))
                        control_list_length = len(control_dict[tech][day][barcode])
                        """ The below if statement is necessary bc if the list is only 1 cell line, then the range below 
                            that needs to be at least 1 in length. So it is purely for indexing purposes"""
                        if control_list_length > 1:
                            control_list_length = control_list_length - 1
                        for i in range(control_list_length):
                            cell_lines.append('{0}: {1}'.format(control_dict[tech][day][barcode][i], str(results_var[i])))
                            ctrl_avg_dict[cell_line_dict_ID][control_dict[tech][day][barcode][i]] = str(results_var[i])


def create_excel_file():
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = 'Control Averages'

    sheet['A1'].value = 'Cell Line'
    sheet['B1'].value = 'Day 1'
    sheet['C1'].value = 'D1 AVG'
    sheet['D1'].value = 'Day 7'
    sheet['E1'].value = 'D7 AVG'
    sheet['F1'].value = 'Difference (D7 - D1)'
    sheet['G1'].value = 'Increase Factor'
    wb.save('AvgControlSheet.xlsx')


def write_excel_file(file, control_dict, average_dict):
    num_of_missing_barcodes = 0
    excel_counter = 2
    control_list_counter = 0
    wb = openpyxl.load_workbook(file)
    sheet = wb.active
    for tech in control_dict:
        for date in control_dict[tech]:
            for barcode in control_dict[tech][date]:
                day1_barcode = d1_list[control_list_counter]
                day7_barcode = d7_list[control_list_counter]
                control_list_counter += 1
                missing_check = True
                for cell_name in control_dict[tech][date][barcode]:
                    if cell_name in average_dict['Day1'] and cell_name in average_dict['Day7']:
                        sheet['A{}'.format(excel_counter)].value = cell_name
                        sheet['B{}'.format(excel_counter)].value = day1_barcode
                        sheet['C{}'.format(excel_counter)].value = int(average_dict['Day1'][cell_name])
                        sheet['D{}'.format(excel_counter)].value = day7_barcode
                        sheet['E{}'.format(excel_counter)].value = int(average_dict['Day7'][cell_name])
                        sheet['F{}'.format(excel_counter)].value = \
                            (int(average_dict['Day7'][cell_name]) - int(average_dict['Day1'][cell_name]))
                        sheet['G{}'.format(excel_counter)].value = \
                            ceil(int(average_dict['Day7'][cell_name]) / int(average_dict['Day1'][cell_name]))
                        missing_check = False
                        excel_counter += 1
                if missing_check:
                    num_of_missing_barcodes += 1
                    print(day1_barcode, day7_barcode)
    wb.save(file)
    return num_of_missing_barcodes


def write_to_file(file, control_dict1, average_dict):
    with open(file, 'w') as file:
        for tech in control_dict1:
            file.write('**')
            file.write(tech)
            file.write('**')
            file.write('\n')
            for date in control_dict1[tech]:
                file.write(date)
                file.write('\n')
                for barcode in control_dict1[tech][date]:
                    for line in control_dict1[tech][date][barcode]:
                        if line in average_dict['Day1'] and line in average_dict['Day7']:
                            file.write(str(line))
                            file.write('\n')
                            file.write('Day 1 Result: {}\n'.format(ctrl_avg_dict['Day1'][line]))
                            file.write('Day 7 Result: {}\n'.format(ctrl_avg_dict['Day7'][line]))
                            file.write('\n')


directory = os.listdir('results')
cell_lines = []

tech_list = []
ctrl_avg_dict = {'Day1': {}, 'Day7': {}}

control_avg_function(d1_dict, 'Day1')
control_avg_function(d7_dict, 'Day7')

write_to_file('controlResults.txt', d1_dict, ctrl_avg_dict)

create_excel_file()

missing_bars = write_excel_file('AvgControlSheet.xlsx', d1_dict, ctrl_avg_dict)

if missing_bars > 0:
    print('\n{} barcodes were not found and could not be processed'.format(missing_bars))
else:
    print('\nAll files found and processed.')


'''
12/3/2020

Last I left off on this project, I just completed exporting results on organization to excel file. In addition, I have 
created side by side results of d1 & d7 comparison in a txt file, just for variation. I should be able to test out more
and more cella vista results files with the merged sheets.

DON'T worry about trying to make the cell lines alphabetical, you can sort them any which way in excel. 

Next, I will try and implement this into a database and see what I can come up with.. great progress so far though
'''

'''
2/8/2021
The project was having issues when trying to index for cell avgs. The control_list_length var, when looped, was too long 
when reaching 8 cell lines per barcode, so I tried indexing with "for i in range(control_list_length - 1)". However, I
then ran into a problem when it would try to index a 1 item list. The range (control_list_length - 1) would be zero
which then won't do anything, so I created an if statement that changes the length if the length is greater than 1.
This was purely for indexing purposes, as it does not indicate the actual list length of the iteration at hand. This was
necessary so the range would not end up being zero, and so that it was trying to index var[8] for a list that only had
8 items total.

I also added in an increase factor to be written in the excel sheet to see how much the cells increased by ie. 75x, 10x
'''
