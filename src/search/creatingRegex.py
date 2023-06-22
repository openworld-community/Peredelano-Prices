import re

def matching(userChoice):

    # in: user query string
    #
    # from: regular expression to search

    regexesForApple = list()
    regexesForMilk = list()
    regexesForMeat = list()


    match userChoice:
        case "apple":

            # Voli/Franca/Aroma
            search_string = "jabuka"
            regex = re.compile(search_string, re.IGNORECASE)

            return regex
        case "milk":

            #Voli/Franca/Aroma
            search_string = "mlijeko"
            regex = re.compile(search_string, re.IGNORECASE)

            return regex
        case "meat":

            # тут какое-то адище получается

            #  Voli
            search_string = "mesara"
            regexV = re.compile(search_string, re.IGNORECASE)

            # Franca
            search_string = "meso"
            regexF = re.compile(search_string, re.IGNORECASE)

            # Aroma
            search_string = "kobasica"
            regexA = re.compile(search_string, re.IGNORECASE)

            regexesForMeat.append(regexA)
            regexesForMeat.append(regexF)
            regexesForMeat.append(regexV)

            return regexesForMeat

    return "not correct"
