from django.db import models
from django.conf.locale import LANG_INFO
from django.db import transaction

LANGUAGES = tuple([
    (k, v['name']) for k, v in LANG_INFO.items() if v.get('name')
])


class Dataset(models.Model):
    name = models.CharField(max_length=255, unique=True)
    language = models.CharField(max_length=7, choices=LANGUAGES)

    @staticmethod
    @transaction.atomic
    def load_rasa_dataset(rasa_nlu_data, name, language):
        dataset = Dataset.objects.create(name=name, language=language)
        entity_types = {}
        for raw_example in rasa_nlu_data['common_examples']:
            text = raw_example['text']
            intent = raw_example['intent']

            example = Example.objects.create(dataset=dataset, text=text, intent=intent)
            for raw_entity in raw_example['entities']:
                start = raw_entity['start']
                end = raw_entity['end']
                value = raw_entity['value']
                raw_type = raw_entity['entity']

                if raw_type not in entity_types:
                    entity_type = EntityType.objects.create(dataset=dataset, name=raw_type, color='red')
                    entity_types[raw_type] = entity_type
                else:
                    entity_type = entity_types[raw_type]
                Entity.objects.create(example=example, start=start, end=end, value=value, type=entity_type)

        Synonym.objects.bulk_create([
            Synonym(dataset=dataset, value=synonyms['value'], text=text)
            for synonyms in rasa_nlu_data['entity_synonyms']
            for text in synonyms['synonyms']
        ])

        RegexFeature.objects.bulk_create([
            RegexFeature(dataset=dataset, name=regex_feature['name'], pattern=regex_feature['pattern'])
            for regex_feature in rasa_nlu_data['regex_features']
        ])

        return dataset


class Synonym(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    text = models.CharField(max_length=255)


class Example(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    text = models.TextField()
    intent = models.CharField(max_length=255)


class EntityType(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)


class Entity(models.Model):
    example = models.ForeignKey(Example, on_delete=models.CASCADE)
    start = models.IntegerField(null=False)
    end = models.IntegerField(null=False)
    value = models.CharField(max_length=255)
    type = models.ForeignKey(EntityType, on_delete=models.CASCADE)


class RegexFeature(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    pattern = models.CharField(max_length=255)
