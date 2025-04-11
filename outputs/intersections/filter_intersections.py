import pickle
import pandas as pd
from collections import defaultdict
import plotly.graph_objects as go

def visualize_similarities(snakey_data_sources_with_labels, snakey_data_targets_with_labels, output_name):
    left_elements = snakey_data_sources_with_labels
    right_elements = snakey_data_targets_with_labels

    unique_elements = list(set(left_elements + right_elements))
    element_to_index = {element: idx for idx, element in enumerate(unique_elements)}

    sources = []
    targets = []
    values = []

    for i, left in enumerate(left_elements):
        if i < len(right_elements):
            right = right_elements[i]
            sources.append(element_to_index[left])
            targets.append(element_to_index[right])
            values.append(1)

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=30,
            thickness=30,
            line=dict(color="black", width=0.5),
            label=unique_elements
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    )])

    fig.update_layout(title_text="Intersections" + output_name.split("_")[1], font_size=14, width=1000, height=2000)
    fig.show()

    fig.write_image(output_name + ".png", scale=3)
    fig.write_html(output_name + ".html")

    return "Done!"

def reduce_specific_pairs(pairs, subclass_dict):
    result = []
    removed = set()

    for i in range(len(pairs)):
        if i in removed:
            continue
        for j in range(i + 1, len(pairs)):
            if j in removed:
                continue
            a1, a2 = pairs[i]
            b1, b2 = pairs[j]

            if (a1 in subclass_dict.get(b1, []) or a1 in subclass_dict.get(b2, []) or
                    a2 in subclass_dict.get(b1, []) or a2 in subclass_dict.get(b2, [])):
                removed.add(j)
            elif (b1 in subclass_dict.get(a1, []) or b1 in subclass_dict.get(a2, []) or
                  b2 in subclass_dict.get(a1, []) or b2 in subclass_dict.get(a2, [])):
                removed.add(i)
                break

    for i in range(len(pairs)):
        if i not in removed:
            result.append(pairs[i])
    return result

with open("./dataset_class_ansectors.pkl", "rb") as f:
    dataset_class_ansectors = pickle.load(f)

with open("./dataset_class_descendants.pkl", "rb") as f:
    dataset_class_descendants = pickle.load(f)

with open("chebi_string_labels.pkl", "rb") as f:
    chebi_string_labels = pickle.load(f)

train_data = pd.read_pickle("train.pkl")
chebi_labels = list(train_data.columns[3:])

chebi_labels_formatted = []
for idx_i, chebi_id_i in enumerate(chebi_labels):
    CHEBI_ID_i = "CHEBI:{id}".format(id=chebi_id_i)
    chebi_labels_formatted.append(CHEBI_ID_i)

final_output = defaultdict(list)
for boxes_from_model in ["boxes_Cui.pkl", "boxes_Norm.pkl"]:
    with open("./" + boxes_from_model.split(".")[0] + "_snakey_data_sources_with_labels.pkl", "rb") as f:
        sources = pickle.load(f)
    with open("./" + boxes_from_model.split(".")[0] + "_snakey_data_targets_with_labels.pkl", "rb") as f:
        targets = pickle.load(f)
    with open("./" + boxes_from_model.split(".")[0] + "_dictionary_of_names.pkl", "rb") as f:
        dictionary_of_names = pickle.load(f)

    number_of_relations = len(sources)
    targets_dictionary = defaultdict(list)
    for i in range(number_of_relations):
        source_pair = sources[i].split(" ∩ ")
        targets_dictionary[targets[i]].append([source_pair[0], source_pair[1]])

    final_output[boxes_from_model.split(".")[0]] = []
    for k, v in targets_dictionary.items():
        reduced_pairs = reduce_specific_pairs(v, dataset_class_descendants)
        final_output[boxes_from_model.split(".")[0]].append([k, reduced_pairs])

for model, intersections in final_output.items():
    new_sources = []
    new_targets = []
    for item in intersections:
        for i in range(len(item[1])):
            new_sources.append(dictionary_of_names[ str(item[1][i][0]) ] + "(" + str(item[1][i][0]) + ")" + " ∩ " + dictionary_of_names[ str(item[1][i][1]) ] + "(" + str(item[1][i][1]) + ")")
            new_targets.append(dictionary_of_names[str(item[0])] + "(" + str(item[0]) + ")")

    visualize_similarities(new_sources, new_targets, model)
