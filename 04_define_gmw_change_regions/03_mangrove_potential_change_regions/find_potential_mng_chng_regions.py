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

        if self.params['gmw_buf_tile'] is None and self.params['diff_dB_img'] is None:
            band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1)]
            rsgislib.imagecalc.bandMath(self.params['gmw_buf_chng_rgns_img'], 'gmw==1?1:0', 'KEA', rsgislib.TYPE_16INT, band_defns)
            rsgislib.rastergis.populateStats(self.params['gmw_buf_chng_rgns_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        elif self.params['diff_dB_img'] is None:
            band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                          rsgislib.imagecalc.BandDefn('gmw_buf', self.params['gmw_buf_tile'], 1)]
            rsgislib.imagecalc.bandMath(self.params['gmw_buf_chng_rgns_img'], 'gmw==1?1:gmw_buf==1?1:0', 'KEA', rsgislib.TYPE_16INT, band_defns)
            rsgislib.rastergis.populateStats(self.params['gmw_buf_chng_rgns_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        else:
            band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                          rsgislib.imagecalc.BandDefn('gmw_buf', self.params['gmw_buf_tile'], 1),
                          rsgislib.imagecalc.BandDefn('minHH', self.params['min_dB_img'], 1),
                          rsgislib.imagecalc.BandDefn('maxHH', self.params['max_dB_img'], 1),
                          rsgislib.imagecalc.BandDefn('difHH', self.params['diff_dB_img'], 1)]
            rsgislib.imagecalc.bandMath(self.params['gmw_buf_chng_rgns_img'], 'gmw==1?1:(gmw_buf==1)&&(difHH>800)&&(minHH<-1000)&&(maxHH>-1500)?1:0', 'KEA', rsgislib.TYPE_16INT, band_defns)
            rsgislib.rastergis.populateStats(self.params['gmw_buf_chng_rgns_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])



    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "gmw_buf_tile", "min_dB_img", "max_dB_img", "diff_dB_img", "gmw_buf_chng_rgns_img", "tmp_dir"]

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


