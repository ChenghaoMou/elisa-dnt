from utils import find, split, visual, options, mark
import argparse
import re


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='DNT Preprocess script')
    
    parser.add_argument('src', type=str,
                        help='source file')
    parser.add_argument('src_output', type=str,
                        help='source output file')
    parser.add_argument('ini_output', type=str,
                        help='source ini file')                
    parser.add_argument('--tgt', type=str, default="",
                        help='target file')
    parser.add_argument('--cross', type=bool, default=False,
                        help='whether use reference taregt file for regex extraction')
    parser.add_argument('schema', type=str,
                        help="schema: del or sub")
    parser.add_argument('--visual', nargs=1,
                        help="html file path, visualize the regex on input dataset")

    args = parser.parse_args()
    print(args)
    
    if args.visual:
        with open(args.visual[0], "w") as o:
            o.write("""
            <link href="https://fonts.googleapis.com/css?family=Source+Sans+Pro&display=swap&subset=cyrillic,cyrillic-ext,greek,greek-ext,latin-ext,vietnamese" rel="stylesheet">
            <style>
                html,body{
                    font-family: 'Source Sans Pro', sans-serif;
                }
                """+"\n".join([".%s {%s}"%(key, value) for key, value in options["colors"].items()])+"""
            </style>
            """)

    path = args.src
    
    split(args.src, args.src_output, args.ini_output, schema=args.schema, ref=args.tgt if args.schema == "sub" and args.cross else "")

    if args.visual:
        if args.tgt == "":
            for line in open(path):
                matches = find(line)
                if matches:
                    res = visual(line, matches, options)
                    with open(args.visual[0], "a+") as o:
                        o.write(f"<p>{res}</p>" + "\n")
        else:
            src_lines, tgt_lines = open(path).readlines(), open(args.tgt).readlines()
            assert len(src_lines) == len(tgt_lines)
            for src_line, tgt_line in zip(src_lines, tgt_lines):
                src_matches = find(src_line)
                tgt_matches = find(tgt_line)

                src_matches_text = [src_line[m.start(0):m.end(0)] for m in src_matches]
                tgt_matches_text = [tgt_line[m.start(0):m.end(0)] for m in tgt_matches]

                x_matches = list(set(src_matches_text).intersection(set(tgt_matches_text)))

                x_src_matches = [m for m in src_matches if src_line[m.start(0):m.end(0)] in x_matches] if args.cross else src_matches
                x_tgt_matches = [m for m in tgt_matches if tgt_line[m.start(0):m.end(0)] in x_matches] if args.cross else tgt_matches

                if x_matches:
                    res = visual(src_line, x_src_matches, options)
                    with open(args.visual[0], "a+") as o:
                        o.write(f"<p>{res}</p>" + "\n")
                    
                    res = visual(tgt_line, x_tgt_matches, options)
                    with open(args.visual[0], "a+") as o:
                        o.write(f"<p>{res}</p>" + "\n")
