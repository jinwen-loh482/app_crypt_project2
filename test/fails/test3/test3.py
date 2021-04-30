import phe.encoding
from phe import paillier
import math
import pickle

class TestEncodedNumber(phe.encoding.EncodedNumber):
    BASE = 64
    LOG2_BASE = math.log(BASE, 2)

def main():
    with open('pubkey.pickle', 'rb') as handle:
        pubkey = pickle.load(handle)
    with open('prikey.pickle', 'rb') as handle:
        prikey = pickle.load(handle)
    
    int1 = 10
    int2 = 10
    int3 = 0

    eint1 = TestEncodedNumber.encode(pubkey, int1)
    assert int1 == eint1.decode()

    cint1 = pubkey.encrypt(eint1)
    pint1 = prikey.decrypt_encoded(cint1, TestEncodedNumber)
    # print("before: {} encrypted: {} decrypted: {}".format(int1, cint1.ciphertext(), pint1.decode()))

    eint2 = TestEncodedNumber.encode(pubkey, int2)
    assert int2 == eint2.decode()

    cint2 = pubkey.encrypt(eint2)

    eint3 = TestEncodedNumber.encode(pubkey, int3)
    assert int3 == eint3.decode()

    cint3 = pubkey.encrypt(eint3)

    tint = cint1 - cint2
    tint.obfuscate()
    pint2 = prikey.decrypt_encoded(tint, TestEncodedNumber)
    pint3 = prikey.decrypt_encoded(cint3, TestEncodedNumber)
    print("decrypted sub: {}".format(pint2.decode()))
    print("decrypted zero: {}".format(pint3.decode()))
    print("encrypted sub: {}".format(tint.ciphertext()))
    print("encrypted zero: {}".format(cint3.ciphertext()))
    print("sub equals zero: {}".format(tint.ciphertext() == cint3.ciphertext()))

def gen_keys():
    pubkey, prikey = paillier.generate_paillier_keypair()
    with open('pubkey.pickle', 'wb') as handle:
        pickle.dump(pubkey, handle)
    with open('prikey.pickle', 'wb') as handle:
        pickle.dump(prikey, handle)

if __name__ =='__main__':
    # gen_keys()
    main()