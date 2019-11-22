import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import random

from bokeh.io import output_file, output_notebook, save
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, LabelSet
from bokeh.layouts import row, column, gridplot
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import reset_output

json_file = 'PriorityLog.json' #### add file path to json file
csv_file = 'battery_log.csv' #### add file path to desired csv file
out_html = 'filename_brian.html' #### add html file path for final result
always_on = ['EEG','H'] #### sensors in node_struct.csv which should always be on

with open(json_file) as data_file:
    j2 = json.load(data_file)

dfa0 = pd.DataFrame()
for n in range(len(j2["PriorityLog"])):

    ind = []
    l_battery = []
    val = j2["PriorityLog"][n]['CurrentPriorityTable']

    for i in val:
        ind.append(i)
        l_battery.append(val[i]['battery'])

    ts = j2["PriorityLog"][n]['TimeStamp']
    dfa = pd.DataFrame({'TS':[ts for i in ind], 'Sensor':ind, 'Battery_Level':l_battery})
    dfa0 = dfa.append(dfa0).copy()
    dfa0['Battery_Level'] = dfa0['Battery_Level'].astype(float).round(2)
    dfa0 = dfa0.drop_duplicates()
    dfa0.to_csv(csv_file, index = False)
        
df = pd.read_csv(csv_file)

df['TS'] = df['TS'].str.slice(0,19).astype('datetime64[s]')
sensors = list(np.unique(df['Sensor']))

cs = ''
figures = ''
for i in sensors:
    cs = cs + "\n\n\n" + "dfs_"+i+" = df[df['Sensor'] == '"+i+"'] \nsource = ColumnDataSource(dfs_"+i+") \np_"+i+" = figure(x_axis_type='datetime', plot_width=500, plot_height=250, title = '"+i+"s Remaining Power') \np_"+i+".line('TS', 'Battery_Level', source=source, color = random.choice(['firebrick','green','blue','orange'])) \np_"+i+".sizing_mode = 'scale_width'; \np_"+i+".toolbar.logo = None; \np_"+i+".toolbar_location = None"
    figures = figures + "'p_"+i+"', "

s_fig_list = "fig_list = list(["+figures[:-2]+"])"

exec(cs)
exec(s_fig_list)
s = ''
for i in range(len(fig_list)):
    if i%2 == 0:
        try:
            s = s + "row("+fig_list[i]+","+fig_list[i+1]+"),"
        except:
            s = s + "row("+fig_list[i]+"),"

struct_s = "save(column(p,"+s[:-1]+"))"
output_file(out_html, mode='inline')

ns = pd.read_csv("node_struct.csv")
val = j2["PriorityLog"][-1]['CurrentPriorityTable']
active_sensor = next(iter(val))
ns['Flag'] = np.where((ns['Label'] == active_sensor) |  (ns['Label'].isin(always_on)), 'green', 'navy')
ns['Size'] = np.where(ns['Flag'] == 'green', 30, 15)

source = ColumnDataSource(ns)
p = figure(plot_width = 1000, plot_height = 400, title = 'Topology Multi-Hop')
p.circle('X','Y', color='Flag' , size = 'Size', alpha=0.5, source = source)
labels = LabelSet(x='X', y='Y', text='Label', level='glyph',source=source)
p.toolbar.logo = None
p.toolbar_location = None
p.axis.visible = False
p.add_layout(labels)

exec(struct_s)