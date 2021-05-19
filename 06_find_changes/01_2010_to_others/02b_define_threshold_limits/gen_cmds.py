from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        rsgis_utils = rsgislib.RSGISPyUtils()
        prjs_lut = rsgis_utils.readJSON2Dict(kwargs['prjs_lut_file'])
        for gmw_prj in prjs_lut:

            proj_thres_files = list()
            for year in kwargs['years']:
                prj_thres_file = self.find_file(kwargs['prj_thres_dir'].format(year), "{}*.json".format(gmw_prj))
                if prj_thres_file is not None:
                    proj_thres_files.append(prj_thres_file)


            if len(proj_thres_files) > 0:
                out_file = os.path.join(kwargs['out_dir'], '{}_thres_limits.json'.format(gmw_prj))

                if (not os.path.exists(out_file)):
                    c_dict = dict()
                    c_dict['gmw_prj'] = gmw_prj
                    c_dict['proj_thres_files'] = proj_thres_files
                    c_dict['out_file'] = out_file
                    c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_chng_thres_limits".format(gmw_prj))
                    if not os.path.exists(c_dict['tmp_dir']):
                        os.mkdir(c_dict['tmp_dir'])
                    self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            prjs_lut_file='/scratch/a.pfb/gmw_v3_change/scripts/03_prepare_datasets/09_create_project_tile_lut/gmw_projects_luts.json',
            prj_thres_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_{}_prj_thres',
            years=['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020'],
            out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_prj_thres_limits',
            tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_2010_XXXX_prj_thres", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("calc_project_thresholds.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'calc_project_thresholds'
    process_tools_cls = 'CalcProjectThreholds'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
