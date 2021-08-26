from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis
import rsgislib.segmentation
import rsgislib.imagemorphology

logger = logging.getLogger(__name__)


class ProcessImgTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        morph_5_out_file = os.path.join(self.params['tmp_dir'], "morph_5_op.gmtxt")
        rsgislib.imagemorphology.createCircularOp(morph_5_out_file, 5)

        morph_7_out_file = os.path.join(self.params['tmp_dir'], "morph_7_op.gmtxt")
        rsgislib.imagemorphology.createCircularOp(morph_7_out_file, 7)

        out_open_morph_img = os.path.join(self.params['tmp_dir'], "{}_opening.kea".format(self.params['tile']))
        out_tmp_img = os.path.join(self.params['tmp_dir'], "{}_morph_tmp.kea".format(self.params['tile']))
        rsgislib.imagemorphology.imageOpening(self.params['gmw_pot_chng_rgns_img'],
                                              out_open_morph_img, out_tmp_img,
                                              morph_5_out_file, True, 5, "KEA",
                                              rsgislib.TYPE_8UINT)

        out_close_morph_img = os.path.join(self.params['tmp_dir'], "{}_closing.kea".format(self.params['tile']))
        out_tmp_img = os.path.join(self.params['tmp_dir'],
                                   "{}_morph_tmp.kea".format(self.params['tile']))
        rsgislib.imagemorphology.imageClosing(self.params['gmw_pot_chng_rgns_img'],
                                              out_close_morph_img, out_tmp_img,
                                              morph_7_out_file, True, 7, "KEA",
                                              rsgislib.TYPE_8UINT)

        morph_chk_pxls_msk = os.path.join(self.params['tmp_dir'], '{}_morph_chk_pxls_msk.kea'.format(self.params['tile']))
        band_defns = [
            rsgislib.imagecalc.BandDefn('base_msk', self.params['gmw_pot_chng_rgns_img'], 1),
            rsgislib.imagecalc.BandDefn('open_msk', out_open_morph_img, 1),
            rsgislib.imagecalc.BandDefn('close_msk', out_close_morph_img, 1)
        ]
        rsgislib.imagecalc.bandMath(morph_chk_pxls_msk, '(base_msk==1)&&(open_msk==0)?1:(base_msk==0)&&(close_msk==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)

        morph_chkd_pxls_msk = os.path.join(self.params['tmp_dir'], '{}_morph_chkd_pxls_msk.kea'.format(self.params['tile']))
        band_defns = [
            rsgislib.imagecalc.BandDefn('test_msk', morph_chk_pxls_msk, 1),
            rsgislib.imagecalc.BandDefn('dist', self.params["gmw_dist_img"], 1),
            rsgislib.imagecalc.BandDefn('gmw', self.params["gmw_tile"], 1)
        ]
        rsgislib.imagecalc.bandMath(morph_chkd_pxls_msk, '(test_msk==1)&&(gmw==1)?1:(test_msk==1)&&(dist<10)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)

        morph_pxls_msk_fnl = os.path.join(self.params['tmp_dir'], '{}_morph_pxls_msk_fnl.kea'.format(self.params['tile']))
        band_defns = [
            rsgislib.imagecalc.BandDefn('morph_msk', morph_chkd_pxls_msk, 1),
            rsgislib.imagecalc.BandDefn('msk_open', out_open_morph_img, 1)
        ]
        rsgislib.imagecalc.bandMath(morph_pxls_msk_fnl, '(morph_msk==1)||(msk_open==1)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)

        msk_clumps = os.path.join(self.params['tmp_dir'], '{}_morph_pxls_msk_fnl_clumps.kea'.format(self.params['tile']))
        rsgislib.segmentation.clump(morph_pxls_msk_fnl, msk_clumps, 'KEA', False, 0, False)
        rsgislib.rastergis.populateStats(msk_clumps, False, False, True)

        msk_clumps_rmsml = os.path.join(self.params['tmp_dir'], '{}_morph_pxls_msk_fnl_clumps_rmsml.kea'.format(  self.params['tile']))
        rsgislib.segmentation.rmSmallClumps(msk_clumps, msk_clumps_rmsml, 5, 'KEA')

        band_defns = [rsgislib.imagecalc.BandDefn('chg_msk', msk_clumps_rmsml, 1)]
        rsgislib.imagecalc.bandMath(self.params['gmw_morph_chng_rgns_img'], 'chg_msk>0?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
        rsgislib.rastergis.populateStats(self.params['gmw_morph_chng_rgns_img'], True, True, True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])



    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "gmw_dist_img", "gmw_pot_chng_rgns_img", "gmw_morph_chng_rgns_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.self.params['gmw_morph_chng_rgns_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.self.params['gmw_morph_chng_rgns_img']):
            os.remove(self.self.params['gmw_morph_chng_rgns_img'])

        # Reset the tmp dir
        if os.path.exists(self.self.params['tmp_dir']):
            shutil.rmtree(self.self.params['tmp_dir'])
        os.mkdir(self.self.params['tmp_dir'])

if __name__ == "__main__":
    ProcessImgTile().std_run()


