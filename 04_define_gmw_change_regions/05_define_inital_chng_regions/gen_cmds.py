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

            gmw_gadm_img = os.path.join(kwargs['gadm_tiles_dir'], '{}_gadm.kea'.format(tile_basename))
            gmw_coastal_img = os.path.join(kwargs['coastal_tiles_dir'], '{}_coastal_area.kea'.format(tile_basename))
            gmw_dist_img = os.path.join(kwargs['gmw_dist_dir'], '{}_dist_pxls.kea'.format(basename))
            gmw_srtm_img = os.path.join(kwargs['srtm_tiles_dir'], '{}_srtm.kea'.format(tile_basename))
            gmw_bathy_img = os.path.join(kwargs['bathy_tiles_dir'], '{}_bathy.kea'.format(tile_basename))
            gmw_ocean_img = os.path.join(kwargs['ocean_tile_dir'], '{}_ocean_water.kea'.format(tile_basename))

            out_img = os.path.join(kwargs['out_dir'], '{}_pot_chng_ocean_chg_rgns.kea'.format(tile_basename))

            if (not os.path.exists(out_img)):
                print("rm {}".format(gmw_dist_img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['gmw_dist'] = gmw_dist_img
                c_dict['gadm_img'] = gmw_gadm_img
                c_dict['coastal_area'] = gmw_coastal_img
                c_dict['srtm_img'] = gmw_srtm_img
                c_dict['gmw_bathy_img'] = gmw_bathy_img
                c_dict['gmw_ocean_img'] = gmw_ocean_img
                c_dict['out_img'] = out_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_pot_chng_ocean_chg_rgns".format(tile_basename))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
                              gadm_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/other_base_data/gadm_gmw_tiles',
                              coastal_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/other_base_data/gadm_coastal_area',
                              gmw_dist_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_v3_init_dist',
                              srtm_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/other_base_data/srtm_gmw_tiles',
                              bathy_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/other_base_data/bathymetry_gmw_tiles',
                              ocean_tile_dir='/scratch/a.pfb/gmw_v3_change/data/other_base_data/ocean_water_tiles',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/pot_chng_ocean_chg_rgns',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.pop_params_db()
        self.create_slurm_sub_sh("pot_chng_ocean_chg_rgns", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
