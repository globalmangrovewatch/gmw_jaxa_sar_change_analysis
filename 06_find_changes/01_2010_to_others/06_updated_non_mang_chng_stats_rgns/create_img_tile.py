from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        band_defns = [rsgislib.imagecalc.BandDefn('chg_rgns', self.params['chng_stats_rgns_img'], 1),
                      rsgislib.imagecalc.BandDefn('mng_chg', self.params['mng_chng_img'], 1),
                      rsgislib.imagecalc.BandDefn('n_mng_chg', self.params['nmng_chng_img'], 1)]
        rsgislib.imagecalc.bandMath(self.params['out_img'], '(chg_rgns==1)&&(n_mng_chg==1)?0:(chg_rgns==0)&&(mng_chg==1)?1:chg_rgns', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "year", "chng_stats_rgns_img", "mng_chng_img", "nmng_chng_img", "out_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


