import stl
import math
import numpy as np
import os
import sys
from stl import mesh

import tkinter as tk
from tkinter.ttk import *

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
global imgNew, imgOpn,imgExt, imgCub,imgSph,imgPyr

class MainWin(object):
    main_body = mesh.Mesh.from_file('RaspS.stl')

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("RS Design VER 0.00")
        self.window.iconbitmap('RaspSNK.ico')
        self.create_widgets()


    def create_widgets(self):
        self.window['padx'] = 10
        self.window['pady'] = 10

        # Frame
        frame1 = Frame(self.window, relief=tk.RIDGE)
        frame1.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=0, pady=0)

        frame2 = Frame(self.window, relief=tk.RIDGE)
        frame2.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=0, pady=0)
        self.plotFrame = self.PlotFrame(frame1, frame2)

        frame3 = Frame(self.window, relief=tk.RIDGE)
        frame3.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=0, pady=0)

        self.workFrame = self.WorkFrame(frame3, self.plotFrame)
        # File buttons
        FileFrame = tk.Frame(self.window)
        lb = Label(FileFrame)
        lb.grid(column=0, row=0, padx=10, pady=0)
        imgNew = tk.PhotoImage(file="new.png")
        btnNew = tk.Button(FileFrame, compound=tk.TOP,image = imgNew , width=20, height=20, command=New)
        btnNew.image = imgNew
        btnNew.grid(column=0, row=0, padx=2)
        imgOpn = tk.PhotoImage(file="opn.png")
        btnOpn = tk.Button(FileFrame, image = imgOpn, width=20, height=20, command=Opn)
        btnOpn.image = imgOpn
        btnOpn.grid(column=0, row=1, padx=3)
        imgExt = tk.PhotoImage(file="ext.png")
        btnExt = tk.Button(FileFrame, image = imgExt, width=20, height=20, command=Ext)
        btnExt.image = imgExt
        btnExt.grid(column=0, row=2, padx=3)
        FileFrame.grid(row=0, column=0, sticky="nsew", padx=10)
        
        # Create buttons
        CrtFrame = tk.Frame(self.window)
        lb = Label(CrtFrame)
        lb.grid(column=0, row=0)
        imgCub = tk.PhotoImage(file="cub.png")
        btnCub = tk.Button(CrtFrame, image =imgCub, width=20, height=20, command=Cub)
        btnCub.image = imgCub
        btnCub.grid(column=0, row=1)
        imgSph = tk.PhotoImage(file="sph.png")
        btnSph = tk.Button(CrtFrame, image=imgSph, width=20, height=20, command=Sph)
        btnSph.image = imgSph
        btnSph.grid(column=0, row=2)

        imgCon = tk.PhotoImage(file="cone.png")
        btnCon = tk.Button(CrtFrame, image=imgCon, width=20, height=20, command=Con)
        btnCon.image = imgCon
        btnCon.grid(column=0, row=3)
        
        CrtFrame.grid(row=0, column=2, sticky="nsew", padx=10)

    class PlotFrame(object):
        # The plot
        def __init__(self, parent1, parent2):
            main_body = mesh.Mesh.from_file('RaspS.stl')
            self.parent1 = parent1
            self.parent2 = parent2
            self.observers = []
            self.x = 0
            self.y = 0
            canvas = self.plot()
            self.plot_toolbar(canvas)

        def plot(self):
            # The actual plot

            fig = plt.Figure()
            # To be able to rotate we have to draw an empty canvas first before plotting a figure
            canvas = FigureCanvasTkAgg(fig, self.parent1)
            canvas.draw()
            
            ax = mplot3d.Axes3D(fig)
            ax.add_collection3d(mplot3d.art3d.Poly3DCollection(main_body.vectors))
            canvas.mpl_connect('button_press_event', self.onclick)
            scale = main_body.points.flatten('F')
            ax.auto_scale_xyz(scale, scale, scale)
            
             
            return canvas

        def plot_toolbar(self, canvas):
            # The tool bar to the plot
            toolbar = NavigationToolbar2Tk(canvas, self.parent2)
            toolbar.update()
            canvas.get_tk_widget().grid(row=1, column=1)
            canvas.draw()

        def onclick(self, event):
            # Setting the position
            self.set_new_position(event.x, event.y)

        def set_new_position(self, x, y):
            self.x = x
            self.y = y
            for callback in self.observers:
                # Calling the methods that have been captured so far and passing them the arguments of x, y to do with as they please
                callback(self.x, self.y)

        def bind_to(self, callback):
            self.observers.append(callback)

    class WorkFrame():
        def __init__(self, parent, plot_frame):
            self.parent =  parent
            self.x = 0
            self.y = 0
            self.plot_frame = plot_frame
            self.plot_frame.bind_to(self.update_position)
            self.display()

        def update_position(self, x, y):
            self.x = x
            self.y = y
            # Adding the requirement to run the display code again after an update
            self.display()

        def display(self):
            l_x = tk.Label(self.parent, text ='Xposition: ' + str(self.x))
            l_y = tk.Label(self.parent, text ='Yposition: ' + str(self.y))
            l_x.grid(row = 0,  column=0)
            l_y.grid(row = 0,  column=1)

# For now this part doesn't seem to have any effect on the program:

#__saved_context__ = {}

#def saveContext():
    #import sys
    #__saved_context__.update(sys.modules[__name__].__dict__)

#def restoreContext():
    #import sys
    #names = sys.modules[__name__].__dict__.keys()
    #for n in list(names):
        #if n not in __saved_context__:
            #del sys.modules[__name__].__dict__[n]
#clear = restoreContext
#saveContext()
#clear()

def find_mins_maxs(obj):
    minx = maxx = miny = maxy = minz = maxz = None
    for p in obj.points:
        # p contains (x, y, z)
        if minx is None:
            minx = p[stl.Dimension.X]
            maxx = p[stl.Dimension.X]
            miny = p[stl.Dimension.Y]
            maxy = p[stl.Dimension.Y]
            minz = p[stl.Dimension.Z]
            maxz = p[stl.Dimension.Z]
        else:
            maxx = max(p[stl.Dimension.X], maxx)
            minx = min(p[stl.Dimension.X], minx)
            maxy = max(p[stl.Dimension.Y], maxy)
            miny = min(p[stl.Dimension.Y], miny)
            maxz = max(p[stl.Dimension.Z], maxz)
            minz = min(p[stl.Dimension.Z], minz)
    return minx, maxx, miny, maxy, minz, maxz


def translate(_solid, step, padding, multiplier, axis):
    if 'x' == axis:
        items = 0, 3, 6
    elif 'y' == axis:
        items = 1, 4, 7
    elif 'z' == axis:
        items = 2, 5, 8
    else:
        raise RuntimeError('Unknown axis %r, expected x, y or z' % axis)

    # _solid.points.shape == [:, ((x, y, z), (x, y, z), (x, y, z))]
    _solid.points[:, items] += (step * multiplier) + (padding * multiplier)


def copy_obj(obj, dims, num_rows, num_cols, num_layers):
    w, l, h = dims
    copies = []
    for layer in range(num_layers):
        for row in range(num_rows):
            for col in range(num_cols):
                # Skipping the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # Padding the space between objects by 10% of the dimension being translated
                if col != 0:
                    translate(_copy, w, w / 10., col, 'x')
                if row != 0:
                    translate(_copy, l, l / 10., row, 'y')
                if layer != 0:
                    translate(_copy, h, h / 10., layer, 'z')
                copies.append(_copy)
    return copies
def New():
#    lb = Label(program.window, text=35*" ")
#    lb.grid(column=2, row=0)

#    fig = plt.figure(figsize=(6,5), dpi=100)
#    canvas = FigureCanvasTkAgg(fig, program.window)
#    canvas.draw()
#    ax = fig.add_subplot(111, projection='3d')
    
    data = np.zeros(100, dtype=mesh.Mesh.dtype)
    New = mesh.Mesh(data, remove_empty_areas=False)
    New.save('RaspS.stl', mode=stl.Mode.ASCII)
    main_body = mesh.Mesh.from_file('RaspS.stl')
    
    os.execl(sys.executable, sys.executable, *sys.argv)
    #program.window.update_idletasks()
    #program.window.update()
        
def Opn():

    program.window.filename =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [("STL files","*.stl")])
    fileout =program.window.filename
    OPENF = mesh.Mesh.from_file(fileout)
    #OPENF.save('RaspS.stl', mode=stl.Mode.ASCII)  # save as ASCII

    main_body = mesh.Mesh.from_file('RaspS.stl')

    openf = copy_obj(OPENF, (w1, l1, h1), 1, 1, 1)
    
    minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(OPENF)
    w2 = maxx - minx
    l2 = maxy - miny
    h2 = maxz - minz
    translate(OPENF, w1, w1 / 10., 3, 'x')
    combined = mesh.Mesh(np.concatenate([main_body.data, OPENF.data]))

    combined.save('RaspS.stl', mode=stl.Mode.ASCII)  # save as ASCII
    main_body = mesh.Mesh.from_file('RaspS.stl')

    os.execl(sys.executable, sys.executable, *sys.argv)
    #program.window.update()
    #program.window.update_idletasks()

def Ext():
    quit()


def Save():
    plt.savefig(name)
    
def Cub():
    Cubimp=tk.Tk()
    Cuframe=tk.Frame(Cubimp)
    tk.Label(Cuframe, text="Height").grid(row=0)
    tk.Label(Cuframe, text="Width").grid(row=1)
    tk.Label(Cuframe, text="Length").grid(row=2)
    tk.Label(Cuframe, text="X").grid(row=3)
    tk.Label(Cuframe, text="Y").grid(row=4)
    tk.Label(Cuframe, text="Z").grid(row=5)
    hc = tk.Entry(Cuframe)
    hc.insert(tk.END, "1")
    
    wc = tk.Entry(Cuframe)
    wc.insert(tk.END, "1")

    lc = tk.Entry(Cuframe)
    lc.insert(tk.END, "1")

    xc = tk.Entry(Cuframe)
    xc.insert(tk.END, "0")

    yc = tk.Entry(Cuframe)
    yc.insert(tk.END, "0")

    zc = tk.Entry(Cuframe)
    zc.insert(tk.END, "0")

    hc.grid(row=0, column=1)
    wc.grid(row=1, column=1)
    lc.grid(row=2, column=1)
    xc.grid(row=3, column=1)
    yc.grid(row=4, column=1)
    zc.grid(row=5, column=1)
    Cuframe.grid(row=0, column=0)
    def Cubcal():
        XYZ=[float(hc.get()), float(wc.get()), float(lc.get())]
        HWL=[float(xc.get()),float(yc.get()),float(zc.get())]
        Nod=np.array([\
        [XYZ(1)-HWL(1), XYZ(1)-HWL(1),XYZ(1)-HWL(1)],
        [XYZ(1)+1, XYZ(1)-1, XYZ(1)-1],
        [XYZ(1)+1, XYZ(1)+1, XYZ(1)-1],
        [XYZ(1)-1, XYZ(1)+1, XYZ(1)-1],
        [XYZ(1)-1, XYZ(1)-1, XYZ(1)+1],
        [XYZ(1)+1, XYZ(1)-1, XYZ(1)+1],
        [XYZ(1)+1, XYZ(1)+1, XYZ(1)+1],
        [XYZ(1)-1, XYZ(1)+1, XYZ(1)+1]])
        
        
    
    btnOK = tk.Button(Cubimp, text = "OK" , width=15, height=3,command=Cubcal)

        

    btnOK.grid(column=0, row=1)
    
    
def Sph():
    pass
    
def Con():
    pass


# Using an existing stl file
main_body = mesh.Mesh.from_file('RaspS.stl')

# Finding the max dimensions & getting the height, width, length
minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)
w1 = maxx - minx
l1 = maxy - miny
h1 = maxz - minz

# Creating the splash screen
root = tk.Tk()

# Showing no frame
root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (width*0.7, height*0.7, width*0.2, height*0.2))

image = tk.PhotoImage(file="Splash.gif")
canvas = tk.Canvas(root, height=height*0.8, width=width*0.8, bg="white")
canvas.create_image(width*0.3, height*0.3, image=image)
canvas.pack()

# Showing the splash screen for 5000 milliseconds, then destroying
root.after(1, root.destroy)
root.mainloop()
print ("RaspiSnakes")

# Creating the entire GUI program
program = MainWin()

# Starting the GUI event loop
program.window.mainloop()

