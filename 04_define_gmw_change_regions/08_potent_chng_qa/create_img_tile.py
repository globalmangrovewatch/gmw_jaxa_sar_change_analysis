from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.vectorutils
import rsgislib.rastergis

logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        add_rgns_img = os.path.join(self.params['tmp_dir'], "{}_add_rgns.kea".format(self.params['tile']))
        rsgislib.vectorutils.rasteriseVecLyr(self.params['add_rgns_vec_file'], self.params['add_rgns_vec_lyr'],
                                             self.params['gmw_tile'], add_rgns_img, gdalformat="KEA",
                                             burnVal=1, datatype=rsgislib.TYPE_8UINT, vecAtt=None, vecExt=False,
                                             thematic=True, nodata=0)

        rm_rgns_img = os.path.join(self.params['tmp_dir'], "{}_rm_rgns.kea".format(self.params['tile']))
        rsgislib.vectorutils.rasteriseVecLyr(self.params['rm_rgns_vec_file'], self.params['rm_rgns_vec_lyr'],
                                             self.params['gmw_tile'], rm_rgns_img, gdalformat="KEA",
                                             burnVal=1, datatype=rsgislib.TYPE_8UINT, vecAtt=None, vecExt=False,
                                             thematic=True, nodata=0)

        qa_v2_rgns_img = os.path.join(self.params['tmp_dir'], "{}_qa_v2_rgns.kea".format(self.params['tile']))
        rsgislib.vectorutils.rasteriseVecLyr(self.params['not_mng_qa_vec_file'], self.params['not_mng_qa_vec_lyr'],
                                             self.params['gmw_tile'], qa_v2_rgns_img, gdalformat="KEA",
                                             burnVal=1, datatype=rsgislib.TYPE_8UINT, vecAtt=None, vecExt=False,
                                             thematic=True, nodata=0)

        band_defns = [rsgislib.imagecalc.BandDefn('pot_chng', self.params['pot_chng_rgns_img'], 1),
                      rsgislib.imagecalc.BandDefn('add', add_rgns_img, 1),
                      rsgislib.imagecalc.BandDefn('rm', rm_rgns_img, 1),
                      rsgislib.imagecalc.BandDefn('notmng', qa_v2_rgns_img, 1)]
        rsgislib.imagecalc.bandMath(self.params['out_img'], '(rm == 1) || (notmng==1)?0:(add==1)?1:pot_chng', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "pot_chng_rgns_img", "add_rgns_vec_file", "add_rgns_vec_lyr", "rm_rgns_vec_file",
                "rm_rgns_vec_lyr", "not_mng_qa_vec_file", "not_mng_qa_vec_lyr" "out_img", "tmp_dir"]


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


