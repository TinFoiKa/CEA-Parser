"""
This is for multivariate graphing, recreating xvp_graph() in parse.py
to be modified to support nIV-1DV relationships

Used for thrust visualisation in bonus 1 and other graphings in bonus 2
"""

import matplotlib.pyplot as pl
from matplotlib.font_manager import FontProperties
import numpy as np
import mplcursors

import cea as c

symbols = [".", "^", "2", "s", "+", "p", "*", "x", "d"]

# TODO: a lot of this stuff could do with some OOP refactoring but
# the developer is NOT touching OOP until things actually work
# some are marked with (OOP!) many prolly aren't

def max(results: list):
    """
    Takes in a list of values and the IVs that result in them (OOP!)

    Returns the maximum including the IVs
    """

    return

def graph4(layers: list[str, bool, list], XYZ, jk, axis):
    """
    This helper function is only for rendering the 4IV layer, as it's used for both
    m_depth == 4 and m_depth == 5 characteristic graphs


    """
    X, Y, Z = XYZ

    j, k = jk

    axis.scatter3D(X, Y, Z, marker=symbols[k], c=layers[3][2][j], 
                    label=layers[2][2][k], cmap = 'viridis',
                    depthshade=False)
    
        
def nd_graph(tensor: np.array, layers: list[tuple[str, bool, list]], title = "", constants = []) -> None:
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
    * <x, y, colour, shape, time, z> is the maximum 6D representation (and corresponds to layers)
    * 3D representation (most common) is <x, y, z>
    * 4D representation should be presented as <x, y, colour/shape, z>
    * Categorical variables (like fuel) have a maximum length of 9
    
    Displays if not interrupted, returns None otherwise
    """
    
    # implementation right now is only 3 IV, 4 IV can be done
    # with some work but I lowk don't like graphics

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

    # inputs (for now) is a parallel array for [names][values]
    if constants.__len__() > 0:
        tabax = fig.add_subplot(projection='3d')
        tabax.axis('off')
        table = tabax.table(constants, colLabels=['Constant', 'Value'], loc ='left')
        table.auto_set_column_width([0,1])
        # Make headers bold
        for (row, col), cell in table.get_celld().items():
            if row == 0 or col == -1:
                cell.set_text_props(fontproperties=FontProperties(weight='bold'))
            
    axis = fig.add_subplot(projection = '3d')
    axis.xaxis.pane.fill = False
    axis.yaxis.pane.fill = False
    axis.zaxis.pane.fill = False
    axis.zaxis.pane.set_linestyle('none')

    

    # Meshgrid is stupid as fuck
    x = iv_arr[0][2]
    y = iv_arr[1][2]

    # if any side is categorical, turn into numerical values but reset ticks
    x_temp = x
    y_temp = y
    if layers[0][1]:
        x = np.arange(x.__len__())
    if layers[1][1]:
        y = np.arange(y.__len__())
    X,Y = np.meshgrid(x,y)
    X = X.ravel()
    Y = Y.ravel()

    # 5th is just 4 + a time slider
    if m_depth == 5:
        # stack holds the Z and the j, and k that Z value is found at
        # consider that i is encapsulated in the direct index of the list
        stack = []
        
        for t in tensor:
            for j, m in enumerate(t):
                for k, d in enumerate(m):
                    Z = np.ravel(d)
                    stack.append([Z, j, k])
        
        # list that the 'time' slider should be demarcated with
        ran = layers[-2][2]



        axis.colorbar(label=layers[2][0])
    # omg 4 vars is soooo quirky
    elif m_depth == 4:
        # this first unpacking is for the first variable layer
        for j, t in enumerate(tensor):
            # this one peels us into 2D
            for k, m in enumerate(t):
                Z = np.ravel(m)
                graph4(tensor, layers, [X,Y,Z], axis)

        axis.colorbar(label=layers[2][0])
    # set up the layered scatter for 3 vars
    elif m_depth == 3:
        # decide if we're using a symbol or heat map
        use_sym = layers[2][1]

        # this layers the scatter plots on top of each other
        for i, (t, l) in enumerate(zip(tensor, layers[2][2])):
            # ravel the 2d t to match X and Y dimension 1D
            Z = np.ravel(t)

            # if 3 IV and categorical, 
            if use_sym:
                # based on symbols
                axis.scatter3D(X, Y, Z, marker=symbols[i], label=l, depthshade=False) 
            else: # if continuous, heat map
                axis.scatter3D(X, Y, Z, c=l, cmap='viridis', depthshade=False)
                
            # # Draw thin lines from each point to the xy-plane (z=0)
            # for i in range(len(X)):
            #     axis.plot([X[i], X[i]], [Y[i], Y[i]], [Z[i], 0], c='blue', linewidth=0.5, alpha=0.7)
                    
        if not use_sym:
            axis.colorbar(label=layers[2][0])
    elif m_depth == 2:
        Z = np.ravel(tensor)
        print(X, Y, Z)
        
        # simple 3d scatter
        axis.scatter3D(X, Y, Z, alpha=0.7, depthshade=True)

        if layers[0][1]:
            axis.set_xticks(x)
            axis.set_xticklabels(x_temp, rotation=10)
        if layers[1][1]:
            axis.set_yticks(y)
            axis.set_yticklabels(y_temp, rotation=23)

        # Draw thin lines from each point to the xy-plane (z=0)
        for i in range(len(X)):
            axis.plot([X[i], X[i]], [Y[i], Y[i]], [Z[i], Z.min()-10], c='b', linewidth=0.6, alpha=0.5)
    
    axis.set_zlim3d(Z.min()-10)

    # this behaviour is consistent for all graphs
    axis.set_xlabel(layers[0][0])
    axis.set_ylabel(layers[1][0], labelpad=10)
    axis.set_zlabel(layers[-1][0], labelpad=10)

    # add an input display on the side (?)

    # for use_sym
    if m_depth == 3 and layers[2][1]:
        axis.legend(loc='upper center', bbox_to_anchor=(1, 0),
                    ncol=2, title=layers[2][0])

    title = "CEA Multivariate Relation to " + layers[-1][0] if title == "" else title
    axis.set_title(title)

    fig.tight_layout()

    # TODO: cursor update handling for point hovering
    # cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Transient)

    # @cursor.connect("add")
    # def on_add(sel):
    #     x, y, width, height = sel.artist[sel.index].get_bbox().bounds
    #     sel.annotation.set(text=f"{x+width/2}: {height}", position=(0, 20), anncoords="offset points")
    #     sel.annotation.xy = (x + width / 2, y + height)

    pl.show()

def i2_test_1():
    # 2 IV test case 1 is fuel + O/F v. Isp
    fuel_types = ["75/25 eth", '95/5 eth', "50/50 eth", "CH4", "Kerosene"]
    of_ratios = [1.1, 1.2, 1.3, 1.5, 1.6, 1.7]

    # results in Isp
    isp_res = []

    for fuel in fuel_types:
        obj = c.CEA_Obj(oxName=c.pms["Ox"], fuelName=fuel)
        of_res = []
        for of in of_ratios:
            of_res.append(float(obj.get_Isp(Pc=c.pms["Pc"], MR=of, eps=c.pms["Eps"])))

        isp_res.append(of_res)

    # isp_res is our tensor array, which means we convert it
    tensor = np.array(isp_res)

    layers = [
        tuple(['O/F Ratios', False, of_ratios]),
        tuple(['Fuel Type', True, fuel_types]),
        tuple(['$I_{sp} (s)$', False, []])
    ]
    
    constants = [
        ["Oxidiser", 'LOx'],
        ["Pressure (psia)", c.pms["Pc"]],
        ["A/A*", c.pms["Eps"]]
    ]

    nd_graph(tensor, layers, constants=constants)

def i2_test_2():
    # This case is Chamber pressure and O/F Ratio
    of_ratios = [1.1, 1.2, 1.3, 1.5, 1.6, 1.7]
    pressures = [100, 200, 300, 400, 500]

    # results in Isp
    isp_res = []

    for p in pressures:
        obj = c.CEA_Obj(oxName=c.pms["Ox"], fuelName="75/25 eth")
        of_res = []
        for of in of_ratios:
            of_res.append(float(obj.get_Isp(Pc=p, MR=of, eps=c.pms["Eps"])))

        isp_res.append(of_res)

    # isp_res is our tensor array, which means we convert it
    tensor = np.array(isp_res)

    layers = [
        tuple(['O/F Ratios', False, of_ratios]),
        tuple(['Pressures (psia)', True, pressures]),
        tuple(['$I_{sp} (s)$', False, []])
    ]
    
    constants = [
        ["Oxidiser", 'LOx'],
        ["Fuel", "75/25 Ethanol"],
        ["A/A*", c.pms["Eps"]]
    ]

    nd_graph(tensor, layers, constants=constants)

def i3_test_1():
    # 2 IV test case 1 is fuel + O/F + pressures v. Isp
    # 2 IV test case 1 is fuel + O/F v. Isp
    fuel_types = ["75/25 eth", '95/5 eth', "50/50 eth", "CH4", "Kerosene"]
    of_ratios = [1.1, 1.2, 1.3, 1.5, 1.6, 1.7]
    pressures = [100, 200, 300, 400, 500]

    # results in Isp
    isp_res = []

    for fuel in fuel_types:
        obj = c.CEA_Obj(oxName=c.pms["Ox"], fuelName=fuel)
        of_res = []
        for of in of_ratios:
            p_res = []
            for p in pressures:
                p_res.append(float(obj.get_Isp(Pc=p, MR=of, eps=c.pms["Eps"])))

            of_res.append(p_res)
        isp_res.append(of_res)

    # isp_res is our tensor array, which means we convert it
    tensor = np.array(isp_res)

    layers = [
        tuple(['Pressure (psia)', False, pressures]),
        tuple(['O/F Ratios', False, of_ratios]),
        tuple(['Fuel Type', True, fuel_types]),
        tuple(['$I_{sp} (s)$', False, []])
    ]

    nd_graph(tensor, layers)

def i5_test_1():
    return

if __name__ == "__main__":
    i2_test_1()
    i2_test_2()
    i3_test_1()
