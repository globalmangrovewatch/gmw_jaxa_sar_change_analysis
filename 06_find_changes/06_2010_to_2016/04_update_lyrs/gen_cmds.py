from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)

            potent_chng_msk_img = os.path.join(kwargs['potent_chng_msk_dir'], '{}_2010_v3_chg_rgn.kea'.format(tile_basename))
            mng_chng_img = os.path.join(kwargs['chng_img_dir'], '{}_{}_mng_chng.kea'.format(tile_basename, kwargs['sar_year']))
            nmng_chng_img = os.path.join(kwargs['chng_img_dir'], '{}_{}_not_mng_chng.kea'.format(tile_basename, kwargs['sar_year']))

            out_gmw_up_msk = os.path.join(kwargs['out_dir'], '{}_{}_v3_init.kea'.format(tile_basename, kwargs['sar_year']))
            out_gmw_up_potent_chng_msk = os.path.join(kwargs['out_dir'], '{}_{}_v3_chg_rgn.kea'.format(tile_basename, kwargs['sar_year']))

            if (not os.path.exists(out_gmw_up_msk)) or (not os.path.exists(out_gmw_up_potent_chng_msk)):
                print("rm {}".format(mng_chng_img))
                print("rm {}".format(nmng_chng_img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['potent_chng_msk_img'] = potent_chng_msk_img
                c_dict['mng_chng_img'] = mng_chng_img
                c_dict['nmng_chng_img'] = nmng_chng_img
                c_dict['out_gmw_up_msk'] = out_gmw_up_msk
                c_dict['out_gmw_up_potent_chng_msk'] = out_gmw_up_potent_chng_msk
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                              chng_img_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_2016_chngs',
                              potent_chng_msk_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_chg_rgn',
                              sar_year='2016',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2016_v3')
        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_init_2016_v3", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
