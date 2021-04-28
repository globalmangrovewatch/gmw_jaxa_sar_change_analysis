from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import shutil
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils
import rsgislib.rastergis
import datetime
import osgeo.gdal as gdal
from rios import rat
import numpy
import subprocess

logger = logging.getLogger(__name__)


def extractGZTarFile(in_file, out_dir):
    """

    :param in_file:
    :param out_dir:
    :return:
    """
    cwd = os.getcwd()
    os.chdir(out_dir)
    logger.debug("Executing tar (gz) data extraction.")
    cmd = 'tar -xzf ' + in_file
    logger.debug("Command is: '{}'.".format(cmd))
    try:
        subprocess.call(cmd, shell=True)
    except Exception as e:
        logger.error("Failed to run command: {}".format(cmd))
        raise e
    logger.debug("Executed tar (gz) data extraction.")
    os.chdir(cwd)


class Create2016PALSAR2ARD(PBPTQProcessTool):

    def __init__(self):
        super().__init__(cmd_name='create_jaxa_2016_ard.py', descript=None)

    def do_processing(self, **kwargs):
        if not os.path.exists(self.params['tmp_dir']):
            os.mkdir(self.params['tmp_dir'])

        rsgis_utils = rsgislib.RSGISPyUtils()

        hh_p2_file_pattern = '*_sl_HH_F02DAR'
        hv_p2_file_pattern = '*_sl_HV_F02DAR'

        mask_file_pattern = '*_mask_F02DAR'
        date_file_pattern = '*_date_F02DAR'
        linci_file_pattern = '*_linci_F02DAR'

        hh_p2_fp_file_pattern = '*_sl_HH_FP6QAR'
        hv_p2_fp_file_pattern = '*_sl_HV_FP6QAR'

        mask_fp_file_pattern = '*_mask_FP6QAR'
        date_fp_file_pattern = '*_date_FP6QAR'
        linci_fp_file_pattern = '*_linci_FP6QAR'

        extract_data_dir = os.path.join(self.params['tmp_dir'], '{}_data'.format(self.params['tile']))
        if not os.path.exists(extract_data_dir):
            os.mkdir(extract_data_dir)

        # Extract the data archive
        extractGZTarFile(self.params['arch_file'], extract_data_dir)

        # ALOS-2 PALSAR-2
        # File files
        ref_launch_date = datetime.datetime(2014, 5, 24)
        try:
            hh_file = rsgis_utils.findFile(extract_data_dir, hh_p2_file_pattern)
        except Exception as e:
            try:
                hh_file = rsgis_utils.findFile(extract_data_dir, hh_p2_fp_file_pattern)
            except Exception as e:
                print("Could not find HH file in '{}'".format(extract_data_dir))
                raise e

        try:
            hv_file = rsgis_utils.findFile(extract_data_dir, hv_p2_file_pattern)
        except Exception as e:
            try:
                hv_file = rsgis_utils.findFile(extract_data_dir, hv_p2_fp_file_pattern)
            except Exception as e:
                print("Could not find HV file in '{}'".format(extract_data_dir))
                raise e

        hh_dB_file = os.path.join(self.params['tmp_dir'], '{}_2016_hh_dB.kea'.format(self.params['tile']))
        rsgislib.imagecalc.imageMath(hh_file, hh_dB_file, '(10 * log10(b1^2) - 83.0)*100', 'KEA', rsgislib.TYPE_16INT)

        hv_dB_file = os.path.join(self.params['tmp_dir'], '{}_2016_hv_dB.kea'.format(self.params['tile']))
        rsgislib.imagecalc.imageMath(hv_file, hv_dB_file, '(10 * log10(b1^2) - 83.0)*100', 'KEA', rsgislib.TYPE_16INT)

        # Add HH/HV ratio.
        hhhv_file = os.path.join(self.params['tmp_dir'], '{}_hhhv.kea'.format(self.params['tile']))
        band_defns = [rsgislib.imagecalc.BandDefn('hh', hh_file, 1), rsgislib.imagecalc.BandDefn('hv', hv_file, 1)]
        rsgislib.imagecalc.bandMath(hhhv_file, 'hv==0?0:(hh/hv)*1000', 'KEA', rsgislib.TYPE_16INT, band_defns)

        # Stack Image bands
        # sar_stack_file = os.path.join(self.params['tmp_dir'], '{}_palsar_2016_dB.kea'.format(self.params['tile']))
        rsgislib.imageutils.stackImageBands([hh_dB_file, hv_dB_file, hhhv_file], ["HH", "HV", "HH/HV"],
                                            self.params['sar_img'], None, 0, 'KEA', rsgislib.TYPE_16INT)
        rsgislib.imageutils.popImageStats(self.params['sar_img'], usenodataval=True, nodataval=0, calcpyramids=True)

        try:
            msk_file = rsgis_utils.findFile(extract_data_dir, mask_file_pattern)
        except Exception as e:
            try:
                msk_file = rsgis_utils.findFile(extract_data_dir, mask_fp_file_pattern)
            except Exception as e:
                print("Could not find Mask file in '{}'".format(extract_data_dir))
                raise e

        try:
            date_file = rsgis_utils.findFile(extract_data_dir, date_file_pattern)
        except Exception as e:
            try:
                date_file = rsgis_utils.findFile(extract_data_dir, date_fp_file_pattern)
            except Exception as e:
                print("Could not find Date file in '{}'".format(extract_data_dir))
                raise e

        try:
            linci_file = rsgis_utils.findFile(extract_data_dir, linci_file_pattern)
        except Exception as e:
            try:
                linci_file = rsgis_utils.findFile(extract_data_dir, linci_fp_file_pattern)
            except Exception as e:
                print("Could not find Incidence Angle file in '{}'".format(extract_data_dir))
                raise e

        # Create output mask file.
        rsgislib.imagecalc.imageMath(msk_file, self.params['vmsk_img'], "b1", "KEA",
                                     rsgis_utils.getGDALDataTypeFromImg(msk_file))
        rsgislib.rastergis.populateStats(self.params['vmsk_img'], True, True, True)

        ####### Add Mask descriptions ##########
        rat_img_dataset = gdal.Open(self.params['vmsk_img'], gdal.GA_Update)
        Histogram = rat.readColumn(rat_img_dataset, "Histogram")
        Mask_Type_Names = numpy.empty_like(Histogram, dtype=numpy.dtype('a255'))
        Mask_Type_Names[...] = ""
        Mask_Type_Names[0] = "No data"
        if Mask_Type_Names.shape[0] >= 50:
            Mask_Type_Names[50] = "Ocean and water"
        if Mask_Type_Names.shape[0] >= 100:
            Mask_Type_Names[100] = "Lay over"
        if Mask_Type_Names.shape[0] >= 150:
            Mask_Type_Names[150] = "Shadowing"
        if Mask_Type_Names.shape[0] >= 255:
            Mask_Type_Names[255] = "Land"
        rat.writeColumn(rat_img_dataset, "Type", Mask_Type_Names)
        rat_img_dataset = None
        ########################################

        rsgislib.imagecalc.imageMath(date_file, self.params['date_img'], "b1", "KEA",
                                     rsgis_utils.getGDALDataTypeFromImg(date_file))
        rsgislib.rastergis.populateStats(self.params['date_img'], True, True, True)

        ##################### Define Dates #######################
        rat_img_dataset = gdal.Open(self.params['date_img'], gdal.GA_Update)
        Histogram = rat.readColumn(rat_img_dataset, "Histogram")
        Aqu_Date_Day = numpy.zeros_like(Histogram, dtype=int)
        Aqu_Date_Month = numpy.zeros_like(Histogram, dtype=int)
        Aqu_Date_Year = numpy.zeros_like(Histogram, dtype=int)

        ID = numpy.arange(Histogram.shape[0])
        ID = ID[Histogram > 0]

        for tmp_day_count in ID:
            try:
                tmp_date = ref_launch_date + datetime.timedelta(days=float(tmp_day_count))
            except Exception as e:
                logger.error("Could not create datetime object '{}'".format(e))
                raise e
            Aqu_Date_Day[tmp_day_count] = tmp_date.day
            Aqu_Date_Month[tmp_day_count] = tmp_date.month
            Aqu_Date_Year[tmp_day_count] = tmp_date.year

        rat.writeColumn(rat_img_dataset, "Day", Aqu_Date_Day)
        rat.writeColumn(rat_img_dataset, "Month", Aqu_Date_Month)
        rat.writeColumn(rat_img_dataset, "Year", Aqu_Date_Year)
        rat_img_dataset = None
        #############################################################

        rsgislib.imagecalc.imageMath(linci_file, self.params['linci_img'], "b1", "KEA",
                                     rsgis_utils.getGDALDataTypeFromImg(linci_file))
        rsgislib.rastergis.populateStats(self.params['linci_img'], True, True, True)

        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])

    def required_fields(self, **kwargs):
        return ["tile", "arch_file", "sar_img", "date_img", "vmsk_img", "linci_img", "tmp_dir"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params['sar_img']] = 'gdal_image'
        files_dict[self.params['date_img']] = 'gdal_image'
        files_dict[self.params['vmsk_img']] = 'gdal_image'
        files_dict[self.params['linci_img']] = 'gdal_image'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files.
        if os.path.exists(self.params['sar_img']):
            os.remove(self.params['sar_img'])

        if os.path.exists(self.params['date_img']):
            os.remove(self.params['date_img'])

        if os.path.exists(self.params['vmsk_img']):
            os.remove(self.params['vmsk_img'])

        if os.path.exists(self.params['linci_img']):
            os.remove(self.params['linci_img'])

        # Reset the tmp dir
        if os.path.exists(self.params['tmp_dir']):
            shutil.rmtree(self.params['tmp_dir'])
        os.mkdir(self.params['tmp_dir'])


if __name__ == "__main__":
    Create2016PALSAR2ARD().std_run()


