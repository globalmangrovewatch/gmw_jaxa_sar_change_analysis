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

        if self.params['india_tile_img'] is None:
            band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1)]
            rsgislib.imagecalc.bandMath(self.params['out_img'], 'gmw', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        else:
            band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                          rsgislib.imagecalc.BandDefn('india', self.params['india_tile_img'], 1)]
            rsgislib.imagecalc.bandMath(self.params['out_img'], '(gmw==1)?1:(india==1)?1:gmw', 'KEA', rsgislib.TYPE_8UINT, band_defns)

        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "india_tile_img", "out_img"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

if __name__ == "__main__":
    CreateImageTile().std_run()


