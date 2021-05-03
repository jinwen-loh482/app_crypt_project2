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

There are four programs: zavoral_zhou_loh_barron-Alice_encrypt.py, zavoral_zhou_loh_barron-Carol.py, zavoral_zhou_loh_barron-Alice_decrypt.py, and zavoral_zhou_loh_barron-Darryl.py.

Run encryption as follows from the submission directory:
```
python zavoral_zhou_loh_barron-Alice_encrypt.py
python zavoral_zhou_loh_barron-Carol.py
# enter a category i.e. age
# enter the data to be searched i.e. 63.0
python zavoral_zhou_loh_barron-Alice_decrypt.py
```

Run without encryption as follows from the submission directory:
```
python zavoral_zhou_loh_barron-Darryl.py
# enter a category i.e. age
# enter the data to be searched i.e. 63.0
```

Successes:
- Able to encrypt, compute, and decrypt

Problems:
- Decrypt and encrypt take far too long
- Unable to return partial data

Contributors: Zavoral. Zhou, Loh, Barron