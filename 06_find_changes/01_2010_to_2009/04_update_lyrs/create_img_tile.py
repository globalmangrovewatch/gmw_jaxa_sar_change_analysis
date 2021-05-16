from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):

        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('mng_loss', self.params['mng_chng_img'], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('mng_gain', self.params['nmng_chng_img'], 1))
        exp = '(mng_loss==1)?0:(mng_gain==1)?1:gmw'
        rsgislib.imagecalc.bandMath(self.params['out_gmw_up_msk'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_gmw_up_msk'], True, True, True)

        band_defns = []
        band_defns.append(rsgislib.imagecalc.BandDefn('pchng', self.params['potent_chng_msk_img'], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('mng_loss', self.params['mng_chng_img'], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('mng_gain', self.params['nmng_chng_img'], 1))
        exp = '(mng_loss==1)?1:(mng_gain==1)?0:pchng'
        rsgislib.imagecalc.bandMath(self.params['out_gmw_up_potent_chng_msk'], exp, 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_gmw_up_potent_chng_msk'], True, True, True)

    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "potent_chng_msk_img", "mng_chng_img", "nmng_chng_img", "out_gmw_up_msk", "out_gmw_up_potent_chng_msk"]

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

if __name__ == "__main__":
    CreateImageTile().std_run()


