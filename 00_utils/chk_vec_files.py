import osgeo.gdal as gdal
import os
import argparse
import glob


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


def check_gdal_vector_file(gdal_vec, chkproj=True, epsg_prj=0):
    """
    A function which checks a GDAL compatible vector file and returns an error message if appropriate.

    :param gdal_vec: the file path to the gdal vector file.
    :return: boolean (True: file OK; False: Error found), string (error message if required otherwise empty string)

    """
    file_ok = True
    err_str = ''
    if os.path.exists(gdal_vec):
        err = RSGISGDALErrorHandler()
        err_handler = err.handler
        gdal.PushErrorHandler(err_handler)
        gdal.UseExceptions()

        try:
            vec_ds = gdal.OpenEx(gdal_vec, gdal.OF_VECTOR)
            if vec_ds is None:
                file_ok = False
                err_str = 'GDAL could not open the data source, returned None.'
            else:
                for lyr_idx in range(vec_ds.GetLayerCount()):
                    vec_lyr = vec_ds.GetLayerByIndex(lyr_idx)
                    if vec_lyr is None:
                        file_ok = False
                        err_str = 'GDAL could not open all the vector layers.'
                        break
                if file_ok and chkproj:
                    vec_lyr = vec_ds.GetLayer()
                    if vec_lyr is None:
                        raise Exception("Something has gone wrong checking projection - layer not present")
                    vec_lyr_spt_ref = vec_lyr.GetSpatialRef()
                    if vec_lyr_spt_ref is None:
                        file_ok = False
                        err_str = 'Vector projection is None.'
                    if file_ok:
                        spt_ref_wkt = vec_lyr_spt_ref.ExportToWkt()
                        if spt_ref_wkt is None:
                            file_ok = False
                            err_str = 'Vector projection WKT is None.'
                        elif spt_ref_wkt is '':
                            file_ok = False
                            err_str = 'Vector projection is empty.'

                        if file_ok and (epsg_prj > 0):
                            vec_lyr_spt_ref.AutoIdentifyEPSG()
                            vec_epsg_code = vec_lyr_spt_ref.GetAuthorityCode(None)
                            if vec_epsg_code is None:
                                file_ok = False
                                err_str = 'Vector projection returned a None EPSG code.'
                            elif int(vec_epsg_code) != int(epsg_prj):
                                file_ok = False
                                err_str = 'Vector EPSG ({}) does not match that specified ({})'.format(vec_epsg_code, epsg_prj)

            vec_ds = None
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

def deleteFilesWithBasename(filePath):
    """
    Function to delete all the files which have a path
    and base name defined in the filePath attribute.

    """
    import glob
    baseName = os.path.splitext(filePath)[0]
    fileList = glob.glob(baseName+str('.*'))
    for file in fileList:
        print("Removed: {}".format(file))
        os.remove(file)

def _run_vecfile_chk(img_params):
    vec_file = img_params[0]
    rmerr = img_params[1]
    printnames = img_params[2]
    printerrs = img_params[3]
    multi_file = img_params[4]
    chkproj = img_params[5]
    epsg_prj = img_params[6]

    if printnames:
        print(vec_file)
    try:
        file_ok, err_str = check_gdal_vector_file(vec_file, chkproj, epsg_prj)
        if not file_ok:
            if printerrs:
                print("Error: {}".format(err_str))
            if rmerr:
                if multi_file:
                    deleteFilesWithBasename(vec_file)
                else:
                    os.remove(vec_file)
                    print("Removed {}".format(vec_file))
            else:
                print("rm {}".format(vec_file))
    except Exception as e:
        if printerrs:
            print("Error: '{}'".format(e))
        if rmerr:
            if multi_file:
                deleteFilesWithBasename(vec_file)
            else:
                os.remove(vec_file)
                print("Removed {}".format(vec_file))
        else:
            print("rm {}".format(vec_file))




if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="A utility which can be used to check whether a GDAL "
                                                  "compatible file is valid and if there are any errors or warnings.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file path")
    parser.add_argument("--rmerr", action='store_true', default=False, help="Delete error files from system.")
    parser.add_argument("--printnames", action='store_true', default=False, help="Print file names as checking")
    parser.add_argument("--printerrs", action='store_true', default=False, help="Print the error messages for the vectors")
    parser.add_argument("--chkproj", action='store_true', default=False, help="Check that a projection is defined")
    parser.add_argument("--epsg", type=int, default=0, help="The EPSG code for the projection of the images.")
    parser.add_argument("--multi", action='store_true', default=False, help="For formats which have multiple files "
                                                                            "where all files with the same basename"
                                                                            "will be deleted.")

    args = parser.parse_args()
    print(args.input)

    vec_files = glob.glob(args.input)

    print("File Checks ({} Files Found):".format(len(vec_files)))

    from multiprocessing import Pool
    processes_pool = Pool(1)
    try:
        for vec_file in vec_files:
            try:
                params = [vec_file, args.rmerr, args.printnames, args.printerrs, args.multi, args.chkproj, args.epsg]
                result = processes_pool.apply_async(_run_vecfile_chk, args=[params])
                result.get(timeout=1)
            except Exception as e:
                if args.rmerr:
                    if args.multi:
                        deleteFilesWithBasename(vec_file)
                    else:
                        os.remove(vec_file)
                        print("Removed {}".format(vec_file))
                else:
                    print("rm {}".format(vec_file))
                continue
        processes_pool.join()
    except Exception as inst:
        print("Finished with pool")

    print("Finish Checks")
