from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.segmentation
import rsgislib.rastergis

logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        # Create initial mask from the water occurance layer: thresholded > 20.
        binMaskInit = os.path.join(self.params['tmp_dir'], '{}_binmskinit.kea'.format(self.params['tile']))
        rsgislib.imagecalc.bandMath(binMaskInit, '(WO>20)?1:0', 'KEA', rsgislib.TYPE_8UINT, [rsgislib.imagecalc.BandDefn('WO', self.params['water_occur_img'], 1)])

        # Clump the initial mask so we can find the region which is connected to the ocean.
        binMaskInitClumps = os.path.join(self.params['tmp_dir'], '{}_binmskinit_clumps.kea'.format(self.params['tile']))
        rsgislib.segmentation.clump(binMaskInit, binMaskInitClumps, 'KEA', False, 0)
        rsgislib.rastergis.populateStats(binMaskInitClumps, True, True, True)

        # Populate clumps with binary ocean mask.
        rsgislib.rastergis.populateRATWithStats(self.params['inv_gadm_img'], binMaskInitClumps, [rsgislib.rastergis.BandAttStats(band=1, maxField='OceanMask')])

        # Export the initial ocean water mask.
        rsgislib.rastergis.exportCol2GDALImage(binMaskInitClumps, self.params['out_img'], 'KEA', rsgislib.TYPE_8UINT, 'OceanMask')

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "inv_gadm_img", "water_occur_img", "out_img", "tmp_dir"]

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
    CreateImageTile().std_run()


