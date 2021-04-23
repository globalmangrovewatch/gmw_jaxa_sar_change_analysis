import sys
import ftplib
import os.path


def writeList2File(dataList, outFile):
    """
    Write a list a text file, one line per item.

    :param dataList: List of values to be written to the output file.
    :param out_file: File path to the output file.

    """
    try:
        f = open(outFile, 'w')
        for item in dataList:
            f.write(str(item) + '\n')
        f.flush()
        f.close()
    except Exception as e:
        raise e

def traverseFTP(ftp, dir):
    dirs = []
    nondirs = []
    for item in ftp.mlsd(dir):
        if (item[1]['type'] == 'dir') and ((item[0][0] == 'S') or (item[0][0] == 'N')):
            dirs.append(os.path.join(dir, item[0]))
        elif not ((item[0] == '.') or (item[0] == '..')):
            nondirs.append(os.path.join(dir, item[0]))
    if not nondirs:
        return nondirs

    for subdir in sorted(dirs):
        #print(subdir)
        tmpFilesLst = traverseFTP(ftp, subdir)
        nondirs = nondirs + tmpFilesLst
    return nondirs

def getFTPListings(ftpURL, ftpPath, outputFile):
    print("Opening Connection")
    ftpConn = ftplib.FTP(ftpURL)
    ftpConn.login()
    print("Getting list of files")
    ftpFiles = traverseFTP(ftpConn, ftpPath)
    
    writeList2File(ftpFiles, outputFile)
    print("Finished: {}".format(outputFile))


#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS/ext1/PALSAR_MSC/25m_MSC/2010', './JAXA_PALSAR_2010_FileLst.txt')
#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS/ext1/PALSAR_MSC/25m_MSC/2009', './JAXA_PALSAR_2009_FileLst.txt')
#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS/ext1/PALSAR_MSC/25m_MSC/2008', './JAXA_PALSAR_2008_FileLst.txt')
#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS/ext1/PALSAR_MSC/25m_MSC/2007', './JAXA_PALSAR_2007_FileLst.txt')

#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS-2/ext1/PALSAR-2_MSC/25m_MSC/2015', './JAXA_PALSAR2_2015_FileLst.txt')
#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS-2/ext1/PALSAR-2_MSC/25m_MSC/2016', './JAXA_PALSAR2_2016_FileLst.txt')

#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS-2/ext1/PALSAR-2_MSC/25m_MSC/2017', './JAXA_PALSAR2_2017_FileLst.txt')
#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS-2/ext1/PALSAR-2_MSC/25m_MSC/2018', './JAXA_PALSAR2_2018_FileLst.txt')
getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS-2/ext1/PALSAR-2_MSC/25m_MSC/2019', './JAXA_PALSAR2_2019_FileLst.txt')
getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS-2/ext1/PALSAR-2_MSC/25m_MSC/2020', './JAXA_PALSAR2_2020_FileLst.txt')

#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS-2/JERS-1_MSC/25m_MSC/1996/', './JAXA_JERS-1_1996_FileLst.txt')

#getFTPListings('ftp.eorc.jaxa.jp', '/pub/ALOS/ext1/AW3D30/release', './JAXA_PrismDEM_30m_FileLst.txt')

