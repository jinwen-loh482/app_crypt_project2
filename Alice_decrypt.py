import pandas as pd
import numpy as np
from phe import paillier
import pickle

df = pd.read_csv("encrypted.csv")
df = df.dropna()
df_np = df.to_numpy()

public_key = pickle.load("pubkey.pickle")
private_key = pickle.load("prikey.pickle")

unpickle_vect = []
for row in df_np:
	unpickle_row = [df_np.loads(x) for x in row]
	unpickle_vect.append(unpickle_row)
	# print(unpickle_row)

decrypt_vect = []
for row in unpickle_vect:
	# print(row)
	decrypt_row = [private_key.decrypt(x) for x in row]
	decrypt_vect.append(decrypt_row)
	print(decrypt_row)