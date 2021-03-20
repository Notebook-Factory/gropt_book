# 3 Axis Example

Code example of using GrOpt with the "Naxis" parameter set to 3.

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

## Parameter constraints:

- Run in free mode - no objective function
- Zero and second gradient moment = 11.74 (mT*ms)/m , first gradient moment = -11.74
- Number of axis set to 3

params = {}
params['mode'] = 'free'
params['gmax']  = 0.05
params['smax']  = 50.0
params['moment_params']  = [[0, 0, 0, -1, -1, 11.74, 1.0e-3]]
params['moment_params'].append([1, 0, 0, -1, -1, -11.74, 1.0e-3])
params['moment_params'].append([2, 0, 0, -1, -1, 11.74, 1.0e-3])
params['TE']  = 1.0
params['dt']  = 20e-6
params['Naxis'] = 3

G, dd = gropt.gropt(params, verbose=1)

fig = plot_waveform_interactive(G, params, eddy_lines=[50], width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

### Lower the maximum gradient amplitude and amp up the maximum slew rate, double dt but cut TE in half

params = {}
params['mode'] = 'free'
params['gmax']  = 0.08
params['smax']  = 200.0
params['moment_params']  = [[0, 0, 0, -1, -1, 11.74, 1.0e-3]]
params['moment_params'].append([1, 0, 0, -1, -1, -11.74, 1.0e-3])
params['moment_params'].append([2, 0, 0, -1, -1, 11.74, 1.0e-3])
params['TE']  = 0.50
params['dt']  = 10e-6
params['Naxis'] = 3

G, dd = gropt.gropt(params, verbose=1)

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

### Constraining the peripheral nerve stimulation control to be less than 1 while boosting TE to 0.675

params = {}
params['mode'] = 'free'
params['gmax']  = 0.08
params['smax']  = 200.0
params['moment_params']  = [[0, 0, 0, -1, -1, 11.74, 1.0e-3]]
params['moment_params'].append([1, 0, 0, -1, -1, -11.74, 1.0e-3])
params['moment_params'].append([2, 0, 0, -1, -1, 11.74, 1.0e-3])
params['TE']  = 0.675
params['dt']  = 10e-6
params['Naxis'] = 3
params['pns_thresh'] = 1.0

G, dd = gropt.gropt(params, verbose=1)

fig = plot_waveform_interactive(G, params, width=585, height=430)
plot(fig, filename = 'fig.html', config = config)
display(HTML('fig.html'))

