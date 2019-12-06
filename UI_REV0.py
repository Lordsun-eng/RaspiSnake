import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
import stl
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from matplotlib.figure import Figure
#import openmesh as om
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot


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



def New():
    data = np.zeros(100, dtype=mesh.Mesh.dtype)
    New = mesh.Mesh(data, remove_empty_areas=False)
    New.save('RaspS.stl', mode=stl.Mode.ASCII)
    currfile = mesh.Mesh.from_file('RaspS.stl')
    Ploti = pyplot.figure(figsize=(6,5), dpi=100)
    axes = mplot3d.Axes3D(Ploti)
    ax = axes.add_collection3d(mplot3d.art3d.Poly3DCollection(currfile.vectors))
    chart_type = FigureCanvasTkAgg(Ploti, window)
    chart_type.get_tk_widget().grid(column=2, row=0)

    # Auto scale to the mesh size
    scale = currfile.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)


def Opn():
    window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.stl"),("all files","*.*")))
    fileout =window.filename
    copies = copy_obj(main_body, (w1, l1, h1), 2, 2, 1)

    OPENF = mesh.Mesh.from_file(fileout)
    minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(OPENF)
    w2 = maxx - minx
    l2 = maxy - miny
    h2 = maxz - minz
    translate(OPENF, w1, w1 / 10., 3, 'x')
    copies2 = copy_obj(OPENF, (w2, l2, h2), 2, 2, 1)
    combined = mesh.Mesh(np.concatenate([main_body.data, OPENF.data] +
                                        [copy.data for copy in copies] +
                                        [copy.data for copy in copies2]))

    combined.save('RaspS.stl', mode=stl.Mode.ASCII)  # save as ASCII
    currfile = mesh.Mesh.from_file('RaspS.stl')
    Ploti = pyplot.figure(figsize=(6,5), dpi=100)
    axes = mplot3d.Axes3D(Ploti)
    ax = axes.add_collection3d(mplot3d.art3d.Poly3DCollection(currfile.vectors))
    chart_type = FigureCanvasTkAgg(Ploti, window)
    chart_type.get_tk_widget().grid(column=2, row=0)

    # Auto scale to the mesh size
    scale = currfile.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)
    
def Rec():
    mesh = om.TriMesh()
    # add a a couple of vertices to the mesh
    vh0 = mesh.add_vertex([0, 1, 0])
    vh1 = mesh.add_vertex([1, 0, 0])
    vh2 = mesh.add_vertex([2, 1, 0])
    vh3 = mesh.add_vertex([0,-1, 0])
    vh4 = mesh.add_vertex([2,-1, 0])
    
    # add a couple of faces to the mesh
    fh0 = mesh.add_face(vh0, vh1, vh2)
    fh1 = mesh.add_face(vh1, vh3, vh4)
    fh2 = mesh.add_face(vh0, vh3, vh1)
    
    # add another face to the mesh, this time using a list
    vh_list = [vh2, vh1, vh4]
    fh3 = mesh.add_face(vh_list)
    
    # get the point with vertex handle vh0
    point = mesh.point(vh0)
    
    # get all points of the mesh
    point_array = mesh.points()
    
    # translate the mesh along the x-axis
    point_array += np.array([1, 0, 0])
    
    # write and read meshes
    om.write_mesh('test.stl', mesh)
    your_mesh = mesh.Mesh.from_file('test.stl')
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
    # Auto scale to the mesh size
    scale = your_mesh.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)
    

    
def Sph():
    pass
def Cyl():
    pass
# Using an existing stl file:
main_body = mesh.Mesh.from_file('RaspS.stl')

minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)
w1 = maxx - minx
l1 = maxy - miny
h1 = maxz - minz

## Splash Screen
# create a splash screen, 80% of display screen size, centered,
# displaying a GIF image with needed info, disappearing after 5 seconds
root = tk.Tk()
# show no frame
root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (width*0.6, height*0.6, width*0.1, height*0.1))

#assert os.path.exists(image_file)
image = tk.PhotoImage(file="Splash.gif")
canvas = tk.Canvas(root, height=height*0.6, width=width*0.6, bg="white")
canvas.create_image(width*0.6/2, height*0.6/2, image=image)
canvas.create_text(width*0.6/8, height*0.6/8, text="VER 0.0.0 ")
canvas.pack()
# show the splash screen for 5000 milliseconds then destroy
root.after(5000, root.destroy)
root.mainloop()
# your console program can start here ...
print ("RaspiSnakes")


# find the max dimensions, so we can know the bounding box, getting the height,
# width, length (because these are the step size)...

window = tk.Tk()
ToolboxCreat = tk.Frame(window)
window.iconbitmap('RaspSNK.ico')
btnRec = Button(ToolboxCreat, text="Rectancle", width=10, command=Rec)
btnRec.grid(column=0, row=1)
btnSph = Button(ToolboxCreat, text="Sphere", width=10, command=Sph)
btnSph.grid(column=0, row=2)
btnCyl = Button(ToolboxCreat, text="Cylander", width=10, command=Cyl)
btnCyl.grid(column=0, row=3)
ToolboxCreat.grid(row=0, column=0, sticky="nsew")


ToolboxGen=tk.Frame(window)
btnNew = Button(ToolboxGen, text="New", width=10, command=New)
btnNew.grid(column=0, row=1)
btnOpn = Button(ToolboxGen, text="Open", width=10, command=Opn)
btnOpn.grid(column=0, row=2)
ToolboxGen.grid(row=0, column=1, sticky="nsew")

window.title("Rasp Snakes CAD Software VER 0.0.0")
 
window.geometry('800x600')






