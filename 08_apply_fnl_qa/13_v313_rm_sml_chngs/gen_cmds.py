from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib.tools.filetools

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):

        img_tiles = glob.glob(os.path.join(kwargs['gmw_tiles'].format(1996), "*.kea"))

        for gmw_tile in img_tiles:
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)

            gmw_tiles = dict()
            out_imgs = dict()
            out_files_exist = True
            for year in kwargs['years']:
                out_dir = kwargs['out_dir'].format(year)
                if not os.path.exists(out_dir):
                    os.mkdir(out_dir)

                tiles_dir = kwargs['gmw_tiles'].format(year)
                gmw_tiles[year] = rsgislib.tools.filetools.find_file_none(tiles_dir, "{}*.kea".format(tile_basename))
                out_imgs[year] = os.path.join(out_dir, "{}_{}_mjr_v314.kea".format(tile_basename, year))

                if not os.path.exists(out_imgs[year]):
                    out_files_exist = False

            if not out_files_exist:
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tiles'] = gmw_tiles
                c_dict['out_imgs'] = out_imgs
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_mjr_v314".format(tile_basename))
                if not os.path.exists(kwargs['tmp_dir']):
                    os.mkdir(kwargs['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(gmw_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_{}_v313',
                              years=['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020'],
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_{}_v314',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        
        self.pop_params_db()
        self.create_slurm_sub_sh("gen_gmw_v314", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
