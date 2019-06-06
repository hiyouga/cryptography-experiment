# Cryptographic Algorithms

BUAA-CST Spring 2019 Cryptography Experiment Project Code (Python).

[![LICENSE](https://img.shields.io/packagist/l/doctrine/orm.svg)](LICENSE)

## Requirement

- Python 3
- multiprocessing
- numpy [optional]
- matplotlib [optional]

## Contents

- [utils/](MyCrypto/utils/) - Some useful utilities in cryptography.
  - [bigInt.cpp](MyCrypto/utils/bigInt.cpp) - Big integer arithmetic in C++. [[ref]](https://github.com/faheel/BigInt)
  - [bitarray.py](MyCrypto/utils/bitarray.py) - A bit array class.
  - [matrix.py](MyCrypto/utils/matrix.py) - Arithmetic of matrices.
  - [residue_field.py](MyCrypto/utils/residue_field.py) - Residue field `Z_p`.
  - [extension_field.py](MyCrypto/utils/extension_field.py) - Galois Field `GF[x]/(p(x))`.
  - [galois_field.py](MyCrypto/utils/galois_field.py) - Galois Field `GF_2^m`.
- [algorithms/](MyCrypto/algorithms/) - Basic algorithms in cryptography.
  - [prime_sieve.py](MyCrypto/algorithms/prime_sieve.py) - Generate primes with Sieve of Eratosthenes.
  - [exgcd.py](MyCrypto/algorithms/exgcd.py) -  Extended Euclidean algorithm.
  - [power.py](MyCrypto/algorithms/power.py) - Modular exponentiation algorithm.
  - [crt.py](MyCrypto/algorithms/crt.py) - Chinese Remainder Theorem (CRT).
  - [prime_test.py](MyCrypto/algorithms/prime_test.py) - Probabilistic primality testing. (Miller–Rabin/Fermat/Solovay–Strassen)
  - [prime_root.py](MyCrypto/algorithms/prime_root.py) - Generate prime roots in `Z_p`.
  - [prime_poly.py](MyCrypto/algorithms/prime_poly.py) - Generate prime polynomial in `GF_2^m`.
  - [jacobi.py](MyCrypto/algorithms/jacobi.py) - Calculate the Jacobi symbol.
- [classical/](MyCrypto/classical/) - Classical Cryptography.
  - [affine.py](MyCrypto/classical/affine.py) - Affine Cipher.
  - [vigenere.py](MyCrypto/classical/vigenere.py) - Vigenere Cipher.
  - [vernam.py](MyCrypto/classical/vernam.py) - Vernam Cipher.
  - [crack_single_table.py](MyCrypto/classical/crack_single_table.py) - Crack simple substitution cipher using letter frequency analysis.
  - [hill.py](MyCrypto/classical/hill.py) - Hill cipher and the cracker.
- [des/](MyCrypto/des/) - Data Encryption Standard (DES).
  - [des_utils.py](MyCrypto/des/des_utils.py) - Some utilities in DES.
  - [des.py](MyCrypto/des/des.py) - A 64-bit DES block cipher.
  - [diff_crypt.py](MyCrypto/des/diff_crypt.py) - Use differential cryptanalysis to attack DES cipher.
  - [triple_des.py](MyCrypto/des/triple_des.py) - A 3-DES block cipher.
  - [s_des.py](MyCrypto/des/s_des.py) - A simplified DES cipher.
  - [mitm.py](MyCrypto/des/mitm.py) - Use meet-in-the-middle attack on double S-DES.
- [aes/](MyCrypto/aes/) - Advanced Encryption Standard (AES).
  - [aes.py](MyCrypto/aes/aes.py) - A 128-bit AES block cipher.
  - [fast_aes.py](MyCrypto/aes/fast_aes.py) - A look-up-table implementation of AES to accelerate the algorithm.
  - [block_cipher.py](MyCrypto/aes/block_cipher.py) - Some block cipher modes of operation. (ECB/CBC/CFB)
  - [cipher_gui.py](MyCrypto/aes/cipher_gui.py) - A simple GUI for our block cipher.
- [rsa/](MyCrypto/rsa/) - Rivest-Shamir-Adleman (RSA) cryptosystem.
  - [knapsack_cipher.py](MyCrypto/rsa/knapsack_cipher.py) - A public-key cryptosystem based on knapsack problem.
  - [rsa.py](MyCrypto/rsa/rsa.py) - A 1024-bit RSA public-key cryptosystem.
  - [rsa_oaep.py](MyCrypto/rsa/rsa_oaep.py) - RSA with Optimal Asymmetric Encryption Padding (OAEP).
- [ecc/](MyCrypto/ecc/) - Elliptic-curve cryptography (ECC).
  - [ecc.py](MyCrypto/ecc/ecc.py) - The basic elliptic curve arithmetic.
  - [diffie_hellman_ecc.py](MyCrypto/ecc/diffie_hellman_ecc.py) - The anonymous key agreement protocol over elliptic curves. (Also ECDH)
  - [elgamal_ecc.py](MyCrypto/ecc/elgamal_ecc.py) - The ElGamal public-key cryptosystem over elliptic curves.
  - [sm2.py](MyCrypto/ecc/sm2.py) - The SM2 ([GM/T 0003-2012](http://www.gmbz.org.cn/main/bzlb.html)) public-key cryptography standard.
- [hash/](MyCrypto/hash/) - Cryptographic hash functions.
  - [sha_utils.py](MyCrypto/hash/sha_utils.py) - Some utilities for Secure Hash Algorithm (SHA) family.
  - [sha1.py](MyCrypto/hash/sha1.py) - The SHA-1 (Secure Hash Algorithm 1) hash function.
  - [sha3.py](MyCrypto/hash/sha3.py) - The SHA-3 (Secure Hash Algorithm 3) hash function. (Also Keccak) 
  - [hmac.py](MyCrypto/hash/hmac.py) - A HMAC (Hash-based Message Authentication Code) function with SHA.
  - [birthday_attack.py](MyCrypto/hash/birthday_attack.py) - A birthday attack example on SHA3-16.
  - [message_variants.py](MyCrypto/hash/message_variants.py) - Generate arbitrary number of message variants.
- [dsa/](MyCrypto/dsa/) - Digital signature algorithms.
  - [dsa.py](MyCrypto/dsa/dsa.py) - The NIST proposed DSA in Digital Signature Standard (DSS).
  - [elgamal_dsa.py](MyCrypto/dsa/elgamal_dsa.py) - The ElGamal signature scheme based on DLP.
  - [schnorr_dsa.py](MyCrypto/dsa/schnorr_dsa.py) - The Schnorr signature scheme based on DLP.
  - [sm2_dsa.py](MyCrypto/dsa/sm2_dsa.py) - The SM2 ([GM/T 0003-2012](http://www.gmbz.org.cn/main/bzlb.html)) digital signature algorithm based on ECC.
- [testdata/](MyCrypto/testdata/) - Test data folder.
  - [text.txt](MyCrypto/testdata/text.txt) - A UTF-8 encoded text file contains short Chinese and English sentences.

## Documents

**Simplified Chinese Only!!!**

- [ex1.pdf](Documents/zh-cn/ex1.pdf)
  - [prime_sieve.py](MyCrypto/algorithms/prime_sieve.py)
  - [exgcd.py](MyCrypto/algorithms/exgcd.py)
  - [power.py](MyCrypto/algorithms/power.py)
  - [crt.py](MyCrypto/algorithms/crt.py)
- [ex2.pdf](Documents/zh-cn/ex2.pdf)
  - [prime_test.py](MyCrypto/algorithms/prime_test.py)
  - [galois_field.py](MyCrypto/utils/galois_field.py)
  - [prime_root.py](MyCrypto/algorithms/prime_root.py)
  - [prime_poly.py](MyCrypto/algorithms/prime_poly.py)
- [ex3.pdf](Documents/zh-cn/ex3.pdf)
  - [classical](MyCrypto/classical/)
- [ex4.pdf](Documents/zh-cn/ex4.pdf)
  - [des](MyCrypto/des/)
- [ex5.pdf](Documents/zh-cn/ex5.pdf)
  - [aes.py](MyCrypto/aes/aes.py)
  - [block_cipher.py](MyCrypto/aes/block_cipher.py)
  - [cipher_gui.py](MyCrypto/aes/cipher_gui.py)
- [ex6.pdf](Documents/zh-cn/ex6.pdf)
  - [fast_aes.py](MyCrypto/aes/fast_aes.py)
- [ex7.pdf](Documents/zh-cn/ex7.pdf)
  - [bigInt.cpp](MyCrypto/utils/bigInt.cpp)
  - [rsa](MyCrypto/rsa/)
- [ex8.pdf](Documents/zh-cn/ex8.pdf)
  - [ecc](MyCrypto/ecc/)
- [ex9.pdf](Documents/zh-cn/ex9.pdf)
  - [hash](MyCrypto/hash/)
- [ex10.pdf](Documents/zh-cn/ex10.pdf)
  - [dsa](MyCrypto/dsa/)

## License

This project is licensed under the terms of the [MIT license](LICENSE).

----

**Don't copy, learn.**