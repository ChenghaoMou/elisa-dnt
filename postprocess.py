from utils import restore
import argparse
import re

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='DNT Postprocess script')
    
    parser.add_argument('dnt_src', type=str,
                        help='dnt source file')
    parser.add_argument('dnt_ini', type=str,
                        help="dnt conf file")
    parser.add_argument('output', type=str,
                        help="output path")
    parser.add_argument('scheme', type=str,
                        help="scheme: del or sub")

    args = parser.parse_args()
    print(args)
    scheme = args.scheme
    restore(args.dnt_src, args.dnt_ini, args.output, args.scheme)
    