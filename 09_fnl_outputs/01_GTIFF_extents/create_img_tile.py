from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import osgeo.gdal as gdal
import rsgislib
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

def get_gdal_datatype_from_img(input_img: str):
    """
    Returns the GDAL datatype ENUM (e.g., GDT_Float32) for the inputted raster file.

    :return: ints

    """
    raster = gdal.Open(input_img, gdal.GA_ReadOnly)
    if raster == None:
        raise rsgislib.RSGISPyException(
            "Could not open raster image: '" + input_img + "'"
        )
    band = raster.GetRasterBand(1)
    if band == None:
        raise rsgislib.RSGISPyException(
            "Could not open raster band 1 in image: '" + input_img + "'"
        )
    gdal_dtype = band.DataType
    raster = None
    return gdal_dtype

def get_gdal_format_name(input_img: str):
    """
    Gets the shorthand file format for the input image in uppercase.

    :param input_img: The current name of the GDAL layer.
    :return: string with the file format (e.g., KEA or GTIFF).

    """
    layerDS = gdal.Open(input_img, gdal.GA_ReadOnly)
    gdalDriver = layerDS.GetDriver()
    layerDS = None
    return str(gdalDriver.ShortName).upper()

def set_img_thematic(input_img: str):
    """
    Set all image bands to be thematic.

    :param input_img: The file for which the bands are to be set as thematic
    """
    ds = gdal.Open(input_img, gdal.GA_Update)
    if ds == None:
        raise Exception("Could not open the input_img.")
    for bandnum in range(ds.RasterCount):
        band = ds.GetRasterBand(bandnum + 1)
        band.SetMetadataItem("LAYER_TYPE", "thematic")
    ds = None

def get_img_band_count(input_img: str):
    """
    A function to retrieve the number of image bands in an image file.

    :return: nBands

    """
    rasterDS = gdal.Open(input_img, gdal.GA_ReadOnly)
    if rasterDS == None:
        raise rsgislib.RSGISPyException(
            "Could not open raster image: '" + input_img + "'"
        )

    nBands = rasterDS.RasterCount
    rasterDS = None
    return nBands

def get_img_size(input_img: str):
    """
    A function to retrieve the image size in pixels.

    :return: xSize, ySize

    """
    rasterDS = gdal.Open(input_img, gdal.GA_ReadOnly)
    if rasterDS == None:
        raise rsgislib.RSGISPyException(
            "Could not open raster image: '" + input_img + "'"
        )

    xSize = rasterDS.RasterXSize
    ySize = rasterDS.RasterYSize
    rasterDS = None
    return xSize, ySize

def pop_thmt_img_stats(input_img: str, add_clr_tab: bool=True, calc_pyramids: bool=True, ignore_zero: bool=True):
    """
    A function which populates a byte thematic input image (e.g., classification) with
    pyramids and header statistics (e.g., colour table).

    Note, for more complex thematic images using formats which support raster attribute
    tables (e.g., KEA) then use the rsgislib.rastergis.pop_rat_img_stats function.

    This function is best used aiding the visualisation of GTIFF's.

    :param input_img: input image path
    :param add_clr_tab: boolean specifying whether a colour table should be added
                        (default: True)
    :param calc_pyramids: boolean specifying whether a image pyramids should be added
                        (default: True)
    :param ignore_zero: boolean specifying whether to ignore pixel with a value of zero
                        i.e., as a no data value (default: True)

    """
    import tqdm

    # Get file data type
    data_type = get_gdal_datatype_from_img(input_img)
    if data_type != gdal.GDT_Byte:
        raise Exception("This function only supports byte datasets")

    # Get file format
    img_format = get_gdal_format_name(input_img)
    if img_format == "KEA":
        print("Recommend using rsgislib.rastergis.pop_rat_img_stats for KEA files")
    # Set image as being thematic
    set_img_thematic(input_img)

    if add_clr_tab:
        n_bands = get_img_band_count(input_img)
        gdal_ds = gdal.Open(input_img, gdal.GA_Update)
        for band_idx in tqdm.tqdm(range(n_bands)):
            gdal_band = gdal_ds.GetRasterBand(band_idx + 1)

            # fill in the metadata
            tmp_meta = gdal_band.GetMetadata()

            if ignore_zero:
                gdal_band.SetNoDataValue(0)
                tmp_meta["STATISTICS_EXCLUDEDVALUES"] = "0"

            try:
                (min_val, max_val, mean_val, stddev_val) = gdal_band.ComputeStatistics(False)
            except RuntimeError as e:
                if str(e).endswith('Failed to compute statistics, no '
                                   'valid pixels found in sampling.'):
                    min_val = 0
                    max_val = 0
                    mean_val = 0
                    stddev_val = 0
                else:
                    raise e

            tmp_meta["STATISTICS_MINIMUM"] = "".format(min_val)
            tmp_meta["STATISTICS_MAXIMUM"] = "".format(max_val)
            tmp_meta["STATISTICS_MEAN"] = "".format(mean_val)
            tmp_meta["STATISTICS_STDDEV"] = "".format(stddev_val)
            tmp_meta["STATISTICS_SKIPFACTORX"] = "1"
            tmp_meta["STATISTICS_SKIPFACTORY"] = "1"

            # byte data use 256 bins and the whole range
            hist_min = 0
            hist_max = 255
            hist_step = 1.0
            hist_calc_min = -0.5
            hist_calc_max = 255.5
            hist_n_bins = 256
            tmp_meta["STATISTICS_HISTOBINFUNCTION"] = 'direct'

            hist = gdal_band.GetHistogram(hist_calc_min, hist_calc_max, hist_n_bins, False, False)

            # Check if GDAL's histogram code overflowed. This is not a fool-proof test,
            # as some overflows will not result in negative counts.
            histogram_overflow = (min(hist) < 0)

            if not histogram_overflow:
                # comes back as a list for some reason
                hist = numpy.array(hist)

                # Note that we have explicitly set histstep in each datatype case
                # above. In principle, this can be calculated, as it is done in the
                # float case, but for some of the others we need it to be exactly
                # equal to 1, so we set it explicitly there, to avoid rounding
                # error problems.

                # do the mode - bin with the highest count
                mode_bin = numpy.argmax(hist)
                mode_val = mode_bin * hist_step + hist_min
                tmp_meta["STATISTICS_MODE"] = "{}".format(int(round(mode_val)))
                tmp_meta["STATISTICS_HISTOBINVALUES"] = '|'.join(map(repr, hist)) + '|'
                tmp_meta["STATISTICS_HISTOMIN"] = "{}".format(hist_min)
                tmp_meta["STATISTICS_HISTOMAX"] = "{}".format(hist_max)
                tmp_meta["STATISTICS_HISTONUMBINS"] = "{}".format(hist_n_bins)

                # estimate the median
                mid_num = hist.sum() / 2
                gt_mid = hist.cumsum() >= mid_num
                median_bin = gt_mid.nonzero()[0][0]
                median_val = median_bin * hist_step + hist_min
                tmp_meta["STATISTICS_MEDIAN"] = "{}".format(int(round(median_val)))

            gdal_band.SetMetadata(tmp_meta)

            clr_tab = gdal.ColorTable()
            for i in range(hist_n_bins):
                if (i == 0) and ignore_zero:
                    clr_tab.SetColorEntry(0, (0, 0, 0, 0))
                else:
                    ran_clr = numpy.random.randint(1, 255, 3, dtype=numpy.uint8)
                    clr_tab.SetColorEntry(i, (ran_clr[0], ran_clr[1], ran_clr[2], 255))
            gdal_band.SetRasterColorTable(clr_tab)
            gdal_band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)

        gdal_ds = None

    if calc_pyramids:
        pbar = tqdm.tqdm(total=100)
        callback = lambda *args, **kw: pbar.update()

        img_x_size, img_y_size = get_img_size(input_img)
        if img_x_size < img_y_size:
            min_size = img_x_size
        else:
            min_size = img_y_size

        n_overs = 0
        pyd_lvls = [4, 8, 16, 32, 64, 128, 256, 512]
        for i in pyd_lvls:
            if (min_size // i) > 33:
                n_overs = n_overs + 1

        gdal_ds = gdal.Open(input_img, gdal.GA_Update)
        if img_format == 'GTIFF':
            gdal.SetConfigOption('COMPRESS_OVERVIEW', 'LZW')
        gdal_ds.BuildOverviews('NEAREST', pyd_lvls[:n_overs], callback)
        gdal_ds = None



def hex_to_rgb(hex_str:str):
    """
    A function which converts an hexadecimal colour representation to RGB values
    between 0 and 255.

    For example: #b432be is equal to: 180, 50, 190

    :param hex_str: Input hex string which can be either 7 or 6 characters long.
                    If 7 characters then the first character will be a #.
    :return: R, G, B tuple
    """
    if hex_str[0] == '#':
        hex_str = hex_str[1:]
    if len(hex_str) != 6:
        raise rsgislib.RSGISPyException("String must be of length "
                                        "6 or 7 if starting with #")

    r_hex = hex_str[0:2]
    g_hex = hex_str[2:4]
    b_hex = hex_str[4:6]
    return int(r_hex, 16), int(g_hex, 16), int(b_hex, 16)

def define_colour_table(input_img: str, clr_lut: dict, img_band:int =1):
    """
    A function which defines specific colours for image values for a colour
    table. Note, this function must be used to thematic images which use
    int pixel values.

    :param input_img: input image path
    :param clr_lut: a dict with the pixel value as the key with a single value or
                    list of 3 or 4 values. If 3 values are provided they are
                    interpreted as RGB (values between 0 and 255) while if 4 are
                    provided they are interpreted as RGBA (values between 0 and 255).
                    If a single value is provided then it is interpreted as a
                    hexadecimal value for RGB (e.g., #b432be).
    :param img_band: int specifying the band for the colour table (default = 1)

    """
    gdal_ds = gdal.Open(input_img, gdal.GA_Update)
    gdal_band = gdal_ds.GetRasterBand(img_band)
    clr_tbl = gdal.ColorTable()
    for pxl_val in clr_lut:
        if isinstance(clr_lut[pxl_val], str):
            r, g, b = hex_to_rgb(clr_lut[pxl_val])
            clr_tbl.SetColorEntry(pxl_val, (r, g, b, 255))
        elif isinstance(clr_lut[pxl_val], list) and len(clr_lut[pxl_val]) == 3:
            clr_tbl.SetColorEntry(pxl_val, (clr_lut[pxl_val][0], clr_lut[pxl_val][1], clr_lut[pxl_val][2], 255))
        elif isinstance(clr_lut[pxl_val], list) and len(clr_lut[pxl_val]) == 4:
            clr_tbl.SetColorEntry(pxl_val, (clr_lut[pxl_val][0], clr_lut[pxl_val][1], clr_lut[pxl_val][2], clr_lut[pxl_val][3]))
        else:
            raise rsgislib.RSGISPyException("There should be single string or a list "
                                            "with 3 or 4 values for the colour table.")
    gdal_band.SetRasterColorTable(clr_tbl)
    gdal_band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
    gdal_ds = None


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        os.environ["RSGISLIB_IMG_CRT_OPTS_GTIFF"] = "TILED=YES:COMPRESS=LZW"
        rsgislib.imagecalc.imageMath(self.params['gmw_tile'], self.params['out_img'], 'b1', 'GTIFF', rsgislib.TYPE_8UINT)
        pop_thmt_img_stats(self.params['out_img'])
        clr_lut = dict()
        clr_lut[1] = '#009600'
        define_colour_table(self.params['out_img'], clr_lut)

    def required_fields(self, **kwargs):
        return ["gmw_tile", "out_img"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

if __name__ == "__main__":
    CreateImageTile().std_run()


