import tensorflow as tf
import pathlib
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

np.set_printoptions(precision=4)

dataset = tf.data.Dataset.from_tensor_slices([8, 3, 0, 8, 2, 1])
dataset

for elem in dataset:
  print(elem.numpy())

it = iter(dataset)
print(next(it).numpy())

print(dataset.reduce(0, lambda state, value: state + value).numpy())