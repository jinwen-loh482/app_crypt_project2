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

df = pd.read_pickle("encrypted.pkl")
df = df.dropna()
df_np = df.to_numpy()

public_key, private_key = get_keys()

# unpickle_vect = []
# for row in df_np:
# 	unpickle_row = [df_np.loads(x) for x in row]
# 	unpickle_vect.append(unpickle_row)
# 	# print(unpickle_row)

decrypt_vect = []
for row in df_np:
	# print(row)
	decrypt_row = [private_key.decrypt(x) for x in row]
	decrypt_vect.append(decrypt_row)
	print(decrypt_row)