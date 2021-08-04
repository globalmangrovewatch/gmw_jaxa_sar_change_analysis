import pandas
import os
import glob
import rsgislib.tools.filetools
import rsgislib.tools.utils

gmw_img_tiles = glob.glob('/scratch/a.pfb/gmw_v2_gapfill/data/gmw_tiles/gmw_init_v3_further_qa_part2/*.kea')
gmw_tiles = list()
for gmw_tile in gmw_img_tiles:
    basename = rsgislib.tools.filetools.get_file_basename(gmw_tile, n_comps=2)
    gmw_tiles.append(basename.split('_')[1])

years = [2007, 2008, 2009, 2015, 2016, 2017, 2018, 2019, 2020]

tile_reg_x_offs = dict()
tile_reg_y_offs = dict()
for gmw_tile in gmw_tiles:
    for year in years:
        sar_tiles_dir='/scratch/a.pfb/gmw_v3_change/data/jaxa_tiles/{}'.format(year)
        tile_dir = os.path.join(sar_tiles_dir, gmw_tile)
        if os.path.exists(tile_dir):
            if gmw_tile not in tile_reg_x_offs:
                tile_reg_x_offs[gmw_tile] = dict()
                for tmp_year in years:
                    tile_reg_x_offs[gmw_tile]['{}_x_off'.format(tmp_year)] = None
            if gmw_tile not in tile_reg_y_offs:
                tile_reg_y_offs[gmw_tile] = dict()
                for tmp_year in years:
                    tile_reg_y_offs[gmw_tile]['{}_y_off'.format(tmp_year)] = None

            offs_info_file = os.path.join(tile_dir, '{}_{}_2010_offsets.json'.format(gmw_tile, year))
            if os.path.exists(offs_info_file):
                offs_info = rsgislib.tools.utils.readJSON2Dict(offs_info_file)
                tile_reg_x_offs[gmw_tile]['{}_x_off'.format(year)] = offs_info['x_pxl_off']
                tile_reg_y_offs[gmw_tile]['{}_y_off'.format(year)] = offs_info['y_pxl_off']


df_x_offs_data = pandas.DataFrame(tile_reg_x_offs)
df_y_offs_data = pandas.DataFrame(tile_reg_y_offs)
xls_writer = pandas.ExcelWriter('gmw_reg_offs.xlsx', engine='xlsxwriter')
df_x_offs_data.to_excel(xls_writer, sheet_name='x_offsets')
df_y_offs_data.to_excel(xls_writer, sheet_name='y_offsets')
xls_writer.save()
