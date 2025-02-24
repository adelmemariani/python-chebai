import pickle
import numpy as np
import pandas as pd
import sys

def compute_iou(box1, box2):
    min_box1 = np.minimum(box1[0], box1[1])
    max_box1 = np.maximum(box1[0], box1[1])

    min_box2 = np.minimum(box2[0], box2[1])
    max_box2 = np.maximum(box2[0], box2[1])

    inter_min = np.maximum(min_box1, min_box2)
    inter_max = np.minimum(max_box1, max_box2)
    inter_dims = np.maximum(inter_max - inter_min, 0)
    inter_volume = np.prod(inter_dims)

    volume_box1 = np.prod(max_box1 - min_box1)
    volume_box2 = np.prod(max_box2 - min_box2)

    union_volume = volume_box1 + volume_box2 - inter_volume

    return inter_volume / union_volume if union_volume > 0 else 0.0

def partial_overlap_iou(box1, box2, overlap_threshold=0.95):
    min_box1 = np.minimum(box1[0], box1[1])
    max_box1 = np.maximum(box1[0], box1[1])

    min_box2 = np.minimum(box2[0], box2[1])
    max_box2 = np.maximum(box2[0], box2[1])

    inter_min = np.maximum(min_box1, min_box2)
    inter_max = np.minimum(max_box1, max_box2)
    inter_dims = np.maximum(inter_max - inter_min, 0)

    overlap_dims = inter_dims > 0
    num_overlap_dims = np.sum(overlap_dims)

    if num_overlap_dims / len(inter_dims) >= overlap_threshold:
        inter_volume = np.prod(inter_dims[overlap_dims])

        volume_box1 = np.prod((max_box1 - min_box1)[overlap_dims])
        volume_box2 = np.prod((max_box2 - min_box2)[overlap_dims])

        union_volume = volume_box1 + volume_box2 - inter_volume
        return inter_volume / union_volume if union_volume > 0 else 0.0
    else:
        return 0.0

with open("chebi_string_labels.pkl", "rb") as f:
    chebi_string_labels = pickle.load(f)
print(chebi_string_labels)

train_data = pd.read_pickle("train.pkl")
chebi_labels = list(train_data.columns[3:])
print(chebi_labels)

boxes = pd.read_pickle("boxes_Norm.pkl")

n = len(boxes)
intersections = []

for i in range(n):
    for j in range(n):
        if i != j:
            box1 = boxes[i]
            box2 = boxes[j]

            min_corner_box_1 = np.minimum(box1[0], box1[1])
            max_corner_box_1 = np.maximum(box1[0], box1[1])
            min_corner_box_2 = np.minimum(box2[0], box2[1])
            max_corner_box_2 = np.maximum(box2[0], box2[1])

            dim = len(min_corner_box_1)

            intersection_min = np.zeros(dim)
            intersection_max = np.zeros(dim)
            valid_intersection = True

            for d in range(dim):
                intersection_min[d] = max(min_corner_box_1[d], min_corner_box_2[d])
                intersection_max[d] = min(max_corner_box_1[d], max_corner_box_2[d])

                if intersection_min[d] >= intersection_max[d]:
                    valid_intersection = False
                    break

            if valid_intersection:
                intersections.append({
                    "pair": (i, j),
                    "intersection_min": intersection_min,
                    "intersection_max": intersection_max
                })

print(len(intersections))

iou_threshold = 0.99
similar_boxes = []
similar_boxes_with_labels = []
snakey_data_sources = []
snakey_data_targets = []
snakey_data_sources_with_labels = []
snakey_data_targets_with_labels = []

cnt = 0
for intersection in intersections:
    cnt += 1
    i, j = intersection['pair']

    # to remove duplicates (intersection between i and j is symetric)
    if j > i:
      intersection_box = (intersection['intersection_min'], intersection['intersection_max'])

      for k in range(n):
          if k != i and k != j:
              other_box = boxes[k]
              #iou = compute_iou(intersection_box, other_box)
              iou = partial_overlap_iou(intersection_box, other_box, overlap_threshold=0.99)

              if iou > iou_threshold:
                print(cnt, iou)

              if iou >= iou_threshold:
                  similar_boxes.append({
                      "intersection_pair": (i, j),
                      "similar_box_index": k,
                      "iou": iou
                  })

                  snakey_data_sources.append(str(chebi_labels[i]) + "-" + str(chebi_labels[j]))
                  snakey_data_targets.append(str(chebi_labels[k]))

                  similar_boxes_with_labels.append([
                      str(chebi_string_labels[i]),
                      str(chebi_string_labels[j]),
                      str(chebi_string_labels[k]),
                  ])

                  snakey_data_sources_with_labels.append(str(chebi_string_labels[i]) + "-" + str(chebi_string_labels[j]))
                  snakey_data_targets_with_labels.append(str(chebi_string_labels[k]))

for sim in similar_boxes:
    i, j = sim['intersection_pair']
    k = sim['similar_box_index']
    iou = sim['iou']
    print(f"Intersection of Box {i} & Box {j} is similar to Box {k} with IoU = {iou:.3f}")


with open('similar_boxes_Norm.pkl', 'wb') as similar_boxes_file:
    pickle.dump(similar_boxes, similar_boxes_file)
similar_boxes_file.close()

with open('similar_boxes_with_labels_Norm.pkl', 'wb') as similar_boxes_with_labels_file:
    pickle.dump(similar_boxes_with_labels, similar_boxes_with_labels_file)
similar_boxes_with_labels_file.close()

with open('snakey_data_sources_Norm.pkl', 'wb') as snakey_data_sources_file:
    pickle.dump(snakey_data_sources, snakey_data_sources_file)
snakey_data_sources_file.close()

with open('snakey_data_targets_Norm.pkl', 'wb') as snakey_data_targets_file:
    pickle.dump(snakey_data_targets, snakey_data_targets_file)
snakey_data_targets_file.close()

with open('snakey_data_sources_with_labels_Norm.pkl', 'wb') as snakey_data_sources_with_labels_file:
    pickle.dump(snakey_data_sources_with_labels, snakey_data_sources_with_labels_file)
snakey_data_sources_with_labels_file.close()

with open('snakey_data_targets_with_labels_Norm.pkl', 'wb') as snakey_data_targets_with_labels_file:
    pickle.dump(snakey_data_targets_with_labels, snakey_data_targets_with_labels_file)
snakey_data_targets_with_labels_file.close()