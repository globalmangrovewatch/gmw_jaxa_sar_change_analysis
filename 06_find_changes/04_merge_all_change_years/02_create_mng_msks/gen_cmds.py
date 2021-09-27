

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_mjr_dir']):
            os.mkdir(kwargs['out_mjr_dir'])

        if not os.path.exists(kwargs['out_min_dir']):
            os.mkdir(kwargs['out_min_dir'])

        if not os.path.exists(kwargs['out_max_dir']):
            os.mkdir(kwargs['out_max_dir'])

        img_tiles = glob.glob(kwargs['gmw_sum_tiles'])
        for gmw_sum_tile in img_tiles:
            basename = self.get_file_basename(gmw_sum_tile)
            tile_basename = self.get_file_basename(gmw_sum_tile, n_comps=2)

            out_gmw_mng_mjr_ext_img = os.path.join(kwargs['out_mjr_dir'], '{}_{}_mng_mjr_ext_v3.kea'.format(tile_basename, kwargs['year']))
            out_gmw_mng_min_ext_img = os.path.join(kwargs['out_min_dir'], '{}_{}_mng_min_ext_v3.kea'.format(tile_basename, kwargs['year']))
            out_gmw_mng_max_ext_img = os.path.join(kwargs['out_max_dir'], '{}_{}_mng_max_ext_v3.kea'.format(tile_basename, kwargs['year']))

            if (not os.path.exists(out_gmw_mng_mjr_ext_img)) or (not os.path.exists(out_gmw_mng_min_ext_img)) or (not os.path.exists(out_gmw_mng_max_ext_img)):
                #print("rm {}".format(gmw_sum_tile))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_sum_tile'] = gmw_sum_tile
                c_dict['out_gmw_mng_mjr_ext_img'] = out_gmw_mng_mjr_ext_img
                c_dict['out_gmw_mng_min_ext_img'] = out_gmw_mng_min_ext_img
                c_dict['out_gmw_mng_max_ext_img'] = out_gmw_mng_max_ext_img
                self.params.append(c_dict)


    def run_gen_commands(self):

        years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        for year in years:
            self.gen_command_info(gmw_sum_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_{}/*.kea'.format(year),
                                  year=year,
                                  out_mjr_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_mjr_ext_{}'.format(year),
                                  out_min_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_min_ext_{}'.format(year),
                                  out_max_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_mng_max_ext_{}'.format(year))

        self.pop_params_db()
        self.create_slurm_sub_sh("create_mng_ext_msks", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 n_xtr_cmds=20, job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_img_tile.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_img_tile'
    process_tools_cls = 'CreateImageTile'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
