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

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)

            out_img = os.path.join(kwargs['out_dir'], '{}_{}_mjr_v3_fnl.kea'.format(tile_basename, kwargs['year']))

            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['qa_add_file'] = kwargs['qa_add_file']
                c_dict['qa_add_lyr'] = kwargs['qa_add_lyr']
                c_dict['qa_rm_file'] = kwargs['qa_rm_file']
                c_dict['qa_rm_lyr'] = kwargs['qa_rm_lyr']
                c_dict['out_img'] = out_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_{}_mjr_v3_fnl".format(tile_basename, kwargs['year']))
                if not os.path.exists(kwargs['tmp_dir']):
                    os.mkdir(kwargs['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        for year in years:
            gmw_tiles = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_{}_v310/*.kea'.format(year)

            self.gen_command_info(gmw_tiles=gmw_tiles,
                                  year=year,
                                  qa_add_file='add_mangroves.gpkg',
                                  qa_add_lyr='add_mangroves',
                                  qa_rm_file='rm_mangroves.gpkg',
                                  qa_rm_lyr='rm_mangroves',
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_{}_v311'.format(year),
                                  tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        
        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_apply_qa_fnl_v311", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
