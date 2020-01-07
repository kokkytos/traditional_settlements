# -*- coding: utf-8 -*-
import ConfigParser, os
import tempfile
import ftplib
from PyQt4 import QtGui

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"settings.cfg"))
ftp_host=config.get('ftp', 'ftp_host')
ftp_user=config.get('ftp', 'ftp_user')
ftp_password=config.get('ftp', 'ftp_password')
pdfdir=tempfile.gettempdir()  #get temp directory

#==============================================================================================================================         
def ftpcallback(self, chunk,progressbar, file):
      file.write(chunk)  
      progressbar.setValue(int(progressbar.value() + int(len(chunk))))
  #============================================================================================================================== 
  
  


  
#==============================================================================================================================         
def downloadFileFromServer(lbfiles, filename, savepath, pb):
        """Downloads a file from ft server and saves on disk"""
        # Login
        
        lbfiles.show()
        lbfiles.setText(u'Σύνδεση στον ftp server...')
        ftp = ftplib.FTP(ftp_host)
        ftp.login(ftp_user, ftp_password)
        
        
        # list files on ftp server
        file_list = ftp.nlst()
        # print file_list
        if filename not in file_list:
            QtGui.QMessageBox.information(None, u"Ενημέρωση!", u"Δεν βρέθηκε διαθέσιμο αρχείο στον εξυπηρετητή")
        else:
            # Open the file for writing in binary mode
            file = open(os.path.join(savepath, filename), 'wb')
            filesize = ftp.size(filename)
            
            pb.reset()
            pb.setRange(0, filesize)
            pb.show()
            
            lbfiles.setText(u'Λήψη αρχείου:%s' % filename)
            ftp.retrbinary('RETR %s' % filename, lambda chunk=None, progressbar=pb, file =file : ftpcallback(None,chunk,progressbar,file))
            file.close()

            print "file downloaded"
            ftp.quit()  # close connection
  #==============================================================================================================================           
