import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from matplotlib.animation import FuncAnimation
from matplotlib import animation
from matplotlib import gridspec
from matplotlib.colors import Normalize
from matplotlib.collections import LineCollection


def lowess_smooth(x, frac=0.025):
    x = np.asarray(x)
    return lowess(x, [i for i in range(len(x))], it=0, frac=frac)[:,1]

def new_scale(vals, min, max):
    vals = np.asarray(vals)
    m = np.nanmin(vals)
    M = np.nanmax(vals)
    vals_new = (max-min)/(M-m) * (vals-M) + max
    return vals_new

def tolerant_mean(arrs):
    lens = [len(i) for i in arrs]
    arr = np.ma.empty((np.max(lens),len(arrs)))
    arr.mask = True
    for idx, l in enumerate(arrs):
        arr[:len(l),idx] = l
    return np.nanmean(arr, axis=-1), np.nanstd(arr, axis=-1)

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def instantaneous(temps, tpc):
    response = []
    t, f = tpc
    for i1 in temps: 
        response.append(f[t == find_nearest(t, i1)][0])
    return response

def rate_summation_dev(tpc, regime):
    temp, fit = tpc

    dev_current = 0
    dev_completion = []
    dev_rate = []
    hours = 0
    for i,hourly_t in enumerate(regime):
        inst_dev = fit[temp == find_nearest(temp, hourly_t)]

        # print(find_nearest(temp, hourly_t), min(temp, key=lambda d: abs(d - hourly_t)), hourly_t)

        print(inst_dev)
        inst_dev = float(list(inst_dev)[0])
        # print(inst_dev)

        if dev_current > 1:
            dev_rate.append(np.nan)
            dev_completion.append(np.nan)
        else:
            dev_rate.append(inst_dev)
            dev_completion.append(dev_current)
            dev_current += inst_dev
            hours += 1

    return dev_rate, dev_completion, hours


def rate_summation_size(tpc, regime):
    temp, fit = tpc

    size_current = 0
    size_completion = []
    size_rate = []
    size = 0
    for i,hourly_t in enumerate(regime):
        inst_size = fit[temp == find_nearest(temp, hourly_t)]
        inst_size = float(list(inst_size)[0])

        size_rate.append(inst_size)
        size_completion.append(size_current)
        size_current += inst_size
        size += inst_size

    return size_rate, size_completion, size




dev_tpc = pd.read_csv('./data/dev_rate_tpc_hatch_conf_preds_rezende.csv')
growth_tpc = pd.read_csv('./data/growth_rate_tpc_conf_preds_rezende.csv')
dev_time = pd.read_csv('./data/dev_rate_corrected.csv')
growth_data = pd.read_csv('./data/individual_growth_curves.csv')


growth_data.temp = [float(float(t[:-1])) for t in growth_data.temp]

normalized_growth_data = {k: [] for k in growth_data.keys()[1:]}

for t, temp in growth_data.groupby('temp'):
    for r,replicate in temp.groupby('replicate'):
        dev_time_replicate = dev_time[(dev_time.temperature == t) & (dev_time.replicate == r + '_first_only')]

        if not len(dev_time_replicate):
            continue

        if list(dev_time_replicate.end_time)[0] == 0:
            continue

        replicate = replicate[replicate.timepoint <= list(dev_time_replicate.end_time)[0]]

        replicate.timepoint = new_scale(list(replicate.timepoint), 0, 1)
        replicate.area = new_scale(list(replicate.area), 0, 1)

        for k in normalized_growth_data.keys():
            normalized_growth_data[k].extend(replicate[k])


normalized_growth_data = pd.DataFrame(normalized_growth_data)

growth_coeff = []
for t, temp in normalized_growth_data.groupby('temp'):
    if t != 27.5:
        continue

    time = []
    area = []
    for i in np.arange(0, 1, 0.01):
        temp_filt = temp[(temp.timepoint > i) & (temp.timepoint < i + 0.1)]

        time.append(i)
        area.append(np.nanmean(temp_filt.area))

    area = np.asarray(area)
    area = lowess_smooth(area, 0.1)
    growth_coeff.extend(area[1:] - area[:-1])


growth_coeff = new_scale(growth_coeff, 0, 1) * 1.75


# Test on a particular setpoint
fig, (ax1, ax2) = plt.subplots(1, 2)

setpoint = 25

temp_regime = [setpoint for i in range(1000)]

rate_dev, comp_dev, hours = rate_summation_dev((dev_tpc.temp, dev_tpc.preds), temp_regime)
rate_growth, comp_growth, size = rate_summation_size((growth_tpc.temp, growth_tpc.preds), temp_regime[:hours])
len_diff = len(rate_growth) / len(growth_coeff)
rate = np.interp(
    [i/len_diff for i in range(len(rate_growth))],
    np.arange(0, len(growth_coeff)), growth_coeff
)

rate_growth = np.asarray(rate_growth) * rate


pred_growth = []
g = 0
for i in rate_growth:
    pred_growth.append(g)
    g += i

growth_data_test = growth_data[growth_data.temp == setpoint]

for r, replicate in growth_data_test.groupby('replicate'):
    area = lowess_smooth(replicate.area, 0.1)
    ax1.plot(replicate.timepoint[:len(area)-1], area[1:] - area[:-1], 'k-', alpha=0.2)

ax1.plot(replicate.timepoint[:len(area)-1], area[1:] - area[:-1], 'k-', alpha=0.2, label='Actual growth')

ax1.plot(list(range(hours)), rate_growth, 'r', linewidth=2, label='Predicted growth')
ax1.set_ylim(0, None)
ax1.set_xlabel('Time (hr)')
ax1.set_ylabel('Growth rate ($mm^2$/hr)')
ax1.legend()

for r, replicate in growth_data_test.groupby('replicate'):
    ax2.plot(replicate.timepoint, replicate.area, 'k-', alpha=0.2)

ax2.plot(replicate.timepoint, replicate.area, 'k-', alpha=0.2, label='Actual size')

ax2.plot(list(range(hours)), pred_growth, 'r', linewidth=2, label='Predicted size')

ax2.set_ylim(0, None)
ax2.set_xlabel('Time (hr)')
ax2.set_ylabel('Size ($mm^2$)')
ax2.legend()
plt.show()