import openpyxl

wb = openpyxl.load_workbook('master/master.xlsx')
spreadsheet = wb.get_sheet_by_name('Sheet1')


def append_item_to_list(i1, i2):
    barcode_list = []
    return_list = []
    for colOfCellObjects in spreadsheet[i1:i2]:
        for cellObj in colOfCellObjects:
            if cellObj.value is not None:
                barcode_list.append(cellObj.value.upper())
    for barcode in barcode_list:
        if barcode not in return_list:
            return_list.append(barcode)
    return return_list


def create_control_dict(control_index, control_dict):
    spreadsheet_in_list = []
    column_break = 0
    spreadsheet_lines = []

    """
    This for loop takes the data from the excel sheet and makes it into list items which can then be accessible
    for use in this program
    """

    for line in spreadsheet:
        for x in line:
            spreadsheet_lines.append(x.value)
            column_break += 1
            if column_break == 12:
                column_break = 0
                spreadsheet_in_list.append(spreadsheet_lines)
                spreadsheet_lines = []
                break   # added on 3/17/2021
            """
            The above break was added because the program, for some reason, wasn't skipping to the next line in
            the spreadsheet and was picking it up where it left off from the previous row. This was causing the lists
            to become disoriented and couldn't progress.
            """

    """
    This next for loop takes the above list we created and assigns the necessary values into the dictionary that we
    want to create.
    """
    for list_item in spreadsheet_in_list:
        if list_item[2] is not None:
            tech_name = list_item[2].upper()
            date = list_item[4]
            control_barcode = list_item[control_index]
            if tech_name in control_dict and control_barcode not in control_dict[tech_name]:
                if date in control_dict[tech_name]:
                    pass
                else:
                    control_dict[tech_name][date] = {}
                control_dict[tech_name][date][control_barcode] = []

    """
    The bottom for loop will assign the cell lines to the barcode within the nested dictionary that it belongs to.
    This is done separately because it requires appending items to a list, rather than the last, seemingly similar,
    for loop is used to set the dictionary up until the point of inputing cell lines.
    """
    for list_item1 in spreadsheet_in_list:
        if list_item1[2] is not None:
            name = list_item1[2].upper()
            barcode = list_item1[control_index]
            cell_name = list_item1[3]
            fecha = list_item1[4]

            if name in control_dict:
                if barcode in control_dict[name][fecha] and cell_name not in control_dict[name][fecha][barcode]:
                    control_dict[name][fecha][barcode].append(cell_name)


def separate_csv_items(import_item):
    b_list = []
    char_var = ''
    n_char_var = ''
    for i in import_item:
        if i != '':
            char_var += i
            for char in char_var:
                if char != ',':
                    n_char_var += char
                else:
                    b_list.append(n_char_var)
                    n_char_var = ''
    return b_list


tech_list = append_item_to_list('C2', 'C3000')

d1_list = append_item_to_list('I2', 'I3000')
d7_list = append_item_to_list('K2', 'K3000')
d1_dict = {}
d7_dict = {}
d1_num = 8  # These two numbers will be used for indexing in the function that creates dictionaries
d7_num = 10  # ^^^
for tech in tech_list:
    d1_dict[tech] = {}
    d7_dict[tech] = {}

create_control_dict(d1_num, d1_dict)
create_control_dict(d7_num, d7_dict)

print(str(len(d1_list)) + " control plates being processed")
