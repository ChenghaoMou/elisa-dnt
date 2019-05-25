# encoding: utf-8
# Created by chenghaomou at 2019-05-22
import itertools
import regex as re
import os

rules = {
    "email": r"(?i)([\w!#$%&'*+/=?^`{|}~-]+(?:\.[\w!#$%&'*+/=?^`{|}~-]+)*@(?:[a-z\d](?:[a-z\d-]*[a-z\d])?\.)+[a-z\d](?:[a-z\d-]*[a-z\d])?)",
    "url": r"((?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx)\b/?(?!@))))",
    "hashtag": r"((#\p{N}*[\p{L}_'-]+[\p{L}\p{N}_+-]*)+)",
    "mention": r"((@[\w\-]+)+)",
    "time": r"(?i)(@((([01]?\d|2[0-3]):([0-5]\d)|24:00) ?(pm|am|p\.m|a\.m)?))",
    "html": r"((<\/?(a|img|div).*?>)+)",
    "twitter": r"(pic\.twitter\.com/[a-zA-Z0-9]+)",
}

options = {
    "colors": {
        "email": "background-image:linear-gradient(90deg, #a2fafc, #11a9fc);",
        "url": "background-image:linear-gradient(90deg, #fcd766, #fc7f00);",
        "html": "background-image:linear-gradient(90deg, #aa9cfc, #11a9fc);",
        "mention": "background-image:linear-gradient(90deg, #abfca5, #fce43d);",
        "time": "background-image:linear-gradient(90deg, #abfca5, #fce43d);",
        "hashtag": "background-image:linear-gradient(90deg, #aa9cfc, #fc9ce7);",
        "comb": "background-image:linear-gradient(90deg, #a2fafc, #fce43d);",
    },
    "categories": ["email", "url", "html", "mention", "time", "hashtag", "comb"],
}

RULES = {key: re.compile(value) for key, value in rules.items()}
RULES["comb"] = re.compile("(" + "|".join(rules.values()) + ")+")
MARKERS = [chr(x) for x in range(0x4DC0, 0x4DFF)]


def find(string: str) -> list:

    matches = itertools.chain(*[exp.finditer(string) for exp in RULES.values()])
    matches = [match for match in sorted(matches, key=lambda m: (m.start(0), -m.end(0)))]
    filtered_matches = []

    for i, match in enumerate(matches):
        if i > 0 and filtered_matches[-1].start(0) <= match.start(0) < filtered_matches[-1].end(0):
            continue
        else:
            filtered_matches.append(match)

    return filtered_matches


def mark(string: str, matches: list, scheme: str = "marker") -> tuple:
    if scheme == "marker":

        modification = []

        for i, match in enumerate(matches):
            start, end = match.span(0)
            text = string[start:end]
            modification.append(text)

        for key, value in zip(MARKERS, modification):
            string = string.replace(value, f" {key} ")

        return string, modification, None

    elif scheme == "delete":
        lead = False
        modification = []
        segments = []
        remain = string
        for i, match in enumerate(matches):
            start, end = match.span(0)
            if start == 0:
                lead = True
            text = string[start:end]
            modification.append(text)
            if remain:
                segment, remain = remain.split(text, maxsplit=1)
            if segment:
                segments.append(segment)

        if remain:
            segments.append(remain)

        restore = []
        i, j = 0, 0
        curr = 0
        while i < len(modification) and j < len(segments):
            if lead and (i == 0 or curr % 2 == 0):
                restore.append(modification[i])
                i += 1
                curr += 1
            elif not lead and (j == 0 or curr % 2 == 0):
                restore.append(segments[j])
                j += 1
                curr += 1
            elif not lead and curr % 2 == 1:
                restore.append(modification[i])
                i += 1
                curr += 1
            elif lead and curr % 2 == 1:
                restore.append(segments[j])
                j += 1
                curr += 1

        while i < len(modification):
            restore.append(modification[i])
            i += 1
            curr += 1
        while j < len(segments):
            restore.append(segments[j])
            j += 1
            curr += 1

        try:
            assert "".join(restore) == string, "".join(restore)
        except AssertionError as ae:
            print(string)
            print(matches)
            print(segments)
            print(modification)
            print(restore)
            print(ae)
            print()
            

        return segments, modification, lead


def visual(string: str, matches: list, output: str, options, lan: str = None) -> None:
    def colorize(match, text):
        cls = [key for key, value in RULES.items() if value == match.re][0]
        if cls in options["categories"]:
            if cls != "html":
                return f"""<span class="{cls}">{text}</span>"""
            else:
                text = text.replace("<", "&lt;")
                text = text.replace(">", "&gt;")
                return f"""<span class="{cls}">{text}</span>"""
        else:
            return text

    res = string
    for match in matches:
        start, end = match.span(0)
        text = string[start:end]
        res = res.replace(text, colorize(match, text))

    with open(output, "a+") as o:
        o.write(f"<p>{lan}: {res}</p>" + "\n")


if __name__ == "__main__":

    lang = ["hau", "tgl", "tur", "urd", "swa"]

    # output = "visual.html"

    # print(find("upitia #FursaAsilia @4:00pm. Hakika tutajifunza meng"))

    # with open(output, "w") as o:

    #     style = """
    #     <head>
    #         <meta charset="utf-8">
    #     </head>
    #     <style>
    #         @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro&display=swap&subset=cyrillic,cyrillic-ext,greek,greek-ext,latin-ext,vietnamese');
    #         body{
    #             font-family: 'Source Sans Pro', arial, sans-serif;
    #             font-weight: 300;
    #         }
    #     </style>
    #     """
    #     style += (
    #         f"<style>"
    #         + "".join(""".{0}{{{1}}}""".format(key, value) for key, value in options["colors"].items())
    #         + "</style>\n"
    #     )

    #     o.write(style)

    # for lan in lang:
    #     path1 = "/Users/chenghaomou/Code/Code-ProjectsPyCharm/ElisaTest/elisa-data/{0}-en/elisa.train_1.{0}".format(lan)
    #     path2 = "/Users/chenghaomou/Code/Code-ProjectsPyCharm/ElisaTest/elisa-data/{0}-en/elisa.train_1.en".format(lan)

    #     with open(path1) as source, open(path2) as target:
    #         for src, tgt in zip(source.read().split("\n"), target.read().split("\n")):
    #             matches = find(src)
    #             if matches:
    #                 after, mod, lead = mark(line, matches, scheme="delete")
    #                 visual(line, matches, output, options, lan)

    #                 matches = find(tgt)
    #                 after, mod, lead = mark(line, matches, scheme="delete")
    #                 visual(line, matches, output, options, lan)
    
    for lan in lang:
    
        path = "/Users/chenghaomou/Code/Code-ProjectsPyCharm/ElisaTest/elisa-data/{0}-en/elisa.train_1.{0}".format(lan)

        with open(path) as source, open(path + ".dnt", "w") as o_source, open(path + ".dnt.ini", "w") as o_source_ini:
            for src  in source.read().split("\n"):
                src_matches = find(src)
                src_after, src_mod, src_lead = mark(src, src_matches, scheme="delete")
                for seg in src_after:
                    o_source.write(seg + "\n")
                
                if src_matches:
                    o_source_ini.write(("YL" if src_lead and len(src_after) >= len(src_mod) else "YS" if src_lead else \
                        "NL" if not src_lead and len(src_after) > len(src_mod) else "NS"
                    ) + "\t" + "\t".join(src_mod) + "\n")
                else:
                    o_source_ini.write("IGNORE\n")
        
        with open(path + ".dnt.restore", "w") as o, open(path + ".dnt") as i_source, open(path + ".dnt.ini") as i_source_ini:
            translations = i_source.read().split('\n')
            instructions = i_source_ini.read().split('\n')

            i = 0
            j = 0
            placeholder = []
            while i < len(instructions) and j < len(translations):
                lead, *tokens = instructions[i].split('\t')
                if lead == "IGNORE":
                    o.write(translations[j] + "\n")
                    j += 1
                    i += 1
                    continue
                if lead == "YL":
                    for token in tokens:
                        placeholder.append(token)
                        placeholder.append(translations[j])
                        j += 1
                elif lead == "YS":
                    for x, token in enumerate(tokens):
                        placeholder.append(token)
                        if x < len(tokens) - 1: 
                            placeholder.append(translations[j])
                            j += 1
                if lead == "NL":
                    for token in tokens:
                        placeholder.append(translations[j])
                        placeholder.append(token)
                        j += 1
                    placeholder.append(translations[j])
                    j += 1
                elif lead == "NS":
                    for token in tokens:
                        placeholder.append(translations[j])
                        placeholder.append(token)
                        j += 1
                o.write("".join(placeholder) + "\n")
                placeholder = []
                i += 1

        with open(path) as orign, open(path + ".dnt.restore") as restore:
            for line1, line2 in zip(orign.read().split('\n'), restore.read().split('\n')):
                assert line1 == line2, line1 + '===\t===' + line2





