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


    num = np.zeros_like(xgrid)
    for i in range(len(xgrid)):
        for j in range(len(ygrid)):
            num = 0
            dnm = 0
            for k in range(len(fsamples)):
                dist_squared = (xgrid[i][j] - xsamples[k])**2 + (ygrid[i][j] - ysamples[k])**2
                weight = 10000 * math.exp(-dist_squared/(2.0*std_dev**2))
                num += fsamples[k] * weight
                dnm += weight

            if dnm < 1e-20:
                f_interp[i][j] = 0
            else:
                f_interp[i][j] = num/dnm

    '''
    for i in range(len(xgrid)):
        for j in range(len(ygrid)):
            num = 0
            dnm = 0
            for k in range(len(fsamples)):
                dist_squared = (xgrid[i][j] - xsamples[k])**2 + (ygrid[i][j] - ysamples[k])**2
                weight = 10000 * math.exp(-dist_squared/(2.0*std_dev**2))
                num += fsamples[k] * weight
                dnm += weight

            if dnm < 1e-20:
                f_interp[i][j] = 0
            else:
                f_interp[i][j] = num/dnm
    '''

    '''
    for i in range(len(f_interp)):
        for j in range(len(f_interp[i])):
            if i == 0 and j == 0:
                print('a.a'),
            elif f_interp[i][j] > 0:
                print('x.x'),
            else:
                print('%.1f' %(f_interp[i][j])),
        print('')
    '''

    return f_interp


def main():

    xyrng = np.linspace(0, 1, 100)
    xgrid, ygrid = np.meshgrid(xyrng, xyrng)

    fgrid = f(xgrid, ygrid)

    xwalk, ywalk = np.random.random(size=(2, 500))

    fwalk = f(xwalk, ywalk)
    
    fwalk_interp = interpolate(xgrid, ygrid, xwalk, ywalk, fwalk)

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
