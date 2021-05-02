#!/usr/bin/env python3
import sys
import os

if __name__ == "__main__":
    pwd = os.getcwd()

    for dirpath, dirnames, fnames in os.walk(pwd):

        if "statcounter" not in dirpath:
            continue
        if "original" not in dirpath:
            continue

        for fname in fnames:
            fpath = os.path.join(dirpath, fname)
            o_fname = fname[-10:-6] + ".csv"
            o_fpath = os.path.join(dirpath[:-len("original")], "formatted", o_fname)
            with open(fpath, "r") as f, open(o_fpath, "w") as fout:
                i_colnames = f.readline().split(',')
                o_colnames = []

                for cn in i_colnames:
                    if "unknown" in cn.lower() or "other" in cn.lower():
                        continue
                    o_colnames.append(cn)

                fout.write(",".join(o_colnames) + "\n")

                for line in f:
                    i_colvalues = line.split(",")
                    o_colvalues = []
                    for i in range(len(i_colvalues)):
                        if "unknown" in i_colnames[i].lower() or "other" in i_colnames[i].lower():
                            continue
                        fmtval = i_colvalues[i]
                        if i > 0:
                            fmtval = '"%s"' % fmtval.replace(".",",")
                        o_colvalues.append(fmtval)
                    fout.write(",".join(o_colvalues) + "\n")
