from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        gmw_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in gmw_tiles:
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)

            out_file = os.path.join(kwargs['out_dir'], '{}_stats.json'.format(tile_basename))

            mng_chng_img = os.path.join(kwargs['chng_dir'], '{}_{}_mng_chng_base{}.kea'.format(tile_basename, kwargs['sar_year'], kwargs['base_year']))
            nmng_chng_img = os.path.join(kwargs['chng_dir'], '{}_{}_not_mng_chng_base{}.kea'.format(tile_basename, kwargs['sar_year'], kwargs['base_year']))

            mng_chng_lower_img = os.path.join(kwargs['chng_dir'], '{}_{}_mng_chng_lower_base{}.kea'.format(tile_basename, kwargs['sar_year'], kwargs['base_year']))
            nmng_chng_lower_img = os.path.join(kwargs['chng_dir'], '{}_{}_not_mng_chng_lower_base{}.kea'.format(tile_basename, kwargs['sar_year'], kwargs['base_year']))

            mng_chng_upper_img = os.path.join(kwargs['chng_dir'], '{}_{}_mng_chng_upper_base{}.kea'.format(tile_basename, kwargs['sar_year'], kwargs['base_year']))
            nmng_chng_upper_img = os.path.join(kwargs['chng_dir'], '{}_{}_not_mng_chng_upper_base{}.kea'.format(tile_basename, kwargs['sar_year'], kwargs['base_year']))

            if not os.path.exists(out_file):
                #print("rm {}".format(mng_chng_img))
                #print("rm {}".format(nmng_chng_img))
                c_dict = dict()
                c_dict['img_base_extent'] = gmw_tile
                c_dict['img_mng_chng_tile'] = mng_chng_img
                c_dict['img_nmng_chng_tile'] = nmng_chng_img
                c_dict['img_mng_chng_lower_tile'] = mng_chng_lower_img
                c_dict['img_nmng_chng_lower_tile'] = nmng_chng_lower_img
                c_dict['img_mng_chng_upper_tile'] = mng_chng_upper_img
                c_dict['img_nmng_chng_upper_tile'] = nmng_chng_upper_img
                c_dict['chg_year'] = kwargs['sar_year']
                c_dict['base_year'] = kwargs['base_year']
                c_dict['out_file'] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        years_l1 = ['1996']  # , '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']
        for l1_year in years_l1:
            base_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{}'.format(l1_year)
            chng_years = all_years.copy()
            chng_years.remove(l1_year)
            for chg_year in chng_years:
                self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_{}_v3/*.kea'.format(l1_year),
                                      sar_year = chg_year,
                                      base_year=l1_year,
                                      chng_dir=os.path.join(base_dir, 'gmw_{}_{}_chngs'.format(l1_year, chg_year)),
                                      out_dir=os.path.join(base_dir, 'gmw_{}_{}_chngs_stats'.format(l1_year, chg_year)))


        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_calc_raw_chng_stats_all_years", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_tile_stats.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_tile_stats'
    process_tools_cls = 'CreateTileStats'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
