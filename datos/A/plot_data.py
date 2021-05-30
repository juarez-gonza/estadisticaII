import matplotlib
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    matplotlib.use("pdf")
    with open("data.csv", "r") as f:
        f.readline() # read header
        mshare_av = []
        cve_count = []
        for line in f:
            m, c = line.split(",")
            mshare_av.append(m)
            cve_count.append(c)

        mshare_av = np.array(mshare_av)
        cve_count = np.array(cve_count)
        #plt.plot(mshare_av, cve_count)
        plt.plot([1, 2], [2, 1])
        matplotlib.pyplot.savefig('graph')
