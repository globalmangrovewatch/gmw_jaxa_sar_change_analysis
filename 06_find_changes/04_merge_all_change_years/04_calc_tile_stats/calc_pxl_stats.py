import glob
import argparse

import tqdm

import rsgislib
import rsgislib.imagecalc


def get_tile_pxl_counts(input_imgs_path, output_file):
    input_imgs = glob.glob(input_imgs_path)
    rsgis_utils = rsgislib.RSGISPyUtils()
    out_tile_stats = dict()
    for img in tqdm.tqdm(input_imgs):
        basename = rsgis_utils.get_file_basename(img)
        tile_name = basename.split('_')[1]
        pxl_count = rsgislib.imagecalc.countPxlsOfVal(img, vals=[1])
        out_tile_stats[tile_name] =  int(pxl_count)
    rsgis_utils.writeDict2JSON(out_tile_stats, output_file)

if __name__ == '__main__':
    """
    The command line user interface to RSGISLib DEM download tool.
    """
    parser = argparse.ArgumentParser(prog='calc_pxl_stats.py')
    parser.add_argument("-i", "--imgs", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=True)
    # Call the parser to parse the arguments.
    args = parser.parse_args()

    get_tile_pxl_counts(args.imgs, args.output)
