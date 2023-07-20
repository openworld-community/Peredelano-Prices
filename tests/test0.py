from classification.peredelano_classifier_v0 import pp_classifier
from dao.add_new_fields_to_docs import add_weight_field
from utils.calculations import replace_comma_with_dot


with open("file.txt", "w") as file:
    result = pp_classifier("Francuski makaronsi 24 kom 288g Chateau")
    file.write(str(result[0]))


