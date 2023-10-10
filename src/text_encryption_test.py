
import cbc
import cfb
import binascii

def main():
  running = True
  key = 0b1100101011
  iv = 0b11100111
  with open('rsc/stairwar.txt') as f:
    stairwar = f.read()
  swb = bytearray()
  swb.extend(stairwar.encode())
  print(f'Sample Text:\n  {stairwar}')
  swc_cbc = cbc.encrypt(swb, key, iv)
  swc_cfb = cfb.encrypt(swb, key, iv)
  print(f'CBC ciphertext:\n  {binascii.hexlify(swc_cbc)}')
  print(f'CFB ciphertext:\n  {binascii.hexlify(swc_cfb)}')
  print(f'CBC plaintext:\n  {cbc.decrypt(swc_cbc, key, iv).decode("utf-8")}')
  print(f'CFB plaintext:\n  {cfb.decrypt(swc_cfb, key, iv).decode("utf-8")}')
  print('*' * 80)
  while running:
    plaintext = input("Enter a string to encrypt (or just return to quit): ")
    if not plaintext:
      print("Bye!")
      running = False
    else:
      message_bytes = bytearray()
      message_bytes.extend(plaintext.encode())

      cbc_c = cbc.encrypt(message_bytes, key, iv)
      cfb_c = cfb.encrypt(message_bytes, key, iv)

      print("Encrypted:")
      print(f'  CBC ciphertext: {binascii.hexlify(cbc_c)}')
      print(f'  CFB ciphertext: {binascii.hexlify(cfb_c)}')

      cbc_m = cbc.decrypt(cbc_c, key, iv)
      cfb_m = cfb.decrypt(cfb_c, key, iv)

      print("Decrypted:")
      print(f'  CBC plaintext: {cbc_m.decode("utf-8")}')
      print(f'  CFB plaintext: {cfb_m.decode("utf-8")}')


if __name__ == '__main__':
  main()
