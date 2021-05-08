from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        rsgis_utils = rsgislib.RSGISPyUtils()
        jaxa_tile_lst = rsgis_utils.readTextFile2List(kwargs['tile_list'])

        for tile in jaxa_tile_lst:
            tile_10_img = self.find_file(kwargs['tiles_srch_path_10'].format(tile), "*_db_mskd.kea")

            if tile_10_img is not None:
                start_img =  None
                years = ['1996', '2007', '2008', '2009']
                i = 0
                for srch_path in [kwargs['tiles_srch_path_96'], kwargs['tiles_srch_path_07'], kwargs['tiles_srch_path_08'], kwargs['tiles_srch_path_09']]:
                    tmp_img = self.find_file(srch_path.format(tile), "*_db_mskd.kea")
                    if tmp_img is not None:
                        start_img = tmp_img
                        start_year = years[i]
                        break
                    i = i + 1


                end_img = None
                years = ['2020', '2019', '2018', '2017', '2016', '2015']
                i = 0
                for srch_path in [kwargs['tiles_srch_path_20'], kwargs['tiles_srch_path_19'], kwargs['tiles_srch_path_18'], kwargs['tiles_srch_path_17'], kwargs['tiles_srch_path_16'], kwargs['tiles_srch_path_15']]:
                    tmp_img = self.find_file(srch_path.format(tile), "*_db_mskd.kea")
                    if tmp_img is not None:
                        end_img = tmp_img
                        end_year = years[i]
                        break
                    i = i + 1

                if (start_img is not None) and (end_img is not None):
                    out_img = os.path.join(kwargs['out_path'], '{}_change_comp.tif'.format(tile))

                    if (not os.path.exists(out_img)):
                        c_dict = dict()
                        c_dict['tile'] = tile
                        c_dict['tile_10_img'] = tile_10_img
                        c_dict['start_img'] = start_img
                        c_dict['start_year'] = start_year
                        c_dict['end_img'] = end_img
                        c_dict['end_year'] = end_year
                        c_dict['out_img'] = out_img
                        c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_timeseries_comp".format(tile))
                        if not os.path.exists(c_dict['tmp_dir']):
                            os.mkdir(c_dict['tmp_dir'])
                        self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(tile_list='/scratch/a.pfb/gmw_v3_change/scripts/01_download_jaxa_sar/gmw_jaxa_tile_names.txt',
                              tiles_srch_path_96='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996/{}/',
                              tiles_srch_path_07='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2007/{}/',
                              tiles_srch_path_08='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2008/{}/',
                              tiles_srch_path_09='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2009/{}/',
                              tiles_srch_path_10='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2010/{}/',
                              tiles_srch_path_15='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2015/{}/',
                              tiles_srch_path_16='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2016/{}/',
                              tiles_srch_path_17='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2017/{}/',
                              tiles_srch_path_18='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2018/{}/',
                              tiles_srch_path_19='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2019/{}/',
                              tiles_srch_path_20='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2020/{}/',
                              out_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/timeseries_comps',
                              tmp_dir='/scratch/a.pfb/gmw_v3_change/tmp')
        self.pop_params_db()
        self.create_slurm_sub_sh("timeseries_comps", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_timeseries_comps.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_timeseries_comps'
    process_tools_cls = 'CreateTimeseriesComps'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
