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

        img_tiles = glob.glob(kwargs['base_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile_name = tile_basename.split('_')[1]

            sar_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)
            if kwargs['sar_year'] == '1996':
                sar_img = os.path.join(sar_scn_dir, '{}_1996_db.kea'.format(tile_name))
            elif kwargs['sar_year'] == '2010':
                sar_img = os.path.join(sar_scn_dir, '{}_2010_db_mskd.kea'.format(tile_name))
            else:
                sar_img = os.path.join(sar_scn_dir, '{}_{}_db_mskd_reg.kea'.format(tile_name, kwargs['sar_year']))

            out_img = os.path.join(kwargs['out_dir'], '{}_east_india_chng_rgns.kea'.format(tile_basename))

            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict['tile'] = tile_name
                c_dict['gmw_tile'] = gmw_tile
                c_dict['sar_img'] = sar_img
                c_dict['pchng_img'] = kwargs['pchng_img']
                c_dict['year'] = kwargs['year']
                c_dict['out_img'] = out_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_{}_apply_chng_thres".format(tile_basename, kwargs['year']))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        all_years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        for year in all_years:

            sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/{}'.format(year)
            if year == '1996':
                sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996_v2_reg'

            self.gen_command_info(base_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_base/*.kea',
                                  pochange_rgns_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgn_rgns',
                                  year=year,
                                  sar_tiles_dir=sar_tiles_dir,
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_east_india_edits/gmw_v3_east_india_chgns/{}'.format(year),
                                  tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        
        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_east_india_base", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=1,
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
