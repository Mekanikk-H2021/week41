from vpython import *

G = 6.67e-17 # N km^2 kg^-2   https://no.wikipedia.org/wiki/Gravitasjonskonstanten

origo = vec(0, 0, 0)
startpos_sonde = 10e6 * vec(0.77, 0.65, 0)           # km
startfart_sonde = (origo - startpos_sonde).hat * 10  # km/s
startfart_jupiter = vec(13, 0, 0)                    # km/s

# animasjonsobjekter
jupiter = sphere(pos=origo, vel=startfart_jupiter, radius=70e4, color=color.red, texture=textures.wood_old)
sonde = sphere(pos=startpos_sonde, vel=startfart_sonde, radius=20, make_trail=True)

jupiter.m = 1.9e27 # kg
jupiter.a = vec(0, 0, 0)

# grafer
avstand_plot = graph(fast=False, title="Avstand mellom jupiter og sonden.")
avstand_graf = gcurve()
fart_plot = graph(fast=False, title="Farten til sonden")
fart_graf = gcurve()

# tidsbetingelser
t = 0
dt = 20
tmax = 200000

# Euler Cromer
def update_position(dt, *objects):
    """
    Funksjon som utfører euler cromers metode på objektene som sendes inn i funksjonen

    Parametre:
        dt: float
            En skalar som definerer tidssteget som brukes i hver oppdatering.
    Argumenter:
        *objects: vpython objekt
            Et objekt fra vpython biblioteket. I dette tilfellet er det objektene som skal oppdatere sin posisjon og hastighet.
            NB: objektene må ha definert en akselerasjon på forhånd som:

            obj.a = vpython.vector --- altså et vektor objekt.

            Er du usikker på hvordan å bruke *args (argumenter) se python dokumentasjonen her: https://docs.python.org/3.4/tutorial/controlflow.html#keyword-arguments
    """
    for obj in objects:
        obj.vel = obj.vel + obj.a * dt
        obj.pos = obj.pos + obj.vel * dt

# Oppdaterings loop
while t < tmax:

    # posisjonsvektoren fra jupiter til sonden
    r = jupiter.pos - sonde.pos

    # Newtons gravitasjonslov: https://no.wikipedia.org/wiki/Newtons_gravitasjonslov
    sonde.a = (G * jupiter.m) / r.mag2 * r.hat

    # euler cromer
    update_position(dt, sonde, jupiter)

    # plot
    avstand_graf.plot(t, r.mag)
    fart_graf.plot(t, sonde.vel.mag)

    t += dt

    rate(60*4)
    