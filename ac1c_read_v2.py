
#IMPORT LIBRARIES
import datetime
import glob as glob
import rasterio
import shapefile
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
from matplotlib.ticker import ScalarFormatter
from matplotlib.colors import from_levels_and_colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import rasterio.plot
import contextily as ctx

# DEFINE COASTLINE FILE
coast_path = '/usuaris/tapia/gloria/ccaav2.shp' # THIS ONE IS INSIDE THE FOLDER (PATH?)
sf = shapefile.Reader(coast_path)

# CREATE LIST OF FILES TO EXTRACT
def get_list_files(in_date, end_date):
    list_files = []
    dt_i = in_date

    while dt_i < end_date:
        #path = "/usuaris/tapia/ac1c_plot/19jan2020/acc01h_" + dt_i.strftime("%Y%m%d") + dt_i.strftime("%H%M") + ".tif" THIS PATH IS NO LONGER USEFUL
        #path = "/var/dades/realtime/smc/AC1C/" + dt_i.strftime("%Y%m%d") + "/" + dt_i.strftime("%H%M") + "/CMPAC*.tiff" CORRECT!
        #path = "/var/dades/work/ICGC/2021reconstruccio/events/20200119-20200124/config3/combi/tif" COMPLETE NAME
        dt_path = glob.glob(path)  # only use if you have a star
        list_files.extend(dt_path)  # to make a list of paths
        dt_i = dt_i + datetime.timedelta(hours = 1)
    return list_files

# CREATE LIST OF TITLES FOR PLOTTING
def get_list_dates(in_date, end_date):
    dt_i = in_date
    list_dates = []

    while dt_i < end_date:
        dt_i = dt_i + datetime.timedelta(hours = 1)
        date = datetime.datetime.strftime(dt_i, '%Y-%m-%d %H:%M')
        list_dates.append(date)
    return list_dates

# CREATE FUNCTION TO DIVIDE THE TICKS
def numfmt (x, pos):
    s = f'{x/1000:,.0f}'
    return s

# CREATE COLOR RAMP FOR RAINFALL THRESHOLDS AND PLOT
def plot_tiff(path,title):
    z_pal = [0., .1, .3, .6, 1., 2., 3., 4., 5., 6., 8., 10., 13., 16., 20., 25., 35., 50.]
    pal_rgb = ['#ffffff00', '#d6e2ffff', '#8db2ffff', '#626ff7ff', '#0062ffff', '#019696ff', '#01c634ff',
               '#63ff01ff', '#c6ff34ff', '#ffff02ff', '#ffc601ff', '#ffa001ff', '#ff7c00ff', '#ff1901ff', '#a20a28ff',
               '#9b159dff', '#d294d3ff', '#f6e9f6ff'] # erase '#00000019'

    cmap, norm = from_levels_and_colors(z_pal, pal_rgb, extend = 'max')
    src = rasterio.open(path)
    src_data = src.read(1)
    fig, ax = plt.subplots(figsize=(10, 10))

    ax.set_xlim([250000, 550000])
    ax.set_ylim([4450000, 4770000])

    for axis in [ax.xaxis, ax.yaxis]:
        formatter = ScalarFormatter()
        formatter.set_scientific(False)
        axis.set_major_formatter(formatter)

    ax.imshow(src_data, interpolation = 'none', extent = rasterio.plot.plotting_extent(src))
    ctx.add_basemap(ax, crs = src.crs, source = ctx.providers.CartoDB.Positron, zoom = 8) # Stamen.TonerLite, OpenStreetMap.Mapnik, edgecolor = 'black'
    im = ax.imshow(src_data, cmap = cmap, norm = norm, interpolation = 'none', extent = rasterio.plot.plotting_extent(src)) # extent = rasterio.plot.plotting_extent(src)

    # CHECK HOW TO PLOT THE COASTLINE!
    for coastline in sf.shapeRecords():
        line_coast = coastline.shape.__geo_interface__
        ax.add_patch(PolygonPatch(line_coast, linewidth = 1, fc='none', ec = 'black'))
        ax.autoscale_view()

    ymft = tkr.FuncFormatter(numfmt)
    ax.xaxis.set_major_formatter(ymft)
    ax.yaxis.set_major_formatter(ymft)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.yaxis.set_tick_params(labelsize=12)

    plt.xlabel('x-UTM [km]', fontsize = 15)
    plt.ylabel('y-UTM [km]', fontsize = 15)
    plt.title("Hourly Radar-Rain Gauge Accumulation\n" + title + ' UTC', fontsize = 25, pad = 10)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size = "5%", pad = 0.05)
    cbar = plt.colorbar(im, cax = cax)
    cbar.set_label(label = 'Accumulation [mm/h]', size = 13)
    cbar.set_ticks([0., .1, .3, .6, 1., 2., 3., 4., 5., 6., 8., 10., 13., 16., 20., 25., 35., 50.])
    cbar.set_ticklabels([0., .1, .3, .6, 1., 2., 3., 4., 5., 6., 8., 10., 13., 16., 20., 25., 35., 50.], fontsize = 12)

    plt.tight_layout()
    #plt.savefig('/usuaris/tapia/' + title + '_1.png') UPDATE PATH
    plt.show()
    return


# MAIN FUNCTION TO RUN
if __name__ == '__main__':

    in_date = datetime.datetime(2020, 1, 19, 0, 0)
    end_date = datetime.datetime(2020, 1, 20, 1, 0)

    list_files = get_list_files(in_date, end_date)
    list_dates = get_list_dates(in_date, end_date)
    i = 0
    for file_tif in list_files:
            print(file_tif)
            plot_tiff(file_tif,list_dates[i])
            i =i + 1

