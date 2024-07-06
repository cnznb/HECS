# HECS: An Intelligent Extract Class Refactoring Tool

## Table of Contents

- [Introduction](#Introduction)
- [General of the replication package](#Generalof-the-replication-package)
- [Getting Started](#Getting-Started)
- [Detailed Description](#Detailed-Description)

## Introduction

This document is included in the 'One-to-One or One-to-Many? Suggesting Extract Class Refactoring Opportunities with Intra-class Dependency Hypergraph Neural Network' distribution, which we will refer to as HECS. This is to distinguish the recommended implementation of this Extract Class refactoring from other implementations. In this document, the environment required to make and use the HECS tool is described. Some hints about the installation environment are here, but users need to find complete instructions from other sources. They give a more detailed description of their tools and instructions for using them. Our main environment is located on a computer with windows (windows 11) operating system. The fundamentals should be similar for other platforms, although the way in which the environment is configured will be different. What do I mean by environment? For example, to run python code you will need to install a python interpreter, and if you want to use pre-trained model you will need torch.

## General of the replication package

**/Implementation**: The implementation of the proposed approach.

**/Evaluation**: Replication package for the evaluation section.

**/CaseStudy**: Replication package for the case study.

**/Src**: The code files which is involved in the experiment.

## Getting Started

### Requirements

- Windows
- Git >= 1.9
- Visual Studio Code IDE (Version 1.90.0 or higher)
- Python >= 3.9
- Java >= 11

### Tool Usage Guide

If you want to try out our refactoring tools, we have prepared them for you in the `/Implementation` replication package. You can choose between a command-line tool and an editor-based plugin. To use the HECS tool, please refer to the `README` file located in the `/Implementation` directory. The `README` file contains detailed instructions on how to set up and use the tool.

## Detailed Description

### How to Reproduce Research Methodology

If you find that you need to perform refactoring predictions in bulk and require greater efficiency, you can replicate our research methodology using the files provided in our package. Our package covers every step from dataset preparation to bulk testing with hyperlink predictors. Here's how you can proceed:

####  1.Clone replication package to your local file system

```shell
git clone https://github.com/cnznb/HECS.git
```

####  2.Batch Dataset Preparation

We provide the datasets used in our experiments in the `/Evaluation` replication package, and they are all pre-processed. Of course, you can also construct your own datasets using the [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner) tool. You can follow the code ( `Src/DataPreprocessing/` ) provided in the package to create batch datasets for refactoring prediction. In this step, we extract intra-class dependency graphs from training samples and transform these into hypergraphs.

####  3.Generating Batch Embeddings

Use the code files provided in the package (`Src/DataPreprocessing/nodeEmbedding`  ) to generate various types of embeddings for your batch data. In this step, nodes in hypergraphs are assigned with attributes with pre-trained code model.

####  4.Graph Learning

Then you can feed the attributed hypergraphs obtained from the previous step into an enhanced hypergraph neural network for the purpose of training. The code for the model is located in the `Src/GraphLearning` directory.

####  5.Testing Phase

The detection phase first constructs attributed hypergraph through hypergraph construction and node attribute generation. Based on constructed attributed hypergraphs, the detection phase further conducts refactoring opportunity suggestion via hierarchical model invocation and LLM-based pre-condition verification. Reference code is located in the `Src/RefactoringOpportunitySuggestion` directory. It provides a well-trained model that can be used directly, utilizing the best model combination used in the paper.

###  Pre-trained Model

####  1.pre-trained model link 
CodeBERT: https://huggingface.co/microsoft/codebert-base \
CodeGPT: https://huggingface.co/microsoft/CodeGPT-small-java-adaptedGPT2 \
GraphCodeBERT: https://huggingface.co/microsoft/graphcodebert-base \
CodeT5: https://huggingface.co/Salesforce/codet5-base-multi-sum \
CoTexT: https://huggingface.co/razent/cotext-2-cc \
PLBART: https://huggingface.co/uclanlp/plbart-base

####  2.hyper-parameter settings

| Embedding Technique |                   Hyper-parameter settings                   |
| :-----------------: | :----------------------------------------------------------: |
|      CodeBERT       | train\_batch\_size=2048, embeddings\_size =768, learning\_rate=5e-4, max\_position\_length=512 |
|    GraphCodeBERT    | train\_batch\_size=1024, embeddings\_size =768, learning\_rate=2e-4, max\_sequence\_length=512 |
|       CodeGPT       |      embeddings\_size =768, max\_position\_length=1024       |
|       CodeT5        | train\_batch\_size=1024, embeddings\_size =768, learning\_rate=2e-4, max\_sequence\_length=512 |
|       PLBART        | train\_batch\_size=2048, embeddings\_size =768, dropout=0.1  |
|       CoTexT        | train\_batch\_size=128, embeddings\_size =768, learning\_rate=0.001, model\_parallelism=2, input\_length=1024 |
