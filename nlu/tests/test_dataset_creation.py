from pathlib import Path
import json

from django.test import TestCase

from nlu.models import Dataset


class DatasetTestCase(TestCase):

    def test_load_rasa_dataset(self):
        with (Path(__file__).parent / 'data' / 'demo-rasa.json').open() as demo_data:
            rasa_nlu_data = json.load(demo_data)['rasa_nlu_data']
        dataset = Dataset.load_rasa_dataset(rasa_nlu_data, 'test', 'en')
        self.assertEquals(dataset.name, 'test')

