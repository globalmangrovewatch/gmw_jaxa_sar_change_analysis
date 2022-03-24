import os

import rsgislib.vectorattrs
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis

import numpy
from osgeo import gdal

def get_img_res(input_img: str, abs_vals: bool = False):
    """
    A function to retrieve the image resolution.

    :param input_img: input image file
    :param abs_vals: if True then returned x/y values will be positive (default: False)

    :return: xRes, yRes

    Example:

    .. code:: python

        import rsgislib.imageutils
        x_res, y_res = rsgislib.imageutils.get_img_res("img.kea")

    """
    rasterDS = gdal.Open(input_img, gdal.GA_ReadOnly)
    if rasterDS is None:
        raise rsgislib.RSGISPyException(
            "Could not open raster image: {}".format(input_img)
        )

    geotransform = rasterDS.GetGeoTransform()
    xRes = geotransform[1]
    yRes = geotransform[5]
    if abs_vals:
        yRes = abs(yRes)
        xRes = abs(xRes)
    rasterDS = None
    return xRes, yRes

def calc_wgs84_pixel_area(
    input_img: str, output_img: str, scale: float = 10000, gdalformat: str = "KEA"
):
    """
    A function which calculates the area (in metres) of the pixel projected in WGS84.

    :param input_img: input image, for which the per-pixel area will be calculated.
    :param output_img: output image file.
    :param scale: scale the output area to unit of interest. Scale=10000(Ha),
                        Scale=1(sq m), Scale=1000000(sq km), Scale=4046.856(Acre),
                        Scale=2590000(sq miles), Scale=0.0929022668(sq feet)

    """
    import rsgislib.tools.projection
    from rios import applier

    try:
        progress_bar = rsgislib.TQDMProgressBar()
    except:
        from rios import cuiprogress

        progress_bar = cuiprogress.GDALProgressBar()

    x_res, y_res = get_img_res(input_img, abs_vals=True)

    infiles = applier.FilenameAssociations()
    infiles.input_img = input_img
    outfiles = applier.FilenameAssociations()
    outfiles.outimage = output_img
    otherargs = applier.OtherInputs()
    otherargs.x_res = x_res
    otherargs.y_res = y_res
    otherargs.scale = float(scale)
    aControls = applier.ApplierControls()
    aControls.progress = progress_bar
    aControls.drivername = gdalformat
    aControls.omitPyramids = False
    aControls.calcStats = False

    def _calcPixelArea(info, inputs, outputs, otherargs):
        xBlock, yBlock = info.getBlockCoordArrays()

        x_res_arr = numpy.zeros_like(yBlock, dtype=float)
        x_res_arr[...] = otherargs.x_res
        y_res_arr = numpy.zeros_like(yBlock, dtype=float)
        y_res_arr[...] = otherargs.y_res
        x_res_arr_m, y_res_arr_m = rsgislib.tools.projection.degrees_to_metres(
            yBlock, x_res_arr, y_res_arr
        )
        outputs.outimage = numpy.expand_dims(
            (x_res_arr_m * y_res_arr_m) / otherargs.scale, axis=0
        )

    applier.apply(_calcPixelArea, infiles, outfiles, otherargs, controls=aControls)


roi_vec = "../../10_acc_assess/02_define_site_locations/gmw_change_site_bboxs_ids.geojson"
roi_lyr = "gmw_change_site_bboxs_ids"

roi_ids = rsgislib.vectorattrs.read_vec_column(roi_vec, roi_lyr, "roi_id")

gmw_years = [1996, 2007, 2008, 2009, 2010, 2015, 2016, 2017, 2018, 2019, 2020]
n_years = len(gmw_years)

for roi_id in roi_ids:
    print(f"site: {roi_id}")
    chngs_dir = f"../00_data/01_site_chng_maps/site_{roi_id}"
    out_dir = f"../00_data/02_site_pxl_area"
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)


    for i, base_year in enumerate(gmw_years):
        print(f"\tBase Year: {base_year}")

        if i < n_years-1:
            chng_year = gmw_years[i+1]
            print(f"\t\tChange Year: {chng_year}")

            chng_img = os.path.join(chngs_dir, f"gmw_chng_site_{roi_id}_{base_year}_{chng_year}.kea")
            pxl_area_img = os.path.join(out_dir, f"gmw_chng_site_{roi_id}_pxl_area_ha.kea")

            if i == 0:
                # Calculate the pixel area.
                calc_wgs84_pixel_area(input_img=chng_img, output_img=pxl_area_img, scale=10000, gdalformat='KEA')

            bs = [rsgislib.rastergis.BandAttStats(band=1, sum_field='area_ha')]
            rsgislib.rastergis.populate_rat_with_stats(pxl_area_img, chng_img, bs)
