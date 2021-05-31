import matplotlib
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    matplotlib.use("cairo")
    plt.title("Cantidad de CVEs v/s Market Share")
    plt.xlabel("Market Share (%)")
    plt.ylabel("Cantidad de CVEs")

    with open("data.csv", "r") as f:
        f.readline() # read header
        mshare_av = []
        cve_count = []
        for line in f:
            m, c = line.split(",")
            mshare_av.append(float(m))
            cve_count.append(float(c))

    mshare_av = np.array(mshare_av)
    cve_count = np.array(cve_count)
    plt.scatter(mshare_av, cve_count)

    x = np.linspace(0, 70, 10**3)

# para conseguir solo el grafico de dispersion:
# comentar desde aquí
    plt.plot(
        x,
        (85.4200035526783)*(1)+(2.54449292940217)*(x)+(-0.164225027687621)*(x**2)+(0.00248609032503583)*(x**3),
        label='grado 3'
        )
    plt.plot(
        x,
        (136.403953380621)*(1)+(-11.8197275094572)*(x)+(0.895133553261076)*(x**2)+(-0.0224633236912837)*(x**3)+(0.000183207577586164)*(x**4),
        label='grado 4'
        )
    plt.plot(
        x,
        (124.123550355434)*(1)+(-7.93528531672200)*(x)+(0.533196897675225)*(x**2)+(-0.00907234358851383)*(x**3)+(-2.96059363105172e-5)*(x**4)+(1.21682284054403e-6)*(x**5),
        label='grado 5'
        )

    plt.legend()
# hasta aquí

    matplotlib.pyplot.savefig('graph')
