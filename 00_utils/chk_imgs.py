import osgeo.gdal as gdal
import os
import argparse
import glob

import numpy

class RSGISGDALErrorHandler(object):
    """
    A class representing a generic GDAL Error Handler which
    can be used to pick up GDAL warnings rather than just
    failure errors.
    """

    def __init__(self):
        """
        Init for RSGISGDALErrorHandler. Class attributes are err_level, err_no and err_msg

        """
        from osgeo import gdal
        self.err_level = gdal.CE_None
        self.err_no = 0
        self.err_msg = ''

    def handler(self, err_level, err_no, err_msg):
        """
        The handler function which is called with the error information.

        :param err_level: The level of the error
        :param err_no: The error number
        :param err_msg: The message (string) associated with the error.

        """
        self.err_level = err_level
        self.err_no = err_no
        self.err_msg = err_msg


def check_gdal_image_file(gdal_img, check_bands=True):
    """
    A function which checks a GDAL compatible image file and returns an error message if appropriate.

    :param gdal_img: the file path to the gdal image file.
    :param check_bands: boolean specifying whether individual image bands should be
                        opened and checked (Default: True)
    :return: boolean (True: file OK; False: Error found), string (error message if required otherwise empty string)

    """
    file_ok = True
    err_str = ''
    if os.path.exists(gdal_img):
        err = RSGISGDALErrorHandler()
        err_handler = err.handler
        gdal.PushErrorHandler(err_handler)
        gdal.UseExceptions()
        try:
            if os.path.splitext(gdal_img)[1] == '.kea':
                import h5py
                fH5 = h5py.File(gdal_img, 'r')
                if fH5 is None:
                    file_ok = False
                    err_str = 'h5py could not open the dataset as returned a Null dataset.'
                    raise Exception(err_str)
            raster_ds = gdal.Open(gdal_img, gdal.GA_ReadOnly)
            if raster_ds is None:
                file_ok = False
                err_str = 'GDAL could not open the dataset, returned None.'
            elif check_bands:
                n_bands = raster_ds.RasterCount
                for n in range(n_bands):
                    band = n + 1
                    img_band = raster_ds.GetRasterBand(band)
                    if img_band is None:
                        file_ok = False
                        err_str = 'GDAL could not open band {} in the dataset, returned None.'.format(band)
            raster_ds = None
        except Exception as e:
            file_ok = False
            err_str = str(e)
        else:
            if err.err_level >= gdal.CE_Warning:
                file_ok = False
                err_str = str(err.err_msg)
        finally:
            gdal.PopErrorHandler()
    else:
        file_ok = False
        err_str = 'File does not exist.'
    return file_ok, err_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="A utility which can be used to check whether a GDAL "
                                                  "compatible file is valid and if there are any errors or warnings.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file path")
    parser.add_argument("--size", type=int, default=0, help="Check file sizes - remove lowest 1 percent")

    args = parser.parse_args()
    print(args.input)

    imgs = glob.glob(args.input)
    if args.size > 0:
        file_sizes = []
        for img in imgs:
            file_sizes.append(os.path.getsize(img))

        file_sizes = numpy.array(file_sizes)
        low_thres = numpy.percentile(file_sizes, [args.size])
        print(low_thres)

        print("Lowest {} percent file size:".format(args.size))
        imgs_ok = list()
        for img in imgs:
            if os.path.getsize(img) < low_thres:
                print("rm {}".format(img))
            else:
                imgs_ok.append(img)
        imgs = imgs_ok


    print("File Checks:")
    for img in imgs:
        print(img)
        try:
            file_ok, err_str = check_gdal_image_file(img, check_bands=True)
            if not file_ok:
                print("rm {}".format(img))
        except:
            print("rm {}".format(img))

    print("Finish")
