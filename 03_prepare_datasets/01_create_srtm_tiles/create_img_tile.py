from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imageutils.imagelut
import rsgislib.imageutils


logger = logging.getLogger(__name__)


class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        rsgis_utils = rsgislib.RSGISPyUtils()
        tile_bbox = rsgis_utils.getImageBBOX(self.params['gmw_tile'])

        base_data_img = rsgislib.imageutils.imagelut.getRasterLyr(tile_bbox, self.params['lut_file'], self.params['lut_lyr'], self.params['tmp_dir'])

        rsgislib.imageutils.resampleImage2Match(self.params['gmw_tile'], base_data_img, self.params['out_img'], 'KEA', 'cubicspline', datatype=rsgislib.TYPE_16INT, noDataVal=-32768)
        rsgislib.imageutils.popImageStats(self.params['out_img'], usenodataval=True, nodataval=-32768, calcpyramids=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])


    def required_fields(self, **kwargs):
        return ["tile", "gmw_tile", "lut_file", "lut_lyr", "out_img", "tmp_dir"]

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


