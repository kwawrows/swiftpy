import pandas as pd
from tamaker import TAMaker
from presets import COLLECTION_CENTRAL

df = pd.read_pickle("./data/neutron_col_tps.pkl") #raw tps from TPG

maker = TAMaker(**COLLECTION_CENTRAL)
tas, tps = maker.run(df)

tas.to_pickle("./trig_data/neutron_tas_col_central.pkl")
tps.to_pickle("./trig_data/neutron_tps_col_central.pkl")
