from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import pathlib
import rsgislib.imageutils.imagelut

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        img_tiles = glob.glob(kwargs['gmw_tiles'])

        if not os.path.exists(kwargs['sar_tiles_lut_file']):
            sar_imgs = list()
            for gmw_tile in img_tiles:
                basename = self.get_file_basename(gmw_tile)
                tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
                tile_name = tile_basename.split('_')[1]

                sar_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)

                sar_img = os.path.join(sar_scn_dir, '{}_{}_db_mskd.kea'.format(tile_name, kwargs['sar_year']))
                if os.path.exists(sar_img):
                    sar_imgs.append(sar_img)

            rsgislib.imageutils.imagelut.createImgExtentLUT(sar_imgs, kwargs['sar_tiles_lut_file'], kwargs['sar_tiles_lut_lyr'], 'GPKG')



        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)
            tile_name = tile_basename.split('_')[1]

            sar_scn_dir = os.path.join(kwargs['sar_tiles_dir'], tile_name)

            sar_img = os.path.join(sar_scn_dir, '{}_{}_db_mskd.kea'.format(tile_name, kwargs['sar_year']))
            if os.path.exists(sar_img):
                out_img = os.path.join(sar_scn_dir, '{}_{}_db_mskd_bufd.kea'.format(tile_name, kwargs['sar_year']))

                if (not os.path.exists(out_img)):
                    c_dict = dict()
                    c_dict['tile'] = tile_name
                    c_dict['sar_tiles_lut_file'] = kwargs['sar_tiles_lut_file']
                    c_dict['sar_tiles_lut_lyr'] = kwargs['sar_tiles_lut_lyr']
                    c_dict['sar_img'] = sar_img
                    c_dict['out_img'] = out_img
                    self.params.append(c_dict)


    def run_gen_commands(self):
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2007',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar_2007_lut.gpkg',
            sar_tiles_lut_lyr='palsar_2007_lut',
            sar_year='2007')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2008',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar_2008_lut.gpkg',
            sar_tiles_lut_lyr='palsar_2008_lut',
            sar_year='2008')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2009',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar_2009_lut.gpkg',
            sar_tiles_lut_lyr='palsar_2009_lut',
            sar_year='2009')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2015',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar2_2015_lut.gpkg',
            sar_tiles_lut_lyr='palsar2_2015_lut',
            sar_year='2015')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2016',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar2_2016_lut.gpkg',
            sar_tiles_lut_lyr='palsar2_2016_lut',
            sar_year='2016')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2017',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar2_2017_lut.gpkg',
            sar_tiles_lut_lyr='palsar2_2017_lut',
            sar_year='2017')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2018',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar2_2018_lut.gpkg',
            sar_tiles_lut_lyr='palsar2_2018_lut',
            sar_year='2018')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2019',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar2_2019_lut.gpkg',
            sar_tiles_lut_lyr='palsar2_2019_lut',
            sar_year='2019')
        self.gen_command_info(
            gmw_tiles='/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea',
            sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/2020',
            sar_tiles_lut_file='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/palsar2_2020_lut.gpkg',
            sar_tiles_lut_lyr='palsar2_2020_lut',
            sar_year='2020')

        self.pop_params_db()
        self.create_slurm_sub_sh("gmw_sar_buf_base_imgs", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
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
