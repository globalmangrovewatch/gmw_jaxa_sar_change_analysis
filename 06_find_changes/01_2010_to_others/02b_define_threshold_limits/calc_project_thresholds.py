from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pprint
import shutil
import rsgislib
import rsgislib.imageutils
import numpy


logger = logging.getLogger(__name__)


class CalcProjectThreholds(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='calc_project_thresholds.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        rsgis_utils = rsgislib.RSGISPyUtils()

        # Create output data structure.
        out_thres_lut = dict()
        out_thres_lut['mng_hh_low'] = 0.0
        out_thres_lut['mng_hh_up'] = 0.0
        out_thres_lut['nmng_hh_low'] = 0.0
        out_thres_lut['nmng_hh_up'] = 0.0
        out_thres_lut['mng_hv_low'] = 0.0
        out_thres_lut['mng_hv_up'] = 0.0
        out_thres_lut['nmng_hv_low'] = 0.0
        out_thres_lut['nmng_hv_up'] = 0.0

        mng_hh_thresholds = list()
        mng_hv_thresholds = list()
        nmng_hh_thresholds = list()
        nmng_hv_thresholds = list()

        for thres_file in self.params['proj_thres_files']:
            c_thres_lut = rsgis_utils.readJSON2Dict(thres_file)
            if c_thres_lut['mng_hh'] < 0:
                mng_hh_thresholds.append(c_thres_lut['mng_hh'])
            if c_thres_lut['mng_hv'] < 0:
                mng_hv_thresholds.append(c_thres_lut['mng_hv'])
            if c_thres_lut['nmng_hh'] < 0:
                nmng_hh_thresholds.append(c_thres_lut['nmng_hh'])
            if c_thres_lut['nmng_hv'] < 0:
                nmng_hv_thresholds.append(c_thres_lut['nmng_hv'])

        print(mng_hh_thresholds)
        print(mng_hv_thresholds)
        print(nmng_hh_thresholds)
        print(nmng_hv_thresholds)

        mng_hh_limits = numpy.percentile(mng_hh_thresholds, [10, 90])
        mng_hv_limits = numpy.percentile(mng_hv_thresholds, [10, 90])
        nmng_hh_limits = numpy.percentile(nmng_hh_thresholds, [10, 90])
        nmng_hv_limits = numpy.percentile(nmng_hv_thresholds, [10, 90])

        out_thres_lut['mng_hh_low'] = mng_hh_limits[0]
        out_thres_lut['mng_hh_up'] = mng_hh_limits[1]
        out_thres_lut['mng_hv_low'] = mng_hv_limits[0]
        out_thres_lut['mng_hv_up'] = mng_hv_limits[1]

        out_thres_lut['nmng_hh_low'] = nmng_hh_limits[0]
        out_thres_lut['nmng_hh_up'] = nmng_hh_limits[1]
        out_thres_lut['nmng_hv_low'] = nmng_hv_limits[0]
        out_thres_lut['nmng_hv_up'] = nmng_hv_limits[1]

        mng_hh_glb_lmts = [-1452.46048872,  -1060.64634217]
        mng_hv_glb_lmts = [-1941.87189307, -1577.96959371]
        nmng_hh_glb_lmts = [-1999.16027657, -1254.55570656]
        nmng_hv_glb_lmts = [-2506.76941836, -2172.45179869]

        if out_thres_lut['mng_hh_low'] < mng_hh_glb_lmts[0]:
            out_thres_lut['mng_hh_low'] = mng_hh_glb_lmts[0]
        if out_thres_lut['mng_hh_up'] > mng_hh_glb_lmts[1]:
            out_thres_lut['mng_hh_up'] = mng_hh_glb_lmts[1]

        if out_thres_lut['mng_hv_low'] < mng_hv_glb_lmts[0]:
            out_thres_lut['mng_hv_low'] = mng_hv_glb_lmts[0]
        if out_thres_lut['mng_hv_up'] > mng_hv_glb_lmts[1]:
            out_thres_lut['mng_hv_up'] = mng_hv_glb_lmts[1]

        if out_thres_lut['nmng_hh_low'] < nmng_hh_glb_lmts[0]:
            out_thres_lut['nmng_hh_low'] = nmng_hh_glb_lmts[0]
        if out_thres_lut['nmng_hh_up'] > nmng_hh_glb_lmts[1]:
            out_thres_lut['nmng_hh_up'] = nmng_hh_glb_lmts[1]

        if out_thres_lut['nmng_hv_low'] < nmng_hv_glb_lmts[0]:
            out_thres_lut['nmng_hv_low'] = nmng_hv_glb_lmts[0]
        if out_thres_lut['nmng_hv_up'] > nmng_hv_glb_lmts[1]:
            out_thres_lut['nmng_hv_up'] = nmng_hv_glb_lmts[1]
        
        pprint.pprint(out_thres_lut)

        # Export output thresholds.
        rsgis_utils.writeDict2JSON(out_thres_lut, self.params['out_file'])

        for thres_file in self.params['proj_thres_files']:
            c_thres_lut = rsgis_utils.readJSON2Dict(thres_file)
            file_name = rsgis_utils.get_file_basename(thres_file)
            if (c_thres_lut['mng_hh'] > out_thres_lut['mng_hh_low']) and (c_thres_lut['mng_hh'] < out_thres_lut['mng_hh_up']):
                print("{} in range for MNG HH".format(file_name))
            if (c_thres_lut['mng_hv'] > out_thres_lut['mng_hv_low']) and (c_thres_lut['mng_hv'] < out_thres_lut['mng_hv_up']):
                print("{} in range for MNG HV".format(file_name))
            if (c_thres_lut['nmng_hh'] > out_thres_lut['nmng_hh_low']) and (c_thres_lut['nmng_hh'] < out_thres_lut['nmng_hh_up']):
                print("{} in range for NOT-MNG HH".format(file_name))
            if (c_thres_lut['nmng_hv'] > out_thres_lut['nmng_hv_low']) and (c_thres_lut['nmng_hv'] < out_thres_lut['nmng_hv_up']):
                print("{} in range for NOT-MNG HV".format(file_name))

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["gmw_prj", "proj_thres_files", "out_file", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_file']] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_file']):
            os.remove(self.params['out_file'])

            # Reset the tmp dir
            if os.path.exists(self.params['tmp_dir']):
                shutil.rmtree(self.params['tmp_dir'])
            os.mkdir(self.params['tmp_dir'])

if __name__ == "__main__":
    CalcProjectThreholds().std_run()


