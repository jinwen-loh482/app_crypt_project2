import Pyfhel
import pickle

def main():
    print('test')
    HE = Pyfhel.Pyfhel()
    HE.contextGen(p=65537)
    HE.keyGen()

    print(HE)

    int1 = 127
    int2 = 127
    cint1 = HE.encryptInt(int1)
    help(HE)
    cint2 = HE.encryptInt(int2)

    print("int {} -> ctxt1 {}".format(int1, cint1))
    print("int {} -> ctxt2 {}".format(int2, cint2))

    psub = int1 - int2
    
    # retrieve from serialized object
    pkl_int1 = pickle.dumps(cint1)
    cint1 = pickle.loads(pkl_int1)

    csub = HE.sub(Pyfhel.PyCtxt(cint1), Pyfhel.PyCtxt(cint2))
    tsub = HE.decryptInt(csub)


    negate_csub = HE.negate(Pyfhel.PyCtxt(csub))
    print(HE.decryptInt(negate_csub))
    print(HE.decryptInt(csub))

    pkl_csub = pickle.dumps(csub)
    csub = pickle.loads(pkl_csub)

    pkl_negate_csub = pickle.dumps(negate_csub)
    negate_csub = pickle.loads(pkl_negate_csub)

    print("test {} == {}".format(psub, tsub))
    print("test {} == {}: {}".format(negate_csub, csub, negate_csub == csub))
    print(negate_csub.to_bytes())
    print(csub.to_bytes())
    print(cint1.to_bytes())

if __name__ =='__main__':
    main()