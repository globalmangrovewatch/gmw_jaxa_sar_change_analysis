from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pathlib
import rsgislib
import rsgislib.vectorutils
import rsgislib.imagecalc

logger = logging.getLogger(__name__)


class CreateVectorLayer(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_vector_lyr.py', descript=None)

    def do_processing(self, **kwargs):
        pxl_count = rsgislib.imagecalc.countPxlsOfVal(self.params['img'], vals=[1])
        print("N Pixels: ", pxl_count[0])

        if pxl_count[0] > 0:
            rsgislib.vectorutils.polygoniseRaster2VecLyr(self.params['out_vec'], self.params['lyr_name'], 'GPKG',
                                                         self.params['img'], imgBandNo=1,
                                                         maskImg= self.params['img'], imgMaskBandNo=1)

        pathlib.Path(self.params['out_cmp_file']).touch()



    def required_fields(self, **kwargs):
        return ["tile", "img", "out_vec", "lyr_name", "out_cmp_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_vec']] = 'gdal_vector'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_vec']):
            os.remove(self.params['out_vec'])

        if os.path.exists(self.params['out_cmp_file']):
            os.remove(self.params['out_cmp_file'])


if __name__ == "__main__":
    CreateVectorLayer().std_run()


