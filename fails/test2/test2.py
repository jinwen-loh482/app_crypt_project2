import filecmp
from binascii import unhexlify, b2a_base64
import shutil
import os
import time
import random
import pickle
import threading
import seal
from seal import ChooserEvaluator, \
	Ciphertext, \
	Decryptor, \
	Encryptor, \
	EncryptionParameters, \
	Evaluator, \
	IntegerEncoder, \
	FractionalEncoder, \
	KeyGenerator, \
	MemoryPoolHandle, \
	Plaintext, \
	SEALContext, \
	EvaluationKeys, \
	GaloisKeys, \
	PolyCRTBuilder, \
	ChooserEncoder, \
	ChooserEvaluator, \
	ChooserPoly


def main():
	# even with the secret key.
	parms = EncryptionParameters()

	# We first set the polynomial modulus. This must be a power-of-2 cyclotomic
	# polynomial, i.e. a polynomial of the form "1x^(power-of-2) + 1". The polynomial
	# modulus should be thought of mainly affecting the security level of the scheme;
	# larger polynomial modulus makes the scheme more secure. At the same time, it
	# makes ciphertext sizes larger, and consequently all operations slower.
	# Recommended degrees for poly_modulus are 1024, 2048, 4096, 8192, 16384, 32768,
	# but it is also possible to go beyond this. Since we perform only a very small
	# computation in this example, it suffices to use a very small polynomial modulus
	parms.set_poly_modulus("1x^2048 + 1")

	# Next we choose the [ciphertext] coefficient modulus (coeff_modulus). The size
	# of the coefficient modulus should be thought of as the most significant factor
	# in determining the noise budget in a freshly encrypted ciphertext: bigger means
	# more noise budget. Unfortunately, a larger coefficient modulus also lowers the
	# security level of the scheme. Thus, if a large noise budget is required for
	# complicated computations, a large coefficient modulus needs to be used, and the
	# reduction in the security level must be countered by simultaneously increasing
	# the polynomial modulus.

	# To make parameter selection easier for the user, we have constructed sets of
	# largest allowed coefficient moduli for 128-bit and 192-bit security levels
	# for different choices of the polynomial modulus. These recommended parameters
	# follow the Security white paper at http://HomomorphicEncryption.org. However,
	# due to the complexity of this topic, we highly recommend the user to directly
	# consult an expert in homomorphic encryption and RLWE-based encryption schemes
	# to determine the security of their parameter choices.

	# Our recommended values for the coefficient modulus can be easily accessed
	# through the functions

	#	 coeff_modulus_128bit(int)
	#	 coeff_modulus_192bit(int)

	# for 128-bit and 192-bit security levels. The integer parameter is the degree
	# of the polynomial modulus.

	# In SEAL the coefficient modulus is a positive composite number -- a product
	# of distinct primes of size up to 60 bits. When we talk about the size of the
	# coefficient modulus we mean the bit length of the product of the small primes.
	# The small primes are represented by instances of the SmallModulus class; for
	# example coeff_modulus_128bit(int) returns a vector of SmallModulus instances.

	# It is possible for the user to select their own small primes. Since SEAL uses
	# the Number Theoretic Transform (NTT) for polynomial multiplications modulo the
	# factors of the coefficient modulus, the factors need to be prime numbers
	# congruent to 1 modulo 2*degree(poly_modulus). We have generated a list of such
	# prime numbers of various sizes, that the user can easily access through the
	# functions

	#	 small_mods_60bit(int)
	#	 small_mods_50bit(int)
	#	 small_mods_40bit(int)
	#	 small_mods_30bit(int)

	# each of which gives access to an array of primes of the denoted size. These
	# primes are located in the source file util/globals.cpp.

	# Performance is mainly affected by the size of the polynomial modulus, and the
	# number of prime factors in the coefficient modulus. Thus, it is important to
	# use as few factors in the coefficient modulus as possible.

	# In this example we use the default coefficient modulus for a 128-bit security
	# level. Concretely, this coefficient modulus consists of only one 56-bit prime
	# factor: 0xfffffffff00001.
	parms.set_coeff_modulus(seal.coeff_modulus_128(2048))

	# The plaintext modulus can be any positive integer, even though here we take
	# it to be a power of two. In fact, in many cases one might instead want it to
	# be a prime number; we will see this in example_batching(). The plaintext
	# modulus determines the size of the plaintext data type, but it also affects
	# the noise budget in a freshly encrypted ciphertext, and the consumption of
	# the noise budget in homomorphic multiplication. Thus, it is essential to try
	# to keep the plaintext data type as small as possible for good performance.
	# The noise budget in a freshly encrypted ciphertext is

	#	 ~ log2(coeff_modulus/plain_modulus) (bits)

	# and the noise budget consumption in a homomorphic multiplication is of the
	# form log2(plain_modulus) + (other terms).
	parms.set_plain_modulus(1 << 8)

	# Now that all parameters are set, we are ready to construct a SEALContext
	# object. This is a heavy class that checks the validity and properties of
	# the parameters we just set, and performs and stores several important
	# pre-computations.
	context = SEALContext(parms)

	# Print the parameters that we have chosen
	print_parameters(context)

	# Plaintexts in the FV scheme are polynomials with coefficients integers modulo
	# plain_modulus. To encrypt for example integers instead, one can use an
	# `encoding scheme' to represent the integers as such polynomials. SEAL comes
	# with a few basic encoders:

	# [IntegerEncoder]
	# Given an integer base b, encodes integers as plaintext polynomials as follows.
	# First, a base-b expansion of the integer is computed. This expansion uses
	# a `balanced' set of representatives of integers modulo b as the coefficients.
	# Namely, when b is odd the coefficients are integers between -(b-1)/2 and
	# (b-1)/2. When b is even, the integers are between -b/2 and (b-1)/2, except
	# when b is two and the usual binary expansion is used (coefficients 0 and 1).
	# Decoding amounts to evaluating the polynomial at x=b. For example, if b=2,
	# the integer

	#	 26 = 2^4 + 2^3 + 2^1

	# is encoded as the polynomial 1x^4 + 1x^3 + 1x^1. When b=3,

	#	 26 = 3^3 - 3^0

	# is encoded as the polynomial 1x^3 - 1. In memory polynomial coefficients are
	# always stored as unsigned integers by storing their smallest non-negative
	# representatives modulo plain_modulus. To create a base-b integer encoder,
	# use the constructor IntegerEncoder(plain_modulus, b). If no b is given, b=2
	# is used.

	# [FractionalEncoder]
	# The FractionalEncoder encodes fixed-precision rational numbers as follows.
	# It expands the number in a given base b, possibly truncating an infinite
	# fractional part to finite precision, e.g.

	#	 26.75 = 2^4 + 2^3 + 2^1 + 2^(-1) + 2^(-2)

	# when b=2. For the sake of the example, suppose poly_modulus is 1x^1024 + 1.
	# It then represents the integer part of the number in the same way as in
	# IntegerEncoder (with b=2 here), and moves the fractional part instead to the
	# highest degree part of the polynomial, but with signs of the coefficients
	# changed. In this example we would represent 26.75 as the polynomial

	#	 -1x^1023 - 1x^1022 + 1x^4 + 1x^3 + 1x^1.

	# In memory the negative coefficients of the polynomial will be represented as
	# their negatives modulo plain_modulus.

	# [PolyCRTBuilder]
	# If plain_modulus is a prime congruent to 1 modulo 2*degree(poly_modulus), the
	# plaintext elements can be viewed as 2-by-(degree(poly_modulus) / 2) matrices
	# with elements integers modulo plain_modulus. When a desired computation can be
	# vectorized, using PolyCRTBuilder can result in massive performance improvements
	# over naively encrypting and operating on each input number separately. Thus,
	# in more complicated computations this is likely to be by far the most important
	# and useful encoder. In example_batching() we show how to use and operate on
	# encrypted matrix plaintexts.

	# For performance reasons, in homomorphic encryption one typically wants to keep
	# the plaintext data types as small as possible, which can make it challenging to
	# prevent data type overflow in more complicated computations, especially when
	# operating on rational numbers that have been scaled to integers. When using
	# PolyCRTBuilder estimating whether an overflow occurs is a fairly standard task,
	# as the matrix slots are integers modulo plain_modulus, and each slot is operated
	# on independently of the others. When using IntegerEncoder or FractionalEncoder
	# it is substantially more difficult to estimate when an overflow occurs in the
	# plaintext, and choosing the plaintext modulus very carefully to be large enough
	# is critical to avoid unexpected results. Specifically, one needs to estimate how
	# large the largest coefficient in  the polynomial view of all of the plaintext
	# elements becomes, and choose the plaintext modulus to be larger than this value.
	# SEAL comes with an automatic parameter selection tool that can help with this
	# task, as is demonstrated in example_parameter_selection().

	# Here we choose to create an IntegerEncoder with base b=2.
	encoder = IntegerEncoder(context.plain_modulus())

	# We are now ready to generate the secret and public keys. For this purpose we need
	# an instance of the KeyGenerator class. Constructing a KeyGenerator automatically
	# generates the public and secret key, which can then be read to local variables.
	# To create a fresh pair of keys one can call KeyGenerator::generate() at any time.
	keygen = KeyGenerator(context)
	public_key = keygen.public_key()
	secret_key = keygen.secret_key()

	# To be able to encrypt, we need to construct an instance of Encryptor. Note that
	# the Encryptor only requires the public key.
	encryptor = Encryptor(context, public_key)

	# Computations on the ciphertexts are performed with the Evaluator class.
	evaluator = Evaluator(context)

	# We will of course want to decrypt our results to verify that everything worked,
	# so we need to also construct an instance of Decryptor. Note that the Decryptor
	# requires the secret key.
	decryptor = Decryptor(context, secret_key)

	# We start by encoding two integers as plaintext polynomials.
	value1 = 5
	plain1 = encoder.encode(value1)
	print("Encoded " + (str)(value1) + " as polynomial " + plain1.to_string() + " (plain1)")

	value2 = 5
	plain2 = encoder.encode(value2)
	print("Encoded " + (str)(value2) + " as polynomial " + plain2.to_string() + " (plain2)")
	
	value3 = 0
	plain3 = encoder.encode(value3)
	print("Encoded " + (str)(value3) + " as polynomial " + plain3.to_string() + " (plain3)")

	# Encrypting the values is easy.
	encrypted1 = Ciphertext()
	encrypted2 = Ciphertext()
	encrypted3 = Ciphertext()
	print("Encrypting plain1: ")
	encryptor.encrypt(plain1, encrypted1)
	print("Done (encrypted1)")

	print("Encrypting plain2: ")
	encryptor.encrypt(plain2, encrypted2)
	print("Done (encrypted2)")

	print("Encrypting plain3: ")
	encryptor.encrypt(plain3, encrypted3)
	print("Done (encrypted3)")

	evaluator.negate(encrypted2)

	# Negation does not consume any noise budget.
	print("Noise budget in -encrypted1: " + (str)(decryptor.invariant_noise_budget(encrypted1)) + " bits")

	# Addition can be done in-place (overwriting the first argument with the result,
	# or alternatively a three-argument overload with a separate destination variable
	# can be used. The in-place variants are always more efficient. Here we overwrite
	# encrypted1 with the sum.
	evaluator.add(encrypted1, encrypted2)

	# Now we decrypt and decode our result.
	plain_result = Plaintext()
	print("Decrypting result: ")
	decryptor.decrypt(encrypted1, plain_result)
	print("Done")

	# Print the result plaintext polynomial.
	print("Plaintext polynomial: " + plain_result.to_string())

	# Decode to obtain an integer result.
	print("Decoded integer: " + (str)(encoder.decode_int32(plain_result)))

	plain_result2 = Plaintext()
	print("Decrypting result: ")
	decryptor.decrypt(encrypted3, plain_result2)
	print("Done")

	# Print the result plaintext polynomial.
	print("Plaintext polynomial: " + plain_result2.to_string())

	# Decode to obtain an integer result.
	print("Decoded integer: " + (str)(encoder.decode_int32(plain_result2)))

	encrypted2.save_to_file()
	os.rename("ciphertext.bin", "encrypted2.bin")
	encrypted3.save_to_file()
	os.rename("ciphertext.bin", "encrypted3.bin")
	print("zero equals sub: {}".format(filecmp.cmp("encrypted2.bin", "encrypted3.bin")))
	print("------------ encrypted 2 ------------")
	with open("encrypted2.bin", "rb") as f:
		ciphertext2 = b2a_base64(f.read())
	print("------------ encrypted 3 ------------")
	with open("encrypted3.bin", "rb") as f:
		ciphertext3 = b2a_base64(f.read())
	print("zero equals sub: {}".format(ciphertext2 == ciphertext3))
    shutil.move("encrypted2.bin", "/mnt/project")
    shutil.move("encrypted3.bin", "/mnt/project")

def print_parameters(context):
	print("/ Encryption parameters:")
	print("| poly_modulus: " + context.poly_modulus().to_string())

	# Print the size of the true (product) coefficient modulus
	print("| coeff_modulus_size: " + (str)(context.total_coeff_modulus().significant_bit_count()) + " bits")

	print("| plain_modulus: " + (str)(context.plain_modulus().value()))
	print("| noise_standard_deviation: " + (str)(context.noise_standard_deviation()))

if __name__ == '__main__':
	main()
