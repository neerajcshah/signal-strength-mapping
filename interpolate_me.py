import math
import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return np.sin(4*np.pi*x) * np.cos(4*np.pi*y)

# should return fgrid such that it agrees with the samples
def interpolate(xgrid, ygrid, xsamples, ysamples, fsamples):
    std_dev = .1
    f_interp = np.zeros_like(xgrid)

    print('xgrid',xgrid.shape)
    print('xsamples', xsamples.shape)
    print('fsamples', fsamples.shape)

    dnm = np.zeros_like(xgrid)
    num = np.zeros_like(xgrid)
    
    xgrid = np.tile(xgrid, (len(fsamples),1,1))
    ygrid = np.tile(ygrid, (len(fsamples),1,1))
    
    x_y_f = np.array([xsamples, ysamples, fsamples],dtype=np.float32)
    weight = np.zeros((len(xgrid),len(ygrid), len(fsamples)))
    
    weight = 10000.*np.exp(-(np.square(xgrid.transpose() - x_y_f[0]).transpose() + np.square(ygrid.transpose() - x_y_f[1]).transpose())/(2.0*std_dev**2))
    
    ### now collapse weight into dnm
    dnm = np.sum(weight, axis=0)
    ### Build num from weight and sample f 
    num = np.sum((weight.transpose() * x_y_f[2]).transpose(), axis=0)
    
    return np.where(dnm < 1e-20, 0, num/dnm) 



def main():

    xyrng = np.linspace(0, 1, 100)
    xgrid, ygrid = np.meshgrid(xyrng, xyrng)

    fgrid = f(xgrid, ygrid)

    xwalk, ywalk = np.random.random(size=(2, 500))

    fwalk = f(xwalk, ywalk)
    
    fwalk_interp = interpolate(xgrid, ygrid, xwalk, ywalk, fwalk)
    print(fwalk_interp)
    plt.subplot(1,2,1)
    plt.pcolormesh(xyrng, xyrng, fgrid)
    plt.plot(xwalk, ywalk, 'k.')
    plt.axis('equal')

    plt.subplot(1,2,2)
    plt.pcolormesh(xyrng, xyrng, fwalk_interp)
    #sc = plt.scatter(xwalk, ywalk, c=fwalk)
    #plt.colorbar(sc)
    plt.title('should match image to the left')
    plt.axis('equal')

    
    plt.show()

if __name__ == '__main__':
    main()
