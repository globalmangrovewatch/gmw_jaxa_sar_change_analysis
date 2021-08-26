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

            gmw_dist_regions_img = os.path.join(kwargs['gmw_dist_path'], '{}_dist_pxls.kea'.format(tile_basename))
            gmw_rmsml_chng_rgns_img = os.path.join(kwargs['init_potent_chng'], '{}_v3_init_chng_rgns_rmsml.kea'.format(tile_basename))
            gmw_morph_chng_rgns_img = os.path.join(kwargs['out_tiles_dir'], '{}_v3_init_chng_rgns_rmsml_morph.kea'.format(tile_basename))

            if (not os.path.exists(gmw_morph_chng_rgns_img)):
                #print("rm {}".format(gmw_rmsml_chng_rgns_img))
                c_dict = dict()
                c_dict['tile'] = tile
                c_dict['gmw_tile'] = gmw_tile
                c_dict['gmw_dist_img'] = gmw_dist_regions_img
                c_dict['gmw_pot_chng_rgns_img'] = gmw_rmsml_chng_rgns_img
                c_dict['gmw_morph_chng_rgns_img'] = gmw_morph_chng_rgns_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_morph_chng_rgns".format(tile_basename))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(in_tiles_path='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
                              init_potent_chng='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_v3_init_change_regions_rm_sml',
                              gmw_dist_path='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_v3_init_dist',
                              out_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_v3_init_change_regions_rm_sml_morph',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.pop_params_db()
        self.create_slurm_sub_sh("pot_chng_morph", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_img_tile.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_img_tile'
    process_tools_cls = 'ProcessImgTile'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
