# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_SearchByNomothesia.ui'
#
# Created: Mon Apr 14 18:53:38 2014
#      by: PyQt4 UI code generator 4.10.4-snapshot-f62fabcefe39
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(996, 639)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.tableViewOikismoi = QtGui.QTableView(self.groupBox)
        self.tableViewOikismoi.setObjectName(_fromUtf8("tableViewOikismoi"))
        self.verticalLayout_4.addWidget(self.tableViewOikismoi)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 996, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_5 = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidget_5.sizePolicy().hasHeightForWidth())
        self.dockWidget_5.setSizePolicy(sizePolicy)
        self.dockWidget_5.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.dockWidget_5.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.dockWidget_5.setObjectName(_fromUtf8("dockWidget_5"))
        self.dockWidgetContents_5 = QtGui.QWidget()
        self.dockWidgetContents_5.setObjectName(_fromUtf8("dockWidgetContents_5"))
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents_5)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.dockWidgetContents_5)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.lineEdit = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout_3.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.tableViewNomothesia = QtGui.QTableView(self.groupBox_2)
        self.tableViewNomothesia.setObjectName(_fromUtf8("tableViewNomothesia"))
        self.gridLayout_3.addWidget(self.tableViewNomothesia, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(500, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.dockWidget_5.setWidget(self.dockWidgetContents_5)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_5)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionFek = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/paradosiakoioikismoi/icons/product-sales-report-icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFek.setIcon(icon)
        self.actionFek.setObjectName(_fromUtf8("actionFek"))
        self.actionZoomOikismos = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/paradosiakoioikismoi/icons/1394568050_Zoom.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoomOikismos.setIcon(icon1)
        self.actionZoomOikismos.setObjectName(_fromUtf8("actionZoomOikismos"))
        self.toolBar.addAction(self.actionZoomOikismos)
        self.toolBar.addAction(self.actionFek)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Αναζήτηση με βάση την νομοθεσία", None))
        self.groupBox.setTitle(_translate("MainWindow", "Παραδοσιακοί οικισμοί", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Αναζήτηση νομοθεσίας", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionFek.setText(_translate("MainWindow", "Προβολή υλικού τεκμηρίωσης", None))
        self.actionFek.setToolTip(_translate("MainWindow", "Προβολή υλικού τεκμηρίωσης", None))
        self.actionZoomOikismos.setText(_translate("MainWindow", "Επιλογή και εστίαση στον οικισμό", None))

import resources_rc
