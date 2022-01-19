from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib.tools.filetools

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(gmw_tile)
            tile_base_name = tile_base_name.replace("v3", "v25")

            tif_img = os.path.join(kwargs['tif_dir'], f"{tile_base_name}.tif")
            out_file = os.path.join(kwargs['out_dir'], f"{tile_base_name}.json")

            if not os.path.exists(out_file):
                c_dict = dict()
                c_dict['gmw_tile'] = gmw_tile
                c_dict['tif_img'] = tif_img
                c_dict['out_file'] = out_file
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(gmw_tiles = '/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                              tif_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v25_tif',
                              out_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v25_tif_chkd')

        self.pop_params_db()
        self.create_slurm_sub_sh("check_gmw_extent_mng_gtiff", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
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
