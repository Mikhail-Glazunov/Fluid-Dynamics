#Importing python packages
import numpy as np
from matplotlib import pyplot as plt
import csv

#Empty lists
w=[]
z=[]
xpx=[]
ypx=[]
t=[]

#Reading windspeed csv
with open('radius_windspeed.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for line in readCSV:
        w.append(line[0])
        z.append(line[1])

#Reading rpm txt
with open("20130320_Track_17_5_rpm.txt","r+") as f:
    data=f.readlines()
    for line in data:
        xpx.append(line.strip().split(",")[4])
    for line in data:
        ypx.append(line.strip().split(",")[5])
    for line in data:
        t.append(line.strip().split(",")[2:4])

#Removing header from lists
xpx=xpx[1:]
ypx=ypx[1:]
w=w[1:]
z=z[1:]
t=t[1:]

#Changing time to more reasonable format
for i in range(0, len(t)):
    t[i]=','.join(t[i])
for i in range(0, len(t)):
    t[i]=t[i].replace(",","")
for i in range(0, len(t)):
    t[i]=t[i].replace("0","",1)

#Changing string to int
def int_loop(Z):
  for i in range(0,len(Z)):
    Z[i]=int(Z[i])
  return Z

int_loop(t)
int_loop(xpx)
int_loop(ypx)

#Changing string to float
def float_loop(Z):
    for i in range(0, len(Z)):
        Z[i]=float(Z[i])
    return Z

float_loop(w)
float_loop(z)

#Changing lists to arrays
xpxa=np.array(xpx)
ypxa=np.array(ypx)
wa=np.array(w)
za=np.array(z)
ta=np.array(t)/1000

#Points
X=xpxa-206
Y=-(ypxa-173)

#Rmax value
xmax=X[0]
ymax=Y[0]
rmax=np.sqrt(np.square(xmax)+np.square(ymax))

#Radius
r=np.sqrt(np.square(X)+np.square(Y))

#Theta
theta=np.arctan(Y/X)

#Delta
diff_r=np.diff(r)
diff_t=np.diff(ta)
diff_theta=np.diff(theta)
#Removing negative values from diff theta
for i in range(len(diff_theta)):
    if diff_theta[i]<0:
        diff_theta[i]+=np.pi

#Ur and Utheta
ur=diff_r/diff_t
utheta=diff_theta/diff_t

#R/Rmax and omega
k=r/rmax
omega=17.5

#Removing last point from array
new_r=np.delete(r,218)
new_k=np.delete(k,218)
new_t=np.delete(t,218)

#Rossby number
Ro=utheta/(2*omega*new_r)

#Dry experiment data
wmax=wa[0]
o=wa/wmax
thet=omega*((np.square(wmax)-np.square(wa))/wa)
rossby=thet/(2*omega*wa)

#Angular momentum
U_theta=utheta+omega*new_r
ang_mom=U_theta*new_r

#Changing pixels to physical units
db=430
de=402
ti=16250
tf=49828
asd=((28)/(tf-ti)*1000)
x=(asd*X+173)/28
y=(asd*Y+206)/28

#Angular momentum
U_theta=utheta+omega*new_r
ang_mom=U_theta*new_r

#Theoretical rossby
theory=1/2*((np.square(rmax))/(np.square(new_r))-1)

#Plotting functions
plt.plot(x,y)
plt.show()
plt.plot(new_k,Ro)
plt.show()
plt.plot(new_t,ang_mom)
plt.show()
plt.plot(new_k,theory)
plt.show()
plt.plot(o,rossby)
plt.show()