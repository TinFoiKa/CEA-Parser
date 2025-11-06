"""
Yet again I am turning a 30 minute job into a 45 minute + 5 minute job

This module uses the rocketcea wrapper to execute, in particular,
Trade 1 on the deliverable
"""

from rocketcea.cea_obj import CEA_Obj, add_new_fuel

MPFT = 0.3048 # constant for converting feet into meters

# Constant cea parameters as a dict
pms = {
    "Pc" : 300,
    "MR" : 1.4,
    "Ox" : "LOX",
    "Eps": 3.65
}

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
        isp_results.append(float(c.get_Isp(Pc=pms["Pc"], MR=pms["MR"], eps=pms["Eps"])))

    print(cs_results)
    print(cf_results)
    print(isp_results)

    return cs_results, cf_results, isp_results
