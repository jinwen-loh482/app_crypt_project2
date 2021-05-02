import pandas as pd
import numpy as np

df = pd.read_csv("heart.csv")
df = df.dropna()
df_np = df.to_numpy()

myones = np.ones((df.shape[0], 1))
df_np = np.hstack((myones, df_np))

mycols = ['valid']
for x in df.columns:
	mycols.append(x)
mydf = pd.DataFrame(df_np, columns=mycols)
mydf.to_csv("more_data.csv", index=False)