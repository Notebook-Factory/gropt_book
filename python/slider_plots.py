import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import chart_studio.plotly as py
import cufflinks as cf
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from helper_utils import *


def plot_waveform_sliders(G_list, params_list, suptitle = '', eddy_lines=[], eddy_range = [1e-3,120,1000], width=900, height=550):
    current_trace = 0
    buttons_list = []
    steps = []
    updatemenus = []
    num_sliders = len(G_list)
    for G, params in zip(G_list, params_list):
        n_axis = params.get('Naxis', 1)
        num_traces = 2*n_axis + 5

        TE = params['TE']
        T_readout = params['T_readout']
        diffmode = 0
        if params['mode'][:4] == 'diff':
            diffmode = 1

        dt = (TE-T_readout) * 1.0e-3 / G.shape[1]
        tt = np.arange(G.shape[1]) * dt * 1e3
        tINV = TE/2.0

        bval = get_bval(G, params)
        blabel = 'b-value=%.0f' % bval # TODO: should add "$mm^{2}/s$"

        fig_title = None
        if suptitle:
            fig_title = suptitle + ': ' + blabel
        elif diffmode > 0:
            fig_title = blabel

        fig = go.Figure(layout=dict(xaxis=dict(title="$t [ms]$")))
        buttons = []

        # Gradient
        for i in range(n_axis):
            fig.add_trace(go.Scatter(x=tt, y=G[i]*1000, showlegend=False))
        buttons.append(dict(label = "Gradient",
                       method = "update",
                       args = [{"visible": [True if x>= current_trace and x < current_trace + n_axis
                                            else False for x in range(num_traces*num_sliders)],
                               "showlegend":False},
                               {"shapes":[],
                               "xaxis": {"title": "$t [ms]$"}}]))
        current_trace += n_axis

        # Slew
        for i in range(n_axis):
            fig.add_trace(go.Scatter(x=tt[:-1], y=np.diff(G[i])/dt, visible=False, showlegend=False))
        buttons.append(dict(label = "Slew",
                       method = "update",
                       args = [{"visible": [True if x>= current_trace and x < current_trace + n_axis
                                            else False for x in range(num_traces*num_sliders)],
                               "showlegend":False},
                               {"shapes":[],
                               "xaxis": {"title": "$t [ms]$"}}]))
        current_trace += n_axis

        # Moments
        moment_lines = []
        moment_lines.append({"type":"line", "x0":tt[0], "x1":tt[-1], "y0":0, "y1":0,
                          "line":{"color":"#777777", "width":1, "dash":"dash"}})
        mm = get_moment_plots(G, T_readout, dt, diffmode)
        for i in range(3):
            if diffmode == 1:
                mmt = mm[i]/np.abs(mm[i]).max()
            if diffmode == 0:   
                if i == 0:
                    mmt = mm[i]*1e6
                if i == 1:
                    mmt = mm[i]*1e9
                if i == 2:
                    mmt = mm[i]*1e12
            fig.add_trace(go.Scatter(x=tt, y=mmt, visible=False, name='$M_{%d}$'%i))
        buttons.append(dict(label = "Moments",
                       method = "update",
                       args = [{"visible": [True if x>= current_trace and x < current_trace + 3
                                            else False for x in range(num_traces*num_sliders)],
                               "showlegend":True},
                               {"shapes":moment_lines,
                               "xaxis": {"title": "$Time [ms]$"}}]))
        current_trace += 3

        # Eddy
        all_lam = np.linspace(eddy_range[0],eddy_range[1],eddy_range[2])
        all_e = []
        for lam in all_lam:
            lam = lam * 1.0e-3
            r = np.diff(np.exp(-np.arange(G[0].size+1)*dt/lam))[::-1] # TODO: 3-axis case, right now just assumes 1 axis
            all_e.append(100*r@G[0])
        fig.add_trace(go.Scatter(x=all_lam, y=all_e, visible=False, showlegend=False))

        eddy_draw = []
        for e in eddy_lines:
            min_e = min(all_e)
            max_e = max(all_e)
            amp = 0.1*max(abs(min_e), abs(max_e))
            eddy_draw.append(dict(type="line",
                x0=e, x1=e, y0=min(all_e)-amp, y1=max(all_e)+amp,
                line=dict(color="#D64B4B",
                    width=1,
                    dash="dot")))
        eddy_draw.append({"type":"line", "x0":all_lam[0], "x1":all_lam[-1], "y0":0, "y1":0,
                          "line":{"color":"#777777", "width":1, "dash":"dash"}})
        buttons.append(dict(label = "Eddy",
                       method = "update",
                       args = [{"visible": [True if x>= current_trace and x < current_trace + 1
                                            else False for x in range(num_traces*num_sliders)],
                               "showlegend":False},
                               {"shapes":eddy_draw,
                               'xaxis': {'title': "$\lambda [ms]$"}}]))
        current_trace += 1

        # PNS
        pns_lines = []
        pns_lines.append({"type":"line", "x0":tt[0], "x1":tt[-2], "y0":1, "y1":1,
                      "line":{"color":"#D64B4B", "width":1, "dash":"dot"}})
        pns_lines.append({"type":"line", "x0":tt[0], "x1":tt[-2], "y0":0, "y1":0,
                          "line":{"color":"#777777", "width":1, "dash":"dash"}})
        pns = np.abs(get_stim(G, dt))
        fig.add_trace(go.Scatter(x=tt[:-1], y=pns, visible=False, showlegend=False))
        buttons.append(dict(label = "PNS",
                       method = "update",
                       args = [{"visible": [True if x>= current_trace and x < current_trace + 1
                                            else False for x in range(num_traces*num_sliders)],
                               "showlegend":False},
                               {"shapes":pns_lines,
                               "xaxis": {"title": "$Time [ms]$"}}]))
        current_trace += 1

        buttons_list.append(buttons)
        update_menu = [
            dict(active = 0,
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=1.025,
                xanchor="left",
                y=.825,
                yanchor="top",
                buttons=buttons
                )]
        updatemenus.append(update_menu)
        step = dict(
            method="update",
            label=blabel,
            args=[{"visible": [False] * (num_traces*num_sliders),
                  "updatemenus": update_menu}],  # layout attribute
        )
        for j in range(n_axis):
            step["args"][0]["visible"][current_trace-num_traces+j] = True
        steps.append(step)
    
    sliders = [dict(
        active=0,
        pad={"t": 50},
        steps=steps)]
    fig.update_layout(title=fig_title,
        sliders=sliders,
        updatemenus=updatemenus[0],
        width=width,
        height=height,
        autosize=False,
        margin=dict(t=50, b=50, l=0, r=50),
        template="plotly_white")
    
    return fig
