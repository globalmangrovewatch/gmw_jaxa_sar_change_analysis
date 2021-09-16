from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import pathlib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            #basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile_name = tile_basename.split('_')[1]

            sar_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)
            if os.path.exists(sar_scn_dir):
                if kwargs['sar_year'] == '1996':
                    sar_img = os.path.join(sar_scn_dir, '{}_1996_db.kea'.format(tile_name))
                elif kwargs['sar_year'] == '2010':
                    sar_img = os.path.join(sar_scn_dir, '{}_2010_db_mskd.kea'.format(tile_name))
                else:
                    sar_img = os.path.join(sar_scn_dir, '{}_{}_db_mskd_reg.kea'.format(tile_name, kwargs['sar_year']))

                if os.path.exists(sar_img):
                    potent_chng_msk_img = os.path.join(kwargs['potent_chng_msk_dir'], '{}_{}_stat_chg_rgns_v3_base2010.kea'.format(tile_basename, kwargs['base_year']))

                    out_mng_data = os.path.join(kwargs['out_dir'], '{}_{}_mng_dB.h5'.format(tile_basename, kwargs['sar_year']))
                    out_nmng_data = os.path.join(kwargs['out_dir'], '{}_{}_not_mng_dB.h5'.format(tile_basename, kwargs['sar_year']))

                    if (not os.path.exists(out_mng_data)) or (not os.path.exists(out_nmng_data)):
                        c_dict = dict()
                        c_dict['tile'] = tile_basename
                        c_dict['gmw_tile'] = gmw_tile
                        c_dict['potent_chng_msk_img'] = potent_chng_msk_img
                        c_dict['sar_img'] = sar_img
                        c_dict['out_mng_data'] = out_mng_data
                        c_dict['out_nmng_data'] = out_nmng_data
                        self.params.append(c_dict)


    def run_gen_commands(self):
        all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        years_l1 = ['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']
        for l1_year in years_l1:
            base_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{}'.format(l1_year)
            chng_years = all_years.copy()
            chng_years.remove(l1_year)
            for chg_year in chng_years:
                sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/{}'.format(chg_year)
                if chg_year == '1996':
                    sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996_v2_reg'

                self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_{}_v3/*.kea'.format(l1_year),
                                      potent_chng_msk_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_pchg_stats_rgns_{}_v3'.format(l1_year),
                                      sar_tiles_dir=sar_tiles_dir,
                                      sar_year=chg_year,
                                      base_year=l1_year,
                                      out_dir=os.path.join(base_dir, 'gmw_{}_{}_pxl_vals'.format(l1_year, chg_year)))

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_XXXX_XXXX_pxl_vals", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
