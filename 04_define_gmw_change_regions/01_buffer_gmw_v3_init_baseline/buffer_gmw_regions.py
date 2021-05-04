from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis


logger = logging.getLogger(__name__)


class BufferGMWRegions(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='buffer_gmw_regions.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        gmw_dist_img = os.path.join(self.params['tmp_dir'], "{}_dist_img.kea".format(self.params['tile']))
        rsgislib.imagecalc.calcDist2ImgVals(self.params['gmw_tile'], gmw_dist_img, [1], valsImgBand=1, gdalformat='KEA',
                                            maxDist=300, noDataVal=301, unitGEO=False)

        rsgislib.imagecalc.imageMath(gmw_dist_img, self.params['gmw_buf_regions_img'], '(b1>0)&&(b1<300)?1:0', 'KEA', rsgislib.TYPE_8UINT)
        rsgislib.rastergis.populateStats(self.params['gmw_buf_regions_img'], addclrtab=True, calcpyramids=True, ignorezero=True)
        
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])



    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "gmw_buf_regions_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['gmw_buf_regions_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['gmw_buf_regions_img']):
            os.remove(self.params['gmw_buf_regions_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    BufferGMWRegions().std_run()


