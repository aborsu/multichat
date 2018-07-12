from django import forms
from .models import LANGUAGE_CHOICE, Dataset

DATASET_TYPE_CHOICE = (
    ('RASA_NLU', Dataset.load_rasa_dataset),
)


class UploadDataset(forms.Form):
    name = forms.CharField()
    language = forms.Select(choices=LANGUAGE_CHOICE)
    dataset_type = forms.Select(choices=DATASET_TYPE_CHOICE)
    file = forms.FileField()

    def save(self):
        print(self.cleaned_data['dataset_type'])
        return
