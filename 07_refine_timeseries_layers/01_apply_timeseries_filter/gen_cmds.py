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

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)

            out_img = os.path.join(kwargs['out_dir'], '{}_{}_v3.kea'.format(tile_basename, kwargs['year']))

            if not os.path.exists(out_img):
                if kwargs['year'] == '2015':
                    pre_gmw_img = self.find_file(kwargs['pre_tiles_dir'], "{}*v3.kea".format(tile_basename))
                    if pre_gmw_img is None:
                        print(kwargs['pre_tiles_dir'])
                        print("{}*v3.kea".format(tile_basename))
                        raise Exception("Something has gone wrong - couldn't find the pre image")
                else:
                    pre_gmw_img = self.find_file(kwargs['pre_tiles_dir'], "{}*v3_init.kea".format(tile_basename))
                    if pre_gmw_img is None:
                        print(kwargs['pre_tiles_dir'])
                        print("{}*v3_init.kea".format(tile_basename))
                        raise Exception("Something has gone wrong - couldn't find the pre image")

                if kwargs['year'] == '2009':
                    post_gmw_img = self.find_file(kwargs['post_tiles_dir'], "{}*v3.kea".format(tile_basename))
                    if post_gmw_img is None:
                        print(kwargs['post_tiles_dir'])
                        print("{}*v3.kea".format(tile_basename))
                        raise Exception("Something has gone wrong - couldn't find the post image")
                else:
                    post_gmw_img = self.find_file(kwargs['post_tiles_dir'], "{}*v3_init.kea".format(tile_basename))
                    if post_gmw_img is None:
                        print(kwargs['post_tiles_dir'])
                        print("{}*v3_init.kea".format(tile_basename))
                        raise Exception("Something has gone wrong - couldn't find the post image")


                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['gmw_pre_tile'] = pre_gmw_img
                c_dict['gmw_post_tile'] = post_gmw_img
                c_dict['out_img'] = out_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_{}_chng_timeseries".format(tile_basename, kwargs['year']))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2007_v3/*v3_init.kea',
                              year='2007',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_1996_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2008_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2007_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2008_v3/*v3_init.kea',
                              year='2008',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2007_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2009_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2008_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2009_v3/*v3_init.kea',
                              year='2009',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2008_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2010_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2009_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*v3.kea',
                              year='2010',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2009_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2015_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2015_v3/*v3_init.kea',
                              year='2015',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2016_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2015_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2016_v3/*v3_init.kea',
                              year='2016',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2015_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2017_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2016_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2017_v3/*v3_init.kea',
                              year='2017',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2016_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2018_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2017_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2018_v3/*v3_init.kea',
                              year='2018',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2017_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2019_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2018_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2019_v3/*v3_init.kea',
                              year='2019',
                              pre_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2018_v3',
                              post_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_init_2020_v3',
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2019_v3_fnl',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')

        
        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_chng_timeseries", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
