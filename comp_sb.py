
#IMPORT LIBRARIES
import datetime
import shapefile
import rasterio
import matplotlib.ticker as tkr
from matplotlib.ticker import ScalarFormatter
import contextily as ctx
import matplotlib.pyplot as plt
from descartes import PolygonPatch
from matplotlib.lines import Line2D

# PLOT RESULTS SAVED WITH ACCUM_WL AND INVENTORY
in_date = datetime.datetime(2020, 1, 21)
sf_sb = shapefile.Reader('/var/dades/research/tapia/outputs/wl_sb_plot/wlcomb_'+ in_date.strftime("%Y%m%d") + '.shp') # HERE THE WL_COMB
sf_inv = shapefile.Reader('/var/dades/research/tapia/outputs/landslide_event/inv_1day.shp') # HERE THE INVENTARY

fig = plt.figure(figsize = (10, 10))
ax = fig.gca()
ax.set_xlim([245000, 545000])
ax.set_ylim([4470000, 4770000])

# CREATE FUNCTION TO DIVIDE THE TICKS
def numfmt (x, pos):
    s = f'{x/1000:,.0f}'
    return s

for axis in [ax.xaxis, ax.yaxis]:
    formatter = ScalarFormatter()
    formatter.set_scientific(False)
    axis.set_major_formatter(formatter)
ymft = tkr.FuncFormatter(numfmt)
ax.xaxis.set_major_formatter(ymft)
ax.yaxis.set_major_formatter(ymft)
ax.xaxis.set_tick_params(labelsize=12)
ax.yaxis.set_tick_params(labelsize=12)

for subbasin in sf_sb.shapeRecords():
    poly_geo = subbasin.shape.__geo_interface__
    accum_wl = subbasin.record.comp_value
    if accum_wl >= 1:
        color = 'red'
        outer = '#CDCFCB'
    elif accum_wl == 0:
        color = '#FFEFD5'  #'#BCEE68ff'
        outer = '#CDCFCB'
    else:
        color = '#ffffff00'
        outer = '#ffffff00'
    ax.add_patch(PolygonPatch(poly_geo, fc=color, ec=outer, zorder=1, linewidth=0.3)) # alpha=0.5

for inventory in sf_inv.shapeRecords():
    x, y = zip(*inventory.shape.points)
    inv_date = inventory.record.inc_data
    if (inv_date > '2020-01-23'):
        color_1 = 'yellow'
        markersize_1 = 7
    else:
        color_1 = '#8B1A1A'
        markersize_1 = 5
    ax.plot(x, y, markersize=markersize_1, color=color_1, marker='o', mec = 'black')

# IDENTIFY THE CRS USED
src = rasterio.open("/var/dades/research/tapia/lews/warnings/20200121/wl202001210100.tif")
src_data = src.read(1)
ctx.add_basemap(ax, crs = src.crs, source = ctx.providers.CartoDB.Positron, zoom = 8, alpha = 1)

plt.xlabel('x-UTM [km]', fontsize = 15)
plt.ylabel('y-UTM [km]', fontsize = 15)
plt.title("Landslide Warnings and reported Landslide Events\nfor " + datetime.datetime.strftime(in_date,'%Y-%m-%d'), fontsize = 23, pad = 10)
det_wl = Line2D([0], [0], color='red', marker='s', mec = '#CDCFCB', markersize=7, lw=0)
no_det_wl = Line2D([0], [0], color='#FFEFD5', marker='s', mec = '#CDCFCB', markersize=7, lw=0)
inv_point = Line2D([0], [0], color = '#8B1A1A', marker = 'o', markersize = 6, mec = 'black', lw = 0)

handles = [det_wl, no_det_wl, inv_point]
labels = ["Sub-basin with landslide warning", "Sub-basin without landslide warning", "Reported landslide events"]
plt.legend(handles=handles, labels = labels, fontsize=12, loc="lower right")

plt.tight_layout()
plt.savefig('/var/dades/research/tapia/outputs/landslide_event/comp_sb_' + datetime.datetime.strftime(in_date,'%Y-%m-%d') + '.png')
plt.show()
