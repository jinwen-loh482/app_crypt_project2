import pandas as pd
import numpy as np
from phe import paillier
import pickle

def gen_keys():
    # generate paillier keys
    pubkey, prikey = paillier.generate_paillier_keypair()

    # save private and public keys
    with open('pubkey.pickle', 'wb') as handle:
        pickle.dump(pubkey, handle)
    with open('prikey.pickle', 'wb') as handle:
        pickle.dump(prikey, handle)
    return pubkey, prikey

# Read from csv
# store as numpy array, df_np
df = pd.read_csv("Heart.csv")
df = df.dropna()
df_np = df.to_numpy()

# create private and public keys
public_key, private_key = gen_keys()

cipher_vect = list()
for row in df_np:
    # encrypt each item and append row
	cipher_row = [public_key.encrypt(x) for x in row]
	cipher_vect.append(cipher_row)

# pickle data and columns
mydf = pd.DataFrame(cipher_vect, columns=df.columns)
pd.to_pickle(mydf, "encrypted.pickle")
