
def print_separator():
  print('\n' + '=' * 80 + '\n')


def log(m, indent=0):
  ind = ('  ' * indent)
  indnl = f'\n{ind}'
  m = ind + indnl.join(m.split('\n'))
  print(m)
  

def bitstr(d, length):
  return f'{d:0>{length}b}'
  
  
def matstr(m):
  rowstrs = []
  for r in m:
    rowstrs += [' '.join([str(c) for c in r])]
  return '\n'.join(rowstrs)
  
  
def bytearray_to_str(ba):
  return ' '.join([f'{b:0>8b}' for b in ba])
  
  
def bytearray_to_4_bit_block_string(ba):
  return ' '.join(f'{(b & 0b11110000)>>4:0>4b} {b & 0b1111:0>4b}' for b in ba)
  
  
if __name__ == '__main__':
  print(bitstr(0b00000010, 4))
  
