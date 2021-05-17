from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import pathlib
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils

logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        tmp_tile_img = os.path.join(self.params['tmp_dir'], "{}_1996_db_tile.kea")
        rsgislib.imageutils.resampleImage2Match(self.params['gmw_tile'], self.params['jers1_prj_dB_file'], tmp_tile_img, 'KEA', 'nearestneighbour', datatype=rsgislib.TYPE_32FLOAT, noDataVal=999, multicore=False)

        rsgislib.imagecalc.imageMath(tmp_tile_img, self.params['out_img'], 'b1==999?32767:b1*100', 'KEA', rsgislib.TYPE_16INT)
        rsgislib.imageutils.popImageStats(self.params['out_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        min_val, max_val = rsgislib.imagecalc.getImageBandMinMax(self.params['out_img'], 1, True, 32767)
        print("Min: {}".format(min_val))
        print("Max: {}".format(max_val))

        if (max_val - min_val) < 100:
            os.remove(self.params['out_img'])

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

        pathlib.Path(self.params['out_cmp_file']).touch()


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "jers1_prj_dB_file", "sar_img", "out_img", "out_cmp_file", "tmp_dir"]


    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

        if os.path.exists(self.params['out_cmp_file']):
            os.remove(self.params['out_cmp_file'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CreateImageTile().std_run()


