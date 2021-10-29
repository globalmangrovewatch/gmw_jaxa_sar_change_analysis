import os
import glob
import argparse


def get_file_size(file_path: str, unit: str = "bytes"):
    """
    A function which returns the file size of a file in the specified unit.

    Units:
    * bytes
    * kb - kilobytes  (bytes / 1024)
    * mb - megabytes  (bytes / 1024^2)
    * gb - gigabytes  (bytes / 1024^3)
    * tb - terabytes  (bytes / 1024^4)

    :param file_path: the path to the file for which the size is to be calculated.
    :param unit: the unit for the file size. Options: bytes, kb, mb, gb, tb
    :return: float for the file size.

    """
    import pathlib

    unit = unit.lower()
    if unit not in ["bytes", "kb", "mb", "gb", "tb"]:
        raise Exception("Unit must be one of: bytes, kb, mb, gb, tb")

    p = pathlib.Path(file_path)
    if p.exists() and p.is_file():
        file_size_bytes = p.stat().st_size

        if unit == "kb":
            out_file_size = file_size_bytes / 1024.0
        elif unit == "mb":
            out_file_size = file_size_bytes / 1024.0 ** 2
        elif unit == "gb":
            out_file_size = file_size_bytes / 1024.0 ** 3
        elif unit == "tb":
            out_file_size = file_size_bytes / 1024.0 ** 4
        else:
            out_file_size = file_size_bytes
    else:
        raise Exception("Input file path does not exist")
    return out_file_size


def find_files_size_limits(
    dir_path: str, file_search: str, min_size: int = 0, max_size: int = None
):
    """
    Search for files with a path using glob. Therefore, the file
    paths returned is a true path. Within the file_search provide the file
    names with '*' as wildcard(s).

    :param dir_path: string for the input directory path
    :param file_search: string with a * wildcard for the file being searched for.
    :param min_size: the minimum file size in bytes (default is 0)
    :param max_size: the maximum file size in bytes, if None (default) then ignored.
    :return: string with the path to the file

    Example:

    .. code:: python

        import rsgislib.tools.filetools
        file_paths = rsgislib.tools.filetools.find_files_size_limits("in/dir",
                                                                     "*N15W093*.tif",
                                                                     0, 100000)

    """
    files = glob.glob(os.path.join(dir_path, file_search))
    out_files = list()
    for c_file in files:
        file_size = get_file_size(c_file)
        if (max_size is None) and (file_size > min_size):
            out_files.append(c_file)
        elif (file_size > min_size) and (file_size < max_size):
            out_files.append(c_file)
    return out_files

def delete_file_with_basename(input_file: str, print_rms=True):
    """
    Function to delete all the files which have a path
    and base name defined in the input_file attribute.

    :param input_file: string for the input file name and path

    """
    baseName = os.path.splitext(input_file)[0]
    fileList = glob.glob(baseName + str(".*"))
    for file in fileList:
        if print_rms:
            print("Deleting file: " + str(file))
        os.remove(file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A utility which can be used to check whether a GDAL "
                                                 "compatible file is valid and if there are any errors or warnings.")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file path")
    parser.add_argument("-s", "--size", type=int, required=True, help="Max file size thresholds")
    parser.add_argument("--rmfile", action='store_true', default=False, help="Delete error files from system.")
    parser.add_argument("--printnames", action='store_true', default=False, help="Print file names as checking")

    args = parser.parse_args()

    file_lst = find_files_size_limits('', args.input, min_size=args.size)
    if len(file_lst) > 0:
        for in_file in file_lst:
            if args.printnames:
                print(in_file)
            if args.rmfile:
                delete_file_with_basename(in_file)
            else:
                print("rm {}".format(in_file))


