# -*- coding: utf-8 -*-
'''
/***************************************************************************
 DSGTools Op
                                 A QGIS plugin
 Ferramentas para planejamento militar do Exército Brasileiro
                             -------------------
        begin                : 2017-01-01
        copyright            : (C) 2017 by Diego Benincasa
        email                : benincasa.diego@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
'''

from qgis.PyQt.QtCore import Qt
from qgis.PyQt import QtGui, QtCore
import os, sys
from qgis.utils import iface
from qgis.core import QgsMapLayer, QgsProject
from qgis.PyQt.QtWidgets import QToolBar, QAction, QMessageBox, QMenu
from qgis.PyQt.QtGui import QIcon

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'auxiliar'))

class DSGToolsOp:
	def __init__(self, iface):
		self.iface = iface
		self.actions = []
    	
	def initGui(self):
        #CRIAR ACTIONS
        
        #INICIAR VARIÁVEIS E SINAIS
		self.initVariables()
		self.loadTools()
        
	def initPlugin(self):
		pass
        
	def initVariables(self):
		self.menuBar = self.iface.mainWindow().menuBar()
		self.dsgToolsOp = QMenu(self.iface.mainWindow())
		self.dsgToolsOp.setObjectName(u'DSGToolsOp')
		self.dsgToolsOp.setTitle('Ferramentas Militares')
		self.fieldToolbox = None
		self.menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.dsgToolsOp)
        
	def unload(self):
		for action in self.actions:
			self.iface.removePluginMenu(
				u'DSGTools Op',
				action)

		if self.dsgToolsOp is not None:
			self.menuBar.removeAction(self.dsgToolsOp.menuAction())
		del self.dsgToolsOp

	def add_action(self,
				icon_path,
				text,
				callback,
				enabled_flag=True,
				add_to_menu=True,
				add_to_toolbar=True,
				status_tip=None,
				whats_this=None,
				parent=None):
        
		icon = QIcon(icon_path)
		action = QAction(icon, text, parent)
		action.triggered.connect(callback)
		action.setEnabled(enabled_flag)

		if status_tip is not None:
			action.setStatusTip(status_tip)

		if whats_this is not None:
			action.setWhatsThis(whats_this)

		if add_to_toolbar:
			self.toolbar.addAction(action)

		if add_to_menu:
			self.iface.addPluginToMenu(
				self.menu,
				action)

		self.actions.append(action)

		return action

	def loadTools(self):
		pass
		action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'dimensionsvf.png'),
			text=u'Calculadora de Coordenadas e Dimensões',
			callback=self.loadVirtualFieldGenerator,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.dsgToolsOp.addAction(action)
        
		self.auc_action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'convang.png'),
			text=u'Conversor de unidades angulares',
			callback=self.loadAngleUnitConverter,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.dsgToolsOp.addAction(self.auc_action)

		self.nd_action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'numericalvertexedit.png'),
			text=u'Criação de pontos por coordenadas',
			callback=self.loadNumericalDigitize,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.dsgToolsOp.addAction(self.nd_action)

		self.dec_action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'declconv.png'),
			text=u'Declinação magnética e convergência meridiana',
			callback=self.loadDeclinacaoConvergencia,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.dsgToolsOp.addAction(self.dec_action)
		from .DeclinacaoConvergencia.main import Main as Main_DecConv
		self.mainDecConv = Main_DecConv(iface)
        
		self.geo_action = self.add_action(
		 	os.path.join(os.path.dirname(__file__), 'icons', 'geocoder.png'),
		 	text=u'Geocodificação',
		 	callback=self.loadGeocoding,
		 	parent=self.dsgToolsOp,
		 	add_to_menu=False,
		 	add_to_toolbar=False)
		self.dsgToolsOp.addAction(self.geo_action)
		from .QuickGeocoder.geocoder import QuickGeocoder as Main_Geocoding
		self.mainGeocoding = Main_Geocoding(iface)
        
		# self.az_action = self.add_action(
		# 	os.path.join(os.path.dirname(__file__), 'icons', 'azimuth.png'),
		# 	text=u'Gerador de Azimutes e Distâncias',
		# 	callback=self.loadGeradorAzimutesDistancias,
		# 	parent=self.dsgToolsOp,
		# 	add_to_menu=False,
		# 	add_to_toolbar=False)
		# self.az_action.setCheckable(True)
		# self.dsgToolsOp.addAction(self.az_action)
		# from .GeradorAzimuteDistancia.main import Main as Main_Azimutes
		# self.mainAzimutes = Main_Azimutes(iface)
        
		# self.mi_action = self.add_action(
		# 	os.path.join(os.path.dirname(__file__), 'icons', 'militarySimbology.png'),
		# 	text=u'Localizar carta topográfca (MI) por ponto',
		# 	callback=self.loadDeterminarMI,
		# 	parent=self.dsgToolsOp,
		# 	add_to_menu=False,
		# 	add_to_toolbar=False)
		# self.dsgToolsOp.addAction(self.mi_action)
		# from .DeterminarMI.main import Main as Main_MI
		# self.mainMI = Main_MI(iface)
        
		self.miA_action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'findmiarea.png'),
			text=u"Localizar carta topográfca (MI) por região",
			callback=self.loadDeterminarMIArea,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.dsgToolsOp.addAction(self.miA_action)
		from .DeterminarMIArea.main import Main as Main_MIArea
		self.mainMIArea = Main_MIArea(iface)
        
		self.mt_action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'measuretool.png'),
			text=u'Medição durante aquisição vetorial',
			callback=self.loadMeasureTool,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.mt_action.setCheckable(True)
		self.dsgToolsOp.addAction(self.mt_action)
		from .measureTool.measureTool import MeasureTool as Main_MeasureTool
		self.mainMeasureTool = Main_MeasureTool(iface)
        
		self.mv_action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'numericalvertexedit.png'),
			text=u'Mover pontos por coordenadas',
			callback=self.loadMoveVertex,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.dsgToolsOp.addAction(self.mv_action)
        
		self.ms_action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'militarySimbology.png'),
			text=u'Simbologia Militar',
			callback=self.loadMilitarySimbologyDock,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.dsgToolsOp.addAction(self.ms_action)

		self.pt_action = self.add_action(
			os.path.join(os.path.dirname(__file__), 'icons', 'profileIcon.png'),
			text=u'Traçar perfil do terreno',
			callback=self.loadProfileTool,
			parent=self.dsgToolsOp,
			add_to_menu=False,
			add_to_toolbar=False)
		self.dsgToolsOp.addAction(self.pt_action)
		from .ProfileTool.profileplugin import ProfilePlugin as Main_ProfileTool
		self.mainProfileTool = Main_ProfileTool(iface)
        
	def loadDeterminarMI(self):
		"""
		Finds topographic chart MI that contains a user-clicked point
		"""
		if self.mainMI.isOpen == False:
			self.mainMI.initGui()

	def loadDeterminarMIArea(self):
		"""
        Finds topographic chart MI that contains a user-defined box
        """
		if self.mainMIArea.isOpen == False:
			self.mainMIArea.initGui()
    
	def loadMoveVertex(self):
		"""
        Moves points to a new user-input location
        """
		from .numericalVertexEdit.numericalvertexedit import NumericalVertexEdit as Main_MoveVertex
		self.mainMoveVertex = Main_MoveVertex(iface)
		self.mainMoveVertex.initGui()
		self.mainMoveVertex.run()
        
	def loadNumericalDigitize(self):
		"""
        Creates points by user input of coordinates
        """
		from .numericalDigitize.numericalDigitize import NumericalDigitize as Main_NumericalDigitize
		self.mainNumericalDigitize = Main_NumericalDigitize(iface)
		self.mainNumericalDigitize.initGui()
		self.mainNumericalDigitize.run()
    
	def loadDeclinacaoConvergencia(self):
		"""
        Show magnetic heading and geographic convergence dockable window
        """
		if self.mainDecConv.isOpen == False:
			self.mainDecConv.initGui()
    
	def loadAngleUnitConverter(self):
		"""
        Show angle unit converter dialog
        """
		from .AngleUnitConverter.main import Main
		main = Main(iface)
		main.executePlugin()

	def loadGeocoding(self):
		"""
        Show geocoding dock widget
        """
		if self.mainGeocoding.pluginIsActive == False:
			self.mainGeocoding.run()

	def loadGeradorAzimutesDistancias(self):
		"""
        Add icons to toolbar for generating azimuths and distances
        """
        
		if self.az_action.isChecked():
			self.mainAzimutes.initGui()
		else:
			self.mainAzimutes.unload()
            
	def loadMeasureTool(self):
		"""
        Add icons to toolbar for measuring features during their acquisition
        """
        
		if self.mt_action.isChecked():
			self.mainMeasureTool.initGui()
		else:
			self.mainMeasureTool.unload()
        
	def loadProfileTool(self):
		"""
        Generates a terrain profile
        """
		hasRaster = False
		for l in QgsProject.instance().mapLayers().values():
			if l.type() == QgsMapLayer.RasterLayer:
				hasRaster = True
				break
        
		if hasRaster == False:
			msgBox = QMessageBox(QMessageBox.Information, u"Informação", u"Não há camadas raster para traçar o perfil.", QMessageBox.Ok)
			msgBox.exec_()
			return
        
		if self.mainProfileTool.dockOpened == False:
			self.mainProfileTool.run()
        
	def loadVirtualFieldGenerator(self):
		"""
        Show virtual field generator dialog
        """
		from .VirtualFieldGenerator.virtualFieldGenerator import VirtualFieldGenerator
		dialogVFG = VirtualFieldGenerator(iface)
		dialogVFG.exec_()
    
	def loadMilitarySimbologyDock(self):
		"""
        Shows the Military Simbology Dock
        """
		from .MilitarySimbologyTools.main import Main
		main = Main()
		dlg = main.getFrame()
		dlg.setGeometry(700, 500, 100, 50)
		if dlg:
			dlg.show()

	def showFiringRangeTool(self):
		"""
        Show sthe convert database dialog
        """
		from .FiringRangeTools.firingRangeDialog import FiringRangeDialog
		dlg = FiringRangeDialog(self.iface)
		dlg.show()
		result = dlg.exec_()
		if result:
			pass
