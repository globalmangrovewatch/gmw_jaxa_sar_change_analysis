import rsgislib.imageutils
import glob

input_imgs = glob.glob("/Users/pete/Temp/gmw_v314_dev/gmw_v3_fnl_mjr_2010_v314/*.tif")

rsgislib.imageutils.create_mosaic_images_vrt(input_imgs, "/Users/pete/Development/globalmangrovewatch/gmw_jaxa_sar_change_analysis/10_acc_assess/20_calc_2010_acc_stats/01_create_v3_mosaics/gmw_2010_extent_v314.vrt")
