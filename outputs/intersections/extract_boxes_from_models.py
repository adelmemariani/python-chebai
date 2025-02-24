import pickle
import torch

model_checkpoint = "./cui.ckpt"

checkpoint = torch.load(model_checkpoint, map_location=torch.device('cpu'))
mboxes = checkpoint["state_dict"]["boxes"]

corner_1 = mboxes[:, :, 0]
corner_2 = mboxes[:, :, 1]

boxes = [[corner_1[i].cpu().detach().numpy(), corner_2[i].cpu().detach().numpy()] for i in range(854)]

with open('boxes_Cui.pkl', 'wb') as file:
    pickle.dump(boxes, file)