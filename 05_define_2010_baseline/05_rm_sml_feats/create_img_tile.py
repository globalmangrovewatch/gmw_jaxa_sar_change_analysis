from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil

import numpy

import rsgislib
import rsgislib.imagecalc
import rsgislib.imagemorphology
import rsgislib.segmentation
import rsgislib.rastergis
import rsgislib.rastergis.ratutils


logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        pxl_count = rsgislib.imagecalc.countPxlsOfVal(self.params['chng_rgns_img'], vals=[1])
        print("N Pixels: ", pxl_count[0])

        if pxl_count[0] > 0:
            chgn_rgns_clmps_img = os.path.join(self.params['tmp_dir'], "{}_chng_rgn_clumps.kea".format(self.params['tile']))
            rsgislib.segmentation.clump(self.params['chng_rgns_img'], chgn_rgns_clmps_img, 'KEA', False, 0.0)
            rsgislib.rastergis.populateStats(chgn_rgns_clmps_img, addclrtab=False, calcpyramids=False, ignorezero=True)

            morph_op_3 = os.path.join(self.params['tmp_dir'], "{}_morph_op_3.gmtxt".format(self.params['tile']))
            rsgislib.imagemorphology.createCircularOp(morph_op_3, 3)

            chgn_rgns_erode_img = os.path.join(self.params['tmp_dir'], "{}_chng_rgn_erode.kea".format(self.params['tile']))
            rsgislib.imagemorphology.imageErode(self.params['chng_rgns_img'], chgn_rgns_erode_img, morph_op_3, True, 3, "KEA", rsgislib.TYPE_8UINT)

            bs = [rsgislib.rastergis.BandAttStats(band=1, minField='chng_min', maxField='chng_max')]
            rsgislib.rastergis.populateRATWithStats(chgn_rgns_erode_img, chgn_rgns_clmps_img, bs)

            chgn_rgns_rm_sml_img = os.path.join(self.params['tmp_dir'], "{}_chng_rgn_rm_sml.kea".format(self.params['tile']))
            rsgislib.rastergis.exportCol2GDALImage(chgn_rgns_clmps_img, chgn_rgns_rm_sml_img, "KEA", rsgislib.TYPE_8UINT, 'chng_max')
            rsgislib.rastergis.populateStats(chgn_rgns_rm_sml_img, addclrtab=True, calcpyramids=True, ignorezero=True)

            morph_op_7 = os.path.join(self.params['tmp_dir'], "{}_morph_op_7.gmtxt".format(self.params['tile']))
            rsgislib.imagemorphology.createCircularOp(morph_op_7, 7)

            gmw_mng_dilate_img = os.path.join(self.params['tmp_dir'], "{}_gmw_mng_dilate.kea".format(self.params['tile']))
            rsgislib.imagemorphology.imageDilate(self.params['gmw_tile'], gmw_mng_dilate_img, morph_op_7, True, 7, "KEA", rsgislib.TYPE_8UINT)

            gmw_mng_buf_rgn_img = os.path.join(self.params['tmp_dir'], "{}_gmw_mng_buf_rgn.kea".format(self.params['tile']))
            band_defns = [rsgislib.imagecalc.BandDefn('mng', self.params['gmw_tile'], 1),
                          rsgislib.imagecalc.BandDefn('dilate', gmw_mng_dilate_img, 1),
                          rsgislib.imagecalc.BandDefn('chng', chgn_rgns_rm_sml_img, 1)]
            rsgislib.imagecalc.bandMath(gmw_mng_buf_rgn_img, '(mng==0)&&(dilate==1)&&(chng==0)?1:0', 'KEA', rsgislib.TYPE_8UINT, band_defns)

            gmw_mng_buf_rgn_clumps_img = os.path.join(self.params['tmp_dir'], "{}_gmw_mng_buf_rgn_clumps.kea".format(self.params['tile']))
            rsgislib.segmentation.clump(gmw_mng_buf_rgn_img, gmw_mng_buf_rgn_clumps_img, 'KEA', False, 0.0)
            rsgislib.rastergis.populateStats(gmw_mng_buf_rgn_clumps_img, addclrtab=False, calcpyramids=False, ignorezero=True)

            gmw_mng_buf_rgn_clumps_hist = rsgislib.rastergis.ratutils.getColumnData(gmw_mng_buf_rgn_clumps_img, "Histogram")
            ident_sml_feats = numpy.zeros_like(gmw_mng_buf_rgn_clumps_hist)
            ident_sml_feats[gmw_mng_buf_rgn_clumps_hist<100] = 1
            rsgislib.rastergis.ratutils.setColumnData(gmw_mng_buf_rgn_clumps_img, "ident_sml_feats", ident_sml_feats)

            gmw_mng_dilate_sml_feats_img = os.path.join(self.params['tmp_dir'], "{}_gmw_mng_dilate_sml_feats.kea".format(self.params['tile']))
            rsgislib.rastergis.exportCol2GDALImage(gmw_mng_buf_rgn_clumps_img, gmw_mng_dilate_sml_feats_img, "KEA", rsgislib.TYPE_8UINT, 'ident_sml_feats')

            gmw_mng_dilate_sml_feats_dilate_img = os.path.join(self.params['tmp_dir'], "{}_gmw_mng_dilate_sml_feats_dilate.kea".format(self.params['tile']))
            rsgislib.imagemorphology.imageDilate(gmw_mng_dilate_sml_feats_img, gmw_mng_dilate_sml_feats_dilate_img, morph_op_3, True, 3, "KEA", rsgislib.TYPE_8UINT)

            gmw_mng_dilate_sml_feats_dilate_clumps_img = os.path.join(self.params['tmp_dir'], "{}_gmw_mng_dilate_sml_feats_dilate_clumps.kea".format(self.params['tile']))
            rsgislib.segmentation.clump(gmw_mng_dilate_sml_feats_dilate_img, gmw_mng_dilate_sml_feats_dilate_clumps_img, 'KEA', False, 0.0)
            rsgislib.rastergis.populateStats(gmw_mng_dilate_sml_feats_dilate_clumps_img, addclrtab=False, calcpyramids=False, ignorezero=True)

            bs = [rsgislib.rastergis.BandAttStats(band=1, maxField='chng')]
            rsgislib.rastergis.populateRATWithStats(chgn_rgns_rm_sml_img, gmw_mng_dilate_sml_feats_dilate_clumps_img, bs)

            bs = [rsgislib.rastergis.BandAttStats(band=1, maxField='gmw')]
            rsgislib.rastergis.populateRATWithStats(self.params['gmw_tile'], gmw_mng_dilate_sml_feats_dilate_clumps_img, bs)

            chng_overlap = rsgislib.rastergis.ratutils.getColumnData(gmw_mng_dilate_sml_feats_dilate_clumps_img, "chng")
            gmw_overlap = rsgislib.rastergis.ratutils.getColumnData(gmw_mng_dilate_sml_feats_dilate_clumps_img, "gmw")
            fill_feats = numpy.zeros_like(chng_overlap)
            fill_feats[(chng_overlap == 1) & (gmw_overlap == 1)] = 1
            rsgislib.rastergis.ratutils.setColumnData(gmw_mng_dilate_sml_feats_dilate_clumps_img, "fill_feats", fill_feats)

            gmw_mng_chng_fill_feats_img = os.path.join(self.params['tmp_dir'], "{}_mng_potchng_sml_feats_rgns.kea".format(self.params['tile']))
            rsgislib.rastergis.exportCol2GDALImage(gmw_mng_dilate_sml_feats_dilate_clumps_img, gmw_mng_chng_fill_feats_img, "KEA", rsgislib.TYPE_8UINT, 'fill_feats')

            band_defns = [
                rsgislib.imagecalc.BandDefn('mng', self.params['gmw_tile'], 1),
                rsgislib.imagecalc.BandDefn('potfill', gmw_mng_dilate_sml_feats_img, 1),
                rsgislib.imagecalc.BandDefn('fillrgns', gmw_mng_chng_fill_feats_img, 1),
                rsgislib.imagecalc.BandDefn('chng', chgn_rgns_rm_sml_img, 1)]
            rsgislib.imagecalc.bandMath(self.params['out_img'], '(mng==1)?0:(potfill==1)&&(fillrgns==1)?1:chng', 'KEA', rsgislib.TYPE_8UINT, band_defns)
            rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        else:
            band_defns = [rsgislib.imagecalc.BandDefn('b1', self.params['chng_rgns_img'], 1)]
            rsgislib.imagecalc.bandMath(self.params['out_img'], '0', 'KEA', rsgislib.TYPE_8UINT, band_defns)
            rsgislib.rastergis.populateStats(self.params['out_img'], addclrtab=True, calcpyramids=True, ignorezero=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "chng_rgns_img", "out_img", "tmp_dir"]


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


