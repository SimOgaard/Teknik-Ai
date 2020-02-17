import numpy as np
from sklearn import preprocessing, neighbors, model_selection
import pandas as pd

df=pd.read_csv('KNN/votering.csv')
df.drop(["punkt"],1,inplace=True)
df=df[["rost","parti","fodd","kon","intressent_id"]]

print(list(df))
print(df.head(3))
