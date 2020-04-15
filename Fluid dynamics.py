#Importing python packages
import numpy as np
from matplotlib import pyplot as plt
import csv

#Empty lists
w=[]
z=[]
xpx=[]
ypx=[]
t_hour=[]
t_min=[]
t_sec=[]
t_msec=[]

#Reading rpm txt for time
with open("20130320_Track_17_5_rpm.txt","r+") as f:
    data=f.readlines()
    for line in data:
        t_hour.append(line.strip().split(",")[0])
    for line in data:
        t_min.append(line.strip().split(",")[1])
    for line in data:
        t_sec.append(line.strip().split(",")[2])
    for line in data:
        t_msec.append(line.strip().split(",")[3])


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

#Removing header from lists
xpx=xpx[1:]
ypx=ypx[1:]
w=w[1:]
z=z[1:]
t_hour=t_hour[1:]
t_min=t_min[1:]
t_sec=t_sec[1:]
t_msec=t_msec[1:]

#Changing string to int
def int_loop(Z):
  for i in range(0,len(Z)):
    Z[i]=int(Z[i])
  return Z

int_loop(xpx)
int_loop(ypx)

#Changing string to float
def float_loop(Z):
    for i in range(0, len(Z)):
        Z[i]=float(Z[i])
    return Z

float_loop(w)
float_loop(z)
float_loop(t_hour)
float_loop(t_min)
float_loop(t_sec)
float_loop(t_msec)

#Changing lists to arrays
xpxa=np.array(xpx)
ypxa=np.array(ypx)
wa=np.array(w)
za=np.array(z)


ta_hour=np.array(t_hour)
ta_min=np.array(t_min)
ta_sec=np.array(t_sec)
ta_msec=np.array(t_msec)

#Converting to time
ta= ta_hour*3600 + ta_min*60 + ta_sec + ta_msec/1000

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

#R/Rmax and omega converting to rad s-1
k=r/rmax
omega=17.5*0.1047

#Removing last point from array
new_r=np.delete(r,218)
new_k=np.delete(k,218)
new_t=np.delete(ta,218)

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
plt.plot(x,y,'r')
plt.title('Trajectory of black paper dot')
plt.show()
plt.plot(new_k,Ro,'r')
plt.title('Rossby number over r/rmax (wet experiment)')
plt.show()
plt.plot(new_t,ang_mom,'r')
plt.title('Angular momentum over time')
plt.show()
plt.plot(new_k,theory,'r')
plt.title('Theoretical Rossby prediction')
plt.show()
plt.plot(o,rossby,'r')
plt.title('Rossby number over r/rmax (Dry experiment)')
plt.show()

plt.subplot(3,1,1)
plt.plot(new_k,Ro,'r')
plt.title('Rossby number over r/rmax (wet experiment)')
plt.subplot(3,1,2)
plt.plot(o,rossby,'r')
plt.title('Rossby number over r/rmax (Dry experiment)')
plt.subplot(3,1,3)
plt.plot(new_k,theory,'r')
plt.title('Theoretical Rossby prediction')
plt.show()
