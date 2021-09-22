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

        vld_chng_rgns_img = os.path.join(self.params['tmp_dir'], "{}_vld_chng_rgns.kea".format(self.params['tile']))
        rsgislib.vectorutils.rasteriseVecLyr(self.params['vld_chng_rgns_file'], self.params['vld_chng_rgns_lyr'],
                                             self.params['pre_mng_chng_sum_img'],
                                             vld_chng_rgns_img, gdalformat="KEA", burnVal=1,
                                             datatype=rsgislib.TYPE_8UINT, vecAtt=None, vecExt=False,
                                             thematic=True, nodata=0)

        pre_gain_post_loss_img = os.path.join(self.params['tmp_dir'], "{}_pre_gain_post_loss_msk.kea".format(self.params['tile']))
        band_defns = [rsgislib.imagecalc.BandDefn('pre_mng_chg', self.params['pre_mng_chng_sum_img'], 1),
                      rsgislib.imagecalc.BandDefn('post_mng_chg', self.params['post_mng_chng_sum_img'], 1),
                      rsgislib.imagecalc.BandDefn('v2chg', self.params['v2_chng_rgn_img'], 1),
                      rsgislib.imagecalc.BandDefn('vld_chg', vld_chng_rgns_img, 1)]
        rsgislib.imagecalc.bandMath(pre_gain_post_loss_img, '(v2chg==1)||(vld_chg==1)?0:(pre_mng_chg==1)&&(post_mng_chg==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)

        pre_loss_post_gain_img = os.path.join(self.params['tmp_dir'], "{}_pre_loss_post_gain_msk.kea".format(self.params['tile']))
        band_defns = [rsgislib.imagecalc.BandDefn('pre_nmng_chg', self.params['pre_nmng_chng_sum_img'], 1),
                      rsgislib.imagecalc.BandDefn('post_nmng_chg', self.params['post_nmng_chng_sum_img'], 1),
                      rsgislib.imagecalc.BandDefn('v2chg', self.params['v2_chng_rgn_img'], 1),
                      rsgislib.imagecalc.BandDefn('vld_chg', vld_chng_rgns_img, 1)]
        rsgislib.imagecalc.bandMath(pre_loss_post_gain_img, '(v2chg==1)||(vld_chg==1)?0:(pre_nmng_chg==1)&&(post_nmng_chg==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)

        band_defns = [rsgislib.imagecalc.BandDefn('prgpol', pre_gain_post_loss_img, 1),
                      rsgislib.imagecalc.BandDefn('prlpog', pre_loss_post_gain_img, 1)]
        rsgislib.imagecalc.bandMath(self.params['out_img'], '(prgpol==1)||(prlpog==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "pre_mng_chng_sum_img", "pre_nmng_chng_sum_img", "post_mng_chng_sum_img", "post_nmng_chng_sum_img", "v2_chng_rgn_img", "vld_chng_rgns_file", "vld_chng_rgns_lyr", "out_img", "tmp_dir"]


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


