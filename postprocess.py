from utils import restore
import argparse
import re

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='DNT Postprocess script')
    
    parser.add_argument('dnt_src', type=str,
                        help='dnt source file')
    parser.add_argument('schema', type=str,
                        help="schema: del or sub")
    parser.add_argument('dnt_ini', type=str,
                        help="dnt conf file")
    parser.add_argument('output', type=str,
                        help="output path")

    args = parser.parse_args()
    print(args)
    schema = args.schema
    restore(args.dnt_src, args.schema)
    