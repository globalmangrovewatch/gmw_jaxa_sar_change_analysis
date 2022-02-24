from rsgislib.tools.plotting import get_gdal_thematic_raster_mpl_imshow
import numpy
import matplotlib.pyplot as plt
from celluloid import Camera
import os

out_dir = "chng_animations"
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

gmw_years = ["1996", "2007", "2008", "2009", "2010", "2015", "2016", "2017", "2018", "2019", "2020"]
sites = numpy.arange(1, 39, 1)

print(sites)

for site in sites:
    fig, ax = plt.subplots(figsize=(10, 10))
    camera = Camera(fig)
    for year in gmw_years:
        img_file = f"../00_data/01_site_maps/{year}/gmw_{year}_v312_site_{site}.kea"

        (img_data_arr,
         coords_bbox,
         lgd_patches) = get_gdal_thematic_raster_mpl_imshow(img_file, band=1)

        ax.text(0.4, 1.01, f"Site {site} - {year}", transform=ax.transAxes, fontsize="xx-large")
        plt.imshow(img_data_arr, extent=coords_bbox)
        camera.snap()

    out_ani = os.path.join(out_dir, f"gmw_v312_site_{site}.gif")
    animation = camera.animate()
    animation.save(out_ani, writer='PillowWriter', fps=2)
