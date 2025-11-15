"""
This is a module for parsing NASA CEA Files to generate graphs for use cases
specific to the Rocket Project Application. In order of graphs generated:

1. Fuel v. Performance (FvP)

2. Chamber psia v. Performance (PvP)

3. O/F v. Performance (RvP)
"""

import matplotlib
import matplotlib.pyplot as pl
import numpy as np
import cea as c

matplotlib.rcParams['font.family'] = "Georgia"

# gravity (ms^-2) [fuck linters, jk I love you pylint]
LIL_G = 9.809

def parse_txt(file: str) -> list[list[float]]:
    """
    Helper function that flexibly reads input files and parses for performance data

    Basic logic is that it checks for key headings and reads the lines that follow
    (This is only marginally more work than just reading it I swear this is a good way of doing it)
    """
    # this is the result matrix (list list)
    results = []

    # opne file reading session
    with open(file, "r", encoding="utf-8") as parse:
        j2 = 0

        # line captures
        reserve = 0
        pp = []

        for line in parse:
            # Eg.: (notice 5 s.f., weird space)
            # PERFORMANCE PARAMETERS

            # Ae/At                      1.0000   5.3397
            # CSTAR, M/SEC               1573.9   1573.9
            # CF                         0.6505   1.5036
            # Ivac, M/SEC                1937.3   2654.4
            # Isp, M/SEC                 1023.9   2366.6

            # if key from found (below) is given, iterate next few reserve lines
            if reserve > 0:
                print(line, reserve)
                if reserve in (3, 4): # Cf and Cstar respectively
                    fl = float(line[37:44])
                    pp.append(fl)
                if reserve == 1: # Isp, end of chunk
                    fl = float(line[37:44])/LIL_G
                    pp.append(fl)
                    # append to large results list only at last reserve no
                    results.append(pp)
                    pp = [] # clean for next run

                reserve -= 1
                continue

            # jump heuristically by 80 lines on first and every find
            while j2 < 80:
                j2 += 1
                continue

            # once we've found "PERFORMANCE PARAMETERS", we know next 6 lines will have what we need
            if line.find("PERFORMANCE PARAMETERS") != -1:
                #reset loopwise heuristic jump
                j2 = 0
                # encapsulate next 6 runs of the loop
                reserve = 6

    # flip the 2d list 90 degrees (row col switch, row right now is trial, should be cs cf isp)
    results = list(map(list, zip(*results)))

    print(results)
    # the lion does not care for how many line parses are wasted, for it does not matter.
    return results


# Module-wide constants for graph creation
WIDTH = 10
HEIGHT = 5

def xvp_graph(x_label, iv, results):
    """
    Flexible helper function 2: IV change vs. Performance
    
    Takes dynamic list of IVs and CEA results and produces 3 graphs showing
    c*, C_f, and I_sp for different fuels or conditions.
    """

    # 3 x-axes layout
    fig, (cs, cf, isp) = pl.subplots(1, 3, figsize=(WIDTH, HEIGHT), layout="constrained")
    fig.suptitle(x_label + ' v. Performance')

    [cs_res, cf_res, isp_res] = results
    # print(results)

    x = np.arange(len(iv))
    width = 0.8 # bar width

    # 3 plots with formatted data
    cs.bar(x, np.array(cs_res).flatten(), width, color="orange")
    cs.set_xticks(x)
    cs.set_xticklabels(iv, rotation=45, ha='right')
    cs.set_ylabel('$c* (m/s)$')
    cs.set_ylim(ymin=1000)
    cs.grid(True, axis='y', linestyle='--', alpha=0.7)

    cf.bar(x, np.array(cf_res).flatten(), width)
    cf.set_xticks(x)
    cf.set_xticklabels(iv, rotation=45, ha='right')
    cf.set_ylabel('$C_{f}$')
    cf.set_ylim(ymin=1.3)
    cf.grid(True, axis='y', linestyle='--', alpha=0.7)

    isp.bar(x, np.array(isp_res).flatten(), width, color="green")
    isp.set_xticks(x)
    isp.set_xticklabels(iv, rotation=45, ha='right')
    isp.set_ylabel('$I_{sp} (s)$')
    isp.set_ylim(ymin=100)
    isp.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Adjust layout to prevent label cutoff
    pl.tight_layout()

    pl.show()

if __name__ == "__main__":
    # graph 1 Fuel v. Performance
    fuels = ["75/25 eth", '95/5 eth', "50/50 eth", "CH4", "Kerosene"]
    xvp_graph("Fuel Type",
              ["75/25 Ethanol", "95/5 Eth.", "50/50 Eth.", "Methane", "Kerosene"],
              c.fuel_task(fuels))

    # # graph 2 Chamber Pressure v. Performance
    xvp_graph("Chamber Pressure (psia)",
              [500, 400, 200, 150, 100],
              parse_txt("cea/pvP.txt"))

    # # graph 3 O/F Ratio v. Performance
    xvp_graph("O/F Ratio",
              [1.1, 1.2, 1.3, 1.5, 1.6, 1.7],
              parse_txt("cea/rvP.txt"))
