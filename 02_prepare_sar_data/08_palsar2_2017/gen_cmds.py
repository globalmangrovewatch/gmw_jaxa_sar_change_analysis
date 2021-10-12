from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import pathlib

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        in_archives = glob.glob(kwargs['in_tiles_path'])
        for arch_file in in_archives:
            arch_basename = self.get_file_basename(arch_file)
            tile_name = arch_basename.split('_')[0]

            out_dir = os.path.join(kwargs['out_tiles_dir'], tile_name)
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)

            sar_img = os.path.join(out_dir, '{}_2017_db.kea'.format(tile_name))
            date_img = os.path.join(out_dir, '{}_2017_dates.kea'.format(tile_name))
            vmsk_img = os.path.join(out_dir, '{}_2017_vmsk.kea'.format(tile_name))
            linci_img = os.path.join(out_dir, '{}_2017_linci.kea'.format(tile_name))

            if (not os.path.exists(sar_img)) or (not os.path.exists(date_img)) or (not os.path.exists(vmsk_img)) or (not os.path.exists(linci_img)):
                c_dict = dict()
                c_dict['tile'] = tile_name
                c_dict['arch_file'] = arch_file
                c_dict['sar_img'] = sar_img
                c_dict['date_img'] = date_img
                c_dict['vmsk_img'] = vmsk_img
                c_dict['linci_img'] = linci_img
                c_dict['tmp_dir'] = os.path.join(kwargs['tmp_dir'], "{}_2017_ard".format(tile_name))
                if not os.path.exists(c_dict['tmp_dir']):
                    os.mkdir(c_dict['tmp_dir'])
                self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(in_tiles_path='/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2017/*.tar.gz',
                              out_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2017',
                              tmp_dir='/scratch/a.pfb/gmw_v2_gapfill/tmp')
        self.pop_params_db()
        self.create_slurm_sub_sh("gen_2017_jaxa_ard", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("create_jaxa_2017_ard.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'create_jaxa_2017_ard'
    process_tools_cls = 'Create2017PALSAR2ARD'

    create_tools = GenCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_gapfill_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
