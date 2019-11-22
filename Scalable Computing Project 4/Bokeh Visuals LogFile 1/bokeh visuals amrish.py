import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

from bokeh.io import output_file, output_notebook, save
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import reset_output

import random

files = ['batterylog.json','batterylog.json'] #### add log file paths
out_html = "dashboard_amrish.html" #### add path for output dashboard html file


cs = ''
figures = ''
    
for i in range(len(files)):
    with open(files[i]) as data_file:
        j = json.load(data_file)

    df = pd.io.json.json_normalize(j['Log'])
    df['TimeStamp'] = df['TimeStamp'].astype('datetime64[s]')

    df2 = df[['TimeStamp','CurrentPower']]
    df2 = df2.sort_values(by = 'TimeStamp')
    df2 = df2.set_index('TimeStamp')

    figures = figures + "'p_"+str(i)+"', "
    cs = cs + "\n\n" + "source = ColumnDataSource(df2); \np_"+str(i)+" = figure(x_axis_type='datetime', plot_width=500, plot_height=250, title = 'Remaining Power'); \np_"+str(i)+".line('TimeStamp', 'CurrentPower', source=source, color='firebrick'); \np_"+str(i)+".sizing_mode = 'scale_width'"
    exec(cs)
# output_file('filename.html', mode='inline')
# save(column(row(p,p1),p2))
# reset_output()

s_fig_list = "fig_list = list(["+figures[:-2]+"])"

exec(s_fig_list)

s = ''
for i in range(len(fig_list)):
    if i%2 == 0:
        try:
            s = s + "row("+fig_list[i]+","+fig_list[i+1]+"),"
        except:
            s = s + "row("+fig_list[i]+"),"

struct_s = "save(column("+s[:-1]+"))"
output_file(out_html, mode='inline')
exec(struct_s)