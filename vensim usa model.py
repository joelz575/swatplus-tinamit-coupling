"""
Python model 'vensim usa model.py'
Translated using PySD
"""

import numpy as np

from pysd.py_backend.functions import lookup, Integ
from pysd import cache

__pysd_version__ = "1.9.1"

__data = {"scope": None, "time": lambda: 0}

_subscript_dict = {}

_namespace = {
    "TIME": "time",
    "Time": "time",
    "Runnoff into channels": "runnoff_into_channels",
    "FertilizerN Use per ha": "fertilizern_use_per_ha",
    '"Banana Yields (SWAT+)"': "banana_yields_swat",
    "Net Farmer Income": "net_farmer_income",
    "Corn Selling Price Lookup": "corn_selling_price_lookup",
    "Agricultural Land": "agricultural_land",
    '"Corn Yields (SWAT+)"': "corn_yields_swat",
    "Cultivation Rate": "cultivation_rate",
    "Desired Agricultural Land": "desired_agricultural_land",
    "Fertigation Policy": "fertigation_policy",
    "Expected Profit": "expected_profit",
    "Supply Elasticity Lookup": "supply_elasticity_lookup",
    "Total FertlizerN Use": "total_fertlizern_use",
    "Max Land per Person": "max_land_per_person",
    "Reference Profit": "reference_profit",
    '"Non-Agricultural Land"': "nonagricultural_land",
    "Production Cost": "production_cost",
    "Population": "population",
    "FertilizerN Cost": "fertilizern_cost",
    "FertilizerN Requirement per ha": "fertilizern_requirement_per_ha",
    "Banana Selling Price Lookup": "banana_selling_price_lookup",
    "Base Cost": "base_cost",
    "FINAL TIME": "final_time",
    "INITIAL TIME": "initial_time",
    "SAVEPER": "saveper",
    "TIME STEP": "time_step",
}

##########################################################################
#                            CONTROL VARIABLES                           #
##########################################################################


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


def time():
    return __data["time"]()


@cache.run
def final_time():
    """
    Real Name: FINAL TIME
    Original Eqn: 8
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    The final time for the simulation.
    """
    return 8


@cache.run
def initial_time():
    """
    Real Name: INITIAL TIME
    Original Eqn: 0
    Units: year
    Limits: (None, None)
    Type: constant
    Subs: None

    The initial time for the simulation.
    """
    return 0


@cache.step
def saveper():
    """
    Real Name: SAVEPER
    Original Eqn: TIME STEP
    Units: year
    Limits: (0.0, None)
    Type: component
    Subs: None

    The frequency with which output is stored.
    """
    return time_step()


@cache.run
def time_step():
    """
    Real Name: TIME STEP
    Original Eqn: 1
    Units: year
    Limits: (0.0, None)
    Type: constant
    Subs: None

    The time step for the simulation.
    """
    return 1


##########################################################################
#                             MODEL VARIABLES                            #
##########################################################################


@cache.run
def runnoff_into_channels():
    """
    Real Name: Runnoff into channels
    Original Eqn: 0
    Units: m^3
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 0


@cache.step
def fertilizern_use_per_ha():
    """
    Real Name: FertilizerN Use per ha
    Original Eqn: FertilizerN Requirement per ha*(1-(0.1*Fertigation Policy))
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return fertilizern_requirement_per_ha() * (1 - (0.1 * fertigation_policy()))


@cache.run
def banana_yields_swat():
    """
    Real Name: "Banana Yields (SWAT+)"
    Original Eqn: 10
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 10


@cache.step
def net_farmer_income():
    """
    Real Name: Net Farmer Income
    Original Eqn: "Corn Yields (SWAT+)"*Corn Selling Price Lookup(2008)+"Banana Yields (SWAT+)"*Banana Selling Price Lookup(2008)-Production Cost
    Units: $/ha
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        corn_yields_swat() * corn_selling_price_lookup(2008)
        + banana_yields_swat() * banana_selling_price_lookup(2008)
        - production_cost()
    )


def corn_selling_price_lookup(x):
    """
    Real Name: Corn Selling Price Lookup
    Original Eqn: ( [(2008,0)-(2016,300)],(2008,265),(2009,282.5),(2010,298.7),(2012,163),(2013,183.5),(2014,177.9),(2015,197),(2016,197.8))
    Units: $/tonne
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return lookup(
        x,
        [2008, 2009, 2010, 2012, 2013, 2014, 2015, 2016],
        [265, 282.5, 298.7, 163, 183.5, 177.9, 197, 197.8],
    )


@cache.step
def agricultural_land():
    """
    Real Name: Agricultural Land
    Original Eqn: INTEG ( Cultivation Rate, 8709.46)
    Units: ha
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_agricultural_land()


@cache.run
def corn_yields_swat():
    """
    Real Name: "Corn Yields (SWAT+)"
    Original Eqn: 1.3
    Units: tonne/ha
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1.3


@cache.step
def cultivation_rate():
    """
    Real Name: Cultivation Rate
    Original Eqn: MAX(MIN( Desired Agricultural Land-Agricultural Land , "Non-Agricultural Land" ), -Agricultural Land)/5
    Units: ha/year
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        np.maximum(
            np.minimum(
                desired_agricultural_land() - agricultural_land(),
                nonagricultural_land(),
            ),
            -agricultural_land(),
        )
        / 5
    )


@cache.step
def desired_agricultural_land():
    """
    Real Name: Desired Agricultural Land
    Original Eqn: Supply Elasticity Lookup(Expected Profit/Reference Profit)*Max Land per Person*Population
    Units: ha
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return (
        supply_elasticity_lookup(expected_profit() / reference_profit())
        * max_land_per_person()
        * population()
    )


@cache.run
def fertigation_policy():
    """
    Real Name: Fertigation Policy
    Original Eqn: 0
    Units:
    Limits: (0.0, 1.0, 1.0)
    Type: constant
    Subs: None


    """
    return 0


@cache.step
def expected_profit():
    """
    Real Name: Expected Profit
    Original Eqn: Net Farmer Income
    Units: $/ha
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return net_farmer_income()


def supply_elasticity_lookup(x):
    """
    Real Name: Supply Elasticity Lookup
    Original Eqn: ( [(0,0)-(1,1)],(0,0),(0.235474,0.0921053),(0.370031,0.223684),(0.434251,0.333333),(0.477064,0.425439),(0.504587,0.495614),(0.547401,0.618421),(0.602446,0.780702),(0.737003,0.890351),(1,1))
    Units:
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return lookup(
        x,
        [
            0,
            0.235474,
            0.370031,
            0.434251,
            0.477064,
            0.504587,
            0.547401,
            0.602446,
            0.737003,
            1,
        ],
        [
            0,
            0.0921053,
            0.223684,
            0.333333,
            0.425439,
            0.495614,
            0.618421,
            0.780702,
            0.890351,
            1,
        ],
    )


@cache.step
def total_fertlizern_use():
    """
    Real Name: Total FertlizerN Use
    Original Eqn: Agricultural Land*FertilizerN Use per ha
    Units: m*m*m
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return agricultural_land() * fertilizern_use_per_ha()


@cache.run
def max_land_per_person():
    """
    Real Name: Max Land per Person
    Original Eqn: 22.75
    Units: ha
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 22.75


@cache.run
def reference_profit():
    """
    Real Name: Reference Profit
    Original Eqn: 750
    Units: $/ha/year
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 750


@cache.step
def nonagricultural_land():
    """
    Real Name: "Non-Agricultural Land"
    Original Eqn: INTEG ( -Cultivation Rate, 14509.4)
    Units:
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return _integ_nonagricultural_land()


@cache.step
def production_cost():
    """
    Real Name: Production Cost
    Original Eqn: FertilizerN Use per ha*FertilizerN Cost+Base Cost
    Units: $/ha
    Limits: (None, None)
    Type: component
    Subs: None


    """
    return fertilizern_use_per_ha() * fertilizern_cost() + base_cost()


@cache.run
def population():
    """
    Real Name: Population
    Original Eqn: 1000
    Units: people
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 1000


@cache.run
def fertilizern_cost():
    """
    Real Name: FertilizerN Cost
    Original Eqn: 10
    Units: $/kg
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 10


@cache.run
def fertilizern_requirement_per_ha():
    """
    Real Name: FertilizerN Requirement per ha
    Original Eqn: 281.3
    Units:
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 281.3


def banana_selling_price_lookup(x):
    """
    Real Name: Banana Selling Price Lookup
    Original Eqn: ( [(2008,0)-(2016,400)],(2012,302.8),(2013,315.6),(2014,335.6),(2015,339.1),(2016,396.3))
    Units: $/tonne
    Limits: (None, None)
    Type: lookup
    Subs: None


    """
    return lookup(
        x, [2012, 2013, 2014, 2015, 2016], [302.8, 315.6, 335.6, 339.1, 396.3]
    )


@cache.run
def base_cost():
    """
    Real Name: Base Cost
    Original Eqn: 120
    Units: $/ha
    Limits: (None, None)
    Type: constant
    Subs: None


    """
    return 120


_integ_agricultural_land = Integ(
    lambda: cultivation_rate(), lambda: 8709.46, "_integ_agricultural_land"
)


_integ_nonagricultural_land = Integ(
    lambda: -cultivation_rate(), lambda: 14509.4, "_integ_nonagricultural_land"
)
