# Shams Torabnia & Shukhrat Khuseynov
# GUI & 3D plotting & STL editor (?)
# version 1.0.0

# (3d plotting algorithms were obtained from freely shared codes [stackoverflow, github, etc.])

import stl
import math
import numpy as np
import tkinter as tk

from stl import mesh
from tkinter.ttk import *
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

global main_body
# Using an existing stl file:
main_body = mesh.Mesh.from_file('RaspS.stl')

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
                # skip the position where original being copied is
                if row == 0 and col == 0 and layer == 0:
                    continue
                _copy = mesh.Mesh(obj.data.copy())
                # pad the space between objects by 10% of the dimension being
                # translated
                if col != 0:
                    translate(_copy, w, w / 10., col, 'x')
                if row != 0:
                    translate(_copy, l, l / 10., row, 'y')
                if layer != 0:
                    translate(_copy, h, h / 10., layer, 'z')
                copies.append(_copy)
    return copies



# find the max dimensions, so we can know the bounding box, getting the height, width, length (because these are the step size)...
minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)
w1 = maxx - minx
l1 = maxy - miny
h1 = maxz - minz
def New():
    pass
def Opn():
    window.filename =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [("STL files","*.stl")])
    fileout =window.filename
    OPENF = mesh.Mesh.from_file(fileout)

    openf = copy_obj(OPENF, (w1, l1, h1), 1, 1, 1)
    
    minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(OPENF)
    w2 = maxx - minx
    l2 = maxy - miny
    h2 = maxz - minz
    translate(OPENF, w1, w1 / 10., 3, 'x')
    combined = mesh.Mesh(np.concatenate([main_body.data, OPENF.data]))
    combined.save('RaspS.stl', mode=stl.Mode.ASCII)  # save as ASCII
    main_body = mesh.Mesh.from_file('RaspS.stl')
    canvas = FigureCanvasTkAgg(fig, window)
    ax = mplot3d.Axes3D(fig)
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(main_body.vectors))
    scale = main_body.points.flatten('F')
    ax.auto_scale_xyz(scale, scale, scale)

    canvas.get_tk_widget().grid(row=1, column=1)
    canvas.draw()
    
def Save():
    plt.savefig(name)
    
def Cub():
    pass
def Sph():
    pass
def Cyl():
    pass


# Splash screen (creating a splash screen, 80% of display screen size, centered, displaying a GIF image with needed info, disappearing after 5 seconds)
root = tk.Tk()

# Showing no frame
root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (width*0.6, height*0.6, width*0.1, height*0.1))

image = tk.PhotoImage(file="Splash.gif")
canvas = tk.Canvas(root, height=height*0.6, width=width*0.6, bg="white")
canvas.create_image(width*0.6/2, height*0.6/2, image=image)
canvas.create_text(width*0.6/8, height*0.6/8, text="VER 0.00 ")

# Showing the splash screen for 5000 milliseconds then destroying
root.after(1, root.destroy)
root.mainloop()
print ("RaspiSnakes")

# Starting the main window 
window = tk.Tk()
window['padx'] = 10
window['pady'] = 10
window.iconbitmap('RaspSNK.ico')

# - - - - - - - - - - - - - - - - - - - - -
# Frame
frame1 = Frame(window, relief=tk.RIDGE)
frame1.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=0, pady=0)

frame2 = Frame(window, relief=tk.RIDGE)
frame2.grid(row=1, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=0, pady=0)
plotFrame = PlotFrame(frame1, frame2)

frame3 = Frame(window, relief=tk.RIDGE)
frame3.grid(row=2, column=1, sticky=tk.E + tk.W + tk.N + tk.S, padx=0, pady=0)

self.workFrame = WorkFrame(frame3, self.plotFrame)
# File buttons
FileFrame = tk.Frame(window)
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
CrtFrame = tk.Frame(window)
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

window.title("Rasp Snakes Software VER 0.00")
 
window.geometry('800x600')

fig = plt.Figure()
canvas = FigureCanvasTkAgg(fig, window)
canvas.draw()
main_body = mesh.Mesh.from_file('RaspS.stl')
ax = mplot3d.Axes3D(fig)
ax.add_collection3d(mplot3d.art3d.Poly3DCollection(main_body.vectors))
scale = main_body.points.flatten('F')
ax.auto_scale_xyz(scale, scale, scale)

canvas.get_tk_widget().grid(row=1, column=1)
canvas.draw()




