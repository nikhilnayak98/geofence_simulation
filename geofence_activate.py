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
    data1 = pd.read_csv('data1.csv') 
    data2 = pd.read_csv('data2.csv')

    key = int(data2['0'][1]) # e
    n = int(data1['0'][3])

    # convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** int(key)) % n for char in plaintext]
    # return the array of bytes
    return cipher


def decrypt(ciphertext):
    data1 = pd.read_csv('data1.csv')
    data2 = pd.read_csv('data2.csv')

    key = int(data2['0'][2]) # d
    n = int(data1['0'][3])

    # generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # return the array of bytes as a string
    return ''.join(plain)


if __name__ == '__main__':
    user_name = input('User Details (fetched through RFID tag): ')
    cprint('User Details: ' + str(user_name), 'cyan', attrs=['underline'], file=sys.stderr)
    primes = []
    total_no_primes = 0
    with open('primes.txt') as pfile:
        for line in pfile:
            primes.append(int(line)) # = [int(i) for i in line.split()]
            total_no_primes += 1
    p = primes[random.randint(1, total_no_primes - 1)]
    q = primes[random.randint(1, total_no_primes - 1)]
    r = primes[random.randint(1, total_no_primes - 1)]

    public, private, phi = generate_keypair(p, q, r)
    print('P = ' + str(p) + ', Q = ' + str(q) + ', R = ' + str(r))
   
    cprint('\nPublic Key: ' + str(public), 'green', attrs=['bold'], file=sys.stderr)
    cprint('Private Key: ' + str(private), 'red', attrs=['bold'], file=sys.stderr)

    data1 = [p, q, phi, public[1]]  #  p, q, phi, n
    df = pd.DataFrame(data1)
    df.to_csv('data1.csv') # storage of p, q, phi, n in table 1

    data2 = [r, public[0], private[0]] #  r, e, d
    df = pd.DataFrame(data2)
    df.to_csv('data2.csv') # storage of r, e, d in table 2

    # 20.4861236,85.9339274
    message = input('\nLocation coordinates (fetched from Google Location API): ')
    start_enc = timeit.default_timer()
    encrypted_msg = encrypt(message)
    stop_enc = timeit.default_timer()
    cprint('\nEncrypted cooridinates: ', 'blue', attrs=['bold'], file=sys.stderr)
    cprint(''.join([str(x) for x in encrypted_msg]),'blue', attrs=['bold'], file=sys.stderr)
    cprint('(Time Taken for Encryption: ' + str(stop_enc - start_enc) + ')', 'yellow', file=sys.stderr)

    edf = pd.DataFrame(encrypted_msg)
    edf.to_csv('enc_coordinates.csv', index=False)
    
    print('\n')
    cprint('**********************', 'green', attrs=['bold'], file=sys.stderr)
    cprint('*                    *', 'green', attrs=['bold'], file=sys.stderr)
    cprint('* Geofence Activated *', 'green', attrs=['bold'], file=sys.stderr)
    cprint('*                    *', 'green', attrs=['bold'], file=sys.stderr)
    cprint('**********************', 'green', attrs=['bold'], file=sys.stderr)