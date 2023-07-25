from torch.utils.data import Dataset
import torch


class ProductData(Dataset):
    """Dataset for bert-style classifier
    You can change max_length to diffirentiate between padding and no-padding (also, truncation is True by-default)
    """

    def __init__(self, X, device, tokenizer=None, max_length=24, truncate=True):
        self.X = X
        self.device = device
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.truncate = truncate

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        inputs = self.tokenizer(
            self.X[idx],
            max_length=self.max_length,
            padding='max_length',
            truncation=self.truncate)
        return torch.tensor(inputs['input_ids'], dtype=torch.long).to(self.device), torch.tensor(inputs['attention_mask'], dtype=torch.long).to(self.device)
