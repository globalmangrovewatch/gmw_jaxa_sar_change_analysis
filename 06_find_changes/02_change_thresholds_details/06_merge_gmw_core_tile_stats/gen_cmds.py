from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_prj_dir']):
            os.mkdir(kwargs['out_prj_dir'])
        if not os.path.exists(kwargs['out_tile_dir']):
            os.mkdir(kwargs['out_tile_dir'])

        rsgis_utils = rsgislib.RSGISPyUtils()
        prjs_lut = rsgis_utils.readJSON2Dict(kwargs['prjs_lut_file'])
        for gmw_prj in prjs_lut:
            gmw_prj_tiles = prjs_lut[gmw_prj]

            mng_data_files = list()

            for tile_name in gmw_prj_tiles:
                tile_basename = "GMW_{}".format(tile_name)
                mng_data_file = os.path.join(kwargs['pxl_data_dir'], '{}_{}_mng_dB.h5'.format(tile_basename, kwargs['sar_year']))

                if os.path.exists(mng_data_file):
                    mng_data_files.append(mng_data_file)

            if len(mng_data_files) > 0:
                out_cmp_file = os.path.join(kwargs['out_prj_dir'], '{}_{}_core_sum_stats_cmp.txt'.format(gmw_prj, kwargs['sar_year']))
                out_prj_stats = os.path.join(kwargs['out_prj_dir'], '{}_{}_core_sum_stats.json'.format(gmw_prj, kwargs['sar_year']))

                if (not os.path.exists(out_cmp_file)):
                    for data_file in mng_data_files:
                        print("rm {}".format(data_file))

                    c_dict = dict()
                    c_dict['gmw_prj'] = gmw_prj
                    c_dict['year'] = kwargs['sar_year']
                    c_dict['mng_data_files'] = mng_data_files
                    c_dict['out_tile_dir'] = kwargs['out_tile_dir']
                    c_dict['out_prj_stats'] = out_prj_stats
                    c_dict['out_cmp_file'] = out_cmp_file
                    c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_{}_core_sum_stats".format(gmw_prj, kwargs['sar_year']))
                    if not os.path.exists(c_dict['tmp_dir']):
                        os.mkdir(c_dict['tmp_dir'])
                    self.params.append(c_dict)


    def run_gen_commands(self):
        for year in ['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']:
            self.gen_command_info(
                prjs_lut_file='/scratch/a.pfb/gmw_v3_change/scripts/03_prepare_datasets/09_create_project_tile_lut/gmw_projects_luts.json',
                pxl_data_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_core_{}_pxl_vals'.format(year),
                sar_year=year,
                out_prj_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_core_{}_prj_sar_stats'.format(year),
                out_tile_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_core_{}_tile_sar_stats'.format(year),
                tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_2010_XXXX_prj_plots", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_gmw_core_stats.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_gmw_core_stats'
    process_tools_cls = 'CreateGMWCoreStats'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
