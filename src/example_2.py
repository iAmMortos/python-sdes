import cbc
from log_utils import bytearray_to_str


def main():
  print('Example 2: SDES encryption in CBC mode.\n')
  ms = bytearray([0b00000001, 0b00100011])
  iv = 0b10101010
  k = 0b0111111101
  cs = cbc.encrypt(ms, k, iv, verbose=True)
  print('\n')
  ms2 = cbc.decrypt(cs, k, iv, verbose=True)
  
  print('\n\nSummary:')
  print(f'  Original Message:  {bytearray_to_str(ms)}')
  print(f'  Key:               {k:0>10b}')
  print(f'  Init Vector:       {iv:0>8b}')
  print(f'  Encrypted Message: {bytearray_to_str(cs)}')
  print(f'  Decrypted Message: {bytearray_to_str(ms2)}')
  
  
if __name__ == '__main__':
  main()

