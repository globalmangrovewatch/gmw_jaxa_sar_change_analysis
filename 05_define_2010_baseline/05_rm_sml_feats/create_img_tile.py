from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imagemorphology
import rsgislib.segmentation
import rsgislib.rastergis

logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        chgn_rgns_clmps_img = os.path.join(self.params['tmp_dir'], "{}_chng_rgn_clumps.kea".format(self.params['tile']))
        rsgislib.segmentation.clump(self.params['chng_rgns_img'], chgn_rgns_clmps_img, 'KEA', False, 0.0)

        morph_op = os.path.join(self.params['tmp_dir'], "{}_morph_op.gmtxt".format(self.params['tile']))
        rsgislib.imagemorphology.createCircularOp(morph_op, 3)

        chgn_rgns_erode_img = os.path.join(self.params['tmp_dir'], "{}_chng_rgn_clumps.kea".format(self.params['tile']))
        rsgislib.imagemorphology.imageErode(self.params['chng_rgns_img'], chgn_rgns_erode_img, morph_op, True, 3, "KEA", rsgislib.TYPE_8UINT)

        bs = [rsgislib.rastergis.BandAttStats(band=1, minField='chng_min', maxField='chng_max')]
        rsgislib.rastergis.populateRATWithStats(chgn_rgns_erode_img, chgn_rgns_clmps_img, bs)

        rsgislib.rastergis.exportCol2GDALImage(chgn_rgns_clmps_img, self.params['out_img'], "KEA", rsgislib.TYPE_8UINT, 'chng_max')
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


