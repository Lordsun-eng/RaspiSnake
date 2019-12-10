# Shams Torabnia & Shukhrat Khuseynov
# GUI & 3D plotting (STL?)
# version 1.0

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
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT

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
    lb = Label(window, text=35*" ")
    lb.grid(column=2, row=0)

    #fig = plt.figure(figsize=(6,5), dpi=100)
    #canvas = FigureCanvasTkAgg(fig, window)
    #canvas.draw()
    
    data = np.zeros(100, dtype=mesh.Mesh.dtype)
    New = mesh.Mesh(data, remove_empty_areas=False)
    New.save('RaspS.stl', mode=stl.Mode.ASCII)
    currfile = mesh.Mesh.from_file('RaspS.stl')
    fig = plt.figure(figsize=(6,5), dpi=100)
    axes = mplot3d.Axes3D(fig)
    ax = axes.add_collection3d(mplot3d.art3d.Poly3DCollection(currfile.vectors))
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.get_tk_widget().grid(column=2, row=1)

    # Auto scale to the mesh size
    scale = currfile.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)


def Opn():
    lb = Label(window, text=35*" ")
    lb.grid(column=2, row=0)
    lb = Label(window, text="STL file")
    lb.grid(column=2, row=0)

    #fig = plt.figure(figsize=(6,5), dpi=100)
    #canvas = FigureCanvasTkAgg(fig, window)
    #canvas.draw()
    
    window.filename =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.stl"),("all files","*.*")))
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
    fig = plt.figure(figsize=(6,5), dpi=100)
    axes = mplot3d.Axes3D(fig)
    ax = axes.add_collection3d(mplot3d.art3d.Poly3DCollection(currfile.vectors))
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.get_tk_widget().grid(column=2, row=1)

    # Auto scale to the mesh size
    scale = currfile.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

def Save():
    plt.savefig(name)
    
def Cub():
    lb = Label(window, text=35*" ")
    lb.grid(column=2, row=0)
    lb = Label(window, text="Rectangular prism")
    lb.grid(column=2, row=0)

    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    ax = fig.add_subplot(111, projection='3d')

    cube_definition = [(0,0,0), (0,1,0), (2,0,0), (0,0,3)]
    
    cube_definition_array = [
        np.array(list(item))
        for item in cube_definition
    ]

    points = []
    points += cube_definition_array
    vectors = [
        cube_definition_array[1] - cube_definition_array[0],
        cube_definition_array[2] - cube_definition_array[0],
        cube_definition_array[3] - cube_definition_array[0]
    ]

    points += [cube_definition_array[0] + vectors[0] + vectors[1]]
    points += [cube_definition_array[0] + vectors[0] + vectors[2]]
    points += [cube_definition_array[0] + vectors[1] + vectors[2]]
    points += [cube_definition_array[0] + vectors[0] + vectors[1] + vectors[2]]

    points = np.array(points)

    edges = [
        [points[0], points[3], points[5], points[1]],
        [points[1], points[5], points[7], points[4]],
        [points[4], points[2], points[6], points[7]],
        [points[2], points[6], points[3], points[0]],
        [points[0], points[2], points[4], points[1]],
        [points[3], points[6], points[7], points[5]]
    ]

    faces = mplot3d.art3d.Poly3DCollection(edges, linewidths=1, edgecolors='k')
    faces.set_facecolor((0,0,1,0.1))

    ax.add_collection3d(faces)

    # Plot the points themselves to force the scaling of the axes
    ax.scatter(points[:,0], points[:,1], points[:,2], s=0)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    canvas.get_tk_widget().grid(column=2, row=1)

    global name
    name = 'RectPrism.png' 
    btnSave = Button(window, text="Save", width=10, command=Save)
    btnSave.grid(column=2, row=2, pady=5)
    
def Sph():
    lb = Label(window, text=35*" ")
    lb.grid(column=2, row=0)
    lb = Label(window, text="Sphere")
    lb.grid(column=2, row=0)
    r = 3
        
    fig = plt.figure(figsize=(6,5), dpi=100)            
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(r*x, r*y, r*z)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    canvas.get_tk_widget().grid(column=2, row=1)

    global name
    name = 'Sphere.png' 
    btnSave = Button(window, text="Save", width=10, command=Save)
    btnSave.grid(column=2, row=2, pady=5)
    
def Cyl():
    lb = Label(window, text=35*" ")
    lb.grid(column=2, row=0)
    lb = Label(window, text="Cylinder")
    lb.grid(column=2, row=0)
    
    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()

    r=10; h=10; a=0; nt=100; nv =50;
    theta = np.linspace(0, 2*np.pi, nt)
    v = np.linspace(a, a+h, nv )
    theta, v = np.meshgrid(theta, v)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    z = v
    rstride = 20
    cstride = 10
    
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, alpha=0.2, rstride=rstride, cstride=cstride)
    ax.plot_surface(x, -y, z, alpha=0.2, rstride=rstride, cstride=cstride)
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    canvas.get_tk_widget().grid(column=2, row=1)

    global name
    name = 'Cylinder.png' 
    btnSave = Button(window, text="Save", width=10, command=Save)
    btnSave.grid(column=2, row=2, pady=5)

def Pyr():
    lb = Label(window, text=35*" ")
    lb.grid(column=2, row=0)
    lb = Label(window, text="Pyramid")
    lb.grid(column=2, row=0)
    
    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
        
    ax = fig.add_subplot(111, projection='3d')
    
    # vertices of a pyramid
    v = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1],  [-1, 1, -1], [0, 0, 1]])
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

    # generate list of sides' polygons of our pyramid
    verts = [ [v[0],v[1],v[4]], [v[0],v[3],v[4]],[v[2],v[1],v[4]], [v[2],v[3],v[4]], [v[0],v[1],v[2],v[3]]]

    # plot sides
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(verts, 
    facecolors='cyan', linewidths=1, edgecolors='b', alpha=.25))

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    canvas.get_tk_widget().grid(column=2, row=1)

    global name
    name = 'Pyramid.png' 
    btnSave = Button(window, text="Save", width=10, command=Save)
    btnSave.grid(column=2, row=2, pady=5)

def Paral():
    lb = Label(window, text=35*" ")
    lb.grid(column=2, row=0)
    lb = Label(window, text="Parallelepiped")
    lb.grid(column=2, row=0)

    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    
    ax = fig.add_subplot(111, projection='3d')

    points = np.array([[-1, -1, -1],
                  [1, -1, -1 ],
                  [1, 1, -1],
                  [-1, 1, -1],
                  [-1, -1, 1],
                  [1, -1, 1 ],
                  [1, 1, 1],
                  [-1, 1, 1]])

    P = [[2.06498904e-01 , -6.30755443e-07 ,  1.07477548e-03],
     [1.61535574e-06 ,  1.18897198e-01 ,  7.85307721e-06],
     [7.08353661e-02 ,  4.48415767e-06 ,  2.05395893e-01]]

    Z = np.zeros((8,3))
    for i in range(8): Z[i,:] = np.dot(points[i,:],P)
    Z = 10.0*Z

    r = [-1,1]

    X, Y = np.meshgrid(r, r)
    # plot vertices
    ax.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])

    # list of sides' polygons of figure
    verts = [[Z[0],Z[1],Z[2],Z[3]],
     [Z[4],Z[5],Z[6],Z[7]], 
     [Z[0],Z[1],Z[5],Z[4]], 
     [Z[2],Z[3],Z[7],Z[6]], 
     [Z[1],Z[2],Z[6],Z[5]],
     [Z[4],Z[7],Z[3],Z[0]]]

    # plot sides
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(verts, 
     facecolors='orange', linewidths=1, edgecolors='r', alpha=.25))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    canvas.get_tk_widget().grid(column=2, row=1)

    global name
    name = 'Parallelepiped.png' 
    btnSave = Button(window, text="Save", width=10, command=Save)
    btnSave.grid(column=2, row=2, pady=5)

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
window.iconbitmap('RaspSNK.ico')

# File buttons
ToolboxGen=tk.Frame(window)
btnNew = Button(ToolboxGen, text="New", width=10, command=New)
btnNew.grid(column=0, row=1, padx=2)
btnOpn = Button(ToolboxGen, text="Open", width=10, command=Opn)
btnOpn.grid(column=1, row=1, padx=3)
ToolboxGen.grid(row=0, column=0, sticky="nsew", padx=10, pady=15)



# Figure plotting buttons
ToolboxCreat = tk.Frame(window)
lb = Label(ToolboxCreat, text="Choose a figure:\n")
lb.grid(column=0, row=0, padx=0, pady=0)
btnCub = Button(ToolboxCreat, text="Rectangular prism", width=16, command=Cub)
btnCub.grid(column=0, row=1, pady=3)
btnSph = Button(ToolboxCreat, text="Sphere", width=16, command=Sph)
btnSph.grid(column=0, row=2, pady=2)
btnCyl = Button(ToolboxCreat, text="Cylinder", width=16, command=Cyl)
btnCyl.grid(column=0, row=3, pady=3)
btnPyr = Button(ToolboxCreat, text="Pyramid", width=16, command=Pyr)
btnPyr.grid(column=0, row=4, pady=2)
btnParal = Button(ToolboxCreat, text="Parallelepiped", width=16, command=Paral)
btnParal.grid(column=0, row=5, pady=3)
ToolboxCreat.grid(row=1, column=0, sticky="nsew", padx=31, pady=20)


window.title("Rasp Snakes CAD Software VER 0.0.0")
 
window.geometry('800x600')





