from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pathlib
import rsgislib
import rsgislib.imagecalc
import rsgislib.vectorutils

logger = logging.getLogger(__name__)


class VectoriseMngPotentChgnRgns(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='vectorise_mng_potent_chng_rgns.py', descript=None)

    def do_processing(self, **kwargs):
        pxl_count = rsgislib.imagecalc.countPxlsOfVal(self.params['gmw_potent_chng_tile'], vals=[1])
        print("N Pixels: ", pxl_count[0])

        if pxl_count[0] > 0:
            rsgislib.vectorutils.polygoniseRaster2VecLyr(self.params['gmw_potent_chng_tile_vec'], 'mng_potent_chng', 'GPKG',
                                                         self.params['gmw_potent_chng_tile'], imgBandNo=1,
                                                         maskImg= self.params['gmw_potent_chng_tile'], imgMaskBandNo=1)

        pathlib.Path(self.params['out_cmp_file']).touch()



    def required_fields(self, **kwargs):
        return ["tile", "gmw_potent_chng_tile", "gmw_potent_chng_tile_vec", "out_cmp_file"]

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


