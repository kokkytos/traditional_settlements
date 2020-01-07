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
 This script initializes the plugin, making it known to QGIS.
"""
def name(): 
  return "paradosiakoi oikismoi" 
def description():
  return "paradosiakoi oikismoi aigaiou"
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "1.0"
def classFactory(iface): 
  # load paradosiakoioikismoi class from file paradosiakoioikismoi
  from paradosiakoioikismoi import paradosiakoioikismoi 
  return paradosiakoioikismoi(iface)
