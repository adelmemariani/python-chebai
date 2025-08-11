# Box4Chemi

## Summary
Deep learning methods have shown impressive performance in many applications. However, they often lack mechanisms to ensure that predictions adhere to rules or maintain consistency. In this research, we use box-shaped structures to represent classes defined within an ontology. These box-representations are able to express logical relations between classes and make them transparent. In a case study based on the [ChEBI](https://www.ebi.ac.uk/chebi/) ontology, we introduce a box-embedding method that simultaneously learns to represent taxonomy concepts as geometric boxes and to position instances within the appropriate boxes corresponding to their classifications. We show that our model can successfully learn box representations for classes, ensuring consistency with the underlying logical theory.

## Implementation
This repository contains the code associated with the paper **"Modeling Chemical Hierarchies with Box Embeddings"**. It is based on the [ChEB-AI](https://github.com/ChEB-AI/python-chebai) repository and extends its functionality. The specific code for the Box Embedding model can be found at [here](https://github.com/adelmemariani/python-chebai/blob/bbe4368408fb46b6d57e651dd20760bc14de0a7b/chebai/models/electra.py#L483). Also, the code for evaluations are provided [here](https://github.com/adelmemariani/python-chebai/tree/Box4Chemi/resources).

The image below illustrates the architecture of our system designed for ontology extension.


![Architecture for co-training](https://github.com/adelmemariani/python-chebai/blob/Box4Chemi/resources/co-training_architecture.png)

The following animation visualizes the learned box embeddings during the training process. These embeddings capture containment relationships, which are utilized to infer the hierarchy of classes defined in the ChEBI ontology.
![Boxes during training](https://github.com/adelmemariani/python-chebai/blob/Box4Chemi/resources/visualization_of_boxes_during_training.gif)

**Please note:** For visualization purposes, we demonstrate the model using a simplified 3-dimensional box embedding. However, the best-performing model, as detailed in our paper, operates with a 16-dimensional embedding space.

## Installation

(1) Clone the repository from GitHub:
```
git clone https://github.com/adelmemariani/python-chebai.git
```

(2) Change the working directory to `python-chebai`:
```
cd python-chebai/
```

(3) Switch to the `Box4Chemi` branch:
```
git checkout Box4Chemi
```

(4) Install the package:
```
pip install -e .
```

## Usage

(5) Download and extract the following folder. It includes the training data and a pretrained ELECTRA model necessary to run the experiments:
```
https://zenodo.org/records/16794618
```

(6) Copy the `data` folder to the root of the python-chebai directory, beside the `chebai` folder.

(7) Copy the `pretrained_electra.ckpt` file to the root of the python-chebai directory, beside the `chebai` and `data` folders.

(8) Training is implemented with PyTorch Lightning. The command below runs the experiment:
```
python -m chebai fit --trainer=configs/training/default_trainer.yml --model=configs/model/box.yml  --model.load_prefix=generator. --data=configs/data/chebi100.yml --model.criterion=configs/loss/box_bce.yml --model.pretrained_checkpoint=pretrained_electra.ckpt
```
