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
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                      rsgislib.imagecalc.BandDefn('mng_chg', self.params['mng_chng_img'], 1),
                      rsgislib.imagecalc.BandDefn('n_mng_chg', self.params['nmng_chng_img'], 1)]
        rsgislib.imagecalc.bandMath(self.params['out_gmw_up_msk'], '(gmw==1)&&(mng_chg==1)?0:(gmw==0)&&(n_mng_chg==1)?1:gmw', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_gmw_up_msk'], addclrtab=True, calcpyramids=True, ignorezero=True)

        band_defns = [rsgislib.imagecalc.BandDefn('po_chng', self.params['potent_chng_msk_img'], 1),
                      rsgislib.imagecalc.BandDefn('mng_chg', self.params['mng_chng_img'], 1),
                      rsgislib.imagecalc.BandDefn('n_mng_chg', self.params['nmng_chng_img'], 1)]
        rsgislib.imagecalc.bandMath(self.params['out_gmw_up_potent_chng_msk'], '(po_chng==0)&&(mng_chg==1)?1:(po_chng==1)&&(n_mng_chg==1)?0:po_chng', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_gmw_up_potent_chng_msk'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "potent_chng_msk_img", "mng_chng_img", "nmng_chng_img", "out_gmw_up_msk", "out_gmw_up_potent_chng_msk", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_gmw_up_msk']] = 'gdal_image'
        files_dict[self.params['out_gmw_up_potent_chng_msk']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_gmw_up_msk']):
            os.remove(self.params['out_gmw_up_msk'])

        if os.path.exists(self.params['out_gmw_up_potent_chng_msk']):
            os.remove(self.params['out_gmw_up_potent_chng_msk'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


