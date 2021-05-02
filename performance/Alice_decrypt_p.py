import pandas as pd
import numpy as np
from phe import paillier
import pickle
import time

def get_keys():
	# open paillier keys from files
	with open("pubkey.pickle", 'rb') as handle:
		public_key = pickle.load(handle)
	with open("prikey.pickle", 'rb') as handle:
		private_key = pickle.load(handle)
	return public_key, private_key

# read pickle file from carol
df = pd.read_pickle("encrypted_carol.pickle")
df = df.dropna()

# get valid index
validIndex = df.columns.get_loc('valid')

# convert to np
df_np = df.to_numpy()

# retrieve keys
public_key, private_key = get_keys()

end1 = time.time()
# decrypt each cell in row and return if the row is valid
decrypt_vect = list()
for row in df_np:
	decrypt_row = [private_key.decrypt(cell) for cell in row]
	if int(decrypt_row[validIndex]) == 1:
		decrypt_vect.append(decrypt_row)
end2 = time.time()
print('Time Elapsed: {}'.format(end2-end1))
# print all valid rows
for valid_row in decrypt_vect:
	print(valid_row)