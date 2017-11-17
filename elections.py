import json
from math import pi
from bokeh.plotting import figure, show
from bokeh.models import ranges, ColumnDataSource

with open('election.json', mode='r') as f:
    elections = json.load(f)

strany = [x['name'] for x in elections][:15]
hlasy = [x['votes'] for x in elections][:15]

# Legenda - dá sa čítať

result = sorted(zip(strany, hlasy), key=lambda x: x[1], reverse = True)
strany, hlasy = map(list,zip(*result))

p = figure(x_range = strany, plot_height=500)
p.vbar(x = list(range(len(strany))), top = hlasy, width = 0.7, )

p.xaxis.major_label_orientation = pi/4
p.yaxis.major_label_orientation = "vertical"

show(p)