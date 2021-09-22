from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds
import logging
import os
import glob
import rsgislib
import osgeo.gdal as gdal

logger = logging.getLogger(__name__)

def getImageBandCount(input_img):
    """
    A function to retrieve the number of image bands in an image file.

    :return: nBands

    """
    rasterDS = gdal.Open(input_img, gdal.GA_ReadOnly)
    if rasterDS == None:
        raise rsgislib.RSGISPyException('Could not open raster image: \'' + input_img + '\'')

    nBands = rasterDS.RasterCount
    rasterDS = None
    return nBands

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_dir']):
            os.mkdir(kwargs['out_dir'])

        img_tiles = glob.glob(kwargs['gmw_tiles'])
        for gmw_tile in img_tiles:
            basename = self.get_file_basename(gmw_tile)
            tile_basename = self.get_file_basename(gmw_tile, n_comps=2)

            mng_ext_imgs = list()
            for chng_year in kwargs['chng_years']:
                if chng_year != '2010':
                    mng_ext_img = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from{0}/gmw_base{0}_{1}_mng_ext/{2}_{1}_mng_v3_base{0}.kea'.format(chng_year, kwargs['year'], tile_basename)
                else:
                    mng_ext_img = '/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/from2010/gmw_base2010_mng_{0}_v3/{1}_{0}_mng_v3_base2010.kea'.format(kwargs['year'], tile_basename)
                mng_ext_imgs.append(mng_ext_img)

            out_gmw_mng_sum_img = os.path.join(kwargs['out_dir'], '{}_{}_mng_sum_v3.tif'.format(tile_basename, kwargs['year']))

            if not os.path.exists(out_gmw_mng_sum_img):
                for img in mng_ext_imgs:
                    n_bands = getImageBandCount(img)
                    if n_bands != 1:
                        print("rm {}".format(img))
                c_dict = dict()
                c_dict['tile'] = tile_basename
                c_dict['gmw_tile'] = gmw_tile
                c_dict['year'] = kwargs['year']
                c_dict['mng_ext_imgs'] = mng_ext_imgs
                c_dict['out_gmw_mng_sum_img'] = out_gmw_mng_sum_img
                self.params.append(c_dict)


    def run_gen_commands(self):

        years = ['1996', '2007', '2008', '2009', '2010', '2015', '2016', '2017', '2018', '2019', '2020']
        for year in years:
            chng_years = years.copy()
            chng_years.remove(year)

            self.gen_command_info(gmw_tiles='/scratch/a.pfb/gmw_v3_change/data/gmw_baseline/gmw_2010_v3/*.kea',
                                  year=year,
                                  chng_years=chng_years,
                                  out_dir='/scratch/a.pfb/gmw_v3_change/data/gmw_chng_data/gmw_mng_ext_sum_{}'.format(year))

        self.pop_params_db()
        self.create_slurm_sub_sh("calc_annual_mng_ext", 16448, '/scratch/a.pfb/gmw_v3_change/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file=None, account_name='scw1376', n_cores_per_job=10, n_jobs=10,
                                 n_xtr_cmds=20, job_time_limit='2-23:59',
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
