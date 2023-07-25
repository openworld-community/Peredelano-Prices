import pandas as pd
import peft
import torch
import torch.nn.functional as F
from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
from transformers import Trainer
from torch.utils.data import DataLoader
from sklearn.preprocessing import LabelEncoder
from joblib import load
from preprocessing import ProductData
from torch.utils.data import DataLoader


if torch.cuda.is_available():
    device = torch.device("cuda")
    print("Found CUDA! Using GPU")
else:
    device = torch.device("cpu")
    print("CUDA is not available! Using CPU")

#DATA_FILE = "data.csv"
LORA_PATH = "LightDashing/peredelano-prices-classification"
CLASS_NUM = 17
#DATA_COLUMNS = ['product_name', 'product_class']
#If you are going to use this for real-data inference, where there would be no product class, just delete it in list
BATCH_SIZE = 16
# If you get OOM, decrease this number


label_encoder = load("label_encoder.pkl")
#data = pd.read_csv(DATA_FILE, header=None, index_col=0)
# We need to format data in a single style so there would be no problems with inference in future
#data.columns = DATA_COLUMNS


config = peft.PeftConfig.from_pretrained(LORA_PATH)
model  = XLMRobertaForSequenceClassification.from_pretrained("xlm-roberta-base", problem_type="multi_label_classification", num_labels=CLASS_NUM)
tokenizer = XLMRobertaTokenizer.from_pretrained("xlm-roberta-base")
model = peft.PeftModel.from_pretrained(model, LORA_PATH)
model.eval()
model.to(device)


def classify_product(product_name: str) -> list[tuple]:
    """
    Uses model to classify product class
    """

    inputs = tokenizer(
        product_name)

    #TODO: In future, add max_length to function, so text can be padded and truncated
    #max_length=self.max_length,
    #padding='max_length',
    #truncation=self.truncate)

    input_ids = torch.tensor(inputs['input_ids'], dtype=torch.long).to(device).unsqueeze(0)
    attention_mask = torch.tensor(inputs['attention_mask'], dtype=torch.long).to(device).unsqueeze(0)
    with torch.no_grad():
        logits = model(input_ids, attention_mask).logits.to("cpu")
    probabilities = F.softmax(logits, dim=-1).squeeze()
    return [(*label_encoder.inverse_transform([index]), prob) for index, prob in enumerate(probabilities)]


def classify_product_batches(product_names: list[str]) -> list[list[tuple]]:
    """
    Uses model to classify product class, batched version.
    Change batch size according to your memory needs
    """
    data = ProductData(product_names, device, tokenizer)
    loader = DataLoader(data, batch_size=min(BATCH_SIZE, len(product_names)), shuffle=False)
    predictions = []
    for batch in loader:
        with torch.no_grad():
            logits = model(*batch).logits.to("cpu")
        probabilities = F.softmax(logits, dim=-1)

        batch_predictions = []
        for prob in probabilities:
            batch_predictions.append([(label_encoder.inverse_transform([index]), p.item()) for index, p in enumerate(prob)])

        predictions.extend(batch_predictions)
    return predictions

#print(classify_product_batches(data[DATA_COLUMNS[0]][:20].to_list()))


#with torch.no_grad():
    #for product in data[DATA_COLUMNS[0]]:
        #print(classify_product(product))
        #break


# OLD CODE
#dataset = ProductData(data[DATA_COLUMNS[0]].to_list(), device, tokenizer)
#loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=False)

#predictions = []

#for batch in loader:

    #with torch.no_grad():
        #logits = model(*batch).logits

    #predicted_classes = torch.argmax(logits, dim=-1)
    #predictions.extend(label_encoder.inverse_transform(predicted_classes.to("cpu")))

#output = pd.DataFrame(predictions, columns=['predictions'])
#data = data.reset_index()
#output['product_name'] = data.product_name
#output.to_csv("predictions.csv", index=False)




