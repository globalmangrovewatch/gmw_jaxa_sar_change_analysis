from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils


logger = logging.getLogger(__name__)


class DistGMWRegions(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='dist_to_gmw_regions.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imagecalc.calcDist2ImgVals(self.params['gmw_tile'], self.params['out_img'], [1], valsImgBand=1, gdalformat='KEA', maxDist=300, noDataVal=301, unitGEO=False)
        rsgislib.imageutils.popImageStats(self.params['out_img'], True, 301, True)

    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "out_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    DistGMWRegions().std_run()


