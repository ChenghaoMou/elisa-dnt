# encoding: utf-8
# Created by chenghaomou at 2019-05-23

from extract import find

if __name__ == '__main__':
    lang = ['hau', 'tgl', 'urd', 'tur', 'swa']
    for lan in lang:
        path = "/Users/chenghaomou/Code/Code-ProjectsPyCharm/ElisaTest/elisa-data/{0}-en/elisa.test.{0}".format(lan)
        count = 0
        easy = 0

        with open(path) as i:
            for line in i.read().split('\n'):
                matches = find(line)
                for match in matches:
                    if match.start(0) == 0 or match.end(0) == len(line):
                        # print(line, line[match.span(0)[0]:match.span(0)[1]])
                        easy += 1
                    count += 1

        print(f"{lan} {count:<5} {easy:<5} {easy/count if count > 0 else 0:<5.3f}")


