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
        band_defns = [rsgislib.imagecalc.BandDefn('gmwCore', self.params['gmw_v2_core_img'], 1),
                      rsgislib.imagecalc.BandDefn('gmwUnion', self.params['gmw_v2_union_img'], 1)]
        rsgislib.imagecalc.bandMath(self.params['out_img'], '(gmwCore==0)&&(gmwUnion==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "gmw_v2_union_img", "gmw_v2_core_img", "out_img"]

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


