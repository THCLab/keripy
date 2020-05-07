# Python Implementation of the KERI Core Libraries

Project Name:  keripy


## Installation

### Dependencies
#### Binaries

python 3.82+
libsodium 1.0.18+



#### python packages
lmdb 0.98+
pysodium 0.7.5+
blake3 0.1.5+
argon2-cffi 19.2.0+
msgpack 1.0.0+
simplejson 3.17.0+
cbor2 5.1.0+

$ pip3 install -U lmdb
$ pip3 install -U pysodium
$ pip3 install -U blake3
$ pip3 install -U argon2-cffi
$ pip3 install -U msgpack
$ pip3 install -U simplejson
$ pip3 install -U cbor2
 

## Python Binding Types
https://realpython.com/python-bindings-overview/

ctypes
CFFI
PyBind11
Cython

## Crypto Support

### Blake3 Hashing

Currently libsodium only supports blake2b but blake3 is on roadmap for libsodim 1.x

#### blake3-py
https://github.com/oconnor663/blake3-py

python bindings to the official rust implementation of blake3

Python bindings for the official Rust implementation of BLAKE3, based on PyO3. These bindings expose all the features of BLAKE3, including extendable output, keying, and multithreading.

Uses binary wheels

$ pip3 install blake3


### Seed Stretching 

#### Argon2
Argon2 with Libsodium pwhash

https://libsodium.gitbook.io/doc/password_hashing

Sodium's high-level crypto_pwhash_* API currently leverages the Argon2id function on all platforms. This can change at any point in time, but it is guaranteed that a given version of libsodium can verify all hashes produced by all previous versions, from any platform. Applications don't have to worry about backward compatibility.

The more specific crypto_pwhash_scryptsalsa208sha256_* API uses the more conservative and widely deployed Scrypt function.


https://github.com/hynek/argon2-cffi

pysodium
```python
crypto_pwhash(outlen, passwd, salt, opslimit, memlimit, alg)
```


### LibSodium Python Libraries

#### pysodium
https://github.com/stef/pysodium
Barebones fast small
ctypes binding

#### libnacl
https://github.com/saltstack/libnacl
not as barebones but includes easy functions not in pysodium
ctypes binding

#### pynacl
https://github.com/pyca/pynacl/
bigger more docs more utility functions
Wheel on macos
CFFI binding


#### csodium  (obsolete)
https://github.com/ereOn/csodium
Like pysodium but uses wheel to automatically compile libsodium
not complete stopped dev 4 years ago




### Python Libraries that Support
https://doc.libsodium.org/advanced/ed25519-curve25519

crypto_sign_ed25519_pk_to_curve25519
crypto_sign_ed25519_sk_to_curve25519

#### pysodium
pysodium/__init__.py

```python
def crypto_sign_pk_to_box_pk(pk):
    if pk is None:
        raise ValueError
    if not (len(pk) == crypto_sign_PUBLICKEYBYTES): raise ValueError('Truncated public key')
    res = ctypes.create_string_buffer(crypto_box_PUBLICKEYBYTES)
    __check(sodium.crypto_sign_ed25519_pk_to_curve25519(ctypes.byref(res), pk))
    return res.raw


def crypto_sign_sk_to_box_sk(sk):
    if sk is None:
        raise ValueError
    if not (len(sk) == crypto_sign_SECRETKEYBYTES): raise ValueError('Truncated secret key')
    res = ctypes.create_string_buffer(crypto_box_SECRETKEYBYTES)
    __check(sodium.crypto_sign_ed25519_sk_to_curve25519(ctypes.byref(res), sk))
    return res.raw
```



#### libnacl
libnacl/__init__.py

``` python
def crypto_sign_ed25519_pk_to_curve25519(ed25519_pk):
    '''
    Convert an Ed25519 public key to a Curve25519 public key
    '''
    if len(ed25519_pk) != crypto_sign_ed25519_PUBLICKEYBYTES:
        raise ValueError('Invalid public key')

    curve25519_pk = ctypes.create_string_buffer(crypto_scalarmult_curve25519_BYTES)
    ret = nacl.crypto_sign_ed25519_pk_to_curve25519(curve25519_pk, ed25519_pk)
    if ret:
        raise CryptError('Failed to generate Curve25519 public key')
    return curve25519_pk.raw


def crypto_sign_ed25519_sk_to_curve25519(ed25519_sk):
    '''
    Convert an Ed25519 secret key to a Curve25519 secret key
    '''
    if len(ed25519_sk) != crypto_sign_ed25519_SECRETKEYBYTES:
        raise ValueError('Invalid secret key')

    curve25519_sk = ctypes.create_string_buffer(crypto_scalarmult_curve25519_BYTES)
    ret = nacl.crypto_sign_ed25519_sk_to_curve25519(curve25519_sk, ed25519_sk)
    if ret:
        raise CryptError('Failed to generate Curve25519 secret key')
    return curve25519_sk.raw

```




#### pynacl
pynacl/src/nacl/bindings/__init__.py 
from nacl.bindings.crypto_sign import 
    crypto_sign_ed25519_pk_to_curve25519,
    crypto_sign_ed25519_sk_to_curve25519,
    
def crypto_sign_ed25519_pk_to_curve25519(public_key_bytes):
    """
    Converts a public Ed25519 key (encoded as bytes ``public_key_bytes``) to
    a public Curve25519 key as bytes.
    Raises a ValueError if ``public_key_bytes`` is not of length
    ``crypto_sign_PUBLICKEYBYTES``
    :param public_key_bytes: bytes
    :rtype: bytes
    """
    if len(public_key_bytes) != crypto_sign_PUBLICKEYBYTES:
        raise exc.ValueError("Invalid curve public key")

    curve_public_key_len = crypto_sign_curve25519_BYTES
    curve_public_key = ffi.new("unsigned char[]", curve_public_key_len)

    rc = lib.crypto_sign_ed25519_pk_to_curve25519(curve_public_key,
                                                  public_key_bytes)
    ensure(rc == 0,
           'Unexpected library error',
           raising=exc.RuntimeError)

    return ffi.buffer(curve_public_key, curve_public_key_len)[:]


def crypto_sign_ed25519_sk_to_curve25519(secret_key_bytes):
    """
    Converts a secret Ed25519 key (encoded as bytes ``secret_key_bytes``) to
    a secret Curve25519 key as bytes.
    Raises a ValueError if ``secret_key_bytes``is not of length
    ``crypto_sign_SECRETKEYBYTES``
    :param secret_key_bytes: bytes
    :rtype: bytes
    """
    if len(secret_key_bytes) != crypto_sign_SECRETKEYBYTES:
        raise exc.ValueError("Invalid curve secret key")

    curve_secret_key_len = crypto_sign_curve25519_BYTES
    curve_secret_key = ffi.new("unsigned char[]", curve_secret_key_len)

    rc = lib.crypto_sign_ed25519_sk_to_curve25519(curve_secret_key,
                                                  secret_key_bytes)
    ensure(rc == 0,
           'Unexpected library error',
           raising=exc.RuntimeError)

    return ffi.buffer(curve_secret_key, curve_secret_key_len)[:]


## Encoding Support

### JSON support

https://artem.krylysov.com/blog/2015/09/29/benchmark-python-json-libraries/
https://pythonspeed.com/articles/faster-json-library/

#### simplejson
most complete support but slower than ujsonn or rapidjson
$ pip3 install -U simplejson

#### ujson

fastest but not many options

$ pip install ujson

#### python-rapidjson
 almost as fact as ujson but supports more options
 
### msgpack

msgpack 1.0.0+
$ pip3 install -U msgpack
 
### cbor

cbor2 5.1.0
https://pypi.org/project/cbor2/

$ pip3 install -U cbor2

Not sure if cbor2 uses libcbor or not
$ brew install libcbor 

libcbor 0.7.0