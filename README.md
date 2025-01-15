# Box4Chemi

## Summary
Deep learning methods have shown impressive performance in numerous fields of application. However, they often lack mechanisms which ensure that responses follow rules or are consistent. In this research, we use box-shaped representations of classes with an underlying logical theory. These box-representations are able to express logical relations between classes and make them transparent. In a case study based on the ChEBI ontology, we train a transformer-based model on data that implicitly follows this logical theory, but not explicitly. We find that our model can successfully learn box representations for classes with sufficient support such that they are consistent with the underlying logical theory. 

## Implementation
This repository contains the code associated with the paper **"Modeling Chemical Hierarchies with Box Embeddings"**. It is based on the [ChEB-AI](https://github.com/ChEB-AI/python-chebai) repository and extends its functionality. The specific code for the Box Embedding model can be found at [here](https://github.com/adelmemariani/python-chebai/blob/bbe4368408fb46b6d57e651dd20760bc14de0a7b/chebai/models/electra.py#L483). Also, the code for evaluations are provided [here](https://github.com/adelmemariani/python-chebai/tree/Box4Chemi/resources).

The image below illustrates the architecture of our system designed for ontology extension.

![Architecture for co-training](https://github.com/adelmemariani/python-chebai/blob/Box4Chemi/resources/co-training_architecture.png)

The following animation visualizes the learned box embeddings during the training process. These embeddings capture containment relationships, which are utilized to infer the hierarchy of classes defined in the ChEBI ontology.
![Boxes during training](https://github.com/adelmemariani/python-chebai/blob/Box4Chemi/resources/visualization_of_boxes_during_training.gif)

**Please note:** For visualization purposes, we demonstrate the model using a simplified 3-dimensional box embedding. However, the best-performing model, as detailed in our paper, operates with a 16-dimensional embedding space.


