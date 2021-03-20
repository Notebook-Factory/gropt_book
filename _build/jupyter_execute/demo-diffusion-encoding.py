# Diffusion Encoding Gradients Example

import os

os.chdir("./python/")

import build_gropt
build_gropt.build_gropt()
import gropt

from helper_utils import *
from interactive_plots import plot_waveform_interactive
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from IPython.core.display import display, HTML
init_notebook_mode(connected = True)
config={'showLink': False, 'displayModeBar': False}
from timeit import default_timer as timer

%matplotlib inline

## Constraints on:
- Maximum gradient amplitude: params['gmax']
- Maximum slew rate: params['smax']
- Zero gradient moment = 0 (mT*ms)/m
- Add objective function to maximize b-value
- Add constraint to turn gradients off during excitation RF (T_90), refocusing RF (T_180), and ADC readout (T_redout)

params = {}
params['mode'] = 'diff_bval'   # Objective function that maximizes b-value
params['gmax'] = 50            # Maximum gradient amplitude, mT/m
params['smax'] = 100           # Maximum slew rate, mT/m/ms
params['MMT'] = 0              # Nulling M0
params['T_readout'] = 20       # Time from start to center of readout, ms
params['T_90'] = 3             # Duration of excitation RF pulse, ms
params['T_180'] = 5            # Duration of refocusing RF pulse, ms
params['b'] = 1000             # Diffusion b-value, s/mm^2
params['dt'] = 400e-6          # Raster time of the gradient waveform being optimized

# Convex Optimized Diffusion Encoding (CODE)
G_min, T_min = get_min_TE(params, bval=params['b'], min_TE = 40, max_TE = 120)
print('Minimum TE =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(-1*G_min, params, plot_eddy = False, plot_pns = False, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

## M0 Nulled CODE

Generate a waveform with $M_0 = 0$, other parameters as listed in the code.

TE was manually selected (44.4 ms) to hit b-value = 600

params = {}
# Maximize b-value for diffusion waveforms
params['mode'] = 'diff_bval'

# Hardware constraints
params['gmax']  = 50.0 # Max Gradient Amplitude [mT/m], you can use T/m here too
params['smax']  = 50.0 # Max Slewrate [mT/m/ms]

# Moment nulling
params['MMT']  = 0

# Sequence TE and dt of output [ms]
params['TE']  = 60
params['dt']  = 400e-6

# Time from end of diffusion waveform to TE [ms]
params['T_readout']  = 16.0
# Time of excitation 90 [ms]
params['T_90']  = 4.0
# Time for 180 flip [ms]
params['T_180']  = 6.0

# Run optimization
G, dd = gropt.gropt(params, verbose=1)
fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html')) 

### Run TE finder for bval = 1000

G_min, T_min = get_min_TE(params, bval=1000, verbose=False)

fig = plot_waveform_interactive(G_min, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

## M0+M1 Nulled CODE

Generate a waveform with $M_0 = 0$ and $M_1 = 0$, other parameters as listed in the code.

TE was manually selected (82 ms) to hit b-value = 600

params = {}
params['mode'] = 'diff_bval'
params['gmax']  = 0.05
params['smax']  = 50.0
params['MMT']  = 1
params['TE']  = 82.0
params['T_readout']  = 16.0
params['T_90']  = 4.0
params['T_180']  = 6.0
params['dt']  = 200e-6

G, dd = gropt.gropt(params, verbose=1)

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

Constraining $M_0 = M_1 = 0$ for conventional and optimized diffusion encoding methods mitigate signal losses, due to constant moving tissue

params = {}
params['mode'] = 'diff_bval'
params['gmax'] = 50            # Maximum gradient amplitude, mT/m
params['smax'] = 100           # Maximum slew rate, mT/m/ms
params['T_readout'] = 20       # Time from start to center of EPI readout, ms
params['T_90'] = 3             # Duration of excitation pulse, ms
params['T_180'] = 5            # Duration of refocusing pulse, ms
params['b'] = 1000             # Diffusion b-value, s/mm^2
params['dt'] = 400e-6

# ************
# M0 and M1 nulling
# ************
params['MMT'] = 1              # Nulling M0 and M1



# Convex Optimized Diffusion Encoding (CODE)
G_min, T_min = get_min_TE(params, bval=params['b'], min_TE = 40, max_TE = 120)
print('Minimum TE =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G_min, params, plot_eddy = False, plot_pns = False, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

## M0+M1+M2 Nulled CODE

Generate a waveform with $M_0 = 0$, $M_1 = 0$ and $M_2 = 0$, other parameters as listed in the code.

TE was manually selected (97 ms) to hit b-value = 600

params = {}
params['mode'] = 'diff_bval'
params['gmax']  = 0.05
params['smax']  = 50.0
params['MMT']  = 2
params['TE']  = 97.0
params['T_readout']  = 16.0
params['T_90']  = 4.0
params['T_180']  = 6.0
params['dt']  = 200e-6

G, dd = gropt.gropt(params, verbose=1)

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

Constraining $M_0 = M_1 = M_2 = 0$ for conventional and optimized diffusion encoding methods mitigate signal losses, due to constant moving **and** accelerating tissue

params = {}
params['mode'] = 'diff_bval'
params['gmax'] = 50            # Maximum gradient amplitude, mT/m
params['smax'] = 100           # Maximum slew rate, mT/m/ms
params['T_readout'] = 20       # Time from start to center of EPI readout, ms
params['T_90'] = 3             # Duration of excitation pulse, ms
params['T_180'] = 5            # Duration of refocusing pulse, ms
params['b'] = 1000             # Diffusion b-value, s/mm^2
params['dt'] = 400e-6

# ************
# M0, M1 and M2 nulling
# ************
params['MMT'] = 2              # Nulling M0, M1 and M2


# Convex Optimized Diffusion Encoding (CODE)
G_min, T_min = get_min_TE(params, bval=params['b'], min_TE = 40, max_TE = 120)
print('Minimum TE =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G_min, params, plot_eddy = False, plot_pns = False, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

#### We can constrain PNS for diffusion

params = {}
params['mode'] = 'diff_bval'
params['gmax'] = 50
params['MMT'] = 0
params['T_readout'] = 20.0
params['T_90'] = 3
params['T_180'] = 5
params['dt'] = 100e-6
bval = 1000

# ************
# Use maximum slew rate
# ************
params['smax'] = 200.0

# ************
# Add PNS contraint
# ************
params['pns_thresh'] = 1.0

G_min, T_min = get_min_TE(params, bval, min_TE = 40, max_TE = 120)
print('Minimum TE =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G_min, params, plot_moments = False, plot_eddy = False, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

#### We can also constrain to null for a specific eddy current time constants (lambda) to null diffusion incuded eddy current

params = {}
params['mode'] = 'diff_bval'
params['MMT'] = 0
params['gmax'] = 50
params['smax'] = 100.0
params['T_readout'] = 20.0
params['T_90'] = 3
params['T_180'] = 5
params['dt']= 400e-6
bval = 1000

# ************
# Null eddy current for lambda time constant = 60ms
# ************
params['eddy_params'] = [[60.0, 0.0, 1.0e-4, 0.0]]


G_min, T_min = get_min_TE(params, bval, min_TE = 80, max_TE = 120)
print('Minimum TE =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G_min, params, plot_moments = False, plot_pns = False, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

#### We can constrain to null more than one eddy current time constants (lambda) as well

params = {}
params['mode'] = 'diff_bval'
params['MMT'] = 0
params['gmax'] = 50
params['smax'] = 100.0
params['T_readout'] = 20.0
params['T_90'] = 3
params['T_180'] = 5
params['dt'] = 400e-6
bval = 1000

# ************
# Null eddy current for lambda time constants = 5, 50, and 100ms
# ************
params['eddy_params']  = [[5.0, 0.0, 1.0e-4, 0.0]]
params['eddy_params'].append([50.0, 0.0, 1.0e-4, 0.0])
params['eddy_params'].append([100.0, 0.0, 1.0e-4, 0.0])


G_min, T_min = get_min_TE(params, bval, min_TE = 80, max_TE = 120)
print('Minimum TE =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G_min, params, plot_moments = False, plot_pns = False, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))