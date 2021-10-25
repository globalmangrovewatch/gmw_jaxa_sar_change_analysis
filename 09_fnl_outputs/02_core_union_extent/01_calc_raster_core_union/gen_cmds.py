from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_union_dir']):
            os.mkdir(kwargs['out_union_dir'])

        if not os.path.exists(kwargs['out_core_dir']):
            os.mkdir(kwargs['out_core_dir'])

        gmw_tile_srch = os.path.join(kwargs['gmw_base_dir'].format('2020'), "*.kea")

        img_tiles = glob.glob(gmw_tile_srch)
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile, n_comps=2)

            out_union_img = os.path.join(kwargs['out_union_dir'], '{}_v3_union.tif'.format(basename))
            out_core_img = os.path.join(kwargs['out_core_dir'], '{}_v3_core.tif'.format(basename))

            if (not os.path.exists(out_union_img)) or (not os.path.exists(out_core_img)):
                gmw_imgs = list()
                for year in kwargs['years']:
                    img_dir = kwargs['gmw_base_dir'].format(year)
                    gmw_img = os.path.join(img_dir, "{}_{}_mjr_v3_fnl.kea".format(basename, year))
                    gmw_imgs.append(gmw_img)

                c_dict = dict()
                c_dict['gmw_tile'] = gmw_tile
                c_dict['gmw_imgs'] = gmw_imgs
                c_dict['out_union_img'] = out_union_img
                c_dict['out_core_img'] = out_core_img
                self.params.append(c_dict)


    def run_gen_commands(self):

        self.gen_command_info(gmw_base_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_v3_fnl_mjr_{}_v312/',
                              years=['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020'],
                              out_union_dir='/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_summaries/gmw_v3_union_v312',
                              out_core_dir='/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_summaries/gmw_v3_core_v312')
        
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
