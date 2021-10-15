import numpy as np
import matplotlib.pyplot as plt

# Gravitasjonskonstanten
G = 6.67e-11

# Startposisjonen til Jupiter
r_j = np.array([0, 0])

# Startfarten til Jupiter
v_j = np.array([13, 0]) * 1e3 # m/s

# startposisjonen til sonden
r_s = np.array([.77, .64]) * 1e9 # m

# Startfarten til sonden, definert å være 10 km/s inn mot Jupiter
v_s = (r_j - r_s) / np.linalg.norm(r_j - r_s) * 10e3

M_j = 1.9e27 # kg

# Tidsbetingelser
t = 0
dt = 1000
tmax = 100000

def euler_cromer(dt, r, v, a):
    """
    Euler cromers metode.

    Argumenter:
        dt: float or int
            Tidssteg
        r: array_like
            Posisjonsvektor
        v: array_like
            Hastighetsvektor
        a: array_like
            Akselerasjonsvektor
    """
    v = v + a * dt
    r = r + v * dt
    return v, r

while t < tmax:
    # Linja under "tømmer" plottet for hver iterering, prøv å kommenter denne ut å se hva som skjer.
    # plt.clf()

    # Posisjonsvektoren for sonden i forhold til Jupiter
    r = r_s - r_j
    r_hat = (r) / np.linalg.norm(r)

    # Akselerasjonen til sonden.
    a_s = -G * M_j / np.linalg.norm(r)**2 * r_hat

    # euler cromer
    v_s, r_s = euler_cromer(dt, r_s, v_s, a_s)
    v_j, r_j = euler_cromer(dt, r_j, v_j, 0)

    t += dt
    
    plt.scatter(r_s[0], r_s[1], c="green", s=10)
    plt.scatter(r_j[0], r_j[1], c="red")

    # Setter størrelsen på plottet
    plt.xlim(0, 1.2e9)
    plt.ylim(-1.25e9, 0.6e9)
    plt.title("Jupiter som gravitasjonsslynge for en sonde.")
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    # Denne omgjør plottet til en animasjon som oppdateres med 0.01 sekunders mellomrom
    plt.pause(0.01)
plt.show()