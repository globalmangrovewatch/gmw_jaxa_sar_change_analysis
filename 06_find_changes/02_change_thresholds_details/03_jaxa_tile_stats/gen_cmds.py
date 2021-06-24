from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import pathlib

logger = logging.getLogger(__name__)


def file_is_hidden(in_path):
    """
    A function to test whether a file or folder is 'hidden' or not on the
    file system. Should be cross platform between Linux/UNIX and windows.

    :param in_path: input file path to be tested
    :return: boolean (True = hidden)

    """
    in_path = os.path.abspath(in_path)
    if os.name == 'nt':
        import win32api, win32con
        attribute = win32api.GetFileAttributes(in_path)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        file_name = os.path.basename(in_path)
        return file_name.startswith('.')


def get_dir_list(input_path, inc_hidden=False):
    """
    Function which get the list of directories within the specified path.

    :param input_path: file path to search within
    :param inc_hidden: boolean specifying whether hidden files should be included (default=False)
    :return: list of directory paths

    """
    out_dir_lst = list()
    dir_listing = os.listdir(input_path)
    for item in dir_listing:
        c_path = os.path.join(input_path, item)
        if os.path.isdir(c_path):
            if not inc_hidden:
                if not file_is_hidden(c_path):
                    out_dir_lst.append(c_path)
            else:
                out_dir_lst.append(c_path)
    return out_dir_lst


class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        sar_tile_dirs = get_dir_list(kwargs['sar_tiles_dir'])

        for sar_dir in sar_tile_dirs:
            sar_tile = self.find_file(sar_dir, '*_dB.kea')
            sar_tile_msk = self.find_file(sar_dir, '*_bin_vmsk.kea')
            tile_basename = self.get_file_basename(sar_tile)

            out_stats_file = os.path.join(kwargs['out_dir'], '{}_{}_stats.json'.format(tile_basename, kwargs['sar_year']))

            if not os.path.exists(out_stats_file):
                c_dict = dict()
                c_dict['sar_tile'] = sar_tile
                c_dict['sar_tile_msk'] = sar_tile_msk
                c_dict['out_file'] = out_stats_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        for year in ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']:
            sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/{}'.format(year)
            if year == '1996':
                sar_tiles_dir = '/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/1996_v2_reg'

            self.gen_command_info(sar_tiles_dir=sar_tiles_dir,
                                  sar_year=year,
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/sar_tile_{}_stats'.format(year))

        self.pop_params_db()
        self.create_slurm_sub_sh("jaxa_tile_stats", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
