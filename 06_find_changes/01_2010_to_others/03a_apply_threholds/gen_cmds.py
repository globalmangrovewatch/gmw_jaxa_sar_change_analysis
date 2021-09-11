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

        rsgis_utils = rsgislib.RSGISPyUtils()
        tile_prj_lut = rsgis_utils.readJSON2Dict(kwargs['prjs_lut_file'])

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile_name = tile_basename.split('_')[1]

            gmw_prj = tile_prj_lut[tile_name]
            gmw_proj_thres_file = os.path.join(kwargs['thres_files_dir'], "{}_fnl_thresholds.json".format(gmw_prj))

            sar_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)
            if os.path.exists(sar_scn_dir):
                sar_img = os.path.join(sar_scn_dir, '{}_{}_db_mskd_reg.kea'.format(tile_name, kwargs['sar_year']))
                if not os.path.exists(sar_img):
                    sar_img = None
            else:
                sar_img = None

            potent_chng_msk_img = os.path.join(kwargs['potent_chng_msk_dir'], '{}_2010_v3_chg_rgn_qad_rm_sml.kea'.format(tile_basename))

            out_mng_chng = os.path.join(kwargs['out_dir'], '{}_{}_mng_chng.kea'.format(tile_basename, kwargs['sar_year']))
            out_nmng_chng = os.path.join(kwargs['out_dir'], '{}_{}_not_mng_chng.kea'.format(tile_basename, kwargs['sar_year']))

            out_mng_chng_upper = os.path.join(kwargs['out_dir'], '{}_{}_mng_chng_upper.kea'.format(tile_basename, kwargs['sar_year']))
            out_nmng_chng_upper = os.path.join(kwargs['out_dir'], '{}_{}_not_mng_chng_upper.kea'.format(tile_basename, kwargs['sar_year']))

            out_mng_chng_lower = os.path.join(kwargs['out_dir'], '{}_{}_mng_chng_lower.kea'.format(tile_basename, kwargs['sar_year']))
            out_nmng_chng_lower = os.path.join(kwargs['out_dir'], '{}_{}_not_mng_chng_lower.kea'.format(tile_basename, kwargs['sar_year']))

            calc_intervals = False

            out_files_present = True
            if (not os.path.exists(out_mng_chng)) or (not os.path.exists(out_nmng_chng)):
                out_files_present = False
            elif calc_intervals:
                if (os.path.exists(out_mng_chng_upper)) or (not os.path.exists(out_nmng_chng_upper)) or (not os.path.exists(out_mng_chng_lower)) or (not os.path.exists(out_nmng_chng_lower)):
                    out_files_present = False

            if  not out_files_present:
                #if (sar_vld_img is not None) and os.path.exists(sar_vld_img):
                #    print("rm {}".format(sar_vld_img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['sar_year'] = kwargs['sar_year']
                c_dict['potent_chng_msk_img'] = potent_chng_msk_img
                c_dict['sar_img'] = sar_img
                c_dict['gmw_proj_thres_file'] = gmw_proj_thres_file
                c_dict['out_mng_chng'] = out_mng_chng
                c_dict['out_nmng_chng'] = out_nmng_chng
                c_dict['out_mng_chng_upper'] = out_mng_chng_upper
                c_dict['out_nmng_chng_upper'] = out_nmng_chng_upper
                c_dict['out_mng_chng_lower'] = out_mng_chng_lower
                c_dict['out_nmng_chng_lower'] = out_nmng_chng_lower
                c_dict['calc_intervals'] = calc_intervals
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_{}_apply_chng_thres".format(tile_basename, kwargs['sar_year']))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        for year in ['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']:
            sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/{}'.format(year)
            if year == '1996':
                sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996_v2_reg'

            self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                                  prjs_lut_file='/scratch/a.pfb/gmw_v3_change/scripts/03_prepare_datasets/09_create_project_tile_lut/gmw_tiles_luts.json',
                                  potent_chng_msk_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_fnl_potent_chg_rgn_qad_rm_sml',
                                  sar_tiles_dir=sar_tiles_dir,
                                  sar_year=year,
                                  thres_files_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/fnl_prj_thresholds',
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_2010_{}_chngs'.format(year),
                                  tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_2010_XXXX_chngs", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
