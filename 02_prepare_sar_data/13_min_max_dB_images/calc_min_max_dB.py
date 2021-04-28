from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis


logger = logging.getLogger(__name__)

class CalcMinMaxdB(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='calc_min_max_dB.py', descript=None)

    def do_processing(self, **kwargs):

        if len(self.params['sar_imgs']) == 1:
            rsgislib.imagecalc.imageMath(self.params['sar_imgs'][0], self.params['out_min_dB_img'], "b1", "KEA", rsgislib.TYPE_16INT)
            rsgislib.imageutils.popImageStats(self.params['out_min_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

            rsgislib.imagecalc.imageMath(self.params['sar_imgs'][0], self.params['out_max_dB_img'], "b1", "KEA", rsgislib.TYPE_16INT)
            rsgislib.imageutils.popImageStats(self.params['out_max_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        elif len(self.params['sar_imgs']) > 1:
            rsgislib.imagecalc.calcMultiImgBandStats(self.params['sar_imgs'], self.params['out_min_dB_img'], rsgislib.SUMTYPE_MIN, "KEA", rsgislib.TYPE_16INT, 32767, True)
            rsgislib.imageutils.popImageStats(self.params['out_min_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

            rsgislib.imagecalc.calcMultiImgBandStats(self.params['sar_imgs'], self.params['out_max_dB_img'], rsgislib.SUMTYPE_MAX, "KEA", rsgislib.TYPE_16INT, 32767, True)
            rsgislib.imageutils.popImageStats(self.params['out_max_dB_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        if os.path.exists(self.params['out_min_dB_img']) and os.path.exists(self.params['out_max_dB_img']):
            band_defns = [rsgislib.imagecalc.BandDefn('mindB', self.params['out_min_dB_img'], 1),
                          rsgislib.imagecalc.BandDefn('maxdB', self.params['out_max_dB_img'], 1)]
            rsgislib.imagecalc.bandMath(self.params['out_diff_dB_img'], '(mindB == 32767)?0:(maxdB == 32767)?0:(maxdB-mindB)', 'KEA', rsgislib.TYPE_16INT, band_defns)
            rsgislib.imageutils.popImageStats(self.params['out_diff_dB_img'], usenodataval=True, nodataval=0, calcpyramids=True)

    def required_fields(self, **kwargs):
        return ["tile", "sar_imgs", "out_min_dB_img", "out_max_dB_img", "out_diff_dB_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_min_dB_img']] = 'gdal_image'
        files_dict[self.params['out_max_dB_img']] = 'gdal_image'
        files_dict[self.params['out_diff_dB_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_min_dB_img']):
            os.remove(self.params['out_min_dB_img'])

        if os.path.exists(self.params['out_max_dB_img']):
            os.remove(self.params['out_max_dB_img'])

        if os.path.exists(self.params['out_diff_dB_img']):
            os.remove(self.params['out_diff_dB_img'])


if __name__ == "__main__":
    CalcMinMaxdB().std_run()


