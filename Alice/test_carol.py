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

def get_pub_key():
	with open("pubkey.pickle", 'rb') as handle:
		public_key = pickle.load(handle)
	return public_key

df = pd.read_pickle("encrypted.pickle")
df = df.dropna()
df_np = df.to_numpy()

public_key, private_key = get_keys()

# unpickle_vect = []
# for row in df_np:
# 	unpickle_row = [df_np.loads(x) for x in row]
# 	unpickle_vect.append(unpickle_row)
# 	# print(unpickle_row)

# decrypt_vect = []
# for row in df_np:
# 	# print(row)
# 	decrypt_row = [private_key.decrypt(x) for x in row]
# 	decrypt_vect.append(decrypt_row)
# 	print(decrypt_row)

# enc_63 = public_key.encrypt(63)
enc_63 = 63

# if res matching, then res == 0
res = df_np[0][0] - enc_63
res1 = df_np[0][0] - enc_63


# if (df_np[0][0] + res) == df_np[0][0]:
if res == res1:
	print("Hello")
print(private_key.decrypt(res))