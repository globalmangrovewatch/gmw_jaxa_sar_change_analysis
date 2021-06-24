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
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile_name = tile_basename.split('_')[1]

            sar_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)
            if os.path.exists(sar_scn_dir):
                sar_img = os.path.join(sar_scn_dir, '{}_{}_db.kea'.format(tile_name, kwargs['sar_year']))
                if os.path.exists(sar_img):
                    out_mng_data = os.path.join(kwargs['out_dir'], '{}_{}_mng_dB.h5'.format(tile_basename, kwargs['sar_year']))

                    if not os.path.exists(out_mng_data):
                        c_dict = dict()
                        c_dict['tile'] = tile_basename
                        c_dict['gmw_tile'] = gmw_tile
                        c_dict['sar_img'] = sar_img
                        c_dict['out_mng_data'] = out_mng_data
                        self.params.append(c_dict)


    def run_gen_commands(self):
        for year in ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
            sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/{}'.format(year)
            if year == '1996':
                sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996_v2_reg'

            self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_v3_exts/gmw_core_v3_fnl_tif/*.tif',
                                  sar_tiles_dir=sar_tiles_dir,
                                  sar_year=year,
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_core_{}_pxl_vals'.format(year))

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_2010_XXXX_pxl_vals", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
