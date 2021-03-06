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
    data = np.zeros(100, dtype=mesh.Mesh.dtype)
    New = mesh.Mesh(data, remove_empty_areas=False)
    New.save('RaspS.stl', mode=stl.Mode.ASCII)
    loc_main_body = mesh.Mesh.from_file('RaspS.stl')
    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(loc_main_body.vectors))
    scale = loc_main_body.points.flatten('F')
    ax.auto_scale_xyz(scale, scale, scale)

    canvas.get_tk_widget().grid(row=0, column=1)
    canvas.draw()
    
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
    loc_main_body = mesh.Mesh.from_file('RaspS.stl')

    ax.add_collection3d(mplot3d.art3d.Poly3DCollection(loc_main_body.vectors))
    scale = loc_main_body.points.flatten('F')
    ax.auto_scale_xyz(scale, scale, scale)

    canvas.get_tk_widget().grid(row=0, column=1)
    canvas.draw()
    
def Save():
    pass

def Ext():
    quit()
    
def Cub():
    def Cubcal():
        HWL=[float(hc.get()), float(wc.get()), float(lc.get())]
        XYZ=[float(xc.get()),float(yc.get()),float(zc.get())]
        
        Nod=np.array([\
        [XYZ[0]-HWL[0]/2, XYZ[1]-HWL[1]/2, XYZ[2]-HWL[2]/2],
        [XYZ[0]+HWL[0]/2, XYZ[1]-HWL[1]/2, XYZ[2]-HWL[2]/2],
        [XYZ[0]+HWL[0]/2, XYZ[1]+HWL[1]/2, XYZ[2]-HWL[2]/2],
        [XYZ[0]-HWL[0]/2, XYZ[1]+HWL[1]/2, XYZ[2]-HWL[2]/2],
        [XYZ[0]-HWL[0]/2, XYZ[1]-HWL[1]/2, XYZ[2]+HWL[2]/2],
        [XYZ[0]+HWL[0]/2, XYZ[1]-HWL[1]/2, XYZ[2]+HWL[2]/2],
        [XYZ[0]+HWL[0]/2, XYZ[1]+HWL[1]/2, XYZ[2]+HWL[2]/2],
        [XYZ[0]-HWL[0]/2, XYZ[1]+HWL[1]/2, XYZ[2]+HWL[2]/2]])

        faces = np.array([\
            [0,3,1],
            [1,3,2],
            [0,4,7],
            [0,7,3],
            [4,5,6],
            [4,6,7],
            [5,1,2],
            [5,2,6],
            [2,3,6],
            [3,7,6],
            [0,1,5],
            [0,5,4]])
        
        # Create the mesh
        cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                cube.vectors[i][j] = Nod[f[j],:]
        openf = copy_obj(cube, (w1, l1, h1), 1, 1, 1)
    
        minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(cube)
        w2 = maxx - minx
        l2 = maxy - miny
        h2 = maxz - minz
        translate(cube, w1, w1 / 10., 3, 'x')
        main_body = mesh.Mesh.from_file('RaspS.stl')
        combined = mesh.Mesh(np.concatenate([main_body.data, cube.data]))
        combined.save('RaspS.stl', mode=stl.Mode.ASCII)  # save as ASCII
        loc_main_body = mesh.Mesh.from_file('RaspS.stl')

        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(loc_main_body.vectors))
        scale = loc_main_body.points.flatten('C')
        ax.auto_scale_xyz(scale, scale, scale)

        canvas.get_tk_widget().grid(row=0, column=1)
        canvas.draw()
        main_body=loc_main_body
        Cubimp.grab_release()
        Cubimp.destroy()
        
    def CubCLC():
        Cubimp.grab_release()
        Cubimp.destroy()
    
    Cubimp=tk.Toplevel()
    Cubimp.grab_set()
    Cubimp.overrideredirect(True)
    
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
            
    CFrame=tk.Frame(Cubimp)
    btnOK = tk.Button(CFrame, text = "OK" , width=10, height=1,command=Cubcal)
    btnCLC= tk.Button(CFrame, text = "Cancel" , width=10, height=1,command=CubCLC)
    btnOK.grid(column=0, row=1)
    btnCLC.grid(column=1, row=1)
    CFrame.grid(column=0, row=1)
    
    
        
    


    
def Sph():
    def Sphcal():
        n=20
        Rad=20
        dx=dz=n/Rad


        xc,yc,zc=0,0,0
        Nod=[]
        xmax=xc+Rad
        ymax=yc+Rad
        zmax=zc+Rad
        x=xc-Rad
        y=yc-Rad
        z=zc-Rad
        for Z in range(n):
            z=z+dz
            dx=math.sqrt(Rad**2-z**2)/n
            x=xc-math.sqrt(Rad**2-z**2)
            for X in range(n):
                y=math.sqrt(abs(Rad**2-z**2-x**2))
                Nod.append([x,y,z])
                x=x+dx
        Nod.append([0,0,zc-Rad])
        faces=[]
        nf=0
        for Z in range(n-1):
            
            for X in range(n):
                nf=nf+1
                if Z==0:
                    if X==19:
                        break
                    else:
                        faces.append([nf-1,nf,400])
                        faces.append([nf-1,nf+19,nf+18])
                    
                else:
                    if X==19:
                        break
                    elif X==0:
                        faces.append([nf-1,nf,nf+19])
                    else:
                        faces.append([nf-1,nf+19,nf+18])
                        faces.append([nf-1,nf,nf+19])
                    
            
        faces=np.array(faces)
        Nod=np.array(Nod)
        sph = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                sph.vectors[i][j] = Nod[f[j],:]
        SPH1 = mesh.Mesh(sph.data.copy())
        SPH2 = mesh.Mesh(sph.data.copy())
        SPH3 = mesh.Mesh(sph.data.copy())
        SPH4 = mesh.Mesh(sph.data.copy())
        SPH5 = mesh.Mesh(sph.data.copy())
        SPH2.rotate([0, 1.0, 0.0], math.radians(90))
        SPH3.rotate([0, 1.0, 0.0], math.radians(180))
        SPH4.rotate([0, 1.0, 0.0], math.radians(270))
        SPH5.rotate([1, 0, 0.0], math.radians(90))
        SPH6 = mesh.Mesh(SPH5.data.copy())
        SPH7 = mesh.Mesh(SPH5.data.copy())
        SPH8 = mesh.Mesh(SPH5.data.copy())
        SPH6.rotate([0, 1.0, 0.0], math.radians(90))
        SPH7.rotate([0, 1.0, 0.0], math.radians(180))
        SPH8.rotate([0, 1.0, 0.0], math.radians(270))
        sph = mesh.Mesh(np.concatenate([
        SPH1.data.copy(),
        SPH2.data.copy(),
        SPH3.data.copy(),
        SPH4.data.copy(),
        SPH5.data.copy(),
        SPH6.data.copy(),
        SPH7.data.copy(),
        SPH8.data.copy(),
        ]))

    
        openf = copy_obj(sph, (w1, l1, h1), 1, 1, 1)
    
        minx, maxx, miny, maxy, minz, maxz = find_mins_maxs(sph)
        w2 = maxx - minx
        l2 = maxy - miny
        h2 = maxz - minz
        translate(sph, w1, w1 / 10., 3, 'x')
        main_body = mesh.Mesh.from_file('RaspS.stl')
        combined = mesh.Mesh(np.concatenate([main_body.data, sph.data]))
        combined.save('RaspS.stl', mode=stl.Mode.ASCII)  # save as ASCII
        loc_main_body = mesh.Mesh.from_file('RaspS.stl')

        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(loc_main_body.vectors))
        scale = loc_main_body.points.flatten('C')
        ax.auto_scale_xyz(scale, scale, scale)
    
        canvas.get_tk_widget().grid(row=0, column=1)
        canvas.draw()
        main_body=loc_main_body
        Sphimp.grab_release()
        Sphimp.destroy()
    def SphCLC():
        Sphimp.grab_release()
        Sphimp.destroy()
        
    Sphimp=tk.Toplevel() 
    Sphimp.grab_set()
    Sphimp.overrideredirect(True)
    
    Spframe=tk.Frame(Sphimp)
    tk.Label(Spframe, text="Radius").grid(row=0)
    tk.Label(Spframe, text="X").grid(row=1)
    tk.Label(Spframe, text="Y").grid(row=2)
    tk.Label(Spframe, text="Z").grid(row=3)
    Rad = tk.Entry(Spframe)
    Rad.insert(tk.END, "1")
    
    xc = tk.Entry(Spframe)
    xc.insert(tk.END, "0")

    yc = tk.Entry(Spframe)
    yc.insert(tk.END, "0")

    zc = tk.Entry(Spframe)
    zc.insert(tk.END, "0")

    Rad.grid(row=0, column=1)
    xc.grid(row=3, column=1)
    yc.grid(row=4, column=1)
    zc.grid(row=5, column=1)
    Spframe.grid(row=0, column=0)
            
    CFrame=tk.Frame(Sphimp)
    btnOK = tk.Button(CFrame, text = "OK" , width=10, height=1,command=Sphcal)
    btnCLC= tk.Button(CFrame, text = "Cancel" , width=10, height=1,command=SphCLC)
    btnOK.grid(column=0, row=1)
    btnCLC.grid(column=1, row=1)
    CFrame.grid(column=0, row=1)

        
def Con():
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
# File toolbox
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
        
# Create toolbox
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


window.title("Rasp Snakes Software VER 0.01")
 
window.geometry('800x600')

fig = plt.Figure()
canvas = FigureCanvasTkAgg(fig, window)
canvas.get_tk_widget().grid(row=0, column=1)
main_body = mesh.Mesh.from_file('RaspS.stl')
ax = mplot3d.Axes3D(fig)
ax.add_collection3d(mplot3d.art3d.Poly3DCollection(main_body.vectors))
scale = main_body.points.flatten('F')
ax.auto_scale_xyz(scale, scale, scale)


canvas.draw()


window.mainloop()

