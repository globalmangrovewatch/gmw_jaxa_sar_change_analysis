import pycurl
import os
import pprint

def downloadFile(url, remote_path, local_path, time_out=None, username=None, password=None):
    """

    :param url:
    :param remote_path:
    :param local_path:
    :param time_out: (default 300 seconds if None)
    :param username:
    :param password:
    :return:
    """
    full_path_url = url + remote_path
    success = False
    try:
        if time_out is None:
            time_out = 300

        fp = open(local_path, "wb")
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, full_path_url)
        curl.setopt(pycurl.FOLLOWLOCATION, True)
        curl.setopt(pycurl.NOPROGRESS, 0)
        curl.setopt(pycurl.FOLLOWLOCATION, 1)
        curl.setopt(pycurl.MAXREDIRS, 5)
        curl.setopt(pycurl.CONNECTTIMEOUT, 50)
        curl.setopt(pycurl.TIMEOUT, time_out)
        curl.setopt(pycurl.FTP_RESPONSE_TIMEOUT, 600)
        curl.setopt(pycurl.NOSIGNAL, 1)
        if (not username is None) and (not password is None):
            curl.setopt(pycurl.HTTPAUTH, pycurl.HTTPAUTH_ANY)
            curl.setopt(pycurl.USERPWD, username + ':' + password)
        curl.setopt(pycurl.WRITEDATA, fp)
        print("Starting download of {}".format(full_path_url))
        curl.perform()
        print("Finished download in {0} of {1} bytes for {2}".format(curl.getinfo(curl.TOTAL_TIME), curl.getinfo(curl.SIZE_DOWNLOAD), full_path_url))
        success = True
    except:
        print("An error occurred when downloading {}.".format(os.path.join(url, remote_path)))
        success = False
    return success

def findFileNone(dirPath, fileSearch):
    """
    Search for a single file with a path using glob. Therefore, the file
    path returned is a true path. Within the fileSearch provide the file
    name with '*' as wildcard(s). Returns None is not found.

    :return: string

    """
    import glob
    import os.path
    files = glob.glob(os.path.join(dirPath, fileSearch))
    if len(files) != 1:
        return None
    return files[0]

def readTextFile2List(file):
    """
    Read a text file into a list where each line
    is an element in the list.

    :param file: File path to the input file.
    :return: list

    """
    outList = []
    try:
        dataFile = open(file, 'r')
        for line in dataFile:
            line = line.strip()
            if line != "":
                outList.append(line)
        dataFile.close()
    except Exception as e:
        raise e
    return outList

def writeList2File(dataList, outFile):
    """
    Write a list a text file, one line per item.

    :param dataList: List of values to be written to the output file.
    :param out_file: File path to the output file.

    """
    try:
        f = open(outFile, 'w')
        for item in dataList:
           f.write(str(item)+'\n')
        f.flush()
        f.close()
    except Exception as e:
        raise e

def get_file_basename(filepath, checkvalid=False, n_comps=0):
    """
    Uses os.path module to return file basename (i.e., path and extension removed)

    :param filepath: string for the input file name and path
    :param checkvalid: if True then resulting basename will be checked for punctuation
                       characters (other than underscores) and spaces, punctuation
                       will be either removed and spaces changed to an underscore.
                       (Default = False)
    :param n_comps: if > 0 then the resulting basename will be split using underscores
                    and the return based name will be defined using the n_comps
                    components split by under scores.
    :return: basename for file

    """
    import string
    basename = os.path.splitext(os.path.basename(filepath))[0]
    if checkvalid:
        basename = basename.replace(' ', '_')
        for punct in string.punctuation:
            if (punct != '_') and (punct != '-'):
                basename = basename.replace(punct, '')
    if n_comps > 0:
        basename_split = basename.split('_')
        if len(basename_split) < n_comps:
            raise Exception("The number of components specified is more than the number of components in the basename.")
        out_basename = ""
        for i in range(n_comps):
            if i == 0:
                out_basename = basename_split[i]
            else:
                out_basename = out_basename + '_' + basename_split[i]
        basename = out_basename
    return basename

def get_dir_name(in_file):
    """
    A function which returns just the name of the directory of the input file without the rest of the path.

    :param in_file: string for the input file name and path
    :return: directory name
    """
    in_file = os.path.abspath(in_file)
    dir_path = os.path.dirname(in_file)
    dir_name = os.path.basename(dir_path)
    return dir_name

def create_tile_lut(jaxa_server_lst_file, dir2ignore):
    jaxa_server_lst = readTextFile2List(jaxa_server_lst_file)
    jaxa_file_lut = dict()
    for jaxa_path in jaxa_server_lst:
        file_name = os.path.basename(jaxa_path)
        if 'FNF' not in file_name:
            basename = get_file_basename(jaxa_path, checkvalid=False, n_comps=1)
            base_dir = get_dir_name(jaxa_path)
            if base_dir != dir2ignore:
                jaxa_file_lut[basename] = jaxa_path
    return jaxa_file_lut

def find_run_dwnlds(jaxa_tile_lst_file, jaxa_server_lst_file, dir2ignore, jaxa_server_adrs, out_dir, err_tiles_file):
    jaxa_server_lut = create_tile_lut(jaxa_server_lst_file, dir2ignore)
    #pprint.pprint(jaxa_server_lut)

    jaxa_tile_lst = readTextFile2List(jaxa_tile_lst_file)

    no_file_tiles = list()
    for jaxa_tile in jaxa_tile_lst:
        if jaxa_tile in jaxa_server_lut:
            file2dwnld = jaxa_server_lut[jaxa_tile]
            file_name = os.path.basename(file2dwnld)
            out_file_path = os.path.join(out_dir, file_name)
            #print(out_file_path)
            if not os.path.exists(out_file_path):
                downloadFile(jaxa_server_adrs, file2dwnld, out_file_path, time_out=1200, username=None, password=None)
            elif os.path.getsize(out_file_path) < 1000:
                os.remove(out_file_path)
                downloadFile(jaxa_server_adrs, file2dwnld, out_file_path, time_out=1200, username=None, password=None)
            else:
                print("Already downloaded: {}".format(out_file_path))
        else:
            no_file_tiles.append(jaxa_tile)

    #pprint.pprint(no_file_tiles)
    print("Did not have tiles for {} of {} tiles.".format(len(no_file_tiles), len(jaxa_tile_lst)))
    writeList2File(no_file_tiles, err_tiles_file)

"""
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_JERS-1_1996_FileLst.txt', '1996', 'ftp.eorc.jaxa.jp', '/data/1996', './unavailable_1996_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR_2007_FileLst.txt', '2007', 'ftp.eorc.jaxa.jp', '/data/2007', './unavailable_2007_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR_2008_FileLst.txt', '2008', 'ftp.eorc.jaxa.jp', '/data/2008', './unavailable_2008_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR_2009_FileLst.txt', '2009', 'ftp.eorc.jaxa.jp', '/data/2009', './unavailable_2009_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR_2010_FileLst.txt', '2010', 'ftp.eorc.jaxa.jp', '/data/2010', './unavailable_2010_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR2_2015_FileLst.txt', '2015', 'ftp.eorc.jaxa.jp', '/data/2015', './unavailable_2015_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR2_2016_FileLst.txt', '2016', 'ftp.eorc.jaxa.jp', '/data/2016', './unavailable_2016_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR2_2017_FileLst.txt', '2017', 'ftp.eorc.jaxa.jp', '/data/2017', './unavailable_2017_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR2_2018_FileLst.txt', '2018', 'ftp.eorc.jaxa.jp', '/data/2018', './unavailable_2018_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR2_2019_FileLst.txt', '2019', 'ftp.eorc.jaxa.jp', '/data/2019', './unavailable_2019_tiles.txt')
find_run_dwnlds('../gmw_jaxa_tile_names.txt', '../00_file_listings/JAXA_PALSAR2_2020_FileLst.txt', '2020', 'ftp.eorc.jaxa.jp', '/data/2020', './unavailable_2020_tiles.txt')
"""


find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_JERS-1_1996_FileLst.txt', '1996', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/1996', './unavailable_1996_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR_2007_FileLst.txt', '2007', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2007', './unavailable_2007_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR_2008_FileLst.txt', '2008', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2008', './unavailable_2008_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR_2009_FileLst.txt', '2009', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2009', './unavailable_2009_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR_2010_FileLst.txt', '2010', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2010', './unavailable_2010_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR2_2015_FileLst.txt', '2015', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2015', './unavailable_2015_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR2_2016_FileLst.txt', '2016', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2016', './unavailable_2016_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR2_2017_FileLst.txt', '2017', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2017', './unavailable_2017_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR2_2018_FileLst.txt', '2018', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2018', './unavailable_2018_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR2_2019_FileLst.txt', '2019', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2019', './unavailable_2019_tiles_india_extras.txt')
find_run_dwnlds('../gmw_jaxa_tile_names_extras.txt', '../00_file_listings/JAXA_PALSAR2_2020_FileLst.txt', '2020', 'ftp.eorc.jaxa.jp', '/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/india_extras/2020', './unavailable_2020_tiles_india_extras.txt')


#100Gb per year = ~1Tb

