from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis
import rsgislib.segmentation

logger = logging.getLogger(__name__)


class RMSmallPotentChangeFeatures(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='rm_small_feats.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        inverse_init_msk = os.path.join(self.params['tmp_dir'], '{}_inv_init_msk.kea')
        band_defns = [rsgislib.imagecalc.BandDefn('chg_msk', self.params['gmw_pot_chng_rgns_img'], 1)]
        rsgislib.imagecalc.bandMath(inverse_init_msk, 'chg_msk==1?0:1', 'KEA', rsgislib.TYPE_8UINT, band_defns)

        inverse_init_msk_clumps = os.path.join(self.params['tmp_dir'], '{}_inv_init_msk_clumps.kea')
        rsgislib.segmentation.clump(inverse_init_msk, inverse_init_msk_clumps, 'KEA', False, 0, False)

        inverse_init_msk_clumps_rmsml = os.path.join(self.params['tmp_dir'], '{}_inv_init_msk_clumps_rmsml.kea')
        rsgislib.segmentation.rmSmallClumps(inverse_init_msk_clumps, inverse_init_msk_clumps_rmsml, 10, 'KEA')
        rsgislib.rastergis.populateStats(inverse_init_msk_clumps_rmsml, addclrtab=False, calcpyramids=False, ignorezero=True)

        init_msk_fill_sml = os.path.join(self.params['tmp_dir'], '{}_init_msk_fill_sml.kea')
        band_defns = [rsgislib.imagecalc.BandDefn('chg_msk', inverse_init_msk_clumps_rmsml, 1)]
        rsgislib.imagecalc.bandMath(init_msk_fill_sml, 'chg_msk==0?1:0', 'KEA', rsgislib.TYPE_16INT, band_defns)

        init_msk_fill_clumps = os.path.join(self.params['tmp_dir'], '{}init_msk_fill_sml_clumps.kea')
        rsgislib.segmentation.clump(init_msk_fill_sml, init_msk_fill_clumps, 'KEA', False, 0, False)
        rsgislib.rastergis.populateStats(init_msk_fill_clumps, addclrtab=False, calcpyramids=False, ignorezero=True)

        init_msk_fill_clumps_rmsml = os.path.join(self.params['tmp_dir'], '{}init_msk_fill_sml_clumps_rmsml.kea')
        rsgislib.segmentation.rmSmallClumps(init_msk_fill_clumps, init_msk_fill_clumps_rmsml, 3, 'KEA')

        band_defns = [rsgislib.imagecalc.BandDefn('chg_msk', init_msk_fill_clumps_rmsml, 1)]
        rsgislib.imagecalc.bandMath(self.params['gmw_rmsml_chng_rgns_img'], 'chg_msk==0?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['gmw_rmsml_chng_rgns_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])



    def required_fields(self, **kwargs):
        return ["tile", "gmw_pot_chng_rgns_img", "gmw_rmsml_chng_rgns_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['gmw_rmsml_chng_rgns_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['gmw_rmsml_chng_rgns_img']):
            os.remove(self.params['gmw_rmsml_chng_rgns_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    RMSmallPotentChangeFeatures().std_run()


