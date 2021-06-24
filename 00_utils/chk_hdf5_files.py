import osgeo.gdal as gdal
import osgeo.osr as osr
import numpy
import os
import argparse
import glob


def check_hdf5_file(input_file):
    """
    A function which checks whether a HDF5 file is valid.
    :param input_file: the file path to the input file.
    :return: a boolean - True file is valid. False file is not valid.

    """
    import h5py

    def _check_h5_var(h5_obj):
        lcl_ok = True
        lcl_err = ''
        try:
            if isinstance(h5_obj, h5py.Dataset):
                lcl_ok = True
            elif isinstance(h5_obj, h5py.Group):
                for var in h5_obj.keys():
                    lcl_ok, lcl_err = _check_h5_var(h5_obj[var])
                    if not lcl_ok:
                        break
        except RuntimeError as e:
            lcl_ok = False
            lcl_err = str(e)
        except Exception as e:
            lcl_ok = False
            lcl_err = str(e)
        return lcl_ok, lcl_err

    glb_ok = True
    err_str = ''
    if not os.path.exists(input_file):
        glb_ok = False
    else:
        try:
            fH5 = h5py.File(input_file, 'r')
            if fH5 is None:
                glb_ok = False
                err_str = 'Could not open HDF5 file'
            else:
                for var in fH5.keys():
                    glb_ok, err_str = _check_h5_var(fH5[var])
                    if not glb_ok:
                        break
        except RuntimeError as e:
            glb_ok = False
            err_str = str(e)
        except Exception as e:
            glb_ok = False
            err_str = str(e)
    return glb_ok, err_str


def _run_img_chk(img_params):
    h5_file = img_params[0]
    rmerr = img_params[1]
    printnames = img_params[2]
    printerrs = img_params[3]

    if printnames:
        print(h5_file)
    try:
        file_ok, err_str = check_hdf5_file(h5_file)
        if printerrs and (not file_ok):
            print("Error: '{}'".format(err_str))
        if not file_ok:
            if rmerr:
                os.remove(h5_file)
                print("Removed {}".format(h5_file))
            else:
                print("rm {}".format(h5_file))
    except Exception as e:
        if printerrs:
            print("Error: '{}'".format(e))
        if rmerr:
            os.remove(h5_file)
            print("Removed {}".format(h5_file))
        else:
            print("rm {}".format(h5_file))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A utility which can be used to check whether a GDAL "
                                                 "compatible file is valid and if there are any errors or warnings.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file path")
    parser.add_argument("--rmerr", action='store_true', default=False, help="Delete error files from system.")
    parser.add_argument("--printnames", action='store_true', default=False, help="Print file names as checking")
    parser.add_argument("--printerrs", action='store_true', default=False, help="Print the error messages for the images")

    args = parser.parse_args()
    print(args.input)

    h5_files = glob.glob(args.input)

    print("File Checks ({} Files Found):".format(len(h5_files)))

    from multiprocessing import Pool

    processes_pool = Pool(1)
    try:
        for h5_file in h5_files:
            try:
                params = [h5_file, args.rmerr, args.printnames, args.printerrs,]
                result = processes_pool.apply_async(_run_img_chk, args=[params])
                result.get(timeout=2)
            except Exception as e:
                if args.rmerr:
                    os.remove(h5_file)
                    print("Removed {}".format(h5_file))
                else:
                    print("rm {}".format(h5_file))
                continue
        processes_pool.join()
    except Exception as inst:
        print("Finished with pool")

    print("Finish Checks")
