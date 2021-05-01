import pandas as pd
import numpy as np
from phe import paillier
import pickle

def get_keys():
	with open("pubkey.pickle", 'rb') as handle:
		public_key = pickle.load(handle)
	with open("prikey.pickle", 'rb') as handle:
		private_key = pickle.load(handle)
	return public_key, private_key

df = pd.read_pickle("encrypted_carol.pickle")
df = df.dropna()
validIndex = df.columns.get_loc('valid')
df_np = df.to_numpy()

public_key, private_key = get_keys()

decrypt_vect = list()
for row in df_np:
	decrypt_row = [private_key.decrypt(cell) for cell in row]
	if int(decrypt_row[validIndex]) == 1:
		decrypt_vect.append(decrypt_row)

for row in decrypt_vect:
	print(row)