import csv


list_of_errors = list()
list_to_write = list()


def update_group_to_custom(dictionary, cur_cat, isFound, product_id, product_name, group):
    if not isFound:
        for key, value in dictionary.items():
            if isinstance(value, dict):
                cur_cat = key
                update_group_to_custom(value, cur_cat, isFound, product_id, product_name, group)
            else:
                for g in value:
                    if str(g) == str(group):
                        toRet = cur_cat
                        isFound = True
                        break
            if(isFound):
                break
        if(isFound):
            isWrited = False
            for temp in list_to_write:
                if temp[0] == product_id:
                    isWrited = True
            if not isWrited:
                list_to_write.append([product_id, product_name, toRet])


def to_file(tree_of_categories, list_of_group_Aroma, list_of_group_Franca, list_of_group_Voli, dbname):

    collection_name_Aroma = dbname["fromAroma"]
    collection_name_Franca = dbname["fromFranca"]
    collection_name_Voli = dbname["fromVoli"]

    counter = 0


    cursorA = collection_name_Aroma.find()
    for document in cursorA:
        product_id = document["_id"]
        product_name = document["product"]["name"]
        group = document["group"]

        isTrue = False
        for g in list_of_group_Aroma:
            if g == group:
                isTrue = True
                break

        if(isTrue):
            isFound = False
            update_group_to_custom(tree_of_categories, "start", isFound, product_id, product_name, group)
            counter += 1


    cursorF = collection_name_Franca.find()
    for document in cursorF:
        product_id = document["_id"]
        product_name = document["product"]["name"]
        group = document["group"]

        isTrue = False
        for g in list_of_group_Franca:
            if g == group:
                isTrue = True
                break

        if(isTrue):
            isFound = False
            update_group_to_custom(tree_of_categories, "start", isFound, product_id, product_name, group)
            counter += 1


    cursorV = collection_name_Voli.find()
    for document in cursorV:
        product_id = document["_id"]
        product_name = document["product"]["name"]
        group = document["group"]

        isTrue = False
        for g in list_of_group_Voli:
            if g == group:
                isTrue = True
                break

        if(isTrue):
            isFound = False
            update_group_to_custom(tree_of_categories, "start", isFound, product_id, product_name, group)
            counter += 1


    with open('data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)  # Создаем объект writer
        for data in list_to_write:
            writer.writerow(data)

    with open('errorslist.csv', mode='w', newline='') as file:
        writer = csv.writer(file)  # Создаем объект writer
        for data in list_of_errors:
            writer.writerow(data)


    return counter