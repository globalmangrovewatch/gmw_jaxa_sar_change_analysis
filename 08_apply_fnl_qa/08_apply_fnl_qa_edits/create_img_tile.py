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

        qa_rm_img = os.path.join(self.params['tmp_dir'], "{}_qa_rm_lyr.kea".format(self.params['tile']))
        rsgislib.vectorutils.rasteriseVecLyr(self.params['qa_rm_file'], self.params['qa_rm_lyr'],
                                             self.params['gmw_tile'],
                                             qa_rm_img, gdalformat="KEA", burnVal=1,
                                             datatype=rsgislib.TYPE_8UINT,
                                             vecAtt=None, vecExt=False,
                                             thematic=True, nodata=0)

        qa_add_img = os.path.join(self.params['tmp_dir'], "{}_qa_add_lyr.kea".format(self.params['tile']))
        rsgislib.vectorutils.rasteriseVecLyr(self.params['qa_add_file'], self.params['qa_add_lyr'],
                                             self.params['gmw_tile'],
                                             qa_add_img, gdalformat="KEA", burnVal=1,
                                             datatype=rsgislib.TYPE_8UINT,
                                             vecAtt=None, vecExt=False,
                                             thematic=True, nodata=0)

        band_defns = [rsgislib.imagecalc.BandDefn('gmw', self.params['gmw_tile'], 1),
                      rsgislib.imagecalc.BandDefn('qa_rm', qa_rm_img, 1),
                      rsgislib.imagecalc.BandDefn('qa_add', qa_add_img, 1)]
        rsgislib.imagecalc.bandMath(self.params['out_img'], '(qa_rm==1)?0:(qa_add==1)?1:gmw', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "qa_add_file", "qa_add_lyr", "qa_rm_file", "qa_rm_lyr", "out_img", "tmp_dir"]


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


