from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        rsgis_utils = rsgislib.RSGISPyUtils()
        jaxa_tile_lst = rsgis_utils.readTextFile2List(kwargs['tile_list'])

        for tile in jaxa_tile_lst:
            tile_imgs = glob.glob(kwargs['tiles_srch_path'].format(tile))
            if len(tile_imgs) > 0:
                out_min_dB_img = os.path.join(kwargs['out_min_dB_path'], '{}_min_hh_db_mskd.kea'.format(tile))
                out_max_dB_img = os.path.join(kwargs['out_max_dB_path'], '{}_max_hh_db_mskd.kea'.format(tile))
                out_diff_dB_img = os.path.join(kwargs['out_diff_dB_path'], '{}_dmaxmin_hh_db_mskd.kea'.format(tile))

                if (not os.path.exists(out_min_dB_img)) or (not os.path.exists(out_max_dB_img)) or (not os.path.exists(out_diff_dB_img)):
                    c_dict = dict()
                    c_dict['tile'] = tile
                    c_dict['sar_imgs'] = tile_imgs
                    c_dict['out_min_dB_img'] = out_min_dB_img
                    c_dict['out_max_dB_img'] = out_max_dB_img
                    c_dict['out_diff_dB_img'] = out_diff_dB_img
                    self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(tile_list='/scratch/a.pfb/gmw_v3_change/scripts/01_download_jaxa_sar/gmw_jaxa_tile_names.txt',
                              tiles_srch_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/*/{}/*_db_mskd.kea',
                              out_min_dB_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/min_dB',
                              out_max_dB_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/max_dB',
                              out_diff_dB_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/dmaxmin_dB')
        self.pop_params_db()
        self.create_slurm_sub_sh("calc_min_max_dB", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("calc_min_max_dB.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'calc_min_max_dB'
    process_tools_cls = 'CalcMinMaxdB'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
