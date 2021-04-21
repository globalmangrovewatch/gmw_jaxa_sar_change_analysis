import glob
import os

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

bert_dir = '/dges/MangroveWatch/other_projects/base_datasets/World_BaseData/JAXA/SAR/Download'
scw_dir = 'a.pfb@sunbird.swansea.ac.uk:/scratch/a.pfb/gmw_v3_change/data/jaxa_dwnlds/2010/.'

jaxa_tile_names_file = 'jaxa_tile_names.txt'

tiles = readTextFile2List(jaxa_tile_names_file)
cmds = []
for tile in tiles:
    file_name = "{}_10_MOS.tar.gz".format(tile)
    file_full_path = os.path.join(bert_dir, file_name)
    
    if os.path.exists(file_full_path):
        cmd = 'scp {} {}'.format(file_full_path, scw_dir)
        cmds.append(cmd)
    else:
        print("File is not available: {}".format(file_full_path))    

writeList2File(cmds, 'Upload2020PALSAR.sh')


