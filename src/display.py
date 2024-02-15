import math
import time
import tkinter
from random import random
from serial import Serial # this line not working!!!
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.backends._backend_tk import (NavigationToolbar2Tk)

def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    """!
    boilerplate text
    @param plot_axes
    @param plot_canvas
    @param xlabel
    @param ylabel
    """
    times = [t / 7 for t in range(200)]
    rando = random() * 2 * math.pi - math.pi
    boing = [-math.sin(t + rando) * math.exp(-(t + rando) / 11) for t in times]

    # Draw the plot using 
    plot_axes.plot(times, boing)
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    plot_axes.grid(True)
    plot_canvas.draw()


def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    text
    @param plot_function
    @param xlabel
    @param ylabel
    @param title
    """

    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # create a matplotlib figure
    fig = Figure()
    axes = fig.add_subplot()

    # create the drawing canvas and a navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas, xlabel, ylabel))
    
    # arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # this function runs until the user quits
    tkinter.mainloop()


if __name__ == "__main__":
    
    tk_matplot(plot_example,
               xlabel="Time [ms]",
               ylabel="Boing [cm]",
               title="title")