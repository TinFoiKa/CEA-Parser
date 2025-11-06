"""
This is for multivariate graphing, recreating xvp_graph() in parse.py
to be modified to support nIV-1DV relationships

Used for thrust visualisation in bonus 1 and other graphings in bonus 2
"""

import matplotlib.pyplot as pl
import numpy as np

def nd_graph(tensor: np.array, layers: list[tuple[str, bool, list]], title = "") -> None:
    """
    This is the multidimensional visualisation function which takes an n-dimensional
    numpy matrix and serves to flexibly create a pyplot that can visualise 
    the said dataset (on a 3D cartesian system)

    The depth correspondence of this function should serve the statement, for 
    depth 'd' and matrix dimension n and parallel layers (list of tuples) parameter:

    * layers[d][0] is the name of the variable on the nth axis in the graph
    * layers[d][1] is False if the value is to be represented as continuous and True if categorical
    * layers[d][2] is the list of input values that make up the layer
    * layers[n] corresponds to the DV, and layers[n][2] = empty array []

    Conceptualising this means for a <x,y,z> 3D heatmap, layers[0][0] = 'x', 
    [1] = True, [2] = [1, ..., x_n], and tensor would be a 2-deep result matrix where x
    corresponds to layer 1 (i = 0) and y corresponds to layer 2 (i = 1)

    L1[ L2[ dv(x,y), ...], ...]

    Remarks:
    * 5th layer must be discrete (shape)
    * <x, y, colour, shape, time, z> is the maximum 5D representation (and corresponds to layers)
    * 3D representation (most common) is <x, y, z>
    * 4D representation should be presented as <x, y, colour/shape, z>
    * Categorical variables (like fuel) have a maximum length of 9
    
    Displays if not interrupted, returns None otherwise
    """
    
    # implementation right now is only 3 IV, 4 IV can be done
    # with some work but I lowk don't like graphics

    symbols = [".", "^", "2", "s", "+", "p", "*", "x", "d"]

    # pre-processing (establishing matrix depth):
    m_depth = tensor.ndim
    if m_depth > 5:
        return None
    
    if m_depth < 2:
        # I wish i could directly just impl parse.py's xvp_graph here
        # but alas they have entirely different data structures for results fr
        return None

    # isolate iv/dv arrays in layers
    iv_arr = layers[:-1]
    dv = layers[-1]

    # init pyplot
    fig = pl.figure()
    axis = fig.add_subplot(projection = '3d')

    # Meshgrid is stupid as fuck
    x = iv_arr[0][2]
    y = iv_arr[1][2]

    X,Y = np.meshgrid(x,y)
    X = X.ravel()
    Y = Y.ravel()

    # set up the layered scatter for 3 vars
    if m_depth == 3:
        # decide if we're using a symbol or heat map
        use_sym = layers[2][1]

        # this layers the scatter plots on top of each other
        for i, (t, l) in enumerate(zip(tensor, layers[2][2])):
            # ravel the 2d t to match X and Y dimension 1D
            Z = np.ravel(t)

            # if 3 IV and categorical, 
            if use_sym:
                # based on symbols
                axis.scatter3D(X, Y, Z, marker=symbols[i], label=l) 
            else: # if continuous, heat map
                axis.scatter3D(X, Y, Z, c=l, cmap='viridis')
    elif m_depth == 2:
        Z = np.ravel(tensor)
        
        # simple 3d scatter
        axis.scatter3D(X, Y, Z)

    # this behaviour is consistent for all graphs
    axis.set_xlabel(layers[0][0])
    axis.set_ylabel(layers[1][0])
    axis.set_zlabel(layers[2][0])

    # for use_sym
    if m_depth == 3 and layers[2][1]:
        axis.legend()

    axis.set_title("CEA Multivariate Relation to " + layers[-1][0])

    pl.show()
