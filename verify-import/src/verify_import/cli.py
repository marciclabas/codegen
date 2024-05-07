import argparse

def main():
  parser = argparse.ArgumentParser(description='Import Checker')
  parser.add_argument('PKG', help='Module/package to verify')
  parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')

  args = parser.parse_args()
  from verify_import import walk_modules
  errored = False
  for pkg, e in walk_modules(args.PKG):
    if e is not None:
      print(f"ERROR importing '{pkg}':", e)
      errored = True
    elif args.verbose:
      print(f"Imported '{pkg}'")
  if not errored:
    print('No errors found')

if __name__ == '__main__':
  main()