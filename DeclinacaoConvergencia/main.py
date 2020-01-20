# -*- coding: utf-8 -*-
from qgis.PyQt.QtWidgets import QAction, QToolButton, QMenu, QMessageBox
from qgis.PyQt.QtGui import QIcon
from qgis.core import *
from qgis.gui import *
from .icons import resources_rc
from .UI.interface import Interface
from ..auxiliar.auxDeclConv import AuxiliarDeclConv

import math

class Main:
    def __init__(self, iface):
        '''Construtor'''
        self.iface = iface
        self.isOpen = False

    def initGui(self):
        #CRIAR ACTIONS
        
        #INICIAR VARIÁEIS E SINAIS
        self.initVariables()
        self.initSignals()
        self.openWindow()
        self.isOpen = False
        
    def unload(self):
#        del self.toolbar
        pass
       
    def initVariables(self):
        self.msgBox = QMessageBox()
        self.canvas = self.iface.mapCanvas()
        self.auxiliar = AuxiliarDeclConv(self.iface)
        self.dockWindow = Interface(self.canvas, self.auxiliar)

    def initSignals(self):
        self.dockWindow.closeEvent = self.closeDock
    
    def initPlugin(self):
        pass
    
    def openWindow(self):
        if self.isOpen == False:
            self.iface.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWindow)
            self.isOpen = True
            
    def closeDock(self, e):
        self.dockWindow.ativarButton.setChecked(False)
        del self.dockWindow
        self.isOpen = False

        # vertex_items = [ i for i in self.iface.mapCanvas().scene().items() if issubclass(type(i), QgsVertexMarker)]
        # for ver in vertex_items:
        #     if ver in self.iface.mapCanvas().scene().items():
        #         self.iface.mapCanvas().scene().removeItem(ver)

    
    def gerarGMS(self, ang):
        xg = format( math.modf( ang )[1], '.0f' )
        
        sign = -1 if ang < 0 else 1
        
        xm = format( sign * math.modf( math.modf( ang )[0] * 60 )[1], '.0f' )
        xs = format( sign * math.modf( math.modf( ang )[0] * 60 )[0] * 60, '.3f' )
        
        gms = str(xg) + "° " + str(xm) + u"' " + str(xs) + u'"'
        
        return gms
    
    def closeWindow(self, e):
        pass

    def showMessage(self, text):
        self.msgBox.setIcon(QMessageBox.Critical)
        self.msgBox.setWindowTitle("Erro")
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.setText(text)
        self.msgBox.exec_()
            
    def closeMsgBox(self, b):
        self.msgBox.close()
        
    