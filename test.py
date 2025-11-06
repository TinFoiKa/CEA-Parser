import matplotlib.pyplot as pl
import numpy as np

if __name__ == "__main__":
    fig = pl.figure()
    axis = fig.add_subplot(projection = '3d')

    axis.plot([0,1,2,3], [2,3,4,5], zs=[3,2,1,0], zdir='y', alpha=0.8)

    pl.show()