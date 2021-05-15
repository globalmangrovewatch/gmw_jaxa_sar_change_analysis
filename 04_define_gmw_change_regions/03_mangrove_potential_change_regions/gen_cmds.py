from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import pathlib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        img_tiles = glob.glob(kwargs['in_tiles_path'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile = tile_basename.split('_')[1]

            gmw_buf_tile = os.path.join(kwargs['tiles_buf_path'], '{}_buf_rgns.kea'.format(basename))
            min_dB_img = os.path.join(kwargs['min_dB_img_path'], '{}_min_hh_db_mskd.kea'.format(tile))
            max_dB_img = os.path.join(kwargs['max_dB_img_path'], '{}_max_hh_db_mskd.kea'.format(tile))
            diff_dB_img = os.path.join(kwargs['diff_dB_img_path'], '{}_dmaxmin_hh_db_mskd.kea'.format(tile))

            if not os.path.exists(diff_dB_img):
                diff_dB_img = None

            if not os.path.exists(min_dB_img):
                min_dB_img = None

            if not os.path.exists(max_dB_img):
                max_dB_img = None

            if not os.path.exists(gmw_buf_tile):
                gmw_buf_tile = None

            gmw_buf_chng_rgns_img = os.path.join(kwargs['out_tiles_dir'], '{}_v3_init_chng_rgns.kea'.format(tile_basename))

            if (not os.path.exists(gmw_buf_chng_rgns_img)):
                print("rm {}".format(gmw_buf_tile))
                c_dict = dict()
                c_dict['tile'] = tile
                c_dict['gmw_tile'] = gmw_tile
                c_dict['gmw_buf_tile'] = gmw_buf_tile
                c_dict['min_dB_img'] = min_dB_img
                c_dict['max_dB_img'] = max_dB_img
                c_dict['diff_dB_img'] = diff_dB_img
                c_dict['gmw_buf_chng_rgns_img'] = gmw_buf_chng_rgns_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_buf_chng_rgns".format(tile_basename))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(in_tiles_path='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
                              tiles_buf_path='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_v3_init_buffer/',
                              min_dB_img_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/min_dB',
                              max_dB_img_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/max_dB',
                              diff_dB_img_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/dmaxmin_dB',
                              out_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_v3_init_change_regions',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.pop_params_db()
        self.create_slurm_sub_sh("buffer_gmw_regions", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("find_potential_mng_chng_regions.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'find_potential_mng_chng_regions'
    process_tools_cls = 'FindPotentialMngChngRegions'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
