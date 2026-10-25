"""Matched partner-criterion comparison, with scenario-cluster bootstrap."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import psutil

OUT=Path(__file__).resolve().parent


def main():
    cpus=psutil.Process().cpu_affinity()
    if 0 in cpus and len(cpus)>1:
        psutil.Process().cpu_affinity([c for c in cpus if c!=0])
    data=pd.read_csv(OUT/'episode_metrics.csv')
    data=data[data.status=='complete']
    rng=np.random.default_rng(20261025)
    scenarios=sorted(data.scenario.unique())
    output=[]
    for code in ['W','D','A']:
        sub=data[data.pairing.isin([code+'-'+code,code+'-none'])]
        x=sub.pivot(index=['scenario','level','monitoring'],columns='pairing',values='mutual_take').dropna().reset_index()
        x['diff']=x[code+'-'+code]-x[code+'-none']
        groups=x.groupby('scenario')['diff'].agg(['sum','count']).reindex(scenarios,fill_value=0)
        draws=rng.integers(0,len(scenarios),(10000,len(scenarios)))
        boot=groups['sum'].to_numpy()[draws].sum(1)/groups['count'].to_numpy()[draws].sum(1)
        lo,hi=np.quantile(boot,[.025,.975])
        output.append(dict(rule=code,matched_cells=len(x),same_rule_rate=x[code+'-'+code].mean(),
            mixed_rate=x[code+'-none'].mean(),difference_pp=100*x['diff'].mean(),ci_low_pp=100*lo,ci_high_pp=100*hi))
    pd.DataFrame(output).to_csv(OUT/'partner_criterion_comparison.csv',index=False)
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
