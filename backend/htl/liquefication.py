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
from exposan.htl import create_system, create_model


if __name__ == '__main__':
    # sys = create_system(
    #     configuration='baseline',             # system configurations ('baseline','no_P','PSA')
    #     capacity=100,                         # capacity in dry metric tonne per day
    #     sludge_moisture_content=0.7,          # the moisture content of the feedstock
    #     sludge_dw_ash_content=0.257,          # the ash content of the feedstock (dry weight%)
    #     sludge_afdw_lipid_content=0.204,      # the lipid content of the feedstock (ash-free dry weight%)
    #     sludge_afdw_protein_content=0.463,    # the protein content of the feedstock (ash-free dry weight%)
    #     N_2_P_value=0.3927,                     # the phosphorus to nitrogen mass ratio of the feedstock
    #     )
    # stream = sys.flowsheet.stream
    
    # model = create_model(
    #     system=sys,
    #     plant_size=True,
    #     feedstock='sludge',
    #     include_other_metrics=False,
    #     include_other_CFs_as_metrics=False,
    #     )
    
    model = create_model(
        # system=sys,
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
    # MGD = 1000000/ww_2_dry_sludge
    plant_size.baseline = 240*1e6*3.78541/24 # number from report, 240 MGD to kg/hr
    
    # Want MDSP (minimum diesel selling price) and GWP diesel (global warming potential of diesel)
    df = model.metrics_at_baseline()

    # Does not seem to work
    # plant_size.setter(MGD)
    # MDSP, GWP = [m for m in model.metrics if m.name in ('MDSP', 'GWP diesel')]
    # print(f'{MDSP.name}: ${MDSP.get():.2f} [{MDSP.units}]')
    # print(f'{GWP.name}: {GWP.get():.2f} [{GWP.units}]')
    
    