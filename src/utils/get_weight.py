from dao.CRUD import get_database
import re


def find_weight(product_string):
    # Используем обновленное регулярное выражение для поиска числовых значений перед указанными единицами измерения
    weight_regex = r'(\d+(?:[,.]\d*)?)\s*(?i)(?:l|ml|g|gr|kg)\b'

    # Находим все соответствия в строке
    matches = re.findall(weight_regex, product_string)

    # Преобразуем найденные значения в числа и возвращаем результат
    weights = [float(match.replace(',', '.')) for match in matches]

    if (weights):
        weight = weights[0]

        if (weight < 5):
            weight *= 1000

        # gr/ml
        return weight

    return None


list_to_write = list()
list_of_errors = list()


def write_weight_to_file():
    dbname = get_database()
    collection_name_Aroma = dbname["fromAroma"]
    collection_name_Franca = dbname["fromFranca"]
    collection_name_Voli = dbname["fromVoli"]

    counter = 0

    list_to_write.append("//  //  Aroma  //  //\n")

    cursorA = collection_name_Aroma.find()
    for document in cursorA:
        product_name = document["product"]["name"]
        weight = find_weight(product_name)
        if (weight):
            list_to_write.append(product_name + "  -  weight = " + str(weight) + " gr/ml\n")
        else:
            list_of_errors.append(product_name + "\n")
            counter += 1

    list_to_write.append("\n\n\n//  //  Franca  //  //")

    cursorF = collection_name_Franca.find()
    for document in cursorF:
        product_name = document["product"]["name"]
        weight = find_weight(product_name)
        if (weight):
            list_to_write.append(product_name + "  -  weight = " + str(weight) + " gr/ml\n")
        else:
            list_of_errors.append(product_name + "\n")
            counter += 1

    list_to_write.append("\n\n\n//  //  Voli  //  //")

    cursorV = collection_name_Voli.find()
    for document in cursorV:
        product_name = document["product"]["name"]
        weight = find_weight(product_name)
        if (weight):
            list_to_write.append(product_name + "  -  weight = " + str(weight) + " gr/ml\n")
        else:
            list_of_errors.append(product_name + "\n")
            counter += 1

    with open("weight_check.txt", "w") as file:
        for text in list_to_write:
            file.write(text)

    with open("weight_errors.txt", "w") as file:
        for text in list_of_errors:
            file.write(text)

    return counter
