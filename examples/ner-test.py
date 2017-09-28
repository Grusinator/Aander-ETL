from scikitcrf_ner import entityRecognition as ner

ner.train("sample_train.json")
entities = ner.predict("show me some Indian restaurants")
print(entites)