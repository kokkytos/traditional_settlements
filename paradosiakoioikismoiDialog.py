# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name             : paradosiakoi oikismoi
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
import fnmatch
#import ftplib
import os,sys
import subprocess
import tempfile

from PyQt4 import QtCore, QtGui, QtSql, QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from Ui_paradosiakoioikismoi import Ui_MainWindow
import myftp
#import numpy as np
import pop_pyramid


#setup field indexes for nomothesia
nomothesiaid,name,nomothesia,has_map,has_orio,oikismosid,done,description,notes,newfilename,idnom,category =range (12)


# create the dialog for paradosiakoioikismoi
class paradosiakoioikismoiDialog(QtGui.QMainWindow):
  '''Class to handle traditional settlements of Aegean'''
    

  

  def __init__(self): 
      
    QtGui.QMainWindow.__init__(self) 
    
    # Set up the user interface from Designer. 
    self.ui = Ui_MainWindow ()
    self.ui.setupUi(self)
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
    
    # read settings
    self.config = ConfigParser.ConfigParser()
    self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"settings.cfg"))
    self.read()
    
    
    self.db = QtSql.QSqlDatabase.database( "myconnection") #ανοίγει ταυτόχρονα και η σύνδεση:
    
    '''
    /*********************************************************************************************************************************
    * Returns the database connection called connectionName. The database connection must have been previously added with addDatabase().
    * If open is true (the default) and the database connection is not already open it is opened now. 
    * If no connectionName is specified the default connection is used. 
    * If connectionName does not exist in the list of databases, an invalid connection is returned.
    * ->source: http://qt-project.org/doc/qt-4.8/qsqldatabase.html#database
     /*********************************************************************************************************************************
    '''

    #handles pyramid behaviour
    self.generatePyramid=False
    self.ESYEID=None

    print "DB is already opened:", self.db.isOpen ()
    if not self.db.isOpen ():
            
        ok = self.db.open()
        if ok==True:
            print "Database just opened now!"
        else:
            print "Failed to open database!"
        

 
    #=====================NOMOI ==================================================================================================       
    id4,  id3,  id1,  id2,  name,  mon_pop01,  id,  aegean=range(8)

    self.model = QtSql.QSqlTableModel(self, self.db)
    self.model.setTable("aegean.nomoi")
    self.model.setFilter('aegean=1')  # get only aegean data from database
    self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    self.model.select()
    self.ui.listViewNomoi.setModel(self.model)
    self.ui.listViewNomoi.setModelColumn(4)
    #==============================================================================================================================
    
    
    
    # ====================DHMOI ====================================================================================          
    #field indexes to variables (mappimg to field order in db)
    id4, id3,  id1 ,  id2 ,  name ,  mon_pop01 ,id, aegean=range(8)
	
    self.modeldimoi = QtSql.QSqlTableModel(self, self.db)
    self.modeldimoi.setTable("aegean.dimoi")
    self.modeldimoi.setFilter('aegean=1')  # get only aegean data from database
    self.modeldimoi.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    self.modeldimoi.select()
 
    self.proxyModel = QtGui.QSortFilterProxyModel()
    self.proxyModel.setSourceModel(self.modeldimoi)
    self.proxyModel.setFilterKeyColumn(id)
    self.proxyModel.sort(name, QtCore.Qt.AscendingOrder)
    self.proxyModel.setDynamicSortFilter(True)

    self.ui.listViewDhmoi.setModel(self.proxyModel)
    self.ui.listViewDhmoi.setModelColumn(name);
    self.filterString = QtCore.QRegExp("~#", QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
    self.proxyModel.setFilterRegExp(self.filterString) 
    #==============================================================================================================================
    
    
    
    # ====================OIKISMOI ====================================================================================          
    #field indexes to variables
    id4,id3,id1,id2,name,mon_pop01,id,aegean,dhmosid,paradosiakos=range(10)

    self.modeloikismoi = QtSql.QSqlTableModel(self, self.db)
    self.modeloikismoi.setTable("aegean.oikismoi")
    self.modeloikismoi.setFilter('paradosiakos=1')
    self.modeloikismoi.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    self.modeloikismoi.select()
     
    self.proxyModeloikismoi = QtGui.QSortFilterProxyModel()
    self.proxyModeloikismoi.setSourceModel(self.modeloikismoi)
    self.proxyModeloikismoi.setFilterKeyColumn(id)
    self.proxyModeloikismoi.sort(name, QtCore.Qt.AscendingOrder)
    self.proxyModeloikismoi.setDynamicSortFilter(True)

    self.ui.listViewOikismoi.setModel(self.proxyModeloikismoi)
    self.ui.listViewOikismoi.setModelColumn(name)
    self.filterString2 = QtCore.QRegExp("~#", QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
    self.proxyModeloikismoi.setFilterRegExp(self.filterString2) 
    #==============================================================================================================================
        
    
    # ====================NOMOTHESIA====================================================================================    
    self.nomothesiaModel = QtSql.QSqlQueryModel(self)
    self.nomothesiaModel.setQuery(self.config.get('Sqlsettings', 'selectNomothesia'), self.db)
    

           
    self.nomothesiaModel.setHeaderData(nomothesiaid, QtCore.Qt.Horizontal, "myID")
    self.nomothesiaModel.setHeaderData(nomothesia, QtCore.Qt.Horizontal, u"Νομοθεσία")
    self.nomothesiaModel.setHeaderData(description, QtCore.Qt.Horizontal, u"Λεπτομέρειες")
    self.nomothesiaModel.setHeaderData(category, QtCore.Qt.Horizontal, u"Κατηγορία")
    
    self.proxyModelNomothesia = QtGui.QSortFilterProxyModel()
    self.proxyModelNomothesia.setSourceModel(self.nomothesiaModel)
    self.proxyModelNomothesia.setFilterKeyColumn(oikismosid)
    self.proxyModelNomothesia.sort(nomothesia, QtCore.Qt.AscendingOrder)
    self.proxyModelNomothesia.setDynamicSortFilter(True)
    
    self.ui.tableViewNomothesia.setModel(self.proxyModelNomothesia)
    self.ui.tableViewNomothesia.setVisible(False)
    self.ui.tableViewNomothesia.resizeColumnsToContents()
    self.ui.tableViewNomothesia.setVisible(True)
    self.ui.tableViewNomothesia.setSortingEnabled(True)
    self.ui.tableViewNomothesia.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.ui.tableViewNomothesia.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.ui.tableViewNomothesia.verticalHeader().setVisible(False)
    
    # Hide some columns
    self.columnsToHide = [0, 1, 3, 4, 5, 6, 8, 9, 10]
    for column in self.columnsToHide:
        self.ui.tableViewNomothesia.setColumnHidden(column, True) 

    filterString = QtCore.QRegExp("~#", QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
    self.proxyModelNomothesia.setFilterRegExp(filterString) 
    #==============================================================================================================================
    
    #====================Demographic indices ==================================================================================== =   
    self.modelDeiktes = QtSql.QSqlTableModel(self, self.db)
    self.modelDeiktes.setTable("aegean.deiktes_tbl")
    # self.modelDeiktes.setFilter('id=1')
    self.modelDeiktes.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    self.modelDeiktes.select()
   
    # setup widget mapper
    self.mymapper = QtGui.QDataWidgetMapper(self)
    self.mymapper.setModel(self.modelDeiktes)
    self.mymapper.addMapping(self.ui.lineEdit_Pop, self.modelDeiktes.fieldIndex("total"))
    self.mymapper.addMapping(self.ui.lineEdit_mw, self.modelDeiktes.fieldIndex("andresprosgynaikes"))
    self.mymapper.addMapping(self.ui.lineEdit_dapp, self.modelDeiktes.fieldIndex("deiktisAntikatParagPlith"))
    self.mymapper.addMapping(self.ui.lineEdit_dgp, self.modelDeiktes.fieldIndex("deiktisGiransis"))
    self.mymapper.addMapping(self.ui.lineEdit_de, self.modelDeiktes.fieldIndex("deiktiseksartisis"))
    self.mymapper.addMapping(self.ui.lineEdit_ilikiomenoi1, self.modelDeiktes.fieldIndex("analogia65Pros15_64"))
    self.mymapper.addMapping(self.ui.lineEdit_ilikiomenoi2, self.modelDeiktes.fieldIndex("65plus_epi_totalPOP"))
    #==============================================================================================================================   
  
  
    
    #====================Population by sex and age ================================================================================   
    self.modelPopSexAge = QtSql.QSqlTableModel(self, self.db)
    self.modelPopSexAge.setTable("aegean.pop_sex_age")
    self.modelPopSexAge.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
    #==============================================================================================================================

    
    #====================signals and slots ========================================================================================   
    self.ui.listViewNomoi.selectionModel().currentChanged.connect(self.handler_nomoi)
    self.ui.listViewDhmoi.selectionModel().currentChanged.connect(self.handler_dhmoi)
    self.ui.listViewOikismoi.selectionModel().currentChanged.connect(self.handler_oikismoi)
    self.ui.tableViewNomothesia.doubleClicked.connect(self.NomothesiaDoubleClicked)
    self.ui.actionFek.triggered.connect(self.starpdf)
    self.ui.checkBoxParadosiakoi.stateChanged.connect(self.handler_checkBoxParadosiakoi)
    self.ui.tabWidget.currentChanged.connect(self.handler_tabs)
    self.modeloikismoi.dataChanged.connect(self.handler_data_changed)
    #==============================================================================================================================
    
    
    #====================some extra widgets========================================================================================  
    
    #label to insert in statusBar
    self.lb = QLabel('Ready...')
    self.lb.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
    
    #another label to insert in statusBar
    self.lbfiles = QLabel('')
    self.lbfiles.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Sunken)
    self.lbfiles.hide()
    
    #label to insert in statusBar
    self.pb = QtGui.QProgressBar(self)
    self.pb.hide()
    
    #add widgets to statusBar
    self.statusBar().addWidget(self.lb, 0)
    self.statusBar().addWidget(self.lbfiles, 1)
    self.statusBar().addWidget(self.pb, 2)
   #============================================================================================================================== 

     
    # self.showMaximized()
    # self.setGeometry(500, 600, 350, 300) #just in case to change form size
    # self.setFocus(True)
    # self.activateWindow()
    # self.show()

    

  def handler_data_changed(self, qitemindex, qitemindex2):
      
      print "data changed"
      #print qitemindex


      self.db.transaction()
      #self.modeloikismoi.setData(qitemindex, "test")
      self.modeloikismoi.submitAll()
      self.db.commit()

                
  #==============================================================================================================================               
  def starpdf(self):
      '''just handle pdf button click, get QModelIndex  and calls NomothesiaDoubleClicked'''
      try:
          tableviewindex = self.ui.tableViewNomothesia.selectionModel().selection()  # μπορεί να υπάρχουν πολλές επιλογές/indexes
          myindex = self.proxyModelNomothesia.index(tableviewindex.indexes()[0].row(), 9)  # το 9 αντιστοιχεί στο index της στήλης NEWFILENAME του proxyModelNomothesia
          self.NomothesiaDoubleClicked(myindex)
      except IndexError:
          QtGui.QMessageBox.information(None, u"Ενημέρωση!", u"Επιλέξτε αντικείμενο από το πλαίσιο της νομοθεσίας")
  #============================================================================================================================== 





  #==============================================================================================================================         
  def NomothesiaDoubleClicked(self, qitemindex):
    filename = str(self.proxyModelNomothesia.data(self.proxyModelNomothesia.index(qitemindex.row(), newfilename), 0))
    fullpath = os.path.join(self.pdfdir, filename)
    if not os.path.isfile(fullpath):
        print "File %s doesn't exist in disk, get it from server" % str(filename)
        myftp.downloadFileFromServer(self.lbfiles,filename, self.pdfdir, self.pb)
        # self.downloadwithFTP(filename, None)
        print "File downloaded!"
    if os.path.isfile(fullpath):        
        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", fullpath])  # only the first one
        else:
            os.startfile(fullpath)
    self.pb.hide()
    self.lbfiles.hide()
  #==============================================================================================================================             
  




  
  #==============================================================================================================================             
  def handler_tabs(self,index):

      if index==2:
          self.generatePyramid=True
      else:
          self.generatePyramid=False
      
      if self.generatePyramid ==True:
        #call pyramid update
        self.updatePyramid(self.ESYEID)
  #==============================================================================================================================               
    
    
    
    
  #==============================================================================================================================             
  def handler_nomoi(self, currentListItem, previousListItem):
    myfilter = "^{!s}".format(self.model.data(self.model.index(currentListItem.row(), 6), 0))

    if myfilter == '^':
            myfilter = "~#"
    filterString = QtCore.QRegExp(myfilter, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
    self.lb.setText(self.model.data(self.model.index(currentListItem.row(), 4), 0))
    self.nomoiMsgStatusbar = self.lb.text()
   

    self.proxyModel.setFilterRegExp(filterString)
    
    while self.proxyModel.canFetchMore(currentListItem):
         self.proxyModel.fetchMore(currentListItem)
    
    
    myfilter = "~#"
    filterString = QtCore.QRegExp(myfilter, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
    self.proxyModelNomothesia.setFilterRegExp(filterString)
    self.proxyModeloikismoi.setFilterRegExp(filterString)

    # filter Demographic indices   
    f = "id='{!s}'".format(self.model.data(self.model.index(currentListItem.row(), 6), 0))
    self.modelDeiktes.setFilter(f)  # %  
    self.mymapper.toFirst()
    
    self.ESYEID=self.model.data(self.model.index(currentListItem.row(), 6), 0)
    if self.generatePyramid ==True:
        #call pyramid update
        id =self.model.data(self.model.index(currentListItem.row(), 6), 0)
        self.updatePyramid(id)
  #==============================================================================================================================             
    
    
    
    
    
  #==============================================================================================================================                   
  def handler_dhmoi(self, currentListItem, previousListItem):
        try:
        
            
            myfilter = "^{!s}".format(self.proxyModel.data(self.proxyModel.index(currentListItem.row(), 6), 0)[0:4])
            
            while self.proxyModeloikismoi.canFetchMore(currentListItem):
                self.proxyModeloikismoi.fetchMore(currentListItem)
             
               
            if myfilter == '^':
                myfilter = "~#"
            filterString = QtCore.QRegExp(myfilter, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)
            self.proxyModeloikismoi.setFilterRegExp(filterString)
                        
            self.lb.setText('')
            self.dimoiMsgStatusbar = self.proxyModel.data(self.proxyModel.index(currentListItem.row(), 4), 0)
            self.lb.setText(self.nomoiMsgStatusbar + ">" + self.dimoiMsgStatusbar)
                     
            # filter Demographic indices   
            f = "id='{!s}'".format(self.proxyModel.data(self.proxyModel.index(currentListItem.row(), 6), 0))
            self.modelDeiktes.setFilter(f) 
            self.mymapper.toFirst()
            
            self.ESYEID=self.proxyModel.data(self.proxyModel.index(currentListItem.row(), 6), 0)
            
            #call pyramid update
            if self.generatePyramid ==True:
                id =self.proxyModel.data(self.proxyModel.index(currentListItem.row(), 6), 0)
                self.updatePyramid(id)
                  
        except TypeError:
            print "error"
            self.proxyModeloikismoi.reset()
  #==============================================================================================================================                     
    
    
    
            
        
  #==============================================================================================================================         
  def handler_oikismoi(self, currentListItem, previousListItem):
        
        myfilter = "^{!s}".format(self.proxyModeloikismoi.data(self.proxyModeloikismoi.index(currentListItem.row(), 6), 0))
        if myfilter == '^':
           myfilter = "~#"
        filterString = QtCore.QRegExp(myfilter, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp)

        self.proxyModelNomothesia.setFilterRegExp(filterString)
        
        #set statusbar
        self.lb.setText('')
        try:
            self.OikismoiMsgStatusbar = ">" + self.proxyModeloikismoi.data(self.proxyModeloikismoi.index(currentListItem.row(), 4), 0)
        except TypeError:
            self.OikismoiMsgStatusbar = ""

        self.lb.setText(self.nomoiMsgStatusbar + ">" + self.dimoiMsgStatusbar + self.OikismoiMsgStatusbar)        
        
        while self.proxyModelNomothesia.canFetchMore(currentListItem):
            self.proxyModelNomothesia.fetchMore(currentListItem)
         
         
        # filter statistika    
        myfilter = "id='%s'" % str(self.proxyModeloikismoi.data(self.proxyModeloikismoi.index(currentListItem.row(), 6), 0))
        
        self.modelDeiktes.setFilter(myfilter)
        self.mymapper.toFirst()
        
        self.ESYEID=self.proxyModeloikismoi.data(self.proxyModeloikismoi.index(currentListItem.row(), 6), 0)
        
        #call pyramid update
        if self.generatePyramid ==True:
            id =self.proxyModeloikismoi.data(self.proxyModeloikismoi.index(currentListItem.row(), 6), 0)
            try:
                self.updatePyramid(id)
            except ValueError:
                sys.exc_clear()
  #==============================================================================================================================                     





  #==============================================================================================================================                 
  def updatePyramid(self, id):
        '''Updates population pyramid from database data according to ID '''
        self.modelPopSexAge.setFilter("id='%s'" % str(id))
        self.modelPopSexAge.select()       
        name = self.modelPopSexAge.data(self.modelPopSexAge.index(0, 3))#get the name of nomos or dhmos or oikismos
        
        #generate lists with population 
        males = []
        females = []
        for j in range(7,43,2):
            agevalue=self.modelPopSexAge.data(self.modelPopSexAge.index(0, j))
            males.append(agevalue)
        for j in range(8,44,2):
            agevalue=self.modelPopSexAge.data(self.modelPopSexAge.index(0, j))
            females.append(agevalue) 
        try:             
            self.mpl = pop_pyramid.Qt4MplCanvas(name,males, females, 2001)
            #First delete widgets in verticalLayout_4 inside tab
            while self.ui.verticalLayout_4.count():
                item = self.ui.verticalLayout_4.takeAt(0)
                item.widget().deleteLater()
            
            #then add pyramid    
            self.ui.verticalLayout_4.addWidget(self.mpl) # add the widget in verticalLayout_4
            self.mpl.show()
      
        except ValueError:
                sys.exc_clear()
  #==============================================================================================================================                 
        



  #==============================================================================================================================                     
  def handler_checkBoxParadosiakoi(self, state):        
      '''Handles checkbox to filter paradosiakoi oikismoi'''
      try:
          if int(state) == 0:
                self.modeloikismoi.setFilter('paradosiakos>-1')  # disable filter on model
          else:
                self.modeloikismoi.setFilter('paradosiakos=1')

          index = self.ui.listViewDhmoi.selectionModel().selectedIndexes()[0]
          while self.proxyModeloikismoi.canFetchMore(index):
                self.proxyModeloikismoi.fetchMore(index)
      except IndexError:
         pass
  #==============================================================================================================================         




  #==============================================================================================================================         
  def read(self):
    """Reads Settings for database and ftp"""
    self.dbdriver = self.config.get('postgresql', 'dbdriver')
    self.host = self.config.get('postgresql', 'host')
    
    self.port = int(self.config.get('postgresql', 'port'))
    self.dbname = self.config.get('postgresql', 'dbname')
    self.username = self.config.get('postgresql', 'username')
    self.password = self.config.get('postgresql', 'password')
    self.ftp_host=self.config.get('ftp', 'ftp_host')
    self.ftp_user=self.config.get('ftp', 'ftp_user')
    self.ftp_password=self.config.get('ftp', 'ftp_password')
    
    self.pdfdir=tempfile.gettempdir()  #get temp directory
  #==============================================================================================================================         


  