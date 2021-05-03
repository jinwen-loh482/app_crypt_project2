# app_crypt_project2

dependencies:
- python3
- library: argparse
- library: csv
- library: math
- library: numpy
- library: pandas
- library: phe
- library: pickle
- library: sys

This project simulates homomorphic encryption with a cloud server. In this scenario, 'Alice' is the client and 'Carol' is the cloud server. Additionally, for performance purposes we created 'Darryl' the unencrypted version of the cloud server.

There are four programs: Alice_encrypt.py, Carol.py, Alice_decrypt.py, and Darryl.py.

Run encryption as follows from the submission directory:
```
python Alice_encrypt.py
python Carol.py
# enter a category
# enter the data to be searched
python Alice_decrypt.py
```

Run without encryption as follows from the submission directory:
```
python Darryl.py
# enter a category
# enter the data to be searched
```

Successes:
- Able to encrypt, compute, and decrypt

Problems:
- Decrypt and encrypt take far too long
- Unable to return partial data

Contributors: Zavoral. Zhou, Loh, Barron