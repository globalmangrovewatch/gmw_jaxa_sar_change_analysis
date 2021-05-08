from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis


def create_vrt_band_subset(input_img, bands, out_vrt):
    """
    A function which creates a GDAL VRT for the input image with the bands selected in the
    input list.

    :param input_img: the input GDAL image
    :param bands: a list of bands (in the order they will be in the VRT). Note, band numbering starts at 1.
    :param out_vrt: the output VRT file.

    """
    from osgeo import gdal
    import os
    input_img = os.path.abspath(input_img)
    vrt_options = gdal.BuildVRTOptions(bandList=bands)
    my_vrt = gdal.BuildVRT(out_vrt, [input_img], options=vrt_options)
    my_vrt = None


logger = logging.getLogger(__name__)

class CreateTimeseriesComps(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_timeseries_comps.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        input_imgs = []
        band_names = [self.params['start_year'], '2010', self.params['end_year']]

        rsgis_utils = rsgislib.RSGISPyUtils()
        rsgis_utils.set_envvars_lzw_gtiff_outs()

        if rsgis_utils.getImageBandCount(self.params['start_img']) > 1:
            basename = self.get_file_basename(self.params['start_img'])
            start_hh_img = os.path.join(self.params['tmp_dir'], "{}_hh_dB.vrt".format(basename))
            create_vrt_band_subset(self.params['start_img'], [1], start_hh_img)
            input_imgs.append(start_hh_img)
        else:
            input_imgs.append(self.params['start_img'])

        if rsgis_utils.getImageBandCount(self.params['tile_10_img']) > 1:
            basename = self.get_file_basename(self.params['tile_10_img'])
            tile_2010_hh_img = os.path.join(self.params['tmp_dir'], "{}_hh_dB.vrt".format(basename))
            create_vrt_band_subset(self.params['tile_10_img'], [1], tile_2010_hh_img)
            input_imgs.append(tile_2010_hh_img)
        else:
            input_imgs.append(self.params['tile_10_img'])

        if rsgis_utils.getImageBandCount(self.params['end_img']) > 1:
            basename = self.get_file_basename(self.params['end_img'])
            end_hh_img = os.path.join(self.params['tmp_dir'], "{}_hh_dB.vrt".format(basename))
            create_vrt_band_subset(self.params['end_img'], [1], end_hh_img)
            input_imgs.append(end_hh_img)
        else:
            input_imgs.append(self.params['end_img'])

        rsgislib.imageutils.stackImageBands(input_imgs, band_names, self.params['out_img'], None, 32767, 'GTIFF', rsgislib.TYPE_16INT)
        rsgislib.imageutils.popImageStats(self.params['out_img'], usenodataval=True, nodataval=32767, calcpyramids=True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["tile", "tile_10_img", "start_img", "start_year", "end_img", "end_year", "out_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['out_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['out_img']):
            os.remove(self.params['out_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])


if __name__ == "__main__":
    CreateTimeseriesComps().std_run()


