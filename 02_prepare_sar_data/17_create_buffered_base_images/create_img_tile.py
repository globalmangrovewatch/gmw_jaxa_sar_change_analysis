from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import math
import rsgislib
import rsgislib.imageutils
import rsgislib.imageutils.imagelut

logger = logging.getLogger(__name__)


def createBlankBufImgFromRefImg(input_img, output_img, gdalformat, datatype, buf_pxl_ext=None, buf_spt_ext=None,
                                no_data_val=None):
    """
    A function to create a new image file based on the input image but buffered by the specified amount
    (e.g., 100 pixels bigger on all sides. The buffer amount can ba specified in pixels or spatial units.
    If non-None value is given for both inputs then an error will be produced. By default the no data value
    will be taken from the input image header but if not available or specified within the function call
    then that value will be used.

    :param input_img: input reference image
    :param output_img: output image file.
    :param gdalformat: output image file format.
    :param datatype: is a rsgislib.TYPE_* value providing the data type of the output image.
    :param buf_pxl_ext: the amount the input image will be buffered in pixels.
    :param buf_spt_ext: the amount the input image will be buffered in spatial distance,
                    units are defined from the projection of the input image.
    :param no_data_val: Optional no data value. If None then the no data value will be
                    taken from the input image.

    """
    if (buf_pxl_ext is None) and (buf_spt_ext is None):
        raise Exception("You must specify either the buf_pxl_ext or buf_spt_ext value.")

    if (buf_pxl_ext is not None) and (buf_spt_ext is not None):
        raise Exception("You cannot specify both the buf_pxl_ext or buf_spt_ext value.")

    if no_data_val is None:
        no_data_val = rsgislib.imageutils.getImageNoDataValue(input_img)

        if no_data_val is None:
            raise Exception("You must specify a no data value ")

    x_res, y_res = rsgislib.imageutils.getImageRes(input_img, abs_vals=False)
    x_res_abs = abs(x_res)
    y_res_abs = abs(y_res)
    x_in_size, y_in_size = rsgislib.imageutils.getImageSize(input_img)
    in_img_bbox = rsgislib.imageutils.getImageBBOX(input_img)
    n_bands = rsgislib.imageutils.getImageBandCount(input_img)
    wkt_str = rsgislib.imageutils.getWKTProjFromImage(input_img)

    if buf_spt_ext is not None:
        buf_pxl_ext_x = math.ceil(buf_spt_ext / x_res_abs)
        buf_pxl_ext_y = math.ceil(buf_spt_ext / y_res_abs)

        x_out_size = x_in_size + (2 * buf_pxl_ext_x)
        y_out_size = y_in_size + (2 * buf_pxl_ext_y)

        out_tl_x = in_img_bbox[0] - (buf_pxl_ext_x * x_res_abs)
        out_tl_y = in_img_bbox[3] + (buf_pxl_ext_y * y_res_abs)
    else:
        x_out_size = x_in_size + (2 * buf_pxl_ext)
        y_out_size = y_in_size + (2 * buf_pxl_ext)

        out_tl_x = in_img_bbox[0] - (buf_pxl_ext * x_res_abs)
        out_tl_y = in_img_bbox[3] + (buf_pxl_ext * y_res_abs)

    rsgislib.imageutils.createBlankImage(output_img, n_bands, x_out_size, y_out_size, out_tl_x, out_tl_y, x_res, y_res,
                                         no_data_val, '', wkt_str, gdalformat, datatype)



class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        createBlankBufImgFromRefImg(self.params['sar_img'], self.params['out_img'], 'KEA', rsgislib.TYPE_16INT, buf_pxl_ext=50, buf_spt_ext=None, no_data_val=32767)

        scn_bbox = rsgislib.imageutils.getImageBBOX(self.params['out_img'])
        imgs = rsgislib.imageutils.imagelut.query_img_lut(scn_bbox, self.params['sar_tiles_lut_file'], self.params['sar_tiles_lut_lyr'])

        print(self.params['out_img'])
        print("\t{}\n".format(rsgislib.imageutils.getImageRes(self.params['out_img'])))

        for img in imgs:
            print(img)
            print("\t{}".format(rsgislib.imageutils.getImageRes(img)))

        if len(imgs) > 0:
            rsgislib.imageutils.includeImagesIndImgIntersect(self.params['out_img'], imgs)
            rsgislib.imageutils.popImageStats(input_img=self.params['out_img'], use_no_data=True, no_data_val=32767, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return ["tile", "sar_tiles_lut_file", "sar_tiles_lut_lyr", "sar_img", "out_img"]


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


