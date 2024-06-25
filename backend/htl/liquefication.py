#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan-webapp: Web application for QSDsan

This module is developed by:
    
    Yalin Li <mailto.yalin.li@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/main/LICENSE.txt
for license details.
'''

import warnings
warnings.filterwarnings('ignore')

# Fuel unit conversion
# https://h2tools.org/hyarc/calculator-tools/lower-and-higher-heating-values-fuels

from chaospy import distributions as shape
from exposan.htl import create_model

def htl_calc(existing_flow):
    """
    Take existing flow in MGD (millions of gallons per day) and return the minimum diesel selling price and global warming potential of diesel.
    
    Parameters
    ----------
    existing_flow : float
        The existing flow in MGD.
    """
    
    model = create_model(
        plant_size=True,
        feedstock='sludge',
        include_CFs_as_metrics=False,
        include_other_metrics=False,
        include_other_CFs_as_metrics=False,
    )
    
    param = model.parameter
    sys = model.system
    stream = sys.flowsheet.stream
    
    raw_wastewater = stream.feedstock_assumed_in_wastewater
    dist = shape.Uniform(12618039,18927059)
    
    @param(name='plant_size',
            element=raw_wastewater,
            kind='coupled',
            units='kg/hr',
            baseline=15772549,
            distribution=dist)
    
    def set_plant_size(i):
        raw_wastewater.F_mass=i
    plant_size = model.parameters[-1]

    for p in model.parameters:
        if p.name == 'Ww 2 dry sludge': break
    ww_2_dry_sludge = p.baseline # metric tonne/d/MGD (million gallon per day)

    # Assume 1 million metric tonnes of dry sludge per day
    plant_size.baseline = existing_flow*1e6*3.78541/24 # number from report, x MGD to kg/hr
    df = model.metrics_at_baseline()
    
    # Want MDSP (minimum diesel selling price) and GWP diesel (global warming potential of diesel)
    MDSP, GWP = [m for m in model.metrics if m.name in ('MDSP', 'GWP diesel')]
    
    return MDSP.get(), GWP.get()

if __name__ == '__main__':
    
    import pandas as pd

    MDSP, GWP = htl_calc(240) # 240 MGD
    print(f'MDSP: ${MDSP:.2f} [$/gal diesel]')
    print(f'GWP: {GWP:.2f} [kg CO2/MMBTU diesel]')
    
    
    df = pd.read_csv(r"backend\htl\sludge_production_county_data.csv")
    
    # locate the flow mgd for warren    
    warren_flow_mgd = df.loc[df['County'] == 'Union ', 'Flow MGD'].values[0]
    print(warren_flow_mgd)

    MDSP, GWP = htl_calc(warren_flow_mgd) # 240 MGD
    print(f'MDSP: ${MDSP:.2f} [$/gal diesel]')
    print(f'GWP: {GWP:.2f} [kg CO2/MMBTU diesel]')

    
    
    