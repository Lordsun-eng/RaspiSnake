import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

r=10; h=10; a =0; nt=100; nv =50;

theta = np.linspace(0, 2*np.pi, nt)
v = np.linspace(a, a+h, nv )
theta, v = np.meshgrid(theta, v)
x = r*np.cos(theta)
y = r*np.sin(theta)
z = v
rstride = 20
cstride = 10
ax.plot_surface(x, y, z, alpha=0.2, rstride=rstride, cstride=cstride)
ax.plot_surface(x, -y, z, alpha=0.2, rstride=rstride, cstride=cstride)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plt.show()
