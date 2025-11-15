"""
Yet again I am turning a 30 minute job into a 45 minute + 5 minute job

This module uses the rocketcea wrapper to execute, in particular,
Trade 1 on the deliverable
"""

from rocketcea.cea_obj import CEA_Obj, add_new_fuel
from thrust import mdot, thrust_calc, parse_str

MPFT = 0.3048 # constant for converting feet into meters

# Constant cea parameters as a dict
pms = {
    "Pc" : 300,
    "MR" : 1.4,
    "Ox" : "LOX",
    "Eps": 3.65
}

class CEAInputObj:
    """
    This should let me pass inputs as an optional parameter to be displayed
    on graphs like in multivar.py
    """

    def __init__(self):
        self.a_star = []
        self.ox = []
        self.of = []
        self.pressure = []

def ethanol_mix(ethanol, water):
    """
    Helper function to return a formatted card_str for the CEA add_new_fuel
    """

    return f"""
            fuel C2H5OH(L)   C 2 H 6 O 1
            h,cal=-66370.0      t(k)=298.15       wt%={ethanol}.
            fuel water H 2.0 O 1.0  wt%={water}
            h,cal=-68308.  t(k)=298.15 rho,g/cc = 0.9998
            """

# remember to use these exact names in the types list pls
add_new_fuel("75/25 eth", ethanol_mix(75, 25))
add_new_fuel("95/5 eth", ethanol_mix(95, 5))
add_new_fuel("50/50 eth", ethanol_mix(50,50))

def fuel_task(types: list) -> tuple[list[float], list[float], list[float]]:
    """
    Returns three lists containing c*, C_f, and Isp values respectively

    Different from parse.py in that it does not need to be flipped
    """

    cs_results = []
    cf_results = []
    isp_results = []

    for fuel in types:
        c = CEA_Obj(oxName=pms["Ox"], fuelName=fuel)
        # print(c.get_PambCf(Pc=pms["Pc"], MR=pms["MR"], eps=pms["Eps"])[0])

        # Get values for each metric, convert from ft/s to m/s
        cs_results.append(float(c.get_Cstar(pms["Pc"], pms["MR"])) * MPFT)
        cf_results.append(float(c.get_PambCf(Pc=pms["Pc"], MR=pms["MR"], eps=pms["Eps"])[0]))
        # isp returned properly in seconds
        ispVac = c.get_Isp(Pc=pms["Pc"], MR=pms["MR"], eps=pms["Eps"])*9.807
        isp_results.append(float(c.estimate_Ambient_Isp(Pc=pms["Pc"], MR=pms["MR"], eps=pms["Eps"])[0]))
        print(ispVac, isp_results)

    return cs_results, cf_results, isp_results

def get_thrust_res(pressures, ofs, astars, fuels):
    eps = 3.65

    mat = []
    for of in ofs: # colors
        e = []
        for fuel in fuels: # symbols
            c = CEA_Obj(oxName="LOX", fuelName=fuel)
            d = []
            for p in pressures: # y axis
                k = []
                # txt = c.get_full_cea_output(p, of, eps)
                con_r = 1545.349 # big boy molar constant in imperial
                
                mg = c.get_Throat_MolWt_gamma(p, of, eps)
                r = con_r/(mg[0])

                gamma = c.get_HeatCapacities(p, of, eps)[1] # at throat
                p_t = c.get_Throat_PcOvPe(p, of)
                big_t = c.get_Temperatures(p, of, eps)[1]
                c_star = c.get_Cstar(p, of)
                c_tau = c.get_PambCf(14.7, p, of)[0]

                print(c_star, c_tau)
                
                for a in astars: # x axis
                    m = mdot(a, p_t, big_t, r, gamma)
                    t = thrust_calc(m, c_star, c_tau)
                    k.append(t)
                d.append(k)
            e.append(d)
        mat.append(e)

    return mat
