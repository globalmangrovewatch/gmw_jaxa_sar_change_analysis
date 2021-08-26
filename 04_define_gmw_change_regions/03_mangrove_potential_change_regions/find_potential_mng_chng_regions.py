from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis


logger = logging.getLogger(__name__)


class FindPotentialMngChngRegions(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='find_potential_mng_chng_regions.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        if self.params['gmw_buf_tile'] is None and self.params['diff_hv_dB_img'] is None:
            band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1)]
            rsgislib.imagecalc.bandMath(self.params['gmw_buf_chng_rgns_img'], 'gmw==1?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
            rsgislib.rastergis.populateStats(self.params['gmw_buf_chng_rgns_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        elif self.params['diff_hv_dB_img'] is None:
            band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                          rsgislib.imagecalc.BandDefn('gmw_buf', self.params['gmw_buf_tile'], 1)]
            rsgislib.imagecalc.bandMath(self.params['gmw_buf_chng_rgns_img'], 'gmw==1?1:gmw_buf==1?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
            rsgislib.rastergis.populateStats(self.params['gmw_buf_chng_rgns_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        elif self.params['jers1_1996_img'] is None:
            band_defns = [
                rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
              rsgislib.imagecalc.BandDefn('gmw_buf', self.params['gmw_buf_tile'], 1),
              rsgislib.imagecalc.BandDefn('minHV', self.params['min_hv_dB_img'], 1),
              rsgislib.imagecalc.BandDefn('maxHV', self.params['max_hv_dB_img'], 1),
              rsgislib.imagecalc.BandDefn('difHV', self.params['diff_hv_dB_img'], 1)]
            rsgislib.imagecalc.bandMath(self.params['gmw_buf_chng_rgns_img'], 'gmw==1?1:(gmw_buf==1)&&(difHV>800)&&(minHV<-1800)&&(maxHV>-2500)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
            rsgislib.rastergis.populateStats(self.params['gmw_buf_chng_rgns_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        else:
            band_defns = [
                rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                rsgislib.imagecalc.BandDefn('gmw_buf', self.params['gmw_buf_tile'], 1),
                rsgislib.imagecalc.BandDefn('minHV', self.params['min_hv_dB_img'], 1),
                rsgislib.imagecalc.BandDefn('maxHV', self.params['max_hv_dB_img'], 1),
                rsgislib.imagecalc.BandDefn('difHV', self.params['diff_hv_dB_img'], 1),
                rsgislib.imagecalc.BandDefn('jers1', self.params['jers1_1996_img'], 1)]
            rsgislib.imagecalc.bandMath(self.params['gmw_buf_chng_rgns_img'], 'gmw==1?1:(gmw_buf==1)&&(difHV>800)&&(minHV<-1800)&&(maxHV>-2500)?1:(gmw_buf==1)&&(jers1>-1100)&&(jers1<0)&&(minHV<-1800)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
            rsgislib.rastergis.populateStats(self.params['gmw_buf_chng_rgns_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])



    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "gmw_buf_tile", "jers1_1996_img", "min_hh_dB_img", "max_hh_dB_img", "diff_hh_dB_img", "min_hv_dB_img", "max_hv_dB_img", "diff_hv_dB_img", "gmw_buf_chng_rgns_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['gmw_buf_chng_rgns_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['gmw_buf_chng_rgns_img']):
            os.remove(self.params['gmw_buf_chng_rgns_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    FindPotentialMngChngRegions().std_run()


