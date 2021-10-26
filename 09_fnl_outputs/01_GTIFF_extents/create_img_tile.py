from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import osgeo.gdal as gdal
import rsgislib

logger = logging.getLogger(__name__)


def gdal_translate(input_img, output_img, gdalformat='KEA', options=''):
    """
    Using GDAL translate to convert input image to a different format, if GTIFF selected
    and no options are provided then a cloud optimised GeoTIFF will be outputted.

    :param input_img: Input image which is GDAL readable.
    :param output_img: The output image file.
    :param gdalformat: The output image file format
    :param options: options for the output driver (e.g., "-co TILED=YES -co COMPRESS=LZW -co BIGTIFF=YES")
    """

    options = "-co TILED=YES -co INTERLEAVE=PIXEL -co BLOCKXSIZE=256 -co BLOCKYSIZE=256 -co COMPRESS=LZW -co BIGTIFF=NO -co COPY_SRC_OVERVIEWS=YES"

    try:
        import tqdm
        pbar = tqdm.tqdm(total=100)
        callback = lambda *args, **kw: pbar.update()
    except:
        callback = gdal.TermProgress

    trans_opt = gdal.TranslateOptions(format=gdalformat, options=options, callback=callback)
    gdal.Translate(output_img, input_img, options=trans_opt)

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
        gdal_translate(self.params['gmw_tile'], self.params['out_img'], gdalformat='GTIFF')
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


