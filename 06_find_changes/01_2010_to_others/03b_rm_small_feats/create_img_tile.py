from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.rastergis
import rsgislib.imagecalc
import rsgislib.segmentation

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        chng_clumps = os.path.join(self.params['tmp_dir'], '{}_chng_clumps.kea'.format(self.params['tile']))
        rsgislib.segmentation.clump(self.params['chng_img'], chng_clumps, 'KEA', False, 0, False)
        rsgislib.rastergis.populateStats(chng_clumps, addclrtab=False, calcpyramids=False, ignorezero=True)

        chng_clumps_rmsml = os.path.join(self.params['tmp_dir'], '{}_chng_clumps_rmsml.kea'.format(self.params['tile']))
        rsgislib.segmentation.rmSmallClumps(chng_clumps, chng_clumps_rmsml, 4, 'KEA')

        band_defns = [rsgislib.imagecalc.BandDefn('chg_clps', chng_clumps_rmsml, 1)]
        rsgislib.imagecalc.bandMath(self.params['out_img'], 'chg_clps>0?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["tile", "chng_img", "out_img", "tmp_dir"]

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


