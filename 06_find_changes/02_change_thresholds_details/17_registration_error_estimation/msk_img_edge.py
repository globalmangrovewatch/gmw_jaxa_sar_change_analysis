import rsgislib
import rsgislib.imageutils
import rsgislib.rastergis


input_img = 'GMW_N06E005_2010_v3.tif'
out_msk_img = 'GMW_N06E005_2010_v3_edges.kea'
output_img = 'GMW_N06E005_2010_v3_mskd_edges.kea'
out_tif_img = 'GMW_N06E005_2010_v3_mskd_edges_tif.tif'

rsgislib.imageutils.genImageEdgeMask(input_img, out_msk_img, gdalformat='KEA', n_edge_pxls=100)


rsgislib.imageutils.maskImage(input_img, out_msk_img, output_img, 'KEA', rsgislib.TYPE_8UINT, 0, 1)


rsgislib.imageutils.gdal_translate(output_img, out_tif_img, gdal_format='GTIFF')