##############################################################################
# Institute for the Design of Advanced Energy Systems Process Systems
# Engineering Framework (IDAES PSE Framework) Copyright (c) 2018-2020, by the
# software owners: The Regents of the University of California, through
# Lawrence Berkeley National Laboratory,  National Technology & Engineering
# Solutions of Sandia, LLC, Carnegie Mellon University, West Virginia
# University Research Corporation, et al. All rights reserved.
#
# Please see the files COPYRIGHT.txt and LICENSE.txt for full copyright and
# license information, respectively. Both files are also available online
# at the URL "https://github.com/IDAES/idaes-pse".
##############################################################################
"""
Example property package for Workshop Module 2.

Benzene-Toluene-Hydrogen-Methane system
IDeal VLE with non-condensables
"""
# Import Python libraries
import logging

from pyomo.environ import units as pyunits

# Import IDAES cores
from idaes.core import LiquidPhase, VaporPhase, Component
from idaes.core.phases import PhaseType as PT

from idaes.generic_models.properties.core.state_definitions import FpcTP
from idaes.generic_models.properties.core.eos.ideal import Ideal
from idaes.generic_models.properties.core.phase_equil import smooth_VLE
from idaes.generic_models.properties.core.phase_equil.bubble_dew import \
        IdealBubbleDew
from idaes.generic_models.properties.core.phase_equil.forms import fugacity

import idaes.generic_models.properties.core.pure.Perrys as Perrys
import idaes.generic_models.properties.core.pure.RPP as RPP
import idaes.generic_models.properties.core.pure.NIST as NIST

# Set up logger
_log = logging.getLogger(__name__)


# ---------------------------------------------------------------------
# Configuration dictionary for an ideal Benzene-Toluene system

# Data Sources:
# [1] The Properties of Gases and Liquids (1987)
#     4th edition, Chemical Engineering Series - Robert C. Reid
# [2] Perry's Chemical Engineers' Handbook 7th Ed.
#     Converted to J/mol.K, mol/m^3
# [3] Engineering Toolbox, https://www.engineeringtoolbox.com
#     Retrieved 1st December, 2019
# [4] NIST Webbook, https://webbook.nist.gov/
#     Retrieved 19th June, 2020. Converted from bar to Pa

configuration = {
    # Specifying components
    "components": {
        'benzene': {"type": Component,
                    "dens_mol_liq_comp": Perrys,
                    "enth_mol_liq_comp": Perrys,
                    "enth_mol_ig_comp": RPP,
                    "pressure_sat_comp": NIST,
                    "phase_equilibrium_form": {("Vap", "Liq"): fugacity},
                    "parameter_data": {
                        "mw": (78.1136E-3, pyunits.kg/pyunits.mol),  # [1]
                        "pressure_crit": (48.9e5, pyunits.Pa),  # [1]
                        "temperature_crit": (562.2, pyunits.K),  # [1]
                        "dens_mol_liq_comp_coeff": {
                            '1': (1.0162, pyunits.kmol*pyunits.m**-3),  # [2] pg. 2-98
                            '2': (0.2655, None),
                            '3': (562.16, pyunits.K),
                            '4': (0.28212, None)},
                        "cp_mol_ig_comp_coeff": {
                            'A': (-3.392E1, pyunits.J/pyunits.mol/pyunits.K),  # [1]
                            'B': (4.739E-1, pyunits.J/pyunits.mol/pyunits.K**2),
                            'C': (-3.017E-4, pyunits.J/pyunits.mol/pyunits.K**3),
                            'D': (7.130E-8, pyunits.J/pyunits.mol/pyunits.K**4)},
                        "cp_mol_liq_comp_coeff": {
                            '1': (1.29E5,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-1),  # [2]
                            '2': (-1.7E2,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-2),
                            '3': (6.48E-1,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-3),
                            '4': (0,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-4),
                            '5': (0,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-5)},
                        "enth_mol_form_liq_comp_ref": (
                            -49.0e3, pyunits.J/pyunits.mol),  # [3]
                        "enth_mol_form_vap_comp_ref": (
                            -82.9e3, pyunits.J/pyunits.mol),  # [3]
                        "pressure_sat_comp_coeff": {
                            'A': (4.60362, None),  # [4]
                            'B': (1701.073, pyunits.K),
                            'C': (20.806, pyunits.K)}}},
        'toluene': {"type": Component,
                    "dens_mol_liq_comp": Perrys,
                    "enth_mol_liq_comp": Perrys,
                    "enth_mol_ig_comp": RPP,
                    "pressure_sat_comp": NIST,
                    "phase_equilibrium_form": {("Vap", "Liq"): fugacity},
                    "parameter_data": {
                        "mw": (92.1405E-3, pyunits.kg/pyunits.mol),  # [1]
                        "pressure_crit": (41e5, pyunits.Pa),  # [1]
                        "temperature_crit": (591.8, pyunits.K),  # [1]
                        "dens_mol_liq_comp_coeff": {
                            '1': (0.8488, pyunits.kmol*pyunits.m**-3),  # [2] pg. 2-98
                            '2': (0.26655, None),
                            '3': (591.8, pyunits.K),
                            '4': (0.2878, None)},
                        "cp_mol_ig_comp_coeff": {
                            'A': (-2.435E1, pyunits.J/pyunits.mol/pyunits.K),
                            'B': (5.125E-1, pyunits.J/pyunits.mol/pyunits.K**2),
                            'C': (-2.765E-4, pyunits.J/pyunits.mol/pyunits.K**3),
                            'D': (4.911E-8, pyunits.J/pyunits.mol/pyunits.K**4)},
                        "cp_mol_liq_comp_coeff": {
                            '1': (1.40E5,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-1),  # [2]
                            '2': (-1.522,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-2),
                            '3': (6.95E-1,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-3),
                            '4': (0,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-4),
                            '5': (0,
                                  pyunits.J*pyunits.kmol**-1*pyunits.K**-5)},
                        "enth_mol_form_liq_comp_ref": (
                            -12.0e3, pyunits.J/pyunits.mol),  # [3]
                        "enth_mol_form_vap_comp_ref": (
                            -50.1e3, pyunits.J/pyunits.mol),  # [3]
                        "pressure_sat_comp_coeff": {
                            'A': (4.54436, None),  # [4]
                            'B': (1738.123, pyunits.K),
                            'C': (0.394, pyunits.K)}}},
        'hydrogen': {"type": Component,
                     "valid_phase_types": PT.vaporPhase,
                     "enth_mol_ig_comp": RPP,
                     "parameter_data": {
                         "mw": (2.016e-3, pyunits.kg/pyunits.mol),  # [1]
                         "pressure_crit": (12.9e5, pyunits.Pa),  # [1]
                         "temperature_crit": (33.0, pyunits.K),  # [1]
                         "cp_mol_ig_comp_coeff": {
                             'A': (2.714e1, pyunits.J/pyunits.mol/pyunits.K),
                             'B': (9.274e-3, pyunits.J/pyunits.mol/pyunits.K**2),
                             'C': (-1.381e-5, pyunits.J/pyunits.mol/pyunits.K**3),
                             'D': (7.645e-9, pyunits.J/pyunits.mol/pyunits.K**4)},
                         "enth_mol_form_vap_comp_ref": (
                             0, pyunits.J/pyunits.mol)}},  # standard state
        'methane': {"type": Component,
                    "valid_phase_types": PT.vaporPhase,
                    "enth_mol_ig_comp": RPP,
                    "parameter_data": {
                        "mw": (16.043e-3, pyunits.kg/pyunits.mol),  # [1]
                        "pressure_crit": (46e5, pyunits.Pa),  # [1]
                        "temperature_crit": (190.4, pyunits.K),  # [1]
                        "cp_mol_ig_comp_coeff": {
                            'A': (1.925e1, pyunits.J/pyunits.mol/pyunits.K),
                            'B': (5.213e-2, pyunits.J/pyunits.mol/pyunits.K**2),
                            'C': (1.197e-5, pyunits.J/pyunits.mol/pyunits.K**3),
                            'D': (-1.132e-8, pyunits.J/pyunits.mol/pyunits.K**4)},
                        "enth_mol_form_vap_comp_ref": (
                            -75e3, pyunits.J/pyunits.mol)}}},  # [3]

    # Specifying phases
    "phases":  {'Liq': {"type": LiquidPhase,
                        "equation_of_state": Ideal},
                'Vap': {"type": VaporPhase,
                        "equation_of_state": Ideal}},

    # Set base units of measurement
    "base_units": {"time": pyunits.s,
                   "length": pyunits.m,
                   "mass": pyunits.kg,
                   "amount": pyunits.mol,
                   "temperature": pyunits.K},

    # Specifying state definition
    "state_definition": FpcTP,
    "state_bounds": {"flow_mol_comp": (0, 100, 1000, pyunits.mol/pyunits.s),
                     "temperature": (273.15, 300, 1000, pyunits.K),
                     "pressure": (5e4, 1e5, 1e6, pyunits.Pa)},
    "pressure_ref": (101325, pyunits.Pa),
    "temperature_ref": (300, pyunits.K),

    # Defining phase equilibria
    "phases_in_equilibrium": [("Vap", "Liq")],
    "phase_equilibrium_state": {("Vap", "Liq"): smooth_VLE},
    "bubble_dew_method": IdealBubbleDew}
