"""
motor neuron to tadpole swim

a tadpole is a center (x) and it wiggles and the wiggle propels it forward
"""


DT = 1
SIMTIME = 100
ITERS = int(SIMTIME/DT)

ISI = 2 # interspike interval

# assume constant frequency of motor neurons



class Tadpole:
    forward_per_whip = 1

    def __init__(self, x, tail) -> None:
        self.x = x
        self.tail = tail
        self.data = []

    def move(self):
        self.x += self.forward_per_whip
        self.tail = (1 + self.tail) % 2 # tail goes from 0 and 1

    def log(self):
        self.data.append((self.x, self.tail))


def generate_data():
    tad = Tadpole(0, 0)

    for t in range(0, ITERS, ISI):
        tad.move()
        tad.log()

    return tad.data


