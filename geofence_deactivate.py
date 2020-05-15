import random
import pandas as pd
import timeit
from termcolor import colored, cprint
import sys

'''
Euclid's algorithm for determining the greatest common divisor
Use iteration to make it faster for larger integers
'''
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


'''
Tests to see if a number is prime.
'''
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True


'''
Euclid's extended algorithm for finding the multiplicative inverse of two numbers
'''
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = (int)(temp_phi/e)
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi


def generate_keypair(p, q, r):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
    # n = pqr
    n = p * q * r

    # phi is the totient of n
    phi = (p-1) * (q-1) * (r-1)

    # choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)    
        
    # use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    
    # return public and private keypair
    # public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n), phi)


def encrypt(plaintext):
    data1 = pd.read_csv('table1.csv') 
    data2 = pd.read_csv('table2.csv')

    key = int(data2['0'][1]) # e
    n = int(data1['0'][3])

    # convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** int(key)) % n for char in plaintext]
    # return the array of bytes
    return cipher


def decrypt(ciphertext):
    data1 = pd.read_csv('table1.csv')
    data2 = pd.read_csv('table2.csv')

    key = int(data2['0'][2]) # d
    n = int(data1['0'][3])

    # generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # return the array of bytes as a string
    return ''.join(plain)


if __name__ == '__main__':
    cprint('User Identification (fetched though RFID tag) ', 'cyan', attrs=['bold'], file=sys.stderr)

    cprint('\nUser details to be fetched from Cloud Datastore', 'blue', attrs=['bold'], file=sys.stderr)
    
    enc_coordinates = pd.read_csv('enc_coordinates.csv')
    encrypted_msg = []
    for x in enc_coordinates.values:
        encrypted_msg.append(int(x[0]))

    cprint('\nDecrypted cooridinates: ', 'magenta', attrs=['bold'], file=sys.stderr)
    start_dec = timeit.default_timer()
    cprint(decrypt(encrypted_msg), 'magenta', attrs=['bold'], file=sys.stderr)
    stop_dec = timeit.default_timer()
    cprint('(Time Taken for Decryption: ' + str(stop_dec - start_dec)  + ')', 'yellow', file=sys.stderr)

    print('\n')
    cprint('************************', 'red', attrs=['bold'], file=sys.stderr)
    cprint('*                      *', 'red', attrs=['bold'], file=sys.stderr)
    cprint('* Geofence Deactivated *', 'red', attrs=['bold'], file=sys.stderr)
    cprint('*                      *', 'red', attrs=['bold'], file=sys.stderr)
    cprint('************************', 'red', attrs=['bold'], file=sys.stderr)
