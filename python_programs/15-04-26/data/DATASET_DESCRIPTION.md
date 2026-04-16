# Iris Dataset Description

## Overview
The **Iris dataset** is one of the most famous datasets in machine learning and statistics. It was introduced by Ronald Fisher in 1936 and contains measurements of iris flowers from three different species. This dataset is widely used for classification tasks, educational purposes, and benchmarking machine learning algorithms.

## Dataset Characteristics

| Property | Value |
|----------|-------|
| **Total Samples** | 150 |
| **Number of Features** | 4 |
| **Number of Classes** | 3 |
| **Feature Type** | Numeric (continuous) |
| **Task** | Multi-class Classification |
| **Samples per Class** | 50 (balanced dataset) |

## Features

Each iris flower is described by **4 measurements** (in centimeters):

1. **Sepal Length** - Length of the sepal (outer leaf-like structure)
2. **Sepal Width** - Width of the sepal
3. **Petal Length** - Length of the petal (inner colorful structure)
4. **Petal Width** - Width of the petal

All measurements are continuous numeric values.

## Target Classes (Species)

The dataset contains three iris species:

1. **Iris-setosa** - 50 samples
   - Smallest flowers with shorter petals
   - Petal length: 1.0-1.9 cm
   - Linearly separable from other species

2. **Iris-versicolor** - 50 samples
   - Medium-sized flowers
   - Petal length: 3.0-5.1 cm
   - Overlaps with virginica

3. **Iris-virginica** - 50 samples
   - Largest flowers with longer petals
   - Petal length: 4.5-6.9 cm
   - Overlaps with versicolor

## Source

This dataset was automatically downloaded from the UCI Machine Learning Repository during the first training script execution.
