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

        h5_files = glob.glob(kwargs['input_files'])
        for h5_file in h5_files:
            basename = self.get_file_basename(h5_file)

            out_cmp_file = os.path.join(kwargs['out_dir'], "{}_cmp.txt".format(basename))

            if not os.path.exists(out_cmp_file):
                #print('rm {}'.format(h5_file))
                c_dict = dict()
                c_dict['h5_file'] = h5_file
                c_dict['out_cmp_file'] = out_cmp_file
                self.params.append(c_dict)


    def run_gen_commands(self):

        all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        years_l1 = ['1996']#, '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']
        for l1_year in years_l1:
            base_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{}'.format(l1_year)
            chng_years = all_years.copy()
            chng_years.remove(l1_year)
            for chg_year in chng_years:
                self.gen_command_info(input_files=os.path.join(base_dir, 'gmw_{}_{}_pxl_vals/*.h5'.format(l1_year, chg_year)),
                                      out_dir=os.path.join(base_dir, 'gmw_{}_{}_pxl_vals_chk'.format(l1_year, chg_year)))




        for year in ['1996', '2007', '2008', '2009', '2015', '2016', '2017', '2018', '2019', '2020']:
            sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/{}'.format(year)
            if year == '1996':
                sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996_v2_reg'

            self.gen_command_info(input_files='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_2010_{}_pxl_vals/*.h5'.format(year),
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_2010_{}_pxl_vals_chk'.format(year))

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_2010_XXXX_pxl_vals_chk", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
