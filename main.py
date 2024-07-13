import math
import base64


def trial_division(n):
    L = []  # is the list that we shall add all the divisors of n
    while n % 2 == 0:
        L.append(2)
        n //= 2
    f = 3  # a possible divisor of n, also called trial divisor.
    while f ** 2 <= n:
        if n % f == 0:
            L.append(f)
            n //= f
        else:
            f += 2
    if n != 1:
        L.append(n)
    return L


def fn_function(p, q):
    return (p - 1) * (q - 1)


# function to find the continued fraction of e / n
def continued_fraction(e, n):
    a = []
    while n > 0:
        q = e // n
        r = e % n
        a.append(q)
        e, n = n, r

    return a


def convergent_values(cf):
    convergents = []
    # Initial values for the first convergents
    h1, h2 = 1, 0  # h - 1, h - 2
    k1, k2 = 0, 1  # k - 1, k - 2

    for i in range(len(cf)):
        a = cf[i]
        h = a * h1 + h2
        k = a * k1 + k2
        convergents.append((h, k))
        h2, h1 = h1, h
        k2, k1 = k1, k

    return convergents


# function to find the secret exponent d:
def wiener_attack(convergents, e, n):
    fn = 0
    # φ(Ν) = ed-1 / k
    for k, d in convergents:
        if k > 0:
            fni = (e * d - 1)
            if fni % k == 0:
                fn = fni // k

                # quadratic equation x**2-(Ν-φ(Ν) + 1)x + N = 0
                x = -((n - fn) + 1)
                x1 = x * x - 4 * n
                if x1 >= 0:
                    root = math.isqrt(x1)
                    if root * root == x1:
                        return d

    return "FAIL"


n = 194749497518847283
print("n=", n)
e = 50736902528669041
print("e=", e)

# pq = trial_division(n)
p = 441244597  # pq[0]
q = 441364039  # pq[1]
print("p=", p, "q=", q)

fn = fn_function(p, q)
print("φ(Ν)=", fn)

cf = continued_fraction(e, n)
print("continued fraction:", cf)

convergents = convergent_values(cf)
print("convergents:", convergents)

d = wiener_attack(convergents, e, n)
print("Secret key d=", d)

with open("cipher_message.txt", "r") as ciphermsg:
    ciphermessage = ciphermsg.read()

    base64decoded = base64.b64decode(ciphermessage)
    base64decoded = base64decoded.decode('utf-8')

    ciphertext_str_list = base64decoded.strip('[]''C''=').split(',')
    ciphertext_str_list = [s.replace('\r\n', ',') for s in ciphertext_str_list]

    new_ciphertext_str_list = [num for s in ciphertext_str_list for num in s.split(',')]
    ciphertext_numbers_list = list(map(int, new_ciphertext_str_list))

    decoded_numbers = []
    for num in ciphertext_numbers_list:
        decoded_numbers.append(pow(num, d, n))

    decoded_message = ''
    for num in decoded_numbers:
        decoded_message += ''.join(chr(num))
    print("message:", decoded_message)

