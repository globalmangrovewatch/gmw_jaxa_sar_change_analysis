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

        chng_qa_img = os.path.join(self.params['tmp_dir'], "{}_qa_chng.kea".format(self.params['tile']))
        rsgislib.vectorutils.rasteriseVecLyr(self.params['qa_chng_rgns_file'], self.params['qa_chng_rgns_lyr'], self.params['chng_img'],
                                             chng_qa_img, gdalformat="KEA", burnVal=1,
                                             datatype=rsgislib.TYPE_8UINT, vecAtt=None, vecExt=False,
                                             thematic=True, nodata=0)

        band_defns = [rsgislib.imagecalc.BandDefn('chgqa', chng_qa_img, 1),
                      rsgislib.imagecalc.BandDefn('chg', self.params['chng_img'], 1),
                      rsgislib.imagecalc.BandDefn('v2chg', self.params['v2_chng_rgn_img'], 1),
                      rsgislib.imagecalc.BandDefn('errmsk', self.params['chng_err_msk_img'], 1)]
        rsgislib.imagecalc.bandMath(self.params['out_img'], 'errmsk==1?0:(v2chg==1)||(chgqa==1)?chg:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["tile", "chng_img", "v2_chng_rgn_img", "chng_err_msk_img", "qa_chng_rgns_file", "qa_chng_rgns_lyr", "out_img", "tmp_dir"]

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


