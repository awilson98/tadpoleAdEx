from vpython import *
from generate_swim_data import generate_data

data = generate_data()
print(data)
HEAD_POS = [i[0]/3 for i in data]
TAIL_POS = [i[1] for i in data]

# make a tadpole thing, a sphere attached to a stick
ANGLE = 0
TAIL_CRD = [-2, 2]

scene = canvas(title='tadpole swim from data', width=500, height=500, center=vector(10, 0, 0), )
head = sphere(pos=vector(0, 0, 0), radius=1)
tail = cylinder(pos=vector(0, 0, 0), axis=vector(-5, 0, 0), radius=0.5, make_trail=True)

for i in range(len(data)):
    rate(5)
    head.pos.x = HEAD_POS[i]
    tail.pos.x = HEAD_POS[i]
    tail.axis.z = TAIL_CRD[TAIL_POS[i]]
    