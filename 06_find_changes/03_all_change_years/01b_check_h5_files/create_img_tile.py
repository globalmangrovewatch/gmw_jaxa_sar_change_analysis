from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import h5py
import numpy
import pathlib

logger = logging.getLogger(__name__)

class CreateImageTile(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_img_tile.py', descript=None)

    def do_processing(self, **kwargs):
        fH5 = h5py.File(self.params['h5_file'], 'r')
        data_shp = fH5['DATA/DATA'].shape
        print(data_shp)
        data = numpy.array(fH5['DATA/DATA'])
        data = None
        fH5.close()
        pathlib.Path(self.params['out_cmp_file']).touch()


    def required_fields(self, **kwargs):
        return ["h5_file", "out_cmp_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_cmp_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_cmp_file']):
            os.remove(self.params['out_cmp_file'])

if __name__ == "__main__":
    CreateImageTile().std_run()


