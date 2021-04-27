# Phase Encoding Gradients Example

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
- Zero gradient moment = 11.74 (mT*ms)/m (The area needed to encode a 1mm spatial resolution line in k-space)
- Run in free mode - no objective function

params = {}
params['mode'] = 'free' # Free mode indicates we are in a feasibility search, i.e. no objective function
params['dt'] = 4e-6     # Raster time of the gradient waveform being optimized
params['gmax'] = 50     # Maximum gradient amplitude, mT/m
params['smax'] = 120.0  # Maximum slew rate, mT/m/ms 
params['moment_params'] = [[0, 0, 0, -1, -1, 11.75, 1.0e-3]] # Constraining for M0 = 11.75 with a tolerance of 1.0e-3


G, T_min = get_min_TE(params, max_TE = 2, verbose = 1)
print('Waveform duration =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

### Reduce gmax from 50mT/m to 20mT/m to see the impact

params = {}
params['mode'] = 'free'
params['smax'] = 120.0
params['moment_params'] = [[0, 0, 0, -1, -1, 11.75, 1.0e-3]]
params['dt'] = 4e-6

# ************
# gmax changed to 20 mT/m 
# ************
params['gmax'] = 20


G, T_min = get_min_TE(params, max_TE = 2)
print('Waveform duration =', round(T_min,2), 'ms')
fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

### Add velocity compensation to the waveform by adding the constraint M1=0

params = {}
params['mode'] = 'free'
params['gmax'] = 50
params['smax'] = 120.0
params['dt'] = 4e-6
params['moment_params'] = [[0, 0, 0, -1, -1, 11.75, 1.0e-3]]

# ************
# Additional moment constraint added for M1 = 0 with a tolerance of 1.0e-3
# ************
params['moment_params'].append([0, 1, 0, -1, -1, 0, 1.0e-3])


G, T_min = get_min_TE(params, max_TE = 2.5)
print('Waveform duration =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

### Add acceleration compensation to the waveform by adding the constraint M2=0

params = {}
params['mode'] = 'free'
params['gmax'] = 50
params['smax'] = 100.0
params['dt'] = 4e-6
params['moment_params'] = [[0, 0, 0, -1, -1, 11.75, 1.0e-3]]
params['moment_params'].append([0, 1, 0, -1, -1, 0, 1.0e-3])

# ************
# Additional moment constraint added for M2 = 0
# ************
params['moment_params'].append([0, 2, 0, -1, -1, 0, 1.0e-3])


G, T_min = get_min_TE(params, max_TE = 2.6)
print('Waveform duration =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

### Peripheral Nerve Stimulation (PNS) control

If we use the full power of the gradient slew rates, the same gradient can be played much faster, but PNS will become problematic

params = {}
params['mode'] = 'free'
params['gmax'] = 50
params['moment_params'] = [[0, 0, 0, -1, -1, 11.75, 1.0e-3]]
params['moment_params'].append([0, 1, 0, -1, -1, 0, 1.0e-3])
params['moment_params'].append([0, 2, 0, -1, -1, 0, 1.0e-3])
params['dt'] = 4e-6

# ************
# Increases slew rate to 200
# ************
params['smax'] = 200.0


G, T_min = get_min_TE(params, max_TE = 2)
print('Waveform duration =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

### We can keep the maximum slew rate (200mT/m/ms) and add a PNS constraint to keep PNS < 1.0

params = {}
params['mode'] = 'free'

params['gmax'] = 50
params['smax'] = 200.0

params['moment_params'] = [[0, 0, 0, -1, -1, 11.75, 1.0e-3]]
params['moment_params'].append([0, 1, 0, -1, -1, 0, 1.0e-3])
params['moment_params'].append([0, 2, 0, -1, -1, 0, 1.0e-3])
params['dt'] = 40e-6

# ************
# Add PNS contraint
# ************
params['pns_thresh'] = 1.0

G, T_min = get_min_TE(params, min_TE = 1.6, max_TE = 2.2)
print('Waveform duration =', round(T_min,2), 'ms')

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

## Flow encoding bipolar

$M_0 = 0$ and $M_1 = 11.74$.

params = {}
params['mode'] = 'free'
params['gmax']  = 0.05
params['smax']  = 50.0
params['moment_params']  = [[0, 0, 0, -1, -1, 0.0, 1.0e-3]]
params['moment_params'].append([0, 1, 0, -1, -1, 11.74, 1.0e-3])
params['TE']  = 2.0
params['dt']  = 20e-6

G, dd = gropt.gropt(params)

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

