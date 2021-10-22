from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import osgeo.gdal as gdal


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



class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        gdal_translate(self.params['gmw_tile'], self.params['out_img'], gdalformat='GTIFF')


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


