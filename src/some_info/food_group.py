import csv

data_array1 = []

data_array2 = []

with open('FD_GROUP.csv', newline='') as file1:
    csv_reader1 = csv.reader(file1)
    next(csv_reader1)
    for row in csv_reader1:
        data_array1.append(row)


with open('FOOD_DES.csv', newline='') as file2:
    csv_reader2 = csv.reader(file2)
    next(csv_reader2)
    for row in csv_reader2:
        data_array2.append(row)


data_dict_1 = {}

for temp in data_array1:
    key = temp[0]
    value = temp[1]
    data_dict_1[key] = {"group": value}

# group_key = "0100"
#
# print(data_dict_1[group_key]["group"])


with open('food_group.csv', newline='', mode='w') as file:

    csv_writer = csv.writer(file)

    for product in data_array2:
        key_group = product[1]
        product_desc = product[2]
        group_name = data_dict_1[key_group]["group"]
        data = [group_name, product_desc]
        csv_writer.writerow(data)
