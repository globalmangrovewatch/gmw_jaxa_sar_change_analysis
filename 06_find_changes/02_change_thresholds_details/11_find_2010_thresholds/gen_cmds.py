from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_hh_dir']):
            os.mkdir(kwargs['out_hh_dir'])

        if not os.path.exists(kwargs['out_hv_dir']):
            os.mkdir(kwargs['out_hv_dir'])

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile_name = tile_basename.split('_')[1]

            sar_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)
            if os.path.exists(sar_scn_dir):
                sar_img = os.path.join(sar_scn_dir, '{}_2010_db.kea'.format(tile_name))
                sar_vld_img = os.path.join(sar_scn_dir, '{}_2010_bin_vmsk.kea'.format(tile_name))
                if not os.path.exists(sar_img):
                    sar_img = None
                    sar_vld_img = None
            else:
                sar_img = None
                sar_vld_img = None

            potent_chng_msk_img = os.path.join(kwargs['potent_chng_msk_dir'], '{}_2010_v3_chg_rgn.kea'.format(tile_basename))


            out_hv_file = os.path.join(kwargs['out_hv_dir'], '{}_2010_threshold_tests.json'.format(tile_basename))

            if (not os.path.exists(out_hv_file)):
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['potent_chng_msk_img'] = potent_chng_msk_img
                c_dict['band'] = 'HV'
                c_dict['sar_img'] = sar_img
                c_dict['sar_vld_img'] = sar_vld_img
                c_dict['out_file'] = out_hv_file
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_2010_threshold_tests".format(tile_basename))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)

            out_hh_file = os.path.join(kwargs['out_hh_dir'], '{}_2010_threshold_tests.json'.format(tile_basename))

            if (not os.path.exists(out_hh_file)):
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['potent_chng_msk_img'] = potent_chng_msk_img
                c_dict['band'] = 'HH'
                c_dict['sar_img'] = sar_img
                c_dict['sar_vld_img'] = sar_vld_img
                c_dict['out_file'] = out_hh_file
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_2010_threshold_tests".format(tile_basename))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                              potent_chng_msk_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_chg_rgn',
                              sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010',
                              out_hh_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_hh_test_thresholds',
                              out_hv_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_hv_test_thresholds',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_2010_test_thresholds", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
