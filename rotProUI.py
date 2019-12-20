"""
Rotate Spherical and Cylindrical Projections
Created by Charles Kinter
Email Charles@kinters.net
"""


import pymel.core as pm
from pymel.all import *
import types 

def rotProUI():
    """
        install:
        Place rotProUI.py in your C:\Users\(your user)\Documents\maya\scripts folder


        Usage:
        1. In script editor run (can be added to shelf):
            import rotProUI
            rotProUI()
        2. Select Object or faces
        3. Select projection type from dropdown
        4. Select rotation type
        5. Click project
            
        
    """
    projectionList = ['Cylindrical','Spherical']
    rotationDict = {'90 X':('x',90),'45 X':('x',45),'-90 X':('x',-90),'-45 X':('x',-45),'90 Y':('y',90),'45 Y':('y',45),'-90 Y':('y',-90),'-45 y':('y',-45),'90 Z':('z',90),'45 Z':('z',45),'-90 Z':('z',-90),'-45 Z':('z',-45)}
    rotProWin = pm.window(title='Rotate Projection Tool')
    rotProWinlayout = pm.columnLayout()
    rotProWintitle = pm.text(label ='Please select the type of Projection \n and the RotationType.')
    rotProMenu = pm.optionMenu('rotProMenu2')
    menusorted = rotationDict.keys()
    print menusorted
    menusorted.sort()
    for option in projectionList:
        pm.menuItem( label=option)
    radio = pm.rowColumnLayout(nc = 3)
    rotTypeMenuRadio = pm.radioCollection()
    for option in menusorted:
        pm.radioButton(label=option)    
    SubmitButton = pm.button(label ='Project',c = Callback(RotPro,rotProMenu,rotTypeMenuRadio,rotationDict))
    close = pm.button(label='Close', command=('pm.deleteUI(\"' +rotProWin + '\", window=True)') )
    pm.showWindow(rotProWin)

def RotPro(menu1,menu2,rotationDict,*args):
    print 'ran'
    buttons = pm.radioCollection(menu2,q=True,sl=True)
    rtype = pm.radioButton(buttons,q=True,label=True)
    type = menu1.getValue()
    axis = rotationDict[rtype][0]
    mod = rotationDict[rtype][1]
    print type,axis,mod
    modx = 0
    mody = 0
    modz = 0
    faces =''
    rotationamount = mod
    if axis == 'x':
        modx = rotationamount
        print 'modx',modx
    if axis == 'y':    
        mody = rotationamount
    if axis == 'z':
        modz = rotationamount
    selected = pm.ls(sl=True)
   
    if (len(selected) < 1):
        pm.informBox(title='Object Selection Error', message='Please Select a Single Object', ok='Ok' )
        return
    try:
        shape = selected[0].getChildren()
        faces =shape[0].f[0:]
    except:
            try:
                faces = selected
            except:
                pm.informBox(title='Object Selection Error', message='Please Select a valid Object', ok='Ok' )
                return
    
    projection = pm.polyProjection(faces,rx = modx, ry = mody, rz = modz, type=type,ibd=True,sf=True)[0]
    print projection
    pm.select(d=True)
    pm.select(projection, r=True)
    pm.setToolTo('ShowManips')
    pm.showManipCtx()
    pm.ShowManipulators()
    

rotProUI()
