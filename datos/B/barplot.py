import os

import matplotlib
import matplotlib.pyplot as plt

NROW = 2

if __name__ == "__main__":
    sfolder = os.path.realpath(__file__)[0:-len(__file__)]
    for (root,dirs,files) in os.walk(sfolder):
        if root == sfolder:
            continue
        rownamespath = os.path.join(root, "rownames")
        metricname = root[len(sfolder):]
        colnames = []
        with open(rownamespath, "r") as rnf:
            for line in rnf:
                colnames.append(line.replace('\n',''))


        i = 1
        for f in files:
            if f == "rownames":
                continue

            filepath = os.path.join(root, f)
            year = f[:-len(".csv")]
            vals = []

            fig, axes = plt.subplots()

            with open(filepath, "r") as of:
                for line in of:
                    l = line.replace(',','.').replace('\n','')
                    vals.append(float(l))
            axes.bar(colnames, vals)
            axes.set_title(year)

            outpath = os.path.join(root, year)
            matplotlib.pyplot.savefig(outpath)

            i += 1

