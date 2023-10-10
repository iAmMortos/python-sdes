
from log_utils import log, bitstr, matstr


# swap the front and back half of the bits based on the size
def sw(d, size, verbose=False, indent=0):
  dh = size >> 1
  s1 = ((((1 << dh) - 1) << dh) & d) >> dh
  s2 = ((1 << dh) - 1) & d
  result = (s2 << dh) | s1
  if verbose:
    log('SW - Swapping front and back half of byte:', indent)
    log(f'{bitstr(d, size)} -> {bitstr(result, size)}', indent + 1)
  return result


# perform a circular left shift on the give data by n steps
def lshift(d, n, size, verbose=False, indent=0):
  result = ((d << n) % (1 << size)) | (d >> (size - n))
  if verbose:
    log(f'LSHIFT - Circular Left Shifting by {n} bit(s):', indent)
    log(f'{bitstr(d, size)} -> {bitstr(result, size)}', indent+1)
  return result


# generalized function for rearranging, expanding, and reducing data's bits
def p_arrange(d, order, size, verbose=False, indent=0):
  s = f'{d:0>{size}b}'
  ns = ''
  for o in order:
    ns += s[o]
  result = int(ns, 2)
  if verbose:
    log(f'{bitstr(d, size)}', indent)
    log(f'-> {order}', indent)
    log(f'{bitstr(result, len(order))}', indent)
  return result


# initial permutation
def ip(d, verbose=False, indent=0):
  order = [1, 5, 2, 0, 3, 7, 4, 6]
  if verbose:
    log('IP - Performing Initial Permutation. Rearranging 8 bits:', indent)
  return p_arrange(d, order, 8, verbose, indent+1)


# inverse permutation
def ip2(d, verbose=False, indent=0):
  order = [3, 0, 2, 4, 6, 1, 7, 5]
  if verbose:
    log('IP\' - Performing INVERSE Inverse Permutation. Rearranging 8 bits:', indent)
  return p_arrange(d, order, 8, verbose, indent+1)
  
  
# rearranges 4 bits
def p4(d, verbose=False, indent=0):
  order = [1, 3, 2, 0]
  if verbose:
    log('P4 - Rearranging 4 bits:', indent)
  return p_arrange(d, order, 4, verbose, indent+1)


# reduces 10 bits into 8 bits
def p8(d, verbose=False, indent=0):
  order = [5, 2, 6, 3, 7, 4, 9, 8]
  if verbose:
    log('P8 - Downsizing and rearranging 10 bits to 8 bits:', indent)
  return p_arrange(d, order, 10, verbose, indent+1)


# rearranges 10 bits
def p10(d, verbose=False, indent=0):
  order = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
  if verbose:
    log('P10 - Rearranging 10 bits:', indent)
  return p_arrange(d, order, 10, verbose, indent+1)


# expands 4 bits to 8 bits
def ep(d, verbose=False, indent=0):
  order = [3, 0, 1, 2, 1, 2, 3, 0]
  if verbose:
    log('E/P - Expanding 4 bits to 8 bits:', indent)
  return p_arrange(d, order, 4, verbose, indent+1)


# Generate two 8-bit keys based on initial 10-bit key
def gen_keys(k, verbose=False, indent=0):
  if verbose:
    log('Key Generation - Creating two 8-bit subkeys from one 10-bit key.', indent)
  p1, p2 = split(p10(k, verbose, indent+1), 10, verbose, indent+1)
  p1 = lshift(p1, 1, 5, verbose, indent+1)
  p2 = lshift(p2, 1, 5, verbose, indent+1)
  k1 = p8(join(p1, p2, 10, verbose, indent+1), verbose, indent+1)

  p1 = lshift(p1, 2, 5, verbose, indent+1)
  p2 = lshift(p2, 2, 5, verbose, indent+1)
  k2 = p8(join(p1, p2, 10, verbose, indent+1), verbose, indent+1)

  if verbose:
    log(f'Final Subkeys: {bitstr(k, 10)} -> {bitstr(k1, 8)} {bitstr(k2, 8)}', indent+1)
  return k1, k2


# separate front and back half of bits and return them as a two-ple
def split(d, size, verbose=False, indent=0):
  dh = size >> 1
  s1 = ((((1 << dh) - 1) << dh) & d) >> dh
  s2 = ((1 << dh) - 1) & d
  if verbose:
    log(f'Split - Splitting {size}-bits in half:', indent)
    log(f'{bitstr(s1, size>>1)} {bitstr(s2, size>>1)}', indent+1)
  return s1, s2


# join two bit clumps of equal size into a long bitstring
def join(d1, d2, size, verbose=False, indent=0):
  dh = size >> 1
  result = (d1 << dh) | d2
  if verbose:
    log(f'Join - Combining two {size>>1}-bit strings into one {size}-bit string:', indent)
    log(f'{bitstr(d1, size>>1)} {bitstr(d2, size>>1)} -> {bitstr(result, size)}', indent+1)
  return result
  

# Reduces 4 bits to 2 bits by matrix lookup
def s_lookup(d, matrix, verbose=False, indent=0):
  r = ((8 & d) >> 2) | (1 & d)        # p0 p3
  c = ((4 & d) >> 1) | ((2 & d) >> 1) # p1 p2
  result = matrix[r][c]
  if verbose:
    log(f'Lookup using marix:', indent)
    log(f'{matstr(matrix)}', indent+1)
    log(f'row = {bitstr(d, 4)} -> {bitstr(r, 2)} = {r}', indent)
    log(f'      ^  ^', indent)
    log(f'col = {bitstr(d, 4)} -> {bitstr(c, 2)} = {c}', indent)
    log(f'       ^^', indent)
    log(f'matrix[{r}][{c}] = {result} = {bitstr(result, 2)}', indent)
  return result
  

def s0(d, verbose=False, indent=0):
  matrix = [[1, 0, 3, 2],
            [3, 2, 1, 0],
            [0, 2, 1, 3],
            [3, 1, 3, 2]]
  if verbose:
    log('S0 - Downselecting from 4 bits to 2 bits using a table:', indent)
  return s_lookup(d, matrix, verbose, indent+1)


def s1(d, verbose=False, indent=0):
  matrix = [[0, 1, 2, 3],
            [2, 0, 1, 3],
            [3, 0, 1, 0],
            [2, 1, 0, 3]]
  if verbose:
    log('S1 - Downselecting from 4 bits to 2 bits using a table:', indent)
  return s_lookup(d, matrix, verbose, indent+1)


# Main encryption operation
def f(d, sk, verbose=False, indent=0):
  if verbose:
    log('f(K) - Main encryption function', indent)
  d1, d2 = split(d, 8, verbose, indent+1)
  exp = ep(d2, verbose, indent+1)
  fk = exp ^ sk
  if verbose:
    log(f'XOR - EP {bitstr(exp, 8)} ^ subkey {bitstr(sk, 8)} -> {bitstr(fk, 8)}', indent+1)
  fk1, fk2 = split(fk, 8, verbose, indent+1)
  fk1 = s0(fk1, verbose, indent+1)
  fk2 = s1(fk2, verbose, indent+1)
  pf = p4(join(fk1, fk2, 4, verbose, indent+1), verbose, indent+1)
  d1r = d1 ^ pf
  if verbose:
    log(f'XOR - {bitstr(d1, 4)} ^ {bitstr(pf, 4)} = {bitstr(d1r, 4)}', indent+1)
  result = join(d1r, d2, 8, verbose, indent+1)
  if verbose:
    log(f'Final result of f(K): {bitstr(result, 8)}', indent+1)
  return result


# Perform SDES encryption on message m using key k
def encrypt(m, k, verbose=False):
  if verbose:
    log(f'Encrypting message {bitstr(m, 8)} with key {bitstr(k, 10)} using SDES encryption:', 0)
  k1, k2 = gen_keys(k, verbose, 1)
  result = ip2(f(sw(f(ip(m, verbose, 1), k1, verbose, 1), 8, verbose, 1), k2, verbose, 1), verbose, 1)
  if verbose:
    log(f'Encrypted Ciphertext: {bitstr(result, 8)}', 0)
  return result

  
# Perform SDES decryption on ciphertext c using key k
def decrypt(c, k, verbose=False):
  if verbose:
    log(f'Decrypting ciphertext {bitstr(c, 8)} with key {bitstr(k, 10)} using SDES encryption:', 0)
  k1, k2 = gen_keys(k, verbose, 1)
  result = ip2(f(sw(f(ip(c, verbose, 1), k2, verbose, 1), 8, verbose, 1), k1, verbose, 1), verbose, 1)
  if verbose:
    log(f'Decrypted Plaintext: {bitstr(result, 8)}', 0)
  return result


if __name__ == '__main__':
  k = 0b1010000010
  print(f"Testing Keygen: Given key [{k:0>8b}] produces the folowing subkeys:")
  k1, k2 = gen_keys(k)
  print(f'  {k1:0>8b}')
  print(f'  {k2:0>8b}')
