"""
Create a simple biophysical model of a tadpole swimming (no need to model fluid dynamics).
Ideally, the model should be able to reproduce the following behaviors:
    - swimming
    - struggling
    - flickering

Idea is to do this using segmented body parts, each with their own neural oscillator.
This is similar to a central pattern generator (CPG) model.

To start with, I will use a simple 2-segment model, where there are 2 tail segments.
The head segment will be fixed in place.

Actually instead of modelling segments and doing rigid body dynamics, I can just model
the whole tail like a string oscillating in a sine wave.

swimming is when activity flows from head to tail
struggling is when activity flows from tail to head
flickering is when only a small end of the tail is active

I believe that a harmonic oscillator is a good model for this. I can discretize the
oscillator into segments and give a phase offset to each segment.

Can represent activity by this phase.

How to represent a swimming motion mathematically?
perhaps standard sine wave motion?

wait but how is this biophysical? I need to model the CPG activity.
Do I need segments after all?

And how to represent activity? I can get data on spikes from certain neurons
along the tail -- how to translate this into activity?

essentially the problem is that if I model the tail as standing wave, 
then there are points that have zero amplitude and some have max.

Perhaps the simplest case would be to have N points on the tail,
each point is a harmonic oscillator, and the phase of each oscillator
is determined by the phase of the oscillator before it.
"""
import numpy as np
import matplotlib.pyplot as plt

# animation
from matplotlib.animation import FuncAnimation


class Model:
    def __init__(self, num_segments=5):
        self.num_segments = num_segments
        self.segment_length = 1.0 / num_segments
        # self.phase = np.zeros(num_segments)
        self.phase_offset = np.zeros(num_segments)
        self.amplitude = np.zeros(num_segments)
        self.frequency = np.zeros(num_segments)
        self.dt = 0.1
        self.alpha = 0.05

    def update(self):
        """
        update the phase offset of each segment, depending on the phase offset 
        of the previous segment(?). Don't move the first segment
        """
        for i in range(self.num_segments):
            if i != 0:
                self.phase_offset[i] += self.frequency[i] * self.dt 


    def get_segment_positions(self):
        """
        get the position of each segment.
        """
        x = np.linspace(0, 1, self.num_segments)
        y = self.amplitude * np.sin(self.phase_offset)
        return x, y


    def print_phase_offset(self):
        print(self.phase_offset)


    def print_segment_positions(self):
        x, y = self.get_segment_positions()
        print(y)
 

    def draw_tadpole(self):
        """
        draw the tadpole
        with a fixed head and a tail that oscillates
        the head as a circle at the origin

        label activity of each segment as its phase
        """

        fig, ax = plt.subplots()
        ax.set_ylim(-1.1, 1.1)
        ax.set_xlim(-0.1, 1.1)
        x, y = model.get_segment_positions()

        line, = ax.plot(x, y, 'ko-')
        ax.plot(0, 0, 'o')
        plt.show()

    def set_name(self, name):
        self.name = name


def animate_tadpole():

    model = Model(num_segments=25)
    # make amplitudes linearly increasing from head to tail
    model.amplitude = np.linspace(0, 0.3, model.num_segments)
    # keep frequency constant
    model.frequency = np.ones(model.num_segments)
    # initialize phase offset to be a sine wave
    model.phase_offset = np.sin(np.linspace(0, 2*np.pi, model.num_segments))

    model.alpha = 0.1
    
    # draw tadpole as well as phase offset of each segment

    fig, ax = plt.subplots()
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(-0.1, 1.1)
    x, y = model.get_segment_positions()

    line, = ax.plot(x, y, 'ko-')
    ax.plot(0, 0, 'o')
    
 
    def animate(i):
        model.update()
        x, y = model.get_segment_positions()
        line.set_data(x, y)
        return line,

    anim = FuncAnimation(fig, animate, frames=200, interval=10, blit=True)
    plt.show()

    # save animation 
    # anim.save('tadpole.gif', writer='imagemagick', fps=30)



# for different parameters I think I can get
# swimming, struggling, flickering


def tadpole_swimming():
    """
    set up a tadpole model does head-to-tail swimming
    """
    model = Model(num_segments=25)
    model.set_name("swimming")
    # make amplitudes linearly increasing from head to tail
    model.amplitude = np.linspace(0, 0.3, model.num_segments)
    # keep frequency constant
    model.frequency = np.ones(model.num_segments)
    # initialize phase offset to be a sine wave
    model.phase_offset = np.sin(np.linspace(0, 2*np.pi, model.num_segments))

    return model



def tadpole_struggling():
    """
    set up a tadpole model does tail-to-head swimming
    """
    model = Model(num_segments=25)
    model.set_name("struggling")
    # make amplitudes linearly increasing from head for a few segments
    # then decreasing to 0.1
    model.amplitude = np.zeros(model.num_segments)
    n_increase = 10
    model.amplitude[0:n_increase] = np.linspace(0, 0.3, n_increase)
    model.amplitude[n_increase:] = np.linspace(0.3, 0.1, model.num_segments - n_increase)

    # keep frequency constant
    model.frequency = np.ones(model.num_segments)
    # initialize phase offset to be a sine wave
    model.phase_offset = np.sin(np.linspace(0, 2*np.pi, model.num_segments))

    model.alpha = 0.1

    return model


def tadpole_flickering():
    """
    set up a tadpole model that only swims along few end segments
    of the tail
    """

    model = Model(num_segments=25)
    model.set_name("flickering")
    # make amplitudes linearly increasing from head for a few segments
    # then decreasing to 0.1
    model.amplitude = np.zeros(model.num_segments)
    n_increase_slow = model.num_segments - 6
    model.amplitude[0:n_increase_slow] = np.linspace(0, 0.1, n_increase_slow)
    model.amplitude[n_increase_slow:] = np.linspace(0.1, 0.2, model.num_segments - n_increase_slow)

    # keep frequency constant
    model.frequency = np.ones(model.num_segments)
    # initialize phase offset to be a sine wave
    model.phase_offset = np.sin(np.linspace(0, 2*np.pi, model.num_segments))


    return model


# setup abstract animation function that takes in a model
# and animates it
def animate_model(model):
    """
    take in a model, animate, and save as gif
    """

    fig, ax = plt.subplots()
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(-0.1, 1.1)
    x, y = model.get_segment_positions()

    line, = ax.plot(x, y, 'ko-')
    ax.plot(0, 0, 'o')
    
 
    def animate(i):
        model.update()
        x, y = model.get_segment_positions()
        line.set_data(x, y)
        return line,

    # set title as model name
    plt.title(model.name)

    anim = FuncAnimation(fig, animate, frames=200, interval=15, blit=True)
    plt.show()

    # save animation as model name 
    anim.save(model.name + '.gif', writer='imagemagick', fps=30)


# setup plotting function that takes in a model and
# plots the a single figure that overlays a few model
# updates in increasing opacity
def plot_model(model, ax=None, num_updates=20, model_dt=0.1):
    """
    take in a model, plot a few updates

    create a figure with tadpole at top and phase offset or amplitudes at bottom

    plot on ax if given, otherwise plot on new figure
    """

    model.dt = model_dt

    # use ax if given, otherwise create new figure
    if ax is None:
        ax = plt.gca()
    

    # plot tadpole on top

    ax.set_ylim(-5, 1.1)
    ax.set_xlim(-0.3, 1.3)
    
    # no ticks
    ax.set_xticks([])
    ax.set_yticks([])

    x, y = model.get_segment_positions()

    line, = ax.plot(x, y, 'ko-', alpha=0.1)
    # make head bigger.
    # give it a fill and an edge color black
    ax.plot(0, 0, 'o', markersize=30, color='gray', markeredgecolor='black')

    
    for i in range(num_updates):
        model.update()
        if (i % 5 == 0):
            x, y = model.get_segment_positions()
            # plot with increasing opacity until 1:
            ax.plot(x, y, 'ko-', alpha=(i/num_updates)*0.9)

    # plot ampliudes 
    ax2 = ax.inset_axes([0.1, 0.1, 0.8, 0.3])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.plot(model.amplitude, 'k-')
    ax2.set_ylabel('amplitude')
    ax2.set_xlabel('segment')

    










model_swim = tadpole_swimming()
model_struggle = tadpole_struggling()
model_flicker = tadpole_flickering()

# plot_model(model_swim, model_dt=0.5)
# animate_model(model_swim)

# plot_model(model_struggle, model_dt=0.2)
# animate_model(model_struggle)
# animate_model(model_flicker)
# plot_model(model_flicker, model_dt=0.5)

# animate_model(model_flicker)


# make multi panel figure with all 3 models
def plot_multipanel():
    """
    plot all 3 models in subplots
    """

    model_swim = tadpole_swimming()
    model_struggle = tadpole_struggling()
    model_flicker = tadpole_flickering()


    # setup figure
    fig, axs = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle('Tadpole Swimming Behaviors')


    # plot each model
    plot_model(model_swim, ax=axs[0], num_updates=20, model_dt=0.3)
    plot_model(model_struggle, ax=axs[1], num_updates=20, model_dt=0.3)
    plot_model(model_flicker, ax=axs[2], num_updates=20, model_dt=0.3)

    
    axs[0].set_title('Swimming')
    axs[1].set_title('Struggling')
    axs[2].set_title('Flickering')

    plt.show()



plot_multipanel()







