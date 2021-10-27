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

        img_tiles = glob.glob(kwargs['gmw_tile_srch'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile, n_comps=2)

            gmw_chg_img = os.path.join(kwargs['gmw_chng_dir'], "{}_{}_mjr_v3_fnl.kea".format(basename, kwargs['year']))
            out_img = os.path.join(kwargs['out_dir'], '{}_v3_chng_f1996_t{}.tif'.format(basename, kwargs['year']))

            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict['gmw_base_tile'] = gmw_tile
                c_dict['gmw_chg_img'] = gmw_chg_img
                c_dict['out_img'] = out_img
                self.params.append(c_dict)


    def run_gen_commands(self):
        years = ['2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        for year in years:
            self.gen_command_info(gmw_tile_srch='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_1996_v312/*.kea',
                                  gmw_chng_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_{}_v312'.format(year),
                                  year=year,
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_chngs/gmw_v3_f1996_t{}_v312'.format(year))
        
        self.pop_params_db()
        self.create_slurm_sub_sh("convert_gmw_extent_mng_gtiff", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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