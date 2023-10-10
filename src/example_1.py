import sdes


def main():
  print('Example 1: Simple DES Implementation\n')
  m = 0b10010111
  k = 0b1010000010
  c2 = sdes.encrypt(m, k, verbose=True)
  print('\n')
  m2 = sdes.decrypt(c2, k, verbose=True)
  print('\n')
  print('Summary:')
  print(f'  Original message:  {m:0>8b}')
  print(f'  Key:               {k:0>10b}')
  print(f'  Encrypted message: {c2:0>8b}')
  print(f'  Decrypted message: {m2:0>8b}')


if __name__ == '__main__':
  main()
  
