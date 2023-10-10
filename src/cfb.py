
import sdes
from log_utils import log, bitstr, bytearray_to_4_bit_block_string


def bytearray_8_to_4(ba):
  ba4 = bytearray()
  for b in ba:
    b1, b2 = sdes.split(b, 8)
    ba4.append(b1)
    ba4.append(b2)
  return ba4
  

def bytearray_4_to_8(ba):
  ba8 = bytearray()
  if len(ba) % 2 != 0:
    raise Exception("Can only convert even-numbered 4-bit arrays into 8-bit arrays.")
  for i in range(0, len(ba), 2):
    ba8.append(sdes.join(ba[i], ba[i+1], 8))
  return ba8


def encrypt(ms, k, iv, verbose=False):
  if verbose:
    log(f'Encrypting message using SDES in CFB Mode:', 0)
    log(f'Message: {bytearray_to_4_bit_block_string(ms)}\nKey: {bitstr(k, 10)}\nIV: {bitstr(iv, 8)}', 1)
    log(f'[register] initialized to [IV]: {bitstr(iv, 8)}', 1)
  cs4_out = bytearray()
  ms4 = bytearray_8_to_4(ms)
  register = iv
  for m in ms4:
    o = sdes.encrypt(register, k)
    if verbose:
      log(f'Current plaintext chunk [m]: {bitstr(m, 4)}', 1)
      log(f'Using SDES to encrypt [register] {bitstr(register, 8)} with key {bitstr(k, 10)}: ciphertext: {bitstr(o, 8)}', 2)
    ol, _ = sdes.split(o, 8)
    c = ol ^ m
    cs4_out.append(c)
    r1, r2 = sdes.split(register, 8)
    register = sdes.join(r2, c, 8)
    if verbose:
      log(f'Take first 4 bits [ol] and discard the rest: {bitstr(ol, 4)}', 2)
      log(f'XOR: [m] {bitstr(m, 4)} ^ [ol] {bitstr(ol, 4)} = [c] {bitstr(c, 4)}', 2)
      log(f'Shift [register] 4-bits to the left and replace second half with new cipher chunk: {bitstr(register, 8)}', 2)
  result = bytearray_4_to_8(cs4_out)
  if verbose:
    log(f'Final encrypted ciphertext: {bytearray_to_4_bit_block_string(result)}', 1)
  return result
  

def decrypt(cs, k, iv, verbose=False):
  if verbose:
    log(f'Decrypting message using SDES in CFB Mode:', 0)
    log(f'Ciphertext: {bytearray_to_4_bit_block_string(cs)}\nKey: {bitstr(k, 10)}\nIV: {bitstr(iv, 8)}', 1)
    log(f'[register] initialized to [IV]: {bitstr(iv, 8)}', 1)
  ms4_out = bytearray()
  cs4 = bytearray_8_to_4(cs)
  register = iv
  for c in cs4:
    o = sdes.encrypt(register, k)
    if verbose:
      log(f'Current ciphertext chunk [c]: {bitstr(c, 4)}', 1)
      log(f'Using SDES to encrypt [register] {bitstr(register, 8)} with key {bitstr(k, 10)}: plaintext: {bitstr(o, 8)}', 2)
    ol, _ = sdes.split(o, 8)
    m = ol ^ c
    ms4_out.append(m)
    r1, r2 = sdes.split(register, 8)
    register = sdes.join(r2, c, 8)
    if verbose:
      log(f'Take first 4 bits [ol] and discard the rest: {bitstr(ol, 4)}', 2)
      log(f'XOR: [c] {bitstr(c, 4)} ^ [ol] {bitstr(ol, 4)} = [m] {bitstr(m, 4)}', 2)
      log(f'Shift [register] 4-bits to the left and replace second half with current cipher chunk: {bitstr(register, 8)}', 2)
  result = bytearray_4_to_8(ms4_out)
  if verbose:
    log(f'Final decrypted message: {bytearray_to_4_bit_block_string(result)}', 1)
  return result
