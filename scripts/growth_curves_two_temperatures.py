import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def new_scale(vals, min, max):
    vals = np.asarray(vals)
    m = np.nanmin(vals)
    M = np.nanmax(vals)
    vals_new = (max-min)/(M-m) * (vals-M) + max
    return vals_new


dev_time = pd.read_csv('./data/dev_rate_corrected.csv')
growth_data = pd.read_csv('./data/individual_growth_curves.csv')

growth_data.temp = [float(float(t[:-1])) for t in growth_data.temp]

normalized_growth_data = {k: [] for k in growth_data.keys()[1:]}

fig, (ax1, ax2) = plt.subplots(1, 2, dpi=150)

for t, temp in growth_data.groupby('temp'):
    if t != 15.0 and t != 25:
        continue

    for r,replicate in temp.groupby('replicate'):
        dev_time_replicate = dev_time[(dev_time.temperature == t) & (dev_time.replicate == r + '_first_only')]

        if not len(dev_time_replicate):
            continue

        if list(dev_time_replicate.end_time)[0] == 0:
            continue

        replicate = replicate[replicate.timepoint <= list(dev_time_replicate.end_time)[0]]

        ax1.plot(replicate.timepoint, replicate.area, color='blue' if t == 15 else 'red', alpha=0.2)

        replicate.timepoint = new_scale(list(replicate.timepoint), 0, 1)
        replicate.area = list(replicate.area)

        ax2.plot(replicate.timepoint, replicate.area, color='blue' if t == 15 else 'red', alpha=0.2)

    ax1.plot([0], [0], color='blue' if t == 15 else 'red', label=t)


ax1.set_xlabel('Time (hr)')
ax1.set_ylabel('Size ($mm^2$)')
ax2.set_xlabel('Relative time')

ax1.legend(loc='lower right', title='Temperature:')
plt.show()
