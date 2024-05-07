import argparse

def main():
  parser = argparse.ArgumentParser(description='Import Checker')
  parser.add_argument('PKG', help='Module/package to verify')
  parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
  
  args = parser.parse_args()

  from dslog import Logger
  from verify_import import walk_modules

  logger = Logger.rich().prefix('[VERIFY IMPORT]').limit('DEBUG' if args.verbose else 'INFO')

  errored = False
  for pkg, e in walk_modules(args.PKG):
    if e is not None:
      logger(f"Error importing '{pkg}':", e, level='ERROR')
      errored = True
    else:
      logger(f"Imported '{pkg}'", level='DEBUG')
  if not errored:
    logger('No errors found')

if __name__ == '__main__':
  main()