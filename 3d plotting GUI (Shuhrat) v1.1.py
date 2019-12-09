# Shukhrat Khuseynov
# GUI plotting
# version 1.1

from tkinter import *
from tkinter.ttk import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

window = Tk()
window.title("GUI of Rasp Snakes")
 
window.geometry('185x300')
 
lbl = Label(window, text="   Choose a figure to be plotted.\n")
 
lbl.grid(column=0, row=0)

 
combo = Combobox(window, width=8)
 
combo['values']= ("Sphere", "Box", "Pyramid")
 
combo.current(1) #set the selected item
 
combo.grid(column=0, row=1)

def choose():

    lb2 = Label(window, text="\nThe "+combo.get().lower()+" is chosen.\nEnter its parameter(s):\n")
    lb2.grid(column=0, row=4)

    if combo.get() == "Sphere":
        lb = Label(window, text=30*"-")
        lb.grid(column=0, row=5)
        lb3 = Label(window, text="Radius")
        lb3.grid(column=0, row=5)

        radius = Entry(window,width=5) 
        radius.grid(column=0, row=6)
        radius.focus()
        
        lb = Label(window, text="")
        lb.grid(column=0, row=7)
        
        btn2 = Button(window, text="Plot", width=5, command=plot)
        btn2.grid(column=0, row=10)
        
    elif combo.get() == "Box":
        lb = Label(window, text=30*"-")
        lb.grid(column=0, row=5)
        
        lb3 = Label(window, text="Length, width & height")
        lb3.grid(column=0, row=5)

        length = Entry(window,width=5) 
        length.grid(column=0, row=6)
        length.focus()

        width = Entry(window,width=5) 
        width.grid(column=0, row=7)

        height = Entry(window,width=5) 
        height.grid(column=0, row=8)
        
        lb = Label(window, text="")
        lb.grid(column=0, row=9)
        
        btn2 = Button(window, text="Plot", width=5, command=plot)
        btn2.grid(column=0, row=10)

    else:
        lb = Label(window, text=30*"-")
        lb.grid(column=0, row=5)
        
        lb3 = Label(window, text="Base length & height")
        lb3.grid(column=0, row=5)

        length = Entry(window,width=5) 
        length.grid(column=0, row=6)
        length.focus()
        
        height = Entry(window,width=5) 
        height.grid(column=0, row=7)
        
        lb = Label(window, text="")
        lb.grid(column=0, row=8)
        
        btn2 = Button(window, text="Plot", width=5, command=plot)
        btn2.grid(column=0, row=10)

lb = Label(window, text="")
lb.grid(column=0, row=2)

#radius = Entry()

btn = Button(window, text="Choose", width=8, command=choose)
btn.grid(column=0, row=3)


def plot():

    if combo.get() == "Sphere":

        #r = float(radius.get())
        r = 1
        
        fig = plt.figure()
        plot = Tk()
        plot.title("Figure")
            
        canvas = FigureCanvasTkAgg(fig, plot)
        canvas.draw()

        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))

        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(r*x, r*y, r*z)
            
     
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, plot)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    elif combo.get() == "Box":
        
        fig = plt.figure()
        plot = Tk()
        plot.title("Figure")
            
        canvas = FigureCanvasTkAgg(fig, plot)
        canvas.draw()
        
        ax = fig.gca(projection='3d')
        #ax.set_aspect("equal")

        # draw cube
        def x_y_edge(x_range, y_range, z_range):
               xx, yy = np.meshgrid(x_range, y_range)

               for value in [0, 1]:
                   ax.plot_wireframe(xx, yy, z_range[value], color="r")
                   ax.plot_surface(xx, yy, z_range[value], color="r", alpha=0.2)


        def y_z_edge(x_range, y_range, z_range):
               yy, zz = np.meshgrid(y_range, z_range)

               for value in [0, 1]:
                   ax.plot_wireframe(x_range[value], yy, zz, color="r")
                   ax.plot_surface(x_range[value], yy, zz, color="r", alpha=0.2)


        def x_z_edge(x_range, y_range, z_range):
               xx, zz = np.meshgrid(x_range, z_range)

               for value in [0, 1]:
                   ax.plot_wireframe(xx, y_range[value], zz, color="r")
                   ax.plot_surface(xx, y_range[value], zz, color="r", alpha=0.2)


        def rect_prism(x_range, y_range, z_range):
               x_y_edge(x_range, y_range, z_range)
               y_z_edge(x_range, y_range, z_range)
               x_z_edge(x_range, y_range, z_range)

        rect_prism(np.array([-1, 1]), np.array([-1, 1]), np.array([-0.5, 0.5]))

        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, plot)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

    else:
        
        fig = plt.figure()
        plot = Tk()
        plot.title("Figure")

        canvas = FigureCanvasTkAgg(fig, plot)
        canvas.draw()
        
        ax = fig.add_subplot(111, projection='3d')

        # vertices of a pyramid
        v = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1],  [-1, 1, -1], [0, 0, 1]])
        ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

        # generate list of sides' polygons of our pyramid
        verts = [ [v[0],v[1],v[4]], [v[0],v[3],v[4]],
         [v[2],v[1],v[4]], [v[2],v[3],v[4]], [v[0],v[1],v[2],v[3]]]

        # plot sides
        ax.add_collection3d(Poly3DCollection(verts, 
         facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, plot)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)

window.mainloop()

# 3d plotting algorithms were obtained from freely shared codes
