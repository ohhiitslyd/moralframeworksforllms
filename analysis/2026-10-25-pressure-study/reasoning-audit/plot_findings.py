from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

OUT=Path(__file__).resolve().parent
FIG=OUT/'figures'


def save(fig,name):
    fig.tight_layout()
    for ext in ['png','svg']:
        fig.savefig(FIG/(name+'.'+ext),dpi=170)
    plt.close(fig)


def main():
    FIG.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
        'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none'})
    for file,name,title,labels in [
        ('partner_criterion_comparison.csv','partner-criterion-effect','Adding the same criterion to the partner', ['Welfare','Non-deception','Authority']),
        ('monitoring_cluster_intervals.csv','monitoring-effect','Watched minus unwatched: joint acceptance', ['All pairings','Welfare pairings','Non-deception pairings','Authority pairings'])]:
        data=pd.read_csv(OUT/file)
        fig,ax=plt.subplots(figsize=(10,4.7));fig.subplots_adjust(left=.25,bottom=.20)
        y=np.arange(len(data));v=data.difference_pp.to_numpy()
        ax.errorbar(v,y,xerr=np.array([v-data.ci_low_pp,data.ci_high_pp-v]),fmt='o',color='#236c94',capsize=5,markersize=7)
        ax.axvline(0,color='#7c8794',ls='--',lw=1)
        ax.set_yticks(y,[f'{label} (n={n:,})' for label,n in zip(labels,data.matched_cells)])
        ax.invert_yaxis();ax.set_xlabel('Difference in joint acceptance (percentage points)')
        ax.set_title(title,pad=20,fontweight='bold')
        lo,hi=data.ci_low_pp.min(),data.ci_high_pp.max();ax.set_xlim(min(lo-3,-3),max(hi+6,3))
        for i,row in data.iterrows():
            ax.text(row.ci_high_pp+.5,i,f'{row.difference_pp:+.1f}',va='center',fontsize=10)
        ax.text(0,-.27,'Exploratory 95% intervals: 10,000 bootstraps of 72 scenario clusters. n = matched cells.',transform=ax.transAxes,fontsize=9)
        save(fig,name)
    # Manually coded from the exact quoted messages in the linked casebook.
    fig,ax=plt.subplots(figsize=(10,4.5));x=np.arange(4)
    ax.plot(x,[0,1,0,1],'-o',color='#236c94',label='Agent A',lw=2.5,markersize=8)
    ax.plot(x,[1,0,1,0],'-s',color='#ce8a35',label='Agent B',lw=2.5,markersize=8)
    ax.set_xticks(x,['Public message 1','Public message 2','Public message 3','Private final action'])
    ax.set_yticks([0,1],['Refuse','Take']);ax.set_ylim(-.25,1.35)
    ax.set_title('A pair repeatedly swaps positions instead of converging',fontweight='bold',pad=15)
    ax.legend(loc='upper right',frameon=False);ax.grid(axis='y',alpha=.2)
    ax.text(0,-.22,'S068-L2-W-W-s1-watched · Each message reacts to the previous exchange. Final joint action: blocked.',transform=ax.transAxes,fontsize=9)
    save(fig,'reciprocal-switching-case')


if __name__=='__main__':
    main()
