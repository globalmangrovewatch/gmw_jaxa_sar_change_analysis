from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.vectorutils

logger = logging.getLogger(__name__)


class VectoriseMngPotentChgnRgns(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='vectorise_mng_potent_chng_rgns.py', descript=None)

    def do_processing(self, **kwargs):
        rsgislib.vectorutils.polygoniseRaster2VecLyr(self.params['gmw_potent_chng_tile_vec'], 'mng_potent_chng', 'GPKG',
                                                     self.params['gmw_potent_chng_tile'], imgBandNo=1,
                                                     maskImg= self.params['gmw_potent_chng_tile'], imgMaskBandNo=1)



    def required_fields(self, **kwargs):
        return ["tile", "gmw_potent_chng_tile", "gmw_potent_chng_tile_vec"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['gmw_potent_chng_tile_vec']] = 'gdal_vector'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['gmw_potent_chng_tile_vec']):
            os.remove(self.params['gmw_potent_chng_tile_vec'])


if __name__ == "__main__":
    VectoriseMngPotentChgnRgns().std_run()


