import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT
from matplotlib.figure import Figure
import openmesh as om
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot

## Splash Screen
# create a splash screen, 80% of display screen size, centered,
# displaying a GIF image with needed info, disappearing after 5 seconds
root = tk.Tk()
# show no frame
root.overrideredirect(True)
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (width*0.8, height*0.8, width*0.1, height*0.1))
# take a .jpg picture you like, add text with a program like PhotoFiltre
# (free from http://www.photofiltre.com) and save as a .gif image file

#assert os.path.exists(image_file)
# use Tkinter's PhotoImage for .gif files
image = tk.PhotoImage(file="Splash.gif")
canvas = tk.Canvas(root, height=height*0.8, width=width*0.8, bg="brown")
canvas.create_image(width*0.8/2, height*0.8/2, image=image)
canvas.pack()
# show the splash screen for 5000 milliseconds then destroy
root.after(5000, root.destroy)
root.mainloop()
# your console program can start here ...
print ("RaspiSnakes")

def Opn():
    window.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.stl"),("all files","*.*")))
    fileout =window.filename
    print(fileout)
    currfile = mesh.Mesh.from_file('part1.stl')
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
    

    pass
def Sph():
    pass
def Cyl():
    pass

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

btnOpn = Button(ToolboxGen, text="Open", width=10, command=Opn)
btnOpn.grid(column=0, row=1)
ToolboxGen.grid(row=0, column=1, sticky="nsew")

window.title("Rasp Snakes CAD Software VER 0.0.0")
 
window.geometry('800x600')






