from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import pathlib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        img_tiles = glob.glob(kwargs['tiles_path'])
        for img_tile in img_tiles:
            tile_basename = self.get_file_basename(img_tile)
            tile = tile_basename.split('_')[0]

            vec_file = os.path.join(kwargs['tiles_out_vec'], '{}_vec.gpkg'.format(tile_basename))

            if (not os.path.exists(vec_file)):
                print("rm {}".format(img_tile))
                c_dict = dict()
                c_dict['tile'] = tile
                c_dict['img'] = img_tile
                c_dict['out_vec'] = vec_file
                c_dict['lyr_name'] = kwargs['lyr_name']
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(tiles_path='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                              lyr_name='gmw_v3',
                              tiles_out_vec='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3_vecs')

        self.gen_command_info(tiles_path='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_chg_rgn/*.kea',
                              lyr_name='gmw_2010_potent_chng',
                              tiles_out_vec='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_chg_rgn_vecs')

        self.gen_command_info(tiles_path='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_stats_rgn/*.kea',
                              lyr_name='gmw_2010_potent_chng_stats_rgns',
                              tiles_out_vec='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_stats_rgn_vecs')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_2010_init_water_mask_vecs", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_vector_lyr.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_vector_lyr'
    process_tools_cls = 'CreateVectorLayer'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
