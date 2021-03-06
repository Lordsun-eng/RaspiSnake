# Shams Torabnia & Shukhrat Khuseynov
# GUI & 3D plotting & STL editor (?)
# version 0.0.0

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

def New():
    # cleaning the previous title
    lb = Label(window, text=45*" ")
    lb.grid(column=2, row=1)

    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    ax = fig.add_subplot(111, projection='3d')
    
    data = np.zeros(100, dtype=mesh.Mesh.dtype)
    New = mesh.Mesh(data, remove_empty_areas=False)
    New.save('1.stl', mode=stl.Mode.ASCII)
    currfile = mesh.Mesh.from_file('1.stl')
    
    fig = plt.figure(figsize=(6,5), dpi=100)
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(currfile.vectors))

    # Auto scale to the mesh size
    scale = currfile.points.flatten(-1)
    ax.auto_scale_xyz(scale, scale, scale)

    # naming the axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    canvas = FigureCanvasTkAgg(fig, window)
    canvas.get_tk_widget().grid(column=2, row=2)

    # set parameters button & save button
    GraphFrame = tk.Frame(window)
    btnSet = Button(GraphFrame, text="Set the parameters", width=20, command=SetNew)
    btnSet.grid(column=0, row=0, padx=5)
    global name
    name = 'StlFile.png' 
    btnSave = Button(GraphFrame, text="Save", width=10, command=Save)
    btnSave.grid(column=1, row=0, padx=5)
    GraphFrame.grid(row=3, column=2, pady=5)
def SetNew():
    tk.messagebox.showinfo("Set the parameters", "This feature is not defined for the STL editor.")
    
def Opn():
    window.filename =  tk.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.stl"),("all files","*.*")))
    fileout =window.filename
    OPENF = mesh.Mesh.from_file(fileout)
    OPENF.save('1.stl', mode=stl.Mode.ASCII)  # save as ASCII

    # cleaning the previous title
    lb = Label(window, text=45*" ")
    lb.grid(column=2, row=1)
    
    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    ax = fig.add_subplot(111, projection='3d')

    # printing the according title
    lb = Label(window, text="STL file")
    lb.grid(column=2, row=1)    
    
    # Loading the STL files and adding the vectors to the plot
    stl_mesh = mesh.Mesh.from_file('1.stl')
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(stl_mesh.vectors))

    # Auto scale to the mesh size
    scale = stl_mesh.points.flatten(-1)
    ax.auto_scale_xyz(scale, scale, scale)

    # naming the axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.get_tk_widget().grid(column=2, row=2)

    # set parameters button & save button
    GraphFrame = tk.Frame(window)
    btnSet = Button(GraphFrame, text="Set the parameters", width=20, command=SetOpn)
    btnSet.grid(column=0, row=0, padx=5)
    global name
    name = 'StlFile.png' 
    btnSave = Button(GraphFrame, text="Save", width=10, command=Save)
    btnSave.grid(column=1, row=0, padx=5)
    GraphFrame.grid(row=3, column=2, pady=5)
def SetOpn():
    tk.messagebox.showinfo("Set the parameters", "This feature is not defined for the STL editor.")
    
    """toolbarFrame = tk.Frame(window)
    toolbarFrame.grid(row=2,column=2)
    toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
    toolbar.update()"""
    
    """
    copies = copy_obj(main_body, (w1, l1, h1), 2, 2, 1)
    
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
    """

def Save():
    plt.savefig(name)
    
def Cub():
    # cleaning the previous title
    lb = Label(window, text=45*" ")
    lb.grid(column=2, row=1)

    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    ax = fig.add_subplot(111, projection='3d')
    
    # printing the according title
    lb = Label(window, text="Box (rectangular prism)")
    lb.grid(column=2, row=1)

    cube_definition = [(0,0,0), (0,w,0), (l,0,0), (0,0,h)]
    
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

    # naming the axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # setting axes equal (aspect)
    scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz']); ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]]*3)
    
    canvas.get_tk_widget().grid(column=2, row=2)

    # set parameters button with relevant functions & save button
    GraphFrame = tk.Frame(window)
    btnSet = Button(GraphFrame, text="Set the parameters", width=20, command=SetCub)
    btnSet.grid(column=0, row=0, padx=5)
    global name
    name = 'Box.png' 
    btnSave = Button(GraphFrame, text="Save", width=10, command=Save)
    btnSave.grid(column=1, row=0, padx=5)
    GraphFrame.grid(row=3, column=2, pady=5)
def SetCub():
    global setp
    setp = tk.Tk()
    setp.title("Set the Box")

    lb = Label(setp, text="   The figure is Box.\nEnter its parameter(s):")
    lb.grid(column=0, row=0, pady=10, padx=15)

    global length, width, height
    fr = tk.Frame(setp)
    fr.grid(row=1, column=0, pady=20)
    
    lb1 = Label(fr, text="Length")
    lb1.grid(column=0, row=0, padx=7)
    length = Entry(fr,width=5) 
    length.grid(column=1, row=0, padx=8)
    length.insert(0, str(l))

    lb2 = Label(fr, text="Width")
    lb2.grid(column=0, row=1, padx=7)
    width = Entry(fr,width=5) 
    width.grid(column=1, row=1, padx=8)
    width.insert(0, str(w))

    lb3 = Label(fr, text="Height")
    lb3.grid(column=0, row=2, padx=7)
    height = Entry(fr,width=5) 
    height.grid(column=1, row=2, padx=8)
    height.insert(0, str(h))

    length.focus()
    
    btnOk = Button(fr, text="OK", width=4, command=OkCub)
    btnOk.grid(column=1, row=3, padx=8, pady=15)

    setp.geometry('150x200')
def OkCub():
    global l, w, h, setp
    l = float(length.get())
    w = float(width.get())
    h = float(height.get())
    Cub()
    setp.destroy()
    
def Sph():
    # cleaning the previous title
    lb = Label(window, text=45*" ")
    lb.grid(column=2, row=1)
        
    fig = plt.figure(figsize=(6,5), dpi=100)            
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()

    lb = Label(window, text="Sphere")
    lb.grid(column=2, row=1)

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = np.outer(np.cos(u), np.sin(v))
    y = np.outer(np.sin(u), np.sin(v))
    z = np.outer(np.ones(np.size(u)), np.cos(v))

    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(r*x, r*y, r*z)

    # naming the axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    canvas.get_tk_widget().grid(column=2, row=2)

    # set parameters button with relevant functions & save button
    GraphFrame = tk.Frame(window)
    btnSet = Button(GraphFrame, text="Set the parameters", width=20, command=SetSph)
    btnSet.grid(column=0, row=0, padx=5)
    global name
    name = 'Sphere.png'
    btnSave = Button(GraphFrame, text="Save", width=10, command=Save)
    btnSave.grid(column=1, row=0, padx=5)
    GraphFrame.grid(row=3, column=2, pady=5)
def SetSph():
    global setp
    setp = tk.Tk()
    setp.title("Set the Sphere")

    lb = Label(setp, text=" The figure is Sphere.\nEnter its parameter(s):")
    lb.grid(column=0, row=0, pady=10, padx=15)

    fr = tk.Frame(setp)
    fr.grid(row=1, column=0, pady=20) 
    lb1 = Label(fr, text="Radius")
    lb1.grid(column=0, row=0, padx=7)
    
    global radius
    radius = Entry(fr,width=5) 
    radius.grid(column=1, row=0, padx=8)
    radius.insert(0, str(r))
    radius.focus()

    btnOk = Button(fr, text="OK", width=4, command=OkSph)
    btnOk.grid(column=1, row=1, padx=8, pady=15)

    setp.geometry('150x150')
def OkSph():
    global r, setp
    r = float(radius.get())
    Sph()
    setp.destroy()
    
def Cyl():
    # cleaning the previous title
    lb = Label(window, text=45*" ")
    lb.grid(column=2, row=1)
    
    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()

    # printing the according title
    lb = Label(window, text="Cylinder")
    lb.grid(column=2, row=1)

    global r_cyl, h_cyl
    r=r_cyl; h=h_cyl;
    a=0; nt=100; nv =50;
    
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

    # naming the axes   
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # setting axes equal (aspect)
    scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz']); ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]]*3)
    
    canvas.get_tk_widget().grid(column=2, row=2)

    # set parameters button with relevant functions & save button
    GraphFrame = tk.Frame(window)
    btnSet = Button(GraphFrame, text="Set the parameters", width=20, command=SetCyl)
    btnSet.grid(column=0, row=0, padx=5)
    global name
    name = 'Cylinder.png' 
    btnSave = Button(GraphFrame, text="Save", width=10, command=Save)
    btnSave.grid(column=1, row=0, padx=5)
    GraphFrame.grid(row=3, column=2, pady=5)
def SetCyl():
    global setp
    setp = tk.Tk()
    setp.title("Set the Sphere")

    lb = Label(setp, text="The figure is Cylinder.\nEnter its parameter(s):")
    lb.grid(column=0, row=0, pady=10, padx=15)

    global radius, height
    fr = tk.Frame(setp)
    fr.grid(row=1, column=0, pady=20) 

    lb1 = Label(fr, text="Radius")
    lb1.grid(column=0, row=0, padx=7)
    radius = Entry(fr,width=5) 
    radius.grid(column=1, row=0, padx=8)
    radius.insert(0, str(r_cyl))

    lb2 = Label(fr, text="Height")
    lb2.grid(column=0, row=1, padx=7)
    height = Entry(fr,width=5) 
    height.grid(column=1, row=1, padx=8)
    height.insert(0, str(h_cyl))

    radius.focus()
    
    btnOk = Button(fr, text="OK", width=4, command=OkCyl)
    btnOk.grid(column=1, row=2, padx=8, pady=15)

    setp.geometry('150x170')
def OkCyl():
    global r_cyl, h_cyl, setp
    r_cyl = float(radius.get())
    h_cyl = float(height.get())
    Cyl()
    setp.destroy()
    
def Pyr():
    # cleaning the previous title
    lb = Label(window, text=45*" ")
    lb.grid(column=2, row=1)
    
    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    ax = fig.add_subplot(111, projection='3d')

    # printing the according title
    lb = Label(window, text="Pyramid")
    lb.grid(column=2, row=1)

    global b, h_pyr
    # vertices of a pyramid
    v = np.array([[0, 0, 0], [b, 0, 0], [b, b, 0],  [0, b, 0], [b/2, b/2, h_pyr]])
    ax.scatter3D(v[:, 0], v[:, 1], v[:, 2])

    # generate list of sides' polygons of our pyramid
    verts = [ [v[0],v[1],v[4]], [v[0],v[3],v[4]],[v[2],v[1],v[4]], [v[2],v[3],v[4]], [v[0],v[1],v[2],v[3]]]

    # plot sides
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(verts, 
    facecolors='cyan', linewidths=1, edgecolors='b', alpha=.25))

    # naming the axes
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # setting axes equal (aspect)
    scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz']); ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]]*3)
    
    canvas.get_tk_widget().grid(column=2, row=2)

    # set parameters button with relevant functions & save button
    GraphFrame = tk.Frame(window)
    btnSet = Button(GraphFrame, text="Set the parameters", width=20, command=SetPyr)
    btnSet.grid(column=0, row=0, padx=5)
    global name
    name = 'Pyramid.png' 
    btnSave = Button(GraphFrame, text="Save", width=10, command=Save)
    btnSave.grid(column=1, row=0, padx=5)
    GraphFrame.grid(row=3, column=2, pady=5)
def SetPyr():
    global setp
    setp = tk.Tk()
    setp.title("Set the Pyramid")

    lb = Label(setp, text="The figure is Pyramid.\nEnter its parameter(s):")
    lb.grid(column=0, row=0, pady=10, padx=15)

    global base, height
    fr = tk.Frame(setp)
    fr.grid(row=1, column=0, pady=20) 

    lb1 = Label(fr, text="Base length")
    lb1.grid(column=0, row=0, padx=7)
    base = Entry(fr,width=5) 
    base.grid(column=1, row=0, padx=8)
    base.insert(0, str(b))

    lb2 = Label(fr, text="Height")
    lb2.grid(column=0, row=1, padx=7)
    height = Entry(fr,width=5) 
    height.grid(column=1, row=1, padx=8)
    height.insert(0, str(h_pyr))

    base.focus()
    
    btnOk = Button(fr, text="OK", width=4, command=OkPyr)
    btnOk.grid(column=1, row=2, padx=8, pady=15)

    setp.geometry('150x170')
def OkPyr():
    global b, h_pyr, setp
    b = float(base.get())
    h_pyr = float(height.get())
    Pyr()
    setp.destroy()

def Paral():
    # cleaning the previous title
    lb = Label(window, text=45*" ")
    lb.grid(column=2, row=1)

    fig = plt.figure(figsize=(6,5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, window)
    canvas.draw()
    ax = fig.add_subplot(111, projection='3d')

    # printing the according title
    lb = Label(window, text="Parallelepiped")
    lb.grid(column=2, row=1)

    global s
    points = np.array([[0, 0, 0],
                  [s, 0, 0 ],
                  [s, s, 0],
                  [0, s, 0],
                  [0, 0, s],
                  [s, 0, s],
                  [s, s, s],
                  [0, s, s]])

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

    # naming the axes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # setting axes equal (aspect)
    scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz']); ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]]*3)
    
    canvas.get_tk_widget().grid(column=2, row=2)

    # set parameters button with relevant functions & save button
    GraphFrame = tk.Frame(window)
    btnSet = Button(GraphFrame, text="Set the parameters", width=20, command=SetParal)
    btnSet.grid(column=0, row=0, padx=5)
    global name
    name = 'Parallelepiped.png' 
    btnSave = Button(GraphFrame, text="Save", width=10, command=Save)
    btnSave.grid(column=1, row=0, padx=5)
    GraphFrame.grid(row=3, column=2, pady=5)
def SetParal():
    global setp
    setp = tk.Tk()
    setp.title("Set the Parallelepiped")

    lb = Label(setp, text="The figure is Parallelepiped.\nEnter its parameter(s):")
    lb.grid(column=0, row=0, pady=10, padx=15)

    fr = tk.Frame(setp)
    fr.grid(row=1, column=0, pady=20) 
    lb1 = Label(fr, text="One side")
    lb1.grid(column=0, row=0, padx=7)
    
    global side
    side = Entry(fr,width=5) 
    side.grid(column=1, row=0, padx=8)
    side.insert(0, str(s))

    lb2 = Label(fr, text="Two other sides")
    lb2.grid(column=0, row=1, padx=7)
    lb3 = Label(fr, text="2 * side1")
    lb3.grid(column=1, row=1, padx=7)
    side.focus()
    
    btnOk = Button(fr, text="OK", width=4, command=OkParal)
    btnOk.grid(column=1, row=2, padx=8, pady=15)

    setp.geometry('170x170')
def OkParal():
    global s, setp
    s = float(side.get())
    Paral()
    setp.destroy()

"""
# Using an existing stl file:
main_body = mesh.Mesh.from_file('RaspS.stl')

# find the max dimensions, so we can know the bounding box, getting the height, width, length (because these are the step size)...
minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(main_body)
w1 = maxx - minx
l1 = maxy - miny
h1 = maxz - minz
"""

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
canvas.create_text(width*0.6/8, height*0.6/8, text="VER 0.0.0 ")
canvas.pack()

# Showing the splash screen for 5000 milliseconds then destroying
root.after(5000, root.destroy)
root.mainloop()
print ("RaspiSnakes")

# Starting the main window 
window = tk.Tk()
window.iconbitmap('RaspSNK.ico')

lb = Label(window, text="STL editor")
lb.grid(column=0, row=0)
# File buttons
 
FileFrame = tk.Frame(window)
lb = Label(FileFrame, text="STL file")
lb.grid(column=0, row=0, padx=10, pady=0)
btnNew = Button(FileFrame, text="Empty", width=10, command=New)
btnNew.grid(column=0, row=1, padx=2)
FileFrame = tk.Frame(window)
btnNew = Button(FileFrame, text="New", width=10, command=New)
btnNew.grid(column=0, row=0, padx=2)
btnOpn = Button(FileFrame, text="Open", width=10, command=Opn)
btnOpn.grid(column=1, row=0, padx=3)
FileFrame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

# default parameters
r = 1.0 # radius of the sphere
l = 1.5 # length of the box
w = 1.0 # width of the box
h = 2.0 # height of the box

r_cyl = 10.0 # radius of the cylinder
h_cyl = 20.0 # height of the cylinder
b = 10.0 # base length of the pyramid
h_pyr = 10.0 # height of the pyramid
s = 2.0 # one side of the parallelepiped

# Figure plotting buttons
PlotFrame = tk.Frame(window)
lb = Label(PlotFrame, text="Choose a figure:\n")
lb.grid(column=0, row=0, padx=0, pady=0)
btnCub = Button(PlotFrame, text="Box", width=16, command=Cub)
btnCub.grid(column=0, row=1, pady=3)
btnSph = Button(PlotFrame, text="Sphere", width=16, command=Sph)
btnSph.grid(column=0, row=2, pady=2)
btnCyl = Button(PlotFrame, text="Cylinder", width=16, command=Cyl)
btnCyl.grid(column=0, row=3, pady=3)
btnPyr = Button(PlotFrame, text="Pyramid", width=16, command=Pyr)
btnPyr.grid(column=0, row=4, pady=2)
btnParal = Button(PlotFrame, text="Parallelepiped", width=16, command=Paral)
btnParal.grid(column=0, row=5, pady=3)
PlotFrame.grid(row=2, column=0, sticky="nsew", padx=31, pady=45)

window.title("Rasp Snakes Software VER 0.0.0")
 
window.geometry('800x600')





