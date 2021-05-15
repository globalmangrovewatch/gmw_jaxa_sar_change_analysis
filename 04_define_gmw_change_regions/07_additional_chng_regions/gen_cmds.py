from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import pathlib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)

            pot_chng_rgns_img = os.path.join(kwargs['pot_chng_regs_tiles_dir'], '{}_gmw_v3_pot_chng_ocean_chg_rgns.kea'.format(tile_basename))
            nasa_chng_img = os.path.join(kwargs['nasa_chng_tiles'], '{}_nasa_change.kea'.format(tile_basename))
            gmw_v2_union_img = os.path.join(kwargs['gmw_v2_union_tiles'], '{}_gmw_v2_union.kea'.format(tile_basename))

            out_img = os.path.join(kwargs['out_dir'], '{}_gmw_v3_pot_chng_ocean_chg_rgns_up_gmwv2_nasa.kea'.format(tile_basename))

            if (not os.path.exists(out_img)):
                print("rm {}".format(pot_chng_rgns_img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['pot_chng_rgns_img'] = pot_chng_rgns_img
                c_dict['nasa_chng_img'] = nasa_chng_img
                c_dict['gmw_v2_union_img'] = gmw_v2_union_img
                c_dict['out_img'] = out_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_pot_chng_ocean_chg_rgns_up_v2_nasa".format(tile_basename))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
                              pot_chng_regs_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/pot_gmw_chng_ocean_chg_rgns',
                              nasa_chng_tiles='/scratch/a.pfb/gmw_v3_change/data/other_base_data/nasa_change',
                              gmw_v2_union_tiles='/scratch/a.pfb/gmw_v3_change/data/other_base_data/gmw_v2_union',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/pot_gmw_chng_ocean_chg_rgns_nasa_gmwv2_updates',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.pop_params_db()
        self.create_slurm_sub_sh("pot_gmw_chng_ocean_chg_rgns_nasa_gmwv2", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
