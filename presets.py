"""
Parameter presets for TAMaker.

Import a config dict and unpack it directly into TAMaker::

    from presets import COLLECTION_CENTRAL
    maker = TAMaker(**COLLECTION_CENTRAL)

Plane encoding:  0=U induction,  1=V induction,  2=collection (Z)
"""

COLLECTION_CENTRAL = dict(
    plane=2,
    inspect_threshold=15e3,
    accept_threshold=55e3,
    cluster_cut=22e3,
    peak_adc_cut=80,
    tot_cut=8,
)

COLLECTION_LATERAL = dict(
    plane=2,
    inspect_threshold=15e3,
    accept_threshold=130e3,
    cluster_cut=30e3,
    peak_adc_cut=80,
    tot_cut=8,
)

INDUCTION_V_CENTRAL = dict(
    plane=1,
    inspect_threshold=3.5e3,
    accept_threshold=30e3,
    cluster_cut=5e3,
    peak_adc_cut=80,
    tot_cut=4,
)

INDUCTION_U_CENTRAL = dict(
    plane=0,
    inspect_threshold=3.2e3,
    accept_threshold=30e3,
    cluster_cut=4.5e3,
    peak_adc_cut=80,
    tot_cut=4,
)
