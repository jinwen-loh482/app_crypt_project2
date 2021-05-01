import pandas as pd
import numpy as np
from phe import paillier
import pickle


# Adapted from https://github.com/ibarrond/Pyfhel/blob/master/examples/Demo_Encrypting.py

# Read from csv
# store as numpy array, df_np
df = pd.read_csv("test.csv")
# df = pd.read_csv("test.csv")

df = df.dropna()
df_np = df.to_numpy()
# df_np = df_np.astype(int)
X = df_np[:, :13]
Y = df_np[:, -1]

public_key, private_key = paillier.generate_paillier_keypair()

# c = public_key.encrypt(42)
# pic = pickle.dumps(c)
# upic = pickle.loads(pic)
# p = private_key.decrypt(upic)

cipher_vect = []
# for each 1D numpy array, encrypt using batch Pyfhel
for row in df_np:
	cipher_row = [public_key.encrypt(x) for x in row]
	cipher_vect.append(cipher_row)

pickle_vect = []
for row in cipher_vect:
	pickle_row = [pickle.dumps(x) for x in row]
	pickle_vect.append(pickle_row)

# unpickle_vect = []
# for row in pickle_vect:
# 	unpickle_row = [pickle.loads(x) for x in row]
# 	unpickle_vect.append(unpickle_row)
# 	print(unpickle_row)

# decrypt_vect = []
# for row in unpickle_vect:
# 	# print(row)
# 	decrypt_row = [private_key.decrypt(x) for x in row]
# 	decrypt_vect.append(decrypt_row)
# 	print(decrypt_row)

mydf = pd.DataFrame(pickle_vect)
mydf.to_csv("encrypted.csv", sep=',', index=False)


