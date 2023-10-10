
import sdes
from log_utils import log, bitstr, bytearray_to_str


def encrypt(bs, k, iv, verbose=False):
  ba = bytearray()
  last = iv
  if verbose:
    log(f'Encrypting message using SDES in CBC Mode:', 0)
    log(f'Message: {bytearray_to_str(bs)}\nKey: {bitstr(k, 10)}\nIV: {bitstr(iv, 8)}', 1)
    log(f'[last] initialized to [IV]: {bitstr(iv, 8)}', 1)
  for b in bs:
    d = b ^ last
    c = sdes.encrypt(d, k)
    ba.append(c)
    last = c
    if verbose:
      log(f'Current plaintext chunk [b]: {bitstr(b, 8)}', 1)
      log(f'XOR: [last] {bitstr(last, 8)} ^ [b] {bitstr(b, 8)} = [d] {bitstr(d, 8)}', 2)
      log(f'Using SDES to encrypt [d] {bitstr(d, 8)} with key {bitstr(k, 10)}: ciphertext: {bitstr(c, 8)}', 2)
      log(f'[last] set to new ciphertext: {bitstr(c, 8)}', 2)
  if verbose:
    log(f'Final encrypted ciphertext: {bytearray_to_str(ba)}', 1)
  return ba

    
def decrypt(bs, k, iv, verbose=False):
  ba = bytearray()
  last = iv
  if verbose:
    log(f'Decrypting ciphertext using SDES in CBC Mode:', 0)
    log(f'Ciphertext: {bytearray_to_str(bs)}\nKey: {bitstr(k, 10)}\nIV: {bitstr(iv, 8)}', 1)
    log(f'[last] initialized to [IV]: {bitstr(iv, 8)}', 1)
  for b in bs:
    m = sdes.decrypt(b, k)
    d = m ^ last
    ba.append(d)
    last = b
    if verbose:
      log(f'Current ciphertext chunk [b]: {bitstr(b, 8)}', 1)
      log(f'Using SDES to decrypt [b] {bitstr(b, 8)} with key {bitstr(k, 10)}: message: {bitstr(m, 8)}', 2)
      log(f'XOR: [last] {bitstr(last, 8)} ^ [m] {bitstr(m, 8)} = [d] {bitstr(d, 8)}', 2)
      log(f'[last] set to current ciphertext chunk: {bitstr(b, 8)}', 2)
  if verbose:
    log(f'Final decrypted message: {bytearray_to_str(ba)}', 1)
  return ba

