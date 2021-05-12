from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.vectorutils

logger = logging.getLogger(__name__)


class CreateVectorLayer(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_vector_lyr.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.vectorutils.polygoniseRaster2VecLyr(self.params['out_vec'], self.params['lyr_name'], 'GPKG',
                                                     self.params['img'], imgBandNo=1,
                                                     maskImg= self.params['img'], imgMaskBandNo=1)



    def required_fields(self, **kwargs):
        return ["tile", "img", "out_vec", "lyr_name"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_vec']] = 'gdal_vector'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_vec']):
            os.remove(self.params['out_vec'])


if __name__ == "__main__":
    CreateVectorLayer().std_run()


