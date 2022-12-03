import sys

def check_arg(*args):
  for elem in args:
    if elem in sys.argv:
      return True
  return False

def arg_pos(*args):
  for i, elem in enumerate(args):
    if elem in sys.argv:
      return sys.argv.index(elem)
  return None