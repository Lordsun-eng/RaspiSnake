from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import os
import numpy

VERTICE_COUNT = 100

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

# Load the STL files and add the vectors to the plot
your_mesh = mesh.Mesh.from_file('c:\Part1.stl')
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

# Auto scale to the mesh size
scale = your_mesh.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)
data = numpy.zeros(VERTICE_COUNT, dtype=mesh.Mesh.dtype)
