import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.DataFrame(np.linspace(start=0,stop=10,num=11))

fig, axs = plt.subplots(nrows=2,ncols=2)
squared = np.square(df)
axs[0,0].plot(df,'bo')
axs[0,0].plot(-df,'ro')
axs[0,1].plot(squared,'g',label="Squares")
axs[0,0].plot(-squared,'b')

nums = np.random.randn(1,100).round(2)
new = np.cumsum(nums)
x = np.arange(0,100)

axs[1,0].plot(x,new,label="Toms Graph")
axs[1,0].set_xlim([20,60])

axs[0,1].legend()
axs[1,0].legend()

axs[1,1].set_xlabel(xlabel="Tom")
axs[1,1].set_ylabel(ylabel="Not Tom")

# Bottom Right Axis

xdata = np.linspace(start=0,stop=10*np.pi,num=1000)
ydata = np.sin(xdata)
axs[1,1].set_xticks([0,10*np.pi],minor=True)

data = np.stack((xdata,ydata),axis=1)
print(data)

axs[1,1].plot(xdata,ydata,label="Sin(x)")

plt.tight_layout()
plt.show()