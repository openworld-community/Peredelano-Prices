# from classification.inference import classify_product
#
# print(classify_product("Violife ukus cheddar slajs 140 g (185649)"))
from classification.inference import classify_product_batches
from dao.CRUD import get_database_glovo


def bert_classifier_list():

    list_of_products = list()

    db = get_database_glovo()
    coll = db["prod_for_prod"]

    cursor1 = coll.find()

    for doc in cursor1:
        product_name = doc["product_name"]
        list_of_products.append(product_name)

    results = classify_product_batches(list_of_products)

    with open('test_bert_list.txt', mode='w', encoding='utf-8') as file:
        dict_to_check = {}
        counter_for_doc = 1
        counter_for_result = 1
        cursor2 = coll.find()
        for doc in cursor2:
            product_id = doc["product_id"]
            product_name = doc["product_name"]
            group = doc["group"]
            dict_to_check[str(counter_for_doc)] = [str(product_id), str(product_name), str(group)]
            counter_for_doc += 1

        for result in results:
            max_element = max(result, key=lambda x: x[1])
            for_key = "another_" + str(counter_for_result)
            dict_to_check[for_key] = str(max_element[0])
            counter_for_result += 1

        print(counter_for_result)
        print(counter_for_doc)

        if counter_for_doc == counter_for_result:
            i = 1
            while i < counter_for_doc:
                key1 = str(i)
                key2 = "another_" + str(i)

                from_doc = dict_to_check[key1]
                from_result = dict_to_check[key2]
                group_from_doc = from_doc[2]
                str_from_result = str(from_result)
                group_from_result = str_from_result.replace("['", "").replace("']", "")

                if str(group_from_result) != str(group_from_doc):
                    # toFile1 = str(from_doc)
                    # toFile2 = str(from_result)
                    toFilegroup1 = str(from_doc)
                    toFilegroup2 = str(group_from_result)
                    file.write(toFilegroup1 + " - - " + toFilegroup2 + "\n")

                i += 1




bert_classifier_list()
