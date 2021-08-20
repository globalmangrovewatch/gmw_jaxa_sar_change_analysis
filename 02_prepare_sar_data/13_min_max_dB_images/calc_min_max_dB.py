from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis


def create_vrt_band_subset(input_img, bands, out_vrt):
    """
    A function which creates a GDAL VRT for the input image with the bands selected in the
    input list.

    :param input_img: the input GDAL image
    :param bands: a list of bands (in the order they will be in the VRT). Note, band numbering starts at 1.
    :param out_vrt: the output VRT file.

    """
    from osgeo import gdal
    import os
    input_img = os.path.abspath(input_img)
    vrt_options = gdal.BuildVRTOptions(bandList=bands)
    my_vrt = gdal.BuildVRT(out_vrt, [input_img], options=vrt_options)
    my_vrt = None


logger = logging.getLogger(__name__)

class CalcMinMaxdB(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='calc_min_max_dB.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        if len(self.params['sar_hh_imgs']) == 1:
            rsgislib.imagecalc.imageMath(self.params['sar_hh_imgs'][0], self.params['out_min_hh_dB_img'], "b1", "KEA", rsgislib.TYPE_16INT)
            rsgislib.imageutils.popImageStats(self.params['out_min_hh_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

            rsgislib.imagecalc.imageMath(self.params['sar_hh_imgs'][0], self.params['out_max_hh_dB_img'], "b1", "KEA", rsgislib.TYPE_16INT)
            rsgislib.imageutils.popImageStats(self.params['out_max_hh_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        elif len(self.params['sar_hh_imgs']) > 1:

            vrt_band_sub_imgs = list()
            for sar_img in self.params['sar_hh_imgs']:
                basename = self.get_file_basename(sar_img, n_comps=2)
                sar_hh_vrt_img = os.path.join(self.params['tmp_dir'], "{}_hh_dB.vrt".format(basename))
                create_vrt_band_subset(sar_img, [1], sar_hh_vrt_img)
                vrt_band_sub_imgs.append(sar_hh_vrt_img)

            rsgislib.imagecalc.calcMultiImgBandStats(vrt_band_sub_imgs, self.params['out_min_hh_dB_img'], rsgislib.SUMTYPE_MIN, "KEA", rsgislib.TYPE_16INT, 32767, True)
            rsgislib.imageutils.popImageStats(self.params['out_min_hh_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

            rsgislib.imagecalc.calcMultiImgBandStats(vrt_band_sub_imgs, self.params['out_max_hh_dB_img'], rsgislib.SUMTYPE_MAX, "KEA", rsgislib.TYPE_16INT, 32767, True)
            rsgislib.imageutils.popImageStats(self.params['out_max_hh_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        if os.path.exists(self.params['out_min_hh_dB_img']) and os.path.exists(self.params['out_max_hh_dB_img']):
            band_defns = [rsgislib.imagecalc.BandDefn('mindB', self.params['out_min_hh_dB_img'], 1),
                          rsgislib.imagecalc.BandDefn('maxdB', self.params['out_max_hh_dB_img'], 1)]
            rsgislib.imagecalc.bandMath(self.params['out_diff_hh_dB_img'], '(mindB == 32767)?0:(maxdB == 32767)?0:(maxdB-mindB)', 'KEA', rsgislib.TYPE_16INT, band_defns)
            rsgislib.imageutils.popImageStats(self.params['out_diff_hh_dB_img'], usenodataval=True, nodataval=0, calcpyramids=True)




        if len(self.params['sar_hv_imgs']) == 1:
            rsgislib.imagecalc.imageMath(self.params['sar_hv_imgs'][0], self.params['out_min_hv_dB_img'], "b2", "KEA", rsgislib.TYPE_16INT)
            rsgislib.imageutils.popImageStats(self.params['out_min_hv_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

            rsgislib.imagecalc.imageMath(self.params['sar_hv_imgs'][0], self.params['out_max_hv_dB_img'], "b2", "KEA", rsgislib.TYPE_16INT)
            rsgislib.imageutils.popImageStats(self.params['out_max_hv_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        elif len(self.params['sar_hv_imgs']) > 1:

            vrt_band_sub_imgs = list()
            for sar_img in self.params['sar_hv_imgs']:
                basename = self.get_file_basename(sar_img, n_comps=2)
                sar_hv_vrt_img = os.path.join(self.params['tmp_dir'], "{}_hv_dB.vrt".format(basename))
                create_vrt_band_subset(sar_img, [2], sar_hv_vrt_img)
                vrt_band_sub_imgs.append(sar_hv_vrt_img)

            rsgislib.imagecalc.calcMultiImgBandStats(vrt_band_sub_imgs, self.params['out_min_hv_dB_img'], rsgislib.SUMTYPE_MIN, "KEA", rsgislib.TYPE_16INT, 32767, True)
            rsgislib.imageutils.popImageStats(self.params['out_min_hv_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

            rsgislib.imagecalc.calcMultiImgBandStats(vrt_band_sub_imgs, self.params['out_max_hv_dB_img'], rsgislib.SUMTYPE_MAX, "KEA", rsgislib.TYPE_16INT, 32767, True)
            rsgislib.imageutils.popImageStats(self.params['out_max_hv_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        if os.path.exists(self.params['out_min_hv_dB_img']) and os.path.exists(self.params['out_max_hv_dB_img']):
            band_defns = [rsgislib.imagecalc.BandDefn('mindB', self.params['out_min_hv_dB_img'], 1),
                          rsgislib.imagecalc.BandDefn('maxdB', self.params['out_max_hv_dB_img'], 1)]
            rsgislib.imagecalc.bandMath(self.params['out_diff_hv_dB_img'], '(mindB == 32767)?0:(maxdB == 32767)?0:(maxdB-mindB)', 'KEA', rsgislib.TYPE_16INT, band_defns)
            rsgislib.imageutils.popImageStats(self.params['out_diff_hv_dB_img'], usenodataval=True, nodataval=0, calcpyramids=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["tile", "sar_hh_imgs", "sar_hv_imgs", "out_min_hh_dB_img", "out_max_hh_dB_img", "out_diff_hh_dB_img", "out_min_hv_dB_img", "out_max_hv_dB_img", "out_diff_hv_dB_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_min_hh_dB_img']] = 'gdal_image'
        files_dict[self.params['out_max_hh_dB_img']] = 'gdal_image'
        files_dict[self.params['out_diff_hh_dB_img']] = 'gdal_image'
        files_dict[self.params['out_min_hv_dB_img']] = 'gdal_image'
        files_dict[self.params['out_max_hv_dB_img']] = 'gdal_image'
        files_dict[self.params['out_diff_hv_dB_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_min_hh_dB_img']):
            os.remove(self.params['out_min_hh_dB_img'])

        if os.path.exists(self.params['out_max_hh_dB_img']):
            os.remove(self.params['out_max_hh_dB_img'])

        if os.path.exists(self.params['out_diff_hh_dB_img']):
            os.remove(self.params['out_diff_hh_dB_img'])

        if os.path.exists(self.params['out_min_hv_dB_img']):
            os.remove(self.params['out_min_hv_dB_img'])

        if os.path.exists(self.params['out_max_hv_dB_img']):
            os.remove(self.params['out_max_hv_dB_img'])

        if os.path.exists(self.params['out_diff_hv_dB_img']):
            os.remove(self.params['out_diff_hv_dB_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])


if __name__ == "__main__":
    CalcMinMaxdB().std_run()


