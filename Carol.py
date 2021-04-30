from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import pickle

publickey = 'public.pk'
privatekey = 'private.sk'
context = 'context.con'

HE_Client = Pyfhel()
HE_Client.contextGen(p=65537)
HE_Client.keyGen()

HE_Client.savepublicKey(publickey)
HE_Client.saveContext(context)
HE_Client.savesecretKey(privatekey)

a = 2
b = 4
ca = HE_Client.encryptInt(a)
cb = HE_Client.encryptInt(b)

encrypted = pickle.dumps(ca)
# write to file


HE_Cloud = Pyfhel()
HE_Cloud.restoreContext(context)
HE_Cloud.restorepublicKey(publickey)

# read from file
pa = pickle.loads(encrypted)
ca = PyCtxt(pyfhel=HE_Cloud, copy_ctxt=pa, encoding=int)

csum = HE_Cloud.add(ca, HE_Cloud.encryptInt(6))

print(HE_Client.decryptInt(csum))

try:
    HE_Cloud.decryptInt(ca)
except (RuntimeError,SystemError):
    print('Cloud failed to decrypt')