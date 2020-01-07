# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name			 	 : paradosiakoi oikismoi
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4 import QtSql

from qgis.core import *
import ConfigParser
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from paradosiakoioikismoiDialog import paradosiakoioikismoiDialog
from NomothesiaDialog import NomothesiaDialog
import sys,os
#from sys import settrace
#sys.path.append("/usr/share/eclipse/dropins/pydev/eclipse/plugins/org.python.pydev_3.3.3.201401272249/pysrc/")
#from pydevd import *
import tempfile

import time






class paradosiakoioikismoi: 
  
  
  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface
    
    self.config = ConfigParser.ConfigParser()
    self.config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)),"settings.cfg"))
    self.read()
    
    #postgis layers
    self.postgislayers={
                        "vwoikismoi": ['geometry', u'Οικισμοί', 'pkuid'],
                 "vworiaoikismon": ['geometry', u'Όρια παραδοσιακών οικισμών','pkuid']
                }
      


    dbase = QtSql.QSqlDatabase.addDatabase(self.dbdriver, "myconnection" )
    dbase.setHostName(self.host)
    dbase.setPort(int(self.port)) 
    dbase.setDatabaseName( self.dbname)
    dbase.setUserName(self.username)
    dbase.setPassword( self.password)
    print "DB open state:", dbase.isOpen () 

  
  def generateReport(self):
    
              try:
                  ###GET DATA
                  
                  listviewindex =self.dlg.ui.listViewOikismoi.selectionModel().selection()
                  myindex = self.dlg.proxyModeloikismoi.index(listviewindex.indexes()[0].row(),4) #4= index of column NAME in model
                  oikismosname = self.dlg.proxyModeloikismoi.data(myindex,0)
                  filename = QFileDialog.getSaveFileName(self.dlg, u"Δημιουργία αναφοράς", "", 'pdf(*.pdf)')
                  if filename != "":
                      QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                      if filename.split(".")[-1]!="pdf":
                          filename =   filename + ".pdf"
                      listviewindex =self.dlg.ui.listViewDhmoi.selectionModel().selection()
                      myindex = self.dlg.modeldimoi.index(listviewindex.indexes()[0].row(),4) #4= index of column NAME in model
                      dhmosname = self.dlg.modeldimoi.data(myindex,0)
                      
                      listviewindex =self.dlg.ui.listViewNomoi.selectionModel().selection()
                      myindex = self.dlg.model.index(listviewindex.indexes()[0].row(),4) #4= index of column NAME in model
                      nomosname = self.dlg.model.data(myindex,0)
                      
                      
            
                      
                      #=====================================================================
                      # tableviewindexes = self.dlg.ui.tableViewNomothesia.selectionModel() # μπορεί να υπάρχουν πολλές επιλογές/indexes
                      # print len(tableviewindexes.indexes())
                      # for i in tableviewindexes.indexes():
                      #     print i
                      #=====================================================================
                      #myindex = self.proxyModelNomothesia.index(tableviewindex.indexes()[0].row(), 9) 
                      
                      
                      mapRenderer = self.iface.mapCanvas().mapRenderer()
                      c = QgsComposition(mapRenderer)
                      c.setPlotStyle(QgsComposition.Print)
                      composerMap = QgsComposerMap(c, 135,102,150,100)
                      composerMap.setFrameEnabled(True)   
                      composerMap.setFrameOutlineWidth(0.1)
                      
                      c.addItem(composerMap)
                      
                      #title
                      composerLabel_title = QgsComposerLabel(c)
                      composerLabel_title.setText(u"ΠΑΡΑΔΟΣΙΑΚΟΙ ΟΙΚΙΣΜΟΙ ΣΤΟ ΑΙΓΑΙΟ")
                      composerLabel_title.setFont(QFont("Courier", 16, QFont.Bold))
                      composerLabel_title.setHAlign(Qt.AlignHCenter)
                      composerLabel_title.setVAlign(Qt.AlignVCenter)
                      composerLabel_title.setItemPosition(0,5,c.paperWidth(),10)
                      composerLabel_title.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_title.setFrameEnabled(True)   
                      composerLabel_title.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_title)
                      
                      #date
                      
                      now =  time.strftime("%d/%m/%Y")
                      composerLabel_date = QgsComposerLabel(c)
                      composerLabel_date.setText(u"Ημερομηνία:%s" %now )
                      composerLabel_date.setFont(QFont("Times", 9))
                      composerLabel_date.adjustSizeToText()
                      composerLabel_date.setHAlign(Qt.AlignLeft)
                      composerLabel_date.setVAlign(Qt.AlignVCenter)
                      #composerLabel_date.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_date.setItemPosition(3,17)
                      #composerLabel_date.setFrameEnabled(True)   
                      #composerLabel_date.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_date)
                      
                      
                      #oikismos
                      composerLabel_Oikismos = QgsComposerLabel(c)
                      composerLabel_Oikismos.setText(u"ΟΙΚΙΣΜΟΣ:")
                      composerLabel_Oikismos.setFont(QFont("Times", 12, QFont.Bold))
                      #composerLabel_Oikismos.adjustSizeToText()
                      composerLabel_Oikismos.setHAlign(Qt.AlignLeft)
                      composerLabel_Oikismos.setVAlign(Qt.AlignVCenter)
                      composerLabel_Oikismos.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_Oikismos.setItemPosition(7,32,50,10)
                      composerLabel_Oikismos.setFrameEnabled(True)   
                      composerLabel_Oikismos.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_Oikismos)
                      
                      
                      #dhmos
                      composerLabel_Dhmos= QgsComposerLabel(c)
                      composerLabel_Dhmos.setText(u"ΔΗΜΟΣ/ΚΟΙΝΟΤΗΤΑ:")
                      composerLabel_Dhmos.adjustSizeToText()
                      composerLabel_Dhmos.setHAlign(Qt.AlignLeft)
                      composerLabel_Dhmos.setVAlign(Qt.AlignVCenter)
                      composerLabel_Dhmos.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_Dhmos.setItemPosition(7,42,50,10)
                      composerLabel_Dhmos.setFrameEnabled(True)   
                      composerLabel_Dhmos.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_Dhmos)
                      
                      ##nomos
                      composerLabel_Nomos = QgsComposerLabel(c)
                      composerLabel_Nomos.setText(u"ΝΟΜΟΣ:")
                      composerLabel_Nomos.adjustSizeToText()
                      composerLabel_Nomos.setHAlign(Qt.AlignLeft)
                      composerLabel_Nomos.setVAlign(Qt.AlignVCenter) 
                      composerLabel_Nomos.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_Nomos.setItemPosition(7,52,50,10)
                      composerLabel_Nomos.setFrameEnabled(True)   
                      composerLabel_Nomos.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_Nomos)
                      
                      up=72                      
                       #nomothesia_label
                      composerLabel_nomothesia_label = QgsComposerLabel(c)
                      composerLabel_nomothesia_label.setText(u"Σχετική νομοθεσία")
                      composerLabel_nomothesia_label.setFont(QFont("Times", 12, QFont.Bold))
                      #composerLabel_Oikismos.adjustSizeToText()
                      composerLabel_nomothesia_label.setHAlign(Qt.AlignHCenter)
                      composerLabel_nomothesia_label.setVAlign(Qt.AlignVCenter)
                      composerLabel_nomothesia_label.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_nomothesia_label.setItemPosition(7,up,120,7) #LEFT,UP, WIDTH,HEIGHT
                      composerLabel_nomothesia_label.setFrameEnabled(True)   
                      composerLabel_nomothesia_label.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_nomothesia_label)
                      
                      up+=7
                      #nomothesia_label2
                      composerLabel_nomothesia_label2 = QgsComposerLabel(c)
                      composerLabel_nomothesia_label2.setText(u"Νομοθεσία")
                      composerLabel_nomothesia_label2.setFont(QFont("Times", 10, QFont.Bold))
                      composerLabel_nomothesia_label2.setHAlign(Qt.AlignHCenter)
                      composerLabel_nomothesia_label2.setVAlign(Qt.AlignVCenter)
                      composerLabel_nomothesia_label2.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_nomothesia_label2.setItemPosition(7,up,50,7) #LEFT,UP, WIDTH,HEIGHT
                      composerLabel_nomothesia_label2.setFrameEnabled(True)   
                      composerLabel_nomothesia_label2.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_nomothesia_label2)
                      
                      
                      #nomothesia_label3
                      composerLabel_nomothesia_label3 = QgsComposerLabel(c)
                      composerLabel_nomothesia_label3.setText(u"Λεπτομέρειες")
                      composerLabel_nomothesia_label3.setFont(QFont("Times", 10, QFont.Bold))
                      composerLabel_nomothesia_label3.setHAlign(Qt.AlignHCenter)
                      composerLabel_nomothesia_label3.setVAlign(Qt.AlignVCenter)
                      composerLabel_nomothesia_label3.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_nomothesia_label3.setItemPosition(57,79,70,7) #LEFT,UP, WIDTH,HEIGHT
                      composerLabel_nomothesia_label3.setFrameEnabled(True)   
                      composerLabel_nomothesia_label3.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_nomothesia_label3)
                       
                       #map_label
                      composerLabel_map_label = QgsComposerLabel(c)
                      composerLabel_map_label.setText(u"Απόσπασμα χάρτη")
                      composerLabel_map_label.setFont(QFont("Times", 12, QFont.Bold))
                      composerLabel_map_label.setHAlign(Qt.AlignHCenter)
                      composerLabel_map_label.setVAlign(Qt.AlignVCenter)
                      composerLabel_map_label.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_map_label.setItemPosition(135,95,150,7) #LEFT,UP, WIDTH,HEIGHT
                      composerLabel_map_label.setFrameEnabled(True)   
                      composerLabel_map_label.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_map_label)                     
                      
                      #scalebar
                      item = QgsComposerScaleBar(c)
                      item.setFont(QFont("Times", 9))
                      item.setStyle('Numeric') # optionally modify the style
                      item.setComposerMap(composerMap)
                      item.applyDefaultSize()
                      item.setItemPosition(265,192,18,6)
                      c.addItem(item)
                      
                      #dimografikoi_label
                      composerLabel_dhnografikoi_label = QgsComposerLabel(c)
                      composerLabel_dhnografikoi_label.setText(u"Δημογραφικοί δείκτες")
                      composerLabel_dhnografikoi_label.setFont(QFont("Times", 12, QFont.Bold))
                      composerLabel_dhnografikoi_label.setHAlign(Qt.AlignHCenter)
                      composerLabel_dhnografikoi_label.setVAlign(Qt.AlignVCenter)
                      composerLabel_dhnografikoi_label.setBackgroundColor (QColor(200,200,200,125))
                      composerLabel_dhnografikoi_label.setItemPosition(135,32,150,7) #LEFT,UP, WIDTH,HEIGHT
                      composerLabel_dhnografikoi_label.setFrameEnabled(True)   
                      composerLabel_dhnografikoi_label.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_dhnografikoi_label) 
                      
                      uplabels=39
                      dimograf_labels=[u'Μόνιμος πληθυσμός', u'Αναλογία Ανδρών-Γυναικών', u'Δείκτης Αντικ.Παραγωγικού πληθυσμού',u'Δείκτης γήρανσης', u'Δείκτης εξάρτησης', u'Αναλογία ηλικιωμένων προς δυνητικά ενεργό πληθυσμό', u'Αναλογία των ατόμων άνω των 65 ετών επί του συνολικού πληθυσμού']    
                      for label in  dimograf_labels:
                        composerLabel_dimograf_label = QgsComposerLabel(c)
                        composerLabel_dimograf_label.setText(label)
                        composerLabel_dimograf_label.setFont(QFont("Times", 10))
                        composerLabel_dimograf_label.setHAlign(Qt.AlignHCenter)
                        composerLabel_dimograf_label.setVAlign(Qt.AlignVCenter)
                        composerLabel_dimograf_label.setItemPosition(135,uplabels,120,7)
                        composerLabel_dimograf_label.setFrameEnabled(True)   
                        composerLabel_dimograf_label.setFrameOutlineWidth(0.1)
                        c.addItem(composerLabel_dimograf_label) 

                        uplabels+=7

                          
                        
                      #dimografkoi values
                      
                      for widget in self.dlg.ui.tab_2.children():
                          if isinstance(widget, QLineEdit):
                            print "linedit: %s  - %s" %(widget.objectName(),widget.text())
                           
                            composerLabel_dimograf_value = QgsComposerLabel(c)
                            value=widget.text()
                            if type(value)==QPyNullVariant:
                                value = '-'
                            composerLabel_dimograf_value .setText(value)
                            composerLabel_dimograf_value .setHAlign(Qt.AlignHCenter)
                            composerLabel_dimograf_value .setVAlign(Qt.AlignVCenter)
                            if widget.objectName()=="lineEdit_Pop":
                                composerLabel_dimograf_value .setItemPosition(255,39,30,7)
                            if widget.objectName()=="lineEdit_mw":
                                composerLabel_dimograf_value .setItemPosition(255,46,30,7)
                            if widget.objectName()=="lineEdit_dapp":
                                composerLabel_dimograf_value .setItemPosition(255,53,30,7)   
                            if widget.objectName()=="lineEdit_dgp":
                                composerLabel_dimograf_value .setItemPosition(255,60,30,7)   
                            if widget.objectName()=="lineEdit_de":
                                composerLabel_dimograf_value .setItemPosition(255,67,30,7)   
                            if widget.objectName()=="lineEdit_ilikiomenoi1":
                                composerLabel_dimograf_value .setItemPosition(255,74,30,7)   
                            if widget.objectName()=="lineEdit_ilikiomenoi2":
                                composerLabel_dimograf_value .setItemPosition(255,81,30,7)   
                             
                            composerLabel_dimograf_value .setFrameEnabled(True)   
                            composerLabel_dimograf_value .setFrameOutlineWidth(0.1)
                            c.addItem(composerLabel_dimograf_value )
                          uplabels+=7
									   
                      
                      
                      ##oikismos_value
                      composerLabel_OikismosValue = QgsComposerLabel(c)
                      composerLabel_OikismosValue.setText(oikismosname)
                      composerLabel_OikismosValue.adjustSizeToText()
                      composerLabel_OikismosValue.setHAlign(Qt.AlignLeft)
                      composerLabel_OikismosValue.setVAlign(Qt.AlignVCenter)
                      composerLabel_OikismosValue.setItemPosition(57,32,30,10)
                      composerLabel_OikismosValue.setFrameEnabled(True)   
                      composerLabel_OikismosValue.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_OikismosValue)
                      
                      
                       ##dhmos_value
                      composerLabel_dhmosValue = QgsComposerLabel(c)
                      composerLabel_dhmosValue.setText(dhmosname)
                      composerLabel_dhmosValue.adjustSizeToText()
                      composerLabel_dhmosValue.setHAlign(Qt.AlignLeft)
                      composerLabel_dhmosValue.setVAlign(Qt.AlignVCenter)
                      composerLabel_dhmosValue.setItemPosition(57,42,30,10)
                      composerLabel_dhmosValue.setFrameEnabled(True)   
                      composerLabel_dhmosValue.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_dhmosValue)
                      
                      
                      ##nomos_value
                      composerLabel_NomosValue = QgsComposerLabel(c)
                      composerLabel_NomosValue.setText(nomosname)
                      composerLabel_NomosValue.adjustSizeToText()
                      composerLabel_NomosValue.setHAlign(Qt.AlignLeft)
                      composerLabel_NomosValue.setVAlign(Qt.AlignVCenter)
                      composerLabel_NomosValue.setItemPosition(57,52,30,10)
                      composerLabel_NomosValue.setFrameEnabled(True)   
                      composerLabel_NomosValue.setFrameOutlineWidth(0.1)
                      c.addItem(composerLabel_NomosValue)
                      
                      
                      #nomothesia, add values for each nomothesia
                      mymodel = self.dlg.ui.tableViewNomothesia.model();
                      up+=7
                      for i in range(mymodel.rowCount()):
                        composerLabel_Nomosthesia = QgsComposerLabel(c)
                        composerLabel_Nomosthesia.setText(mymodel.data(mymodel.index(i, 2)))
                        composerLabel_Nomosthesia.setFont(QFont("Times", 10))
                        composerLabel_Nomosthesia.setHAlign(Qt.AlignHCenter)
                        composerLabel_Nomosthesia.setVAlign(Qt.AlignVCenter)
                        composerLabel_Nomosthesia.setItemPosition(7,up,50,7)
                        composerLabel_Nomosthesia.setFrameEnabled(True)   
                        composerLabel_Nomosthesia.setFrameOutlineWidth(0.1)
                        
                        
                        composerLabel_Details = QgsComposerLabel(c)
                        composerLabel_Details = QgsComposerLabel(c)
                        details=mymodel.data(mymodel.index(i, 7))
                        if type(details)==QPyNullVariant:
                            details = '-'
                        composerLabel_Details.setText(details)
                        composerLabel_Details.setHAlign(Qt.AlignHCenter)
                        composerLabel_Details.setVAlign(Qt.AlignVCenter)
                        composerLabel_Details.setItemPosition(57,up,70,7)
                        composerLabel_Details.setFrameEnabled(True)   
                        composerLabel_Details.setFrameOutlineWidth(0.1)
                        
                        c.addItem(composerLabel_Nomosthesia)
                        c.addItem(composerLabel_Details)
                        up+=7    
                      
                      
                      printer = QPrinter()
                      printer.setOutputFormat(QPrinter.PdfFormat)
                      printer.setOutputFileName(filename)
                      printer.setPaperSize(QSizeF(c.paperWidth(), c.paperHeight()), QPrinter.Millimeter)
                      printer.setFullPage(True)
                      printer.setColorMode(QPrinter.Color)
                      printer.setResolution(c.printResolution())
                
                      pdfPainter = QPainter(printer)
                      paperRectMM = printer.pageRect(QPrinter.Millimeter)
                      paperRectPixel = printer.pageRect(QPrinter.DevicePixel)
                      c.render(pdfPainter, paperRectPixel, paperRectMM)
                      
                      pdfPainter.end()
                      QApplication.restoreOverrideCursor()
                      QMessageBox.information(self.dlg, u"Ενημέρωση",u"Η εξαγωγή της αναφοράς ολοκληρώθηκε!")

              except IndexError:
                  QMessageBox.information(None,u"Ενημέρωση!",u"Επιλέξτε οικισμό από την αντίστοιχη λίστα!")
                  return
             


  def zoomToOrio(self):
      """zoom to orio"""
      try:

          self.layers = self.iface.mapCanvas().layers()
          self.layerOrio=self.getlayerbyName(self.layers,self.postgislayers.get('vworiaoikismon')[1])
          self.iface.setActiveLayer(self.layerOrio) 
            
          tableviewindex = self.dlg.ui.tableViewNomothesia.selectionModel().selection()#μπορεί να υπάρχουν πολλές επιλογές/indexes
          myindex = self.dlg.proxyModelNomothesia.index(tableviewindex.indexes()[0].row(),10) 
          idnom = str(self.dlg.proxyModelNomothesia.data(self.dlg.proxyModelNomothesia.index(myindex.row(),10),0))

          self.zoomTo(self.layerOrio, "idnom", idnom)

      except IndexError:
           QMessageBox.information(None,u"Ενημέρωση!",u"Παρακαλώ επιλέξτε νομοθεσία")


    
  def zoomToOikismoi(self, myview, mymodel, layername, searchfield):
      try:

        self.layers = self.iface.mapCanvas().layers()
        self.layerOikismoi=self.getlayerbyName(self.layers,self.postgislayers.get(layername)[1])
        self.iface.setActiveLayer(self.layerOikismoi) 
         

         
        listviewindex =myview.selectionModel().selection()
        myindex = mymodel.index(listviewindex.indexes()[0].row(),6) #6= index of column KODIKOS in model
        KODIKOS = mymodel.data(myindex,0)
        
        self.zoomTo(self.layerOikismoi, searchfield, KODIKOS)


      except IndexError:
          QMessageBox.information(None,u"Ενημέρωση!",u"Παρακαλώ επιλέξτε έναν οικισμό από την αντίστοιχη λίστα")


  
  def zoomTo(self, layer, searchfield, value):
      try:
        self.it = layer.getFeatures( QgsFeatureRequest().setFilterExpression ( u'"%s" = \'%s\'' % (searchfield,str(value)) ) )
        print u'"%s" = \'%s\'' % (searchfield,str(value)) 
        
        if len(list(self.it) )==0:
            QMessageBox.information(None,u"Ενημέρωση!",u"Δεν βρέθηκε το αντικείμενο στο θεματικό επίπεδο:%s!" %layer.name())
            return
            
        del self.it
        self.it = layer.getFeatures( QgsFeatureRequest().setFilterExpression (u'"%s" = \'%s\'' % (searchfield,str(value)) ) )     
        
        layer.setSelectedFeatures( [ f.id() for f in self.it ] )
        self.canvas.zoomToSelected()
      except AttributeError:
          QMessageBox.information(None,u"Ενημέρωση!",u"Δεν βρέθηκε το απαραίτητο θεματικό επίπεδο ή δεν είναι ενεργό")
    
  def AddVectorLayer(self, layername):
      self.layers = self.iface.mapCanvas().layers()#get all layers in mapcanvas
      
      self.layerexist=self.getlayerbyName(self.layers , self.postgislayers.get(layername)[1]) #check if layer already exist
     
      if self.layerexist:
          
          #if layer already exist, msgbox and exit
          reply = QMessageBox.question(None,  u'Ερώτηση',  u"Το θεματικό επίπεδο %s υπάρχει ήδη. \n Να προστεθεί;" %self.postgislayers.get(layername)[1],  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    
          
          if reply == QMessageBox.Yes:
              pass
          else:
              return
      #else add postgis layer and assign some style to oikismoi
      vlayer= self.AddPostgisLayer(layername, self.postgislayers.get(layername)[0], self.postgislayers.get(layername)[1], self.postgislayers.get(layername)[2])

      if vlayer.name() == u"Οικισμοί":
          oikismoi = {
                          '1': ('#f00', u'Παραδοσιακοί οικισμοί στο Αιγαίο'),
                           '0': ('#0f0', u'Οικισμοί')
                         }
           # create a category for each item in animals
          categories = []
          for typos, (color, label) in oikismoi.items():
                    symbol = QgsSymbolV2.defaultSymbol(vlayer.geometryType())
                    symbol.setColor(QColor(color))
                    category = QgsRendererCategoryV2(typos, symbol, label)
                    categories.append(category)
                
                # create the renderer and assign it to a layer
          field = 'PARADOSIAKOS' # field name
          renderer = QgsCategorizedSymbolRendererV2(field, categories)
          vlayer.setRendererV2(renderer)
          
          #Finally add layer to map and toc    
      QgsMapLayerRegistry.instance().addMapLayer(vlayer, True)
      self.iface.mapCanvas().refresh()

                  ###
              

  def AddPostgisLayer(self, tablename, geometrycolumn,layername, keycolumn ):
      """Adds postgis layers """
                  #if not exist, add it
      uri = QgsDataSourceURI()
      # set host name, port, database name, username and password
      uri.setConnection(self.host, str(self.port), self.dbname, self.username,self.password)
       # set database schema, table name, geometry column and optionaly
        # subset (WHERE clause)

      uri.setDataSource(self.schema, tablename, geometrycolumn,'', str(keycolumn))
        
      vlayer = QgsVectorLayer(uri.uri(), layername, "postgres")
      return vlayer
    
  def AddWMSLayer(self):
      """Adds WMS layers """
      uri = QgsDataSourceURI()
      #uri = "http://gis.ktimanet.gr/wms/wmsopen/wmsserver.aspx"
      self.urlwithParams='crs=EPSG:4326&dpiMode=7&featureCount=10&format=image/jpeg&layers=KTBASEMAP&styles=&url=http://gis.ktimanet.gr/wms/wmsopen/wmsserver.aspx'

      rlayer = QgsRasterLayer(self.urlwithParams, u"Ορθοφωτοχάρτες (Εθνικό κτηματολόγιο)", "wms")
      if not rlayer.isValid():
        print "Layer failed to load!"
        QMessageBox.information(None,u"Ενημέρωση!",u"Η προσθήκη του θεματικού επιπέδου απέτυχε")
      QgsMapLayerRegistry.instance().addMapLayer(rlayer, True)
      self.iface.mapCanvas().refresh()
      return rlayer


  def getlayerbyName(self,layers, name):
    """Pass a list with all mapcanvas layers, return a layer or None if not found """
    for layer in layers:
        if layer.name()==name:
            return layer



######################################init##############################################
  def initGui(self):  
    # Create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/paradosiakoioikismoi/icons/icon.png"),  u"Φόρμα αναζήτησης παραδοσιακών οικισμών", self.iface.mainWindow())
    self.action2 = QAction(QIcon(":/plugins/paradosiakoioikismoi/icons/icon3.png"),  u"Φόρμα αναζήτησης με βάση την νομοθεσία", self.iface.mainWindow())

    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("activated()"), self.run) 
    QObject.connect(self.action2, SIGNAL("activated()"), self.runNomothesia) 
    
    
    self.iface.addPluginToMenu(u"Παραδοσιακοί οικισμοί",self.action)
    self.iface.addPluginToMenu(u"Παραδοσιακοί οικισμοί",self.action2)
    
    
    

     # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addToolBarIcon(self.action2)

    
    #some useful objects
    self.canvas = self.iface.mapCanvas()
    

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu(u"Παραδοσιακοί οικισμοί",self.action)
    self.iface.removePluginMenu(u"Παραδοσιακοί οικισμοί",self.action2)
    self.iface.removeToolBarIcon(self.action)
    self.iface.removeToolBarIcon(self.action2)

  # open form paradosiakoi oikismoi
  def run(self): 
    # create and show the dialog 
    self.dlg = paradosiakoioikismoiDialog()
    
    
    self.dlg.setFocus(True)
    self.dlg.activateWindow()
    self.dlg.setStyle(QStyleFactory.create("plastique"))
    #settrace()
    self.dlg.show()
    
    
    #toolbar signals and slots
    self.dlg.ui.actionZoomOikismos.triggered.connect(lambda: self.zoomToOikismoi(self.dlg.ui.listViewOikismoi,self.dlg.proxyModeloikismoi, 'vwoikismoi', "ELSTATID"))
    self.dlg.ui.actionZoomOrio.triggered.connect(self.zoomToOrio)

    #menu signals and slots
    self.dlg.ui.mapper = QSignalMapper()
    self.dlg.ui.mapper.setMapping(self.dlg.ui.actionAddOikismoi, 'vwoikismoi')
    self.dlg.ui.mapper.setMapping(self.dlg.ui.actionAddOria, 'vworiaoikismon')
    
    self.dlg.ui.actionAddOikismoi.triggered.connect(self.dlg.ui.mapper.map)    
    self.dlg.ui.actionAddOria.triggered.connect(self.dlg.ui.mapper.map)
    
    self.dlg.ui.actionKtima.triggered.connect(self.AddWMSLayer)
    
    self.dlg.ui.mapper.mapped['QString'].connect(self.AddVectorLayer)
    
    self.dlg.ui.actionReport.triggered.connect(self.generateReport)
    
    
  # open form nomothesia
  def runNomothesia(self): 
    # create and show the dialog 
    self.dlgnomo = NomothesiaDialog()
    self.dlgnomo.setFocus(True)
    self.dlgnomo.activateWindow()
    self.dlgnomo.setStyle(QStyleFactory.create("plastique"))

    self.dlgnomo.show()
    
    #toolbar signals and slots
    self.dlgnomo.ui.actionZoomOikismos.triggered.connect(lambda: self.zoomToOikismoi(self.dlgnomo.ui.tableViewOikismoi, self.dlgnomo.proxyModeloikismoi,'vwoikismoi', "ELSTATID"))


  #==============================================================================================================================         
  def read(self):
    """Reads Settings for database and ftp"""
    self.dbdriver = self.config.get('postgresql', 'dbdriver')
    self.host = self.config.get('postgresql', 'host')
    
    self.port = int(self.config.get('postgresql', 'port'))
    self.schema = self.config.get('postgresql', 'schema')
    self.dbname = self.config.get('postgresql', 'dbname')
    self.username = self.config.get('postgresql', 'username')
    self.password = self.config.get('postgresql', 'password')
    self.ftp_host=self.config.get('ftp', 'ftp_host')
    self.ftp_user=self.config.get('ftp', 'ftp_user')
    self.ftp_password=self.config.get('ftp', 'ftp_password')
    
    self.pdfdir=tempfile.gettempdir()  #get temp directory
  #==============================================================================================================================     

