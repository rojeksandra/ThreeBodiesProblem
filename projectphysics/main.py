import scipy.integrate
import scipy as sci
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
plt.style.use('Solarize_Light2')

mass=1.989e+30
velocity=30000
radius= 5.326e+12
time=70*365*24*3600*0.5

G = 6.67408e-11

m1=5.0
m2=2.0
m3=1.0

v1=[0.02,0.01,0]
v1=np.array(v1)
v2=[-0.06,0,-0.1]
v2=np.array(v2)
v3=[0,-0.02,0]
v3=np.array(v3)

r1=[-1.5,0,0]
r1=np.array(r1)
r2=[0.5,0,0]
r2=np.array(r2)
r3=[0,0.5,0]
r3=np.array(r3)

def ThreeBody(w, t, G, m1, m2):
    r1 = w[:3]
    r2 = w[3:6]
    r3 = w[6:9]
    v1 = w[9:12]
    v2 = w[12:15]
    v3 = w[15:18]

    r12 = np.linalg.norm(r2 - r1)
    r13 = np.linalg.norm(r3 - r1)
    r23 = np.linalg.norm(r3 - r2)

    dv1pot = G*time*mass/(radius**2*velocity) * m2 * (r2 - r1) / r12 ** 3 + G*time*mass/(radius**2*velocity) * m3 * (r3 - r1) / r13 ** 3
    dr1pot = velocity * time / radius * v1
    dv2pot = G*time*mass/(radius**2*velocity) * m1 * (r1 - r2) / r12 ** 3 + G*time*mass/(radius**2*velocity) * m3 * (r3 - r2) / r23 ** 3
    dr2pot = velocity * time / radius * v2
    v12Link = np.concatenate((dv1pot, dv2pot))
    r12Link = np.concatenate((dr1pot, dr2pot))
    dv3pot = G*time*mass/(radius**2*velocity) * m1 * (r1 - r3) / r13 ** 3 + G*time*mass/(radius**2*velocity) * m2 * (r2 - r3) / r23 ** 3
    dr3pot = velocity*time/radius * v3
    rTogether = np.concatenate((r12Link, dr3pot))
    vTogether = np.concatenate((v12Link, dv3pot))
    wszystkieWyniki = np.concatenate((rTogether, vTogether))
    return wszystkieWyniki

initial_parameter=np.array([r1,r2,r3,v1,v2,v3])
timeSolve=np.linspace(0,10,700)
initial_parameter=initial_parameter.flatten()

three_body_sol=scipy.integrate.odeint(ThreeBody,initial_parameter,timeSolve,args=(G,m1,m2))
r1Solve=three_body_sol[:,:3]
r2Solve=three_body_sol[:,3:6]
r3Solve=three_body_sol[:,6:9]

fig=plt.figure(figsize=(10,10))
ax=fig.add_subplot(111,projection="3d")
ax.plot(r1Solve[:,0],r1Solve[:,1],r1Solve[:,2],color="blue")
ax.plot(r2Solve[:,0],r2Solve[:,1],r2Solve[:,2],color="black")
ax.plot(r3Solve[:,0],r3Solve[:,1],r3Solve[:,2],color="yellow")
ax.scatter(r1Solve[-1,0],r1Solve[-1,1],r1Solve[-1,2],color="blue",marker="o",s=50,label="M1")
ax.scatter(r2Solve[-1,0],r2Solve[-1,1],r2Solve[-1,2],color="black",marker="o",s=100,label="M2")
ax.scatter(r3Solve[-1,0],r3Solve[-1,1],r3Solve[-1,2],color="yellow",marker="o",s=150,label="M3")
ax.set_title("Problem 3 ciał\n",fontsize=14)
ax.set_xlabel("x",fontsize=18)
ax.set_ylabel("y",fontsize=18)
ax.set_zlabel("z",fontsize=18)

fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection="3d")

firstM = [ax.scatter(r1Solve[0, 0], r1Solve[0, 1], r1Solve[0, 2], color="blue", marker="o", s=50)]
secondM = [ax.scatter(r2Solve[0, 0], r2Solve[0, 1], r2Solve[0, 2], color="black", marker="o", s=100)]
thirdM = [ax.scatter(r3Solve[0, 0], r3Solve[0, 1], r3Solve[0, 2], color="yellow", marker="o", s=150)]

def Animate(i, firstM, secondM, thirdM):
    firstM[0].remove()
    secondM[0].remove()
    thirdM[0].remove()

    sciezka1 = ax.plot(r1Solve[:i, 0], r1Solve[:i, 1], r1Solve[:i, 2], color="blue")
    sciezka2 = ax.plot(r2Solve[:i, 0], r2Solve[:i, 1], r2Solve[:i, 2], color="black")
    sciezka3 = ax.plot(r3Solve[:i, 0], r3Solve[:i, 1], r3Solve[:i, 2], color="yellow")
    firstM[0] = ax.scatter(r1Solve[i - 1, 0], r1Solve[i - 1, 1], r1Solve[i - 1, 2], color="blue",marker="o", s=50)
    secondM[0] = ax.scatter(r2Solve[i - 1, 0], r2Solve[i - 1, 1], r2Solve[i - 1, 2], color="black",marker="o", s=100)
    thirdM[0] = ax.scatter(r3Solve[i - 1, 0], r3Solve[i - 1, 1], r3Solve[i - 1, 2], color="yellow",marker="o", s=150)
    return sciezka1, sciezka2, sciezka3, firstM, secondM, thirdM,

ax.set_xlabel("Oś X", fontsize=18)
ax.set_ylabel("Oś Y", fontsize=18)
ax.set_zlabel("Oś Z", fontsize=18)
ax.set_title("Problem 3 ciał \n", fontsize=18)
anim = animation.FuncAnimation(fig, Animate, interval=50, repeat=False, blit=False, fargs=(firstM, secondM, thirdM))
plt.show()
