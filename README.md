# swiftpy

Minimal SWIFT trigger activity builder for DUNE-HD.

Takes a pickle file of Trigger Primitives (TPs)  and produces a DataFrame
of Trigger Activities (TAs) using local energy estimation in a fixed time grid + DBSCAN clustering.

## Dependencies

```
pip install numpy pandas numba tqdm
```

## Quickstart
### (see test.py)
```python
import pandas as pd
from tamaker import TAMaker
from presets import COLLECTION_CENTRAL

df = pd.read_pickle("my_tps.pkl")

maker = TAMaker(**COLLECTION_CENTRAL)
tas, tps = maker.run(df)

tas.to_pickle("tas.pkl")
tps.to_pickle("tps_annotated.pkl")
```

For large datasets spread across multiple runs:

```python
tas, tps = maker.run_by_run(df, output_ta="tas.pkl", output_tp="tps.pkl")
```

## Alg. Parts

1. **Filter** — TPs below `peak_adc_cut` or `tot_cut` are dropped.
2. **Window** — the readout is divided into fixed-width time bins. Each
   `(event, apa, rop, bin)` group is summed to give a window ADC total.
3. **Flag** — windows are flagged:
   - `flag=2` (accept) if window ADC > `accept_threshold`
   - `flag=1` (inspect) if window ADC > `inspect_threshold`
   - `flag=0` (reject) otherwise
4. **Cluster** — inspect windows go through DBSCAN. If the largest cluster
   exceeds `cluster_cut`, the flag is promoted to 2, otherwise it becomes 0.
5. **Output** — only flag-1 and flag-2 windows produce TA rows. The TP
   DataFrame is returned with `TA_id` and `dbscan_label` columns added.

## Presets

| Name                  | Plane | inspect thr | accept thr | cluster cut |
|-----------------------|-------|-------------|------------|-------------|
| `COLLECTION_CENTRAL`  | 2     | 15k         | 55k        | 15k         |
| `COLLECTION_LATERAL`  | 2     | 15k         | 130k       | 17k         |
| `INDUCTION_V_CENTRAL` | 1     | 3.5k        | 30k        | 5k          |
| `INDUCTION_U_CENTRAL` | 0     | 3.2k        | 30k        | 4.5k        |

You can also pass parameters directly to override anything:

```python
maker = TAMaker(**COLLECTION_CENTRAL, cluster_cut=20e3)
```

## Output columns

**tas**

| Column                | Description                                      |
|-----------------------|--------------------------------------------------|
| `event`               | Event number                                     |
| `apa_id`              | APA (detector module) index                      |
| `rop`                 | Readout plane index                              |
| `window_start`        | Start tick of the time window                    |
| `flag`                | 0=rejected, 2=accepted                           |
| `TA_id`               | Unique trigger activity ID                       |
| `total_window_energy` | Sum of TP ADC integrals in the window            |
| `TP_count`            | Number of TPs in the window                      |
| `n_clusters`          | DBSCAN clusters found (-1 for immediate accepts) |
| `max_cluster_energy`  | ADC sum of the largest cluster                   |
| `ch_mean`, `t_mean`   | Unweighted centroid of the TP cloud              |
| `ch_wmean`, `t_wmean` | Charge-weighted centroid                         |

**tps** — same as the input TP DataFrame filtered to the selected plane,
with `TA_id`, `dbscan_label`, and `window_start` columns added.
This can be used for associating TP-TA information 