# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name		     : paradosiakoi oikismoi
Description          : paradosiakoi oikismoi aigaiou
Date                 : 16/Feb/14 
copyright            : (C) 2014 by Leonidas Liakos
email                : leonidas_liakos@yahoo.gr 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import ConfigParser
import ftplib,sys
import os, fnmatch
import subprocess
import sys
import tempfile

from PyQt4 import QtCore, QtGui, QtSql
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Ui_SearchByNomothesia import Ui_MainWindow
import myftp


# create the dialog for paradosiakoioikismoi
class NomothesiaDialog(QtGui.QMainWindow):
  '''Class to handle traditional settlements of Aegean'''
    
  def __init__(self): 
    QtGui.QMainWindow.__init__(self) 
    
    # Set up the user interface from Designer. 
    
    self.ui = Ui_MainWindow ()
    self.ui.setupUi(self)
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    
    self.s = QSettings()
    
    #read settings
    self.config = ConfigParser.ConfigParser()
    self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"settings.cfg"))
    self.read()
    
    #db settings
    self.db = QtSql.QSqlDatabase.database( "myconnection");

    print "DB is already opened:", self.db.isOpen ()
    if not self.db.isOpen ():
            
        ok = self.db.open()
        if ok==True:
            print "Database just opened now!"
        else:
            print "Failed to open database!"
    
    
    # ====================NOMOTHESIA ============================================================================================== 
    #FIELD indexes FROM TABLE aegean.nomothesia
    NOMOTHESIAID,NOMOTHESIA,FILENAME,HAS_MAP,NOTES,TYPE,NEWFILENAME =range(7)
         
    self.nomothesiaModel = QtSql.QSqlRelationalTableModel(self, self.db)
    self.nomothesiaModel.setTable("aegean.nomothesia");
                         
    if self.nomothesiaModel.lastError().isValid(): 
        print("Error during data selection")
        
    self.nomothesiaModel.setRelation(TYPE, QtSql.QSqlRelation("aegean.nomothesia_types", "id", "description"));
    self.nomothesiaModel.select()


    self.nomothesiaModel.setHeaderData(NOMOTHESIA, QtCore.Qt.Horizontal, u"Νομοθεσία")
    self.nomothesiaModel.setHeaderData(TYPE, QtCore.Qt.Horizontal, u"Κατηγορία")
    while self.nomothesiaModel.canFetchMore():
        self.nomothesiaModel.fetchMore()
     
    self.proxyModelNomothesia = QtGui.QSortFilterProxyModel()
    self.proxyModelNomothesia.setSourceModel(self.nomothesiaModel)
    self.proxyModelNomothesia.setFilterKeyColumn(NOMOTHESIA)

    self.ui.tableViewNomothesia.setModel(self.proxyModelNomothesia)
    self.ui.tableViewNomothesia.setVisible(False)
    self.ui.tableViewNomothesia.resizeColumnsToContents()
    self.ui.tableViewNomothesia.setVisible(True)
    self.ui.tableViewNomothesia.setAlternatingRowColors(True)
    self.ui.tableViewNomothesia.setSortingEnabled(True)
    self.ui.tableViewNomothesia.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.ui.tableViewNomothesia.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.ui.tableViewNomothesia.verticalHeader().setVisible(False)
    self.ui.tableViewNomothesia.sortByColumn(NOMOTHESIA, QtCore.Qt.AscendingOrder)#κάνω το sort στο tableview γιατί στο QSortFilterProxyModel δεν δουλεύει όταν το datasource είναι QSqlQueryModel
    #Hide some columns
    self.ui.tableViewNomothesia.setColumnHidden(NOMOTHESIAID,True)
    self.ui.tableViewNomothesia.setColumnHidden(FILENAME,True)
    self.ui.tableViewNomothesia.setColumnHidden(HAS_MAP,True)
    self.ui.tableViewNomothesia.setColumnHidden(NOTES,True)
    self.ui.tableViewNomothesia.setColumnHidden(NEWFILENAME,True)
    
    
    self.ui.tableViewNomothesia.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
    
    #==============================================================================================================================
    
    
    
    
    # ====================OIKISMOI ================================================================================================
    
    #FIELD indexes
    OIKISMOI_NAME,   DIMOI_NAME,   NOMOI_NAME,   NOMOTHESIA_NOMOTHESIA,  oikismoi_has_nomothesia_description, oikismoi_has_nomothesia_nomothesiaid, oikismoi_id = range(7)
    
    self.modeloikismoi = QtSql.QSqlQueryModel(self)
    self.modeloikismoi.setQuery(self.config.get('Sqlsettings', 'selectOikismoi'),self.db)

    if self.modeloikismoi.lastError().isValid(): 
        print("Error during data selection")
        
    self.modeloikismoi.setHeaderData(OIKISMOI_NAME, QtCore.Qt.Horizontal, u"Οικισμός")
    self.modeloikismoi.setHeaderData(DIMOI_NAME, QtCore.Qt.Horizontal, u"Δήμος")
    self.modeloikismoi.setHeaderData(NOMOI_NAME, QtCore.Qt.Horizontal, u"Νομός")
    self.modeloikismoi.setHeaderData(NOMOTHESIA_NOMOTHESIA, QtCore.Qt.Horizontal, u"Νομοθεσία")
    self.modeloikismoi.setHeaderData(oikismoi_has_nomothesia_description, QtCore.Qt.Horizontal, u"Λεπτομέρειες")
    while self.modeloikismoi.canFetchMore():
        self.modeloikismoi.fetchMore()
    
    self.proxyModeloikismoi = QtGui.QSortFilterProxyModel()
    self.proxyModelNomothesia.setSortLocaleAware(True)
    self.proxyModeloikismoi.setSourceModel(self.modeloikismoi)
    self.proxyModeloikismoi.setFilterKeyColumn(oikismoi_has_nomothesia_nomothesiaid)

    self.ui.tableViewOikismoi.setModel(self.proxyModeloikismoi)
    self.ui.tableViewOikismoi.setVisible(False)
    self.ui.tableViewOikismoi.resizeColumnsToContents()
    self.ui.tableViewOikismoi.setVisible(True)
    self.ui.tableViewOikismoi.setSortingEnabled(True)
    self.ui.tableViewOikismoi.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.ui.tableViewOikismoi.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.ui.tableViewOikismoi.sortByColumn(OIKISMOI_NAME, QtCore.Qt.AscendingOrder)#κάνω το sort στο tableview γιατί στο QSortFilterProxyModel δεν δουλεύει όταν το datasource είναι QSqlQueryModel
    self.ui.tableViewOikismoi.verticalHeader().setVisible(False)
    self.ui.tableViewOikismoi.setAlternatingRowColors(True)
    #Hide some columns
    self.ui.tableViewOikismoi.setColumnHidden(oikismoi_has_nomothesia_nomothesiaid,True)
    self.ui.tableViewOikismoi.setColumnHidden(oikismoi_id,True)
    #==============================================================================================================================




    #====================signals and slots ========================================================================================

    self.ui.lineEdit.textChanged.connect(self.setFilterNomothesia)
    self.ui.lineEdit.textChanged.connect(self.setFilterNomothesia)  
    self.ui.tableViewNomothesia.selectionModel().currentChanged.connect(self.setfilterOikismous)
    self.ui.actionFek.triggered.connect(self.starpdf)
    #==============================================================================================================================
    




    #====================some extra widgets========================================================================================  
    self.lb=QLabel('Ready...' )
    self.lb.setFrameStyle(QtGui.QFrame.Panel |QtGui.QFrame.Sunken)
    
    self.lbfiles=QLabel('' )
    self.lbfiles.setFrameStyle(QtGui.QFrame.Panel |QtGui.QFrame.Sunken)
    self.lbfiles.hide()
        
    self.pb = QtGui.QProgressBar(self)
    self.pb.hide()
    
    #add widgets to statusBar
    self.statusBar().addWidget(self.lb,0)
    self.statusBar().addWidget(self.lbfiles,1)
    self.statusBar().addWidget(self.pb, 2)
  #==============================================================================================================================
 




  #==============================================================================================================================             
  def starpdf(self):
      '''just handle pdf button click, get QModelIndex  and calls NomothesiaDoubleClicked'''
      try:
          tableviewindex = self.ui.tableViewNomothesia.selectionModel().selection()#μπορεί να υπάρχουν πολλές επιλογές/indexes
          myindex = self.proxyModelNomothesia.index(tableviewindex.indexes()[0].row(),2) #το 9 αντιστοιχεί στο index της στήλης NEWFILENAME του proxyModelNomothesia
          self.NomothesiaDoubleClicked(myindex)
      except IndexError:
          QtGui.QMessageBox.information(None,u"Ενημέρωση!",u"Επιλέξτε αντικείμενο από το πλαίσιο της νομοθεσίας")
  #==============================================================================================================================                   
  




#===============================================================================
#   #==============================================================================================================================         
#   def ftpcallback(self, chunk,progressbar):
#       self.file.write(chunk)  
#       progressbar.setValue(int(self.pb.value() + int(len(chunk))))
#   #============================================================================================================================== 
#   
# 
# 
# 
#   #==============================================================================================================================         
#   def downloadFileFromServer(self,filename, savepath):
#         """Downloads a file from ft server and saves on disk"""
#         #Login
#         ftp = ftplib.FTP(self.ftp_host)
#         self.lbfiles.show()
#         self.lbfiles.setText(u'Σύνδεση στον ftp server...')
#         ftp.login(self.ftp_user, self.ftp_password)
# 
#         #list files on ftp server
#         file_list = ftp.nlst()
# 
#         if filename not in file_list:
#             QtGui.QMessageBox.information(None,u"Ενημέρωση!",u"Δεν βρέθηκε διαθέσιμο αρχείο στον εξυπηρετητή")
#         else:
#             # Open the file for writing in binary mode
#             self.file = open(os.path.join(savepath,filename), 'wb')
#             filesize = ftp.size(filename)
#             
#             self.pb.reset()
#             self.pb.setRange(0, filesize)
#             self.pb.show()
#             
#             self.lbfiles.setText(u'Λήψη αρχείου:%s'%filename)
#             ftp.retrbinary('RETR %s' % filename, lambda chunk=None, progressbar=self.pb: self.ftpcallback(chunk,progressbar))
#             self.file.close()
# 
#             print "File downloaded"
#             ftp.quit() #close connection
#   #==============================================================================================================================                     
#     
#===============================================================================


       
  #==============================================================================================================================                     
  def NomothesiaDoubleClicked(self,qitemindex):
    filename = str(self.proxyModelNomothesia.data(self.proxyModelNomothesia.index(qitemindex.row(),2),0))
    fullpath=os.path.join(self.pdfdir,filename)
    if not os.path.isfile(fullpath):
        print "File %s doesn't exist in disk, get it from server" %str(filename)
        myftp.downloadFileFromServer(self.lbfiles,filename, self.pdfdir, self.pb)
        print "Done"
    if os.path.isfile(fullpath):        
        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", fullpath])
        else:
            os.startfile(fullpath)
    self.pb.hide()
    self.lbfiles.hide()
  #==============================================================================================================================     
   




  #==============================================================================================================================           
  def setFilterNomothesia(self,newtext):
      myfilter =u".*{!s}".format(str(newtext))

      filterString = QtCore.QRegExp(myfilter,QtCore.Qt.CaseInsensitive,QtCore.QRegExp.RegExp)
      self.proxyModelNomothesia.setFilterRegExp(filterString)
      self.proxyModeloikismoi.setFilterRegExp(QtCore.QRegExp("~#",QtCore.Qt.CaseInsensitive,QtCore.QRegExp.RegExp)) 
  #==============================================================================================================================               
    




  #==============================================================================================================================               
  def setfilterOikismous(self, currentListItem, previousListItem):
      myfilter =  "^{!s}$".format(self.proxyModelNomothesia.data(self.proxyModelNomothesia.index(currentListItem.row(),0),0))
      filterString = QtCore.QRegExp(myfilter,QtCore.Qt.CaseInsensitive,QtCore.QRegExp.RegExp)
      self.proxyModeloikismoi.setFilterRegExp(filterString)
      print filterString
      self.lb.setText(self.proxyModelNomothesia.data(self.proxyModelNomothesia.index(currentListItem.row(),1),0))
  #==============================================================================================================================              
   




  #==============================================================================================================================               
  def read(self):
    """Reads QSettings for database and ftp"""
    self.s = QSettings()
    self.dbdriver = self.config.get('postgresql', 'dbdriver')
    self.host = self.config.get('postgresql', 'host')
    
    self.port = int(self.config.get('postgresql', 'port'))
    self.dbname = self.config.get('postgresql', 'dbname')
    self.username = self.config.get('postgresql', 'username')
    self.password = self.config.get('postgresql', 'password')
    self.ftp_host=self.config.get('ftp', 'ftp_host')
    self.ftp_user=self.config.get('ftp', 'ftp_user')
    self.ftp_password=self.config.get('ftp', 'ftp_password')
    self.pdfdir=tempfile.gettempdir()     
  #==============================================================================================================================               

	
  
    