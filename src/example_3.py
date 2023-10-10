
import cfb
from log_utils import bytearray_to_4_bit_block_string


def main():
  print('Example 3 - SDES Encryption in CFB Mode\n')
  ms = bytearray([0b0001_0010, 0b0011_0100])
  iv = 0b1010_1011
  k = 0b0111111101
  cs = cfb.encrypt(ms, k, iv, verbose=True)
  print('\n')
  ms2 = cfb.decrypt(cs, k, iv, verbose=True)
  
  print('\n\nSummary')
  print(f'  Original message:  {bytearray_to_4_bit_block_string(ms)}')
  print(f'  Key:               {k:0>10b}')
  ivstr = f'{iv:0>8b}'
  print(f'  Init Vector:       {ivstr[:4]} {ivstr[4:]}')
  print(f'  Encrypted message: {bytearray_to_4_bit_block_string(cs)}')
  print(f'  Decrypted message: {bytearray_to_4_bit_block_string(ms2)}')
  
  
if __name__ == '__main__':
  main()

