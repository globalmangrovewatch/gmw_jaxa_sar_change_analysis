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

            mng_chng_imgs = list()
            nmng_chng_imgs = list()

            for year in kwargs['years']:
                mng_chng_img = os.path.join(kwargs['chng_img_dir'].format(year), '{}_{}_mng_chng.kea'.format(tile_basename, year))
                nmng_chng_img = os.path.join(kwargs['chng_img_dir'].format(year), '{}_{}_not_mng_chng.kea'.format(tile_basename, year))

                mng_chng_imgs.append(mng_chng_img)
                nmng_chng_imgs.append(nmng_chng_img)


            out_mng_chng_sum_img = os.path.join(kwargs['out_dir'], '{}_sum_mng_chng.kea'.format(tile_basename))
            out_nmng_chng_sum_img = os.path.join(kwargs['out_dir'], '{}_sum_not_mng_chng.kea'.format(tile_basename))

            if not os.path.exists(out_mng_chng_sum_img):
                for img in mng_chng_imgs:
                    if os.path.exists(img):
                        print(img)
                        n_bands = rsgis_utils.getImageBandCount(img)
                        if n_bands != 1:
                            print("rm {}".format(img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['chng_imgs'] = mng_chng_imgs
                c_dict['out_img'] = out_mng_chng_sum_img
                self.params.append(c_dict)

            if not os.path.exists(out_nmng_chng_sum_img):
                for img in nmng_chng_imgs:
                    if os.path.exists(img):
                        print(img)
                        n_bands = rsgis_utils.getImageBandCount(img)
                        if n_bands != 1:
                            print("rm {}".format(img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['chng_imgs'] = nmng_chng_imgs
                c_dict['out_img'] = out_nmng_chng_sum_img
                self.params.append(c_dict)


    def run_gen_commands(self):
        """
        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                              chng_img_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_{}_chngs_rmsml',
                              years=['1996', '2007', '2008', '2009'],
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_pre_2010_chngs')
        """ 
        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                              chng_img_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_2010_{}_chngs_rmsml',
                              years=['2015', '2016', '2017', '2018', '2019', '2020'],
                              out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_post_2010_chngs')
        

        
        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_sum_chng", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
