import pandas as pd
from rdflib import Graph
import pickle

train_data = pd.read_pickle("train.pkl")

chebi_labels = list(train_data.columns[3:])
print(chebi_labels)

g = Graph()
print("Loading ChEBI...")
g.parse("./chebi_core.owl", format="xml")

print("Loading Done.")

class_string_labels = []
for chebi_id in chebi_labels:
    query_label = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX chebi: <http://purl.obolibrary.org/obo/CHEBI_>

    SELECT ?classID ?classLabel
    WHERE {{
        ?classID rdfs:label ?classLabel .
        FILTER(STR(?classID) = "http://purl.obolibrary.org/obo/CHEBI_{chebi_id}")
    }}
    """
    label_results = g.query(query_label)
    if label_results:
        for row in label_results:
            class_string_labels.append(str(row.classLabel))
            print(row.classID, row.classLabel)


print(class_string_labels)

with open('chebi_string_labels_old.pkl', 'wb') as file:
    pickle.dump(class_string_labels, file)