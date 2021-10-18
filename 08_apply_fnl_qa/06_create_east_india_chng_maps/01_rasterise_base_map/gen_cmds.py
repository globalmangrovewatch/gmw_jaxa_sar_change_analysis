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

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile_name = tile_basename.split('_')[1]

            if tile_name in ["N19E072", "N19E073", "N18E073", "N17E073", "N16E073",
                             "N16E074", "N15E074", "N14E074", "N13E074", "N13E075",
                             "N12E075", "N11E075", "N11E076", "N10E076", "N10E078",
                             "N10E079", "N10E080", "N09E076", "N09E077", "N09E078",
                             "N09E079", "N09E080"]:

                out_img = os.path.join(kwargs['out_dir'], '{}_east_india_base.kea'.format(tile_basename))

                if not os.path.exists(out_img):
                    c_dict = dict()
                    c_dict['tile'] = tile_name
                    c_dict['gmw_tile'] = gmw_tile
                    c_dict['vec_file'] = kwargs['vec_file']
                    c_dict['vec_lyr'] = kwargs['vec_lyr']
                    c_dict['out_img'] = out_img
                    self.params.append(c_dict)


    def run_gen_commands(self):

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_2020_v309/*.kea',
                              vec_file='mng-gap-fill-india-QA.gpkg',
                              vec_lyr='mng-gap-fill-india-QA',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_base',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        
        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_east_india_base", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=1,
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
