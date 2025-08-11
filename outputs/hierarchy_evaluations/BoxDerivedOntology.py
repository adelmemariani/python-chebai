import pickle
import numpy as np
import pandas as pd
from graphviz import Source
from collections import defaultdict

with open("./dataset_class_ansectors.pkl", "rb") as f:
    dataset_class_ansectors = pickle.load(f)

with open("chebi_string_labels.pkl", "rb") as f:
    chebi_string_labels = pickle.load(f)

train_data = pd.read_pickle("train.pkl")
chebi_labels = list(train_data.columns[3:])

chebi_labels_formatted = []
for idx_i, chebi_id_i in enumerate(chebi_labels):
    CHEBI_ID_i = "CHEBI:{id}".format(id=chebi_id_i)
    chebi_labels_formatted.append(CHEBI_ID_i)

class_to_name_dict = {
    chebi_labels_formatted[i]: str(chebi_string_labels[i])
    for i in range(len(chebi_labels_formatted))
}

dataset_class_ancestors_named = defaultdict(list)
for chebi_id, ancestor_ids in dataset_class_ansectors.items():
    child_name = class_to_name_dict.get(chebi_id, chebi_id)
    for anc_id in ancestor_ids:
        ancestor_name = class_to_name_dict.get(anc_id, anc_id)
        dataset_class_ancestors_named[child_name].append(ancestor_name)


label =  "CHEBI:18303"
idx = chebi_labels_formatted.index(label)

for boxes_from_model in ["boxes_Cui.pkl", "boxes_Norm.pkl"]:
    model_name = boxes_from_model.split("_")[1].split(".")[0]

    boxes = pd.read_pickle(boxes_from_model)

    n = len(boxes)
    threshold = 0.03

    parents = [[] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            box1 = boxes[i]
            box2 = boxes[j]

            min1 = np.minimum(box1[0], box1[1])
            max1 = np.maximum(box1[0], box1[1])
            min2 = np.minimum(box2[0], box2[1])
            max2 = np.maximum(box2[0], box2[1])

            dim = len(min1)
            is_inside_per_dim = []
            for d in range(dim):
                error_margin_2 = (max2[d] - min2[d]) * threshold

                min_corner_1 = min1[d]
                max_corner_1 = max1[d]
                min_corner_2 = min2[d]
                max_corner_2 = max2[d]

                is_inside = ((min_corner_1 <= (min_corner_2 + error_margin_2)) and
                             (max_corner_1 >= (max_corner_2 - error_margin_2)))
                is_inside_per_dim.append(is_inside)

            if all(is_inside_per_dim):
                if i not in parents[j]:
                    parents[j].append(i)

    parents_immediate = [[] for _ in range(n)]
    for c in range(n):
        P = parents[c]
        keep = []
        Pset = set(P)
        for p in P:
            if any((q != p) and (p in parents[q]) for q in Pset):
                continue
            keep.append(p)
        parents_immediate[c] = keep

    target = idx

    levels = [[str(chebi_string_labels[target])]]
    visited = {target}

    current = [p for p in parents_immediate[target] if p not in visited]

    while current:
        levels.append([str(chebi_string_labels[p]) for p in current])
        visited.update(current)
        next_level = []
        for child in current:
            for p in parents_immediate[child]:
                if p not in visited and p not in next_level:
                    next_level.append(p)
        current = next_level


    all_nodes = set().union(*levels)
    edges, seen = [], set()
    for c in range(n):
        child_name = str(chebi_string_labels[c])
        if child_name in all_nodes:
            for p in parents_immediate[c]:
                parent_name = str(chebi_string_labels[p])
                if parent_name in all_nodes:
                    e = (child_name, parent_name)
                    if e not in seen:
                        edges.append(e)
                        seen.add(e)

    edges.sort()

    level_of = {name: li for li, lvl in enumerate(levels) for name in lvl}

    same_level_edges = []
    cross_level_edges = []
    for child, parent in edges:
        if level_of.get(child) == level_of.get(parent):
            same_level_edges.append((child, parent))
        else:
            cross_level_edges.append((child, parent))

    dot_lines = [
        'digraph G {',
        '  rankdir=BT;',
        '  nodesep=1.0;',
        '  ranksep=1.0;',
        '  splines=true;',
        '  overlap=false;',
        '  pad=0.4;',
        '  fontsize=18;',
        '  fontname="Helvetica";',
        '',
        '  node [shape=box, style=rounded, color="#000000", fontcolor="#000000",',
        '        fontname="Helvetica", fontsize=20, penwidth=1.4,',
        '        width=0, height=0, margin="0.10,0.06"];',
        '',
        '  edge [arrowsize=1.0, penwidth=1.6];',
        ''

    ]

    for lvl in levels:
        if not lvl:
            continue
        dot_lines.append('  { rank=same; ' + ' '.join(f'"{name}";' for name in lvl) + ' }')

    dot_lines.append('')

    for c, p in cross_level_edges:
        if p in dataset_class_ancestors_named.get(c, []):
            dot_lines.append(f'  "{c}" -> "{p}" [constraint=true, color="darkgreen"];')
        else:
            dot_lines.append(f'  "{c}" -> "{p}" [constraint=true, color="darkred", style=dashed];')

    for c, p in same_level_edges:
        if p in dataset_class_ancestors_named.get(c, []):
            dot_lines.append(f'  "{c}" -> "{p}" [constraint=false, splines=true, penwidth=1.6, color="darkgreen"];')
        else:
            dot_lines.append(
                f'  "{c}" -> "{p}" [constraint=false, splines=true, penwidth=1.6, color="darkred", style=dashed];')

    dot_lines.append('}')
    dot_data = "\n".join(dot_lines)

    print(dot_data)
    #src = Source(dot_data)
    #src.render(f"Box_Derived_Hierarchy_{model_name}", format="png", cleanup=True)
