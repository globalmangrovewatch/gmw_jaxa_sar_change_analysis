from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                      rsgislib.imagecalc.BandDefn('min', self.params['min_ext_img'], 1)]
        rsgislib.imagecalc.bandMath(self.params['out_min_ext_img'], '(gmw==0)&&(min==1)?0:min', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_min_ext_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                      rsgislib.imagecalc.BandDefn('max', self.params['max_ext_img'], 1)]
        rsgislib.imagecalc.bandMath(self.params['out_max_ext_img'], '(gmw==1)&&(max==0)?1:max', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_max_ext_img'], addclrtab=True, calcpyramids=True, ignorezero=True)


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "min_ext_img", "out_min_ext_img", "max_ext_img", "out_max_ext_img"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_min_ext_img']] = 'gdal_image'
        files_dict[self.params['out_max_ext_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_min_ext_img']):
            os.remove(self.params['out_min_ext_img'])

        if os.path.exists(self.params['out_max_ext_img']):
            os.remove(self.params['out_max_ext_img'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


