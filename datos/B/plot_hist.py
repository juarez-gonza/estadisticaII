import os
import matplotlib.pyplot as plt
import matplotlib

BNAME_IDX = 0
SCORE_IDX = -2

cvss_browser = {
    "firefox": {
        "scores": [],
        "color": "b",
        },
    "chrome": {
        "scores": [],
        "color": "g",
        },
    "safari": {
        "scores": [],
        "color": "r",
        },
}

if __name__ == "__main__":
    spath = os.path.realpath(__file__)[:-len(__file__)]
    fmt_path = os.path.realpath(os.path.join(spath, "formatted"))
    first = 1
    for (root, dirs, files) in os.walk(fmt_path):
        for f in files:
            year = f[:-len(".csv")]
            fpath = os.path.join(root, f)
            with open(fpath, "r") as of:
                of.readline()   # read header
                for line in of:
                    line = line.replace('\n', '')
                    fields = line.split("\"")
                    score = float(fields[SCORE_IDX].replace(",","."))
                    fields = line.split(",")
                    bname = fields[BNAME_IDX].lower()
                    cvss_browser[bname]["scores"].append(score)
            print("==========",year,"==========")
            for bname in cvss_browser:
                plt.hist(cvss_browser[bname]["scores"], color=cvss_browser[bname]["color"], alpha=0.5, bins=10, label=bname)
                cvss_browser[bname]["scores"] = []
            plt.gca().set(title=("Histograma de CVSS Score en Firefox, Chrome y Safari %s" % year))
            if first:
                first &= 0
                plt.ylabel("CVSS Score")
                plt.xlim(0, 10)
                plt.legend()
            matplotlib.pyplot.savefig(year)
