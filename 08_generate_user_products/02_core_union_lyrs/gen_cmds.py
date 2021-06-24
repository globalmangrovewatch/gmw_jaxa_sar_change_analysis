from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_core_dir']):
            os.mkdir(kwargs['out_core_dir'])
        if not os.path.exists(kwargs['out_union_dir']):
            os.mkdir(kwargs['out_union_dir'])

        years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']

        img_tiles = glob.glob(kwargs['img_srch'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile, n_comps=2)

            out_core_img = os.path.join(kwargs['out_core_dir'], '{}_core_extent.tif'.format(basename))
            out_union_img = os.path.join(kwargs['out_union_dir'], '{}_union_extent.tif'.format(basename))

            if (not os.path.exists(out_core_img)) or (not os.path.exists(out_union_img)):
                gmw_tiles = list()
                for year in years:
                    gmw_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_{}_v3_fnl_tif'.format(year)
                    gmw_tile_img = os.path.join(gmw_tiles_dir, '{}_{}_v3.tif'.format(basename, kwargs['sar_year']))
                    if os.path.exists(gmw_tile_img):
                        gmw_tiles.append(gmw_tile_img)

                if len(gmw_tiles) > 0:
                    c_dict = dict()
                    c_dict['tile'] = basename
                    c_dict['gmw_tiles'] = gmw_tiles
                    c_dict['out_core_img'] = out_core_img
                    c_dict['out_union_img'] = out_union_img
                    self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                              out_core_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_core_v3_fnl_tif',
                              out_union_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_union_v3_fnl_tif')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_core_union_ext_tif", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
