# From video 16 Create Property Group & Enumerator (Panel)

# 2021-04-18 It works with several runs, each run has a different prefix
# Problem is that when I assign the materials to the newest run,
# it applies it to the older ones, which prevents mixed color scheme runs...

# Change emission_mat to an array of materials, and add a new set of materials
# for each consecutive level.
# With only one level, pretty much no difference!
# Save this one as 2021_04_18_chryzoid_chryzode_panel_before_mat_array_change.py
# Now called 2021_04_18_chryzoid_chryzode_panel.py
# It did not work.
# A better idea: give the lines a second prefix that denotes the color scheme
# and give them their colors accordingly, using only ONE palette!
# 2021-04-21 Now it works with selecting a ref line...
 
# 2021-04-23 tried to install as an addon with the bl_info below, and I got this message:

#  File "C:\Users\jpbjp\AppData\Roaming\Blender Foundation\Blender\2.92\scripts\addons\2021_04_18_chryzoid_chryzode_panel.py", line 272, in chryzoid_operator
#    mats = bpy.data.materials
#AttributeError: '_RestrictData' object has no attribute 'materials'

import bpy
import time
from datetime import datetime
from math import sin, cos, tau, sqrt, atan2, radians
import random
import pprint
import os
from bpy.props import *

# Addon info
bl_info = {
    "name": "Chryzoid UI",
    "author": "JPB",
    "description": "The Blender Chryzoid!",
    "version": "1,0,0",
    "location":"Properties > Materials > The Blender Chryzoid",
    "category": "material",
    "support": "COMMUNITY",
    "blender": (2,92,0)
    }
    
timenow = time.time()

# moved declaration of radius and thickness ratio to top 
radius = 100 # The radius of the circle the points will sit on
radius2ThicknessRatio = 5000
#levelsLogForMaterials = [] # doChryzoid will fill this array to indicate the levels

os.system("cls")
print("-----> 30 time", timenow)
#### START OF REFLINE PROPERTIES
class RefLineProperties(bpy.types.PropertyGroup):
    refLineEnum : bpy.props.EnumProperty(
            name =          "",
            description =   "Pick the Reference Line",
            items =         [   ('ReferenceLine1', "ReferenceLine1", ""),
                                ('ReferenceLine2', "ReferenceLine2", ""),
                                ('ReferenceLine3', "ReferenceLine3", "")
                            ]
        )
#### END OF REFLINE PROPERTIES

#### START OF CLEARLINES PROPERTIES
class ClearLinesProperties(bpy.types.PropertyGroup):
    clearLinesBool : bpy.props.BoolProperty(
            name =  "",
            description="Delete the Existing Lines",
            default = True
            )
#### END OF CLEARLINES PROPERTIES

#### START OF COLORMODE PROPERTIES
class ColorModeProperties(bpy.types.PropertyGroup):
    colorModeEnum : bpy.props.EnumProperty(
            name =          "",
            description =   "Pick the Color Mode",
            items =         [   ('ONE', "ONE", ""),
                                ('RANDOM', "RANDOM", ""),
                                ('SERIAL', "SERIAL", ""),
                                ('LEVEL', "LEVEL", ""),
                                ('LEVEL_SERIAL', "LEVEL_SERIAL", ""),
                                ('POINT', "POINT", "")
                            ]
        )
#### END OF COLORMODE PROPERTIES

#### START OF CHRYZOID PROPERTIES
class ChryzoidProperties(bpy.types.PropertyGroup):
    title :         bpy.props.StringProperty(name="Chryzoid Title")
    numberFrom :    bpy.props.IntProperty(name="", default = 3, min = 3)    
    numberTo :      bpy.props.IntProperty(name="", default = 4, min = 4)    
    skip :          bpy.props.IntProperty(name="", default = 1, min = 1)
    z :             bpy.props.FloatProperty(name="", default = -.05)
    pos_z :         bpy.props.BoolProperty(
                                    name =  "",
                                    description="Use Positive Z",
                                    default = False
                    )
#### END OF CHRYZOID PROPERTIES
    
#### START OF CHRYZODE PROPERTIES
class ChryzodeProperties(bpy.types.PropertyGroup):
    title :         bpy.props.StringProperty(name="Chryzode Title")
    numPoints :     bpy.props.IntProperty(name="", default = 17, min = 3)    
    multiplier :    bpy.props.IntProperty(name="", default = 5, min = 4)
#### END OF CHRYZODE PROPERTIES
    
    
class ChryzoidPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label =          "Chryzoid " + str(abs(round((timenow - round(timenow))*500)))
    bl_idname =         "SCENE_PT_chryzoid"
    bl_space_type =     'VIEW_3D'
    bl_region_type =    'UI'
    bl_category =       "Chryzoid"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        # below: x = y; x is a name YOU choose; y 
        refline_props = scene.refline_properties
        colorMode_props = scene.colorMode_properties
        clearLines_props = scene.clearLines_properties
        chryzoid_props = scene.chryzoid_properties
        chryzode_props = scene.chryzode_properties
        layout.scale_y = 1
        layout.prop(context.scene, "prop")
        row = layout.row()
        row = layout.row()
#        layout.label(text="Pick Ref Line below", icon="IPO_EASE_IN_OUT")
#        row = layout.row(align=True)
#        sub = row.row(align=True)
#        sub.prop(refline_props, "refLineEnum")
        layout.label(text="Pick Color Mode below", icon="EVENT_C")
        row = layout.row(align=True)
        sub = row.row(align=True)
        sub.prop(colorMode_props, "colorModeEnum")
        
        row = layout.row()
        row = layout.row()
        
        split = layout.split()
        # First column
#        col = split.column()
#        sub = col.row()
#        sub.scale_x = 0.1
        
        col = split.column(align = True)
        sub = col.row()
        sub.prop(clearLines_props, "clearLinesBool")
        sub.label(text="Delete Old Lines Before Run", icon="CANCEL")

        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        split = layout.split(factor=.0001)
        col = split.column(align=True)
        #split.label(text="", icon="EVENT_Z")
        split.label(text="Pos Z")
        #col = split.column(align=True)
        split.prop(chryzoid_props, "pos_z")
        split.prop(chryzoid_props, "z")

        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.label(text="Chryzoid")
        row.scale_y = 1
        
        # Create 3 columns, by using a split layout.
        split = layout.split()
        # First column
        col = split.column(align=True)
        sub = col.row()
        col.label(text="From:", icon="EVENT_F")
        col.prop(chryzoid_props, "numberFrom")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="To:", icon="EVENT_T")
        col.prop(chryzoid_props, "numberTo")

        # 3rd column, aligned
        col = split.column(align=True)
        col.label(text="Skip:", icon="EVENT_S")
        col.prop(chryzoid_props, "skip")
        
        row = layout.row(align=True)
        row.scale_y = 1
        row = layout.row()
        row.operator("chryzoid.operator", text="Run Chryzoid")
        
        # Do layout for chryzode
        row = layout.row()
        row = layout.row()
        row = layout.row()
        row.operator("chryzo2.operator", text="Delete Lines")
        row = layout.row()
        row = layout.row()
        row.operator("chryzo3.operator", text="Build New Ref Line")
        
        row = layout.row()
        row.label(text="Chryzode")
        
        # Create two columns, by using a split layout.
        split = layout.split()

        # First column
        col = split.column(align=True)
        sub = col.row()
        col.label(text="# of Points", icon="EVENT_N")
        col.prop(chryzode_props, "numPoints")

        # Second column, aligned
        col = split.column(align=True)
        col.label(text="Multiplier", icon="EVENT_M")
        col.prop(chryzode_props, "multiplier")
        row = layout.row()
        row = layout.row()
        row.operator("chryzo.operator", text="Run Chryzode")
       
def items_prop(self, context):
    return [(ob.name, ob.name, "") for ob in context.scene.objects if (ob.name.find("ReferenceLine") != -1)]


def update_prop(self, context):
    # I don't seem to need to do anything here anymore
    return

# moved this function (view3d_find) to outside this class
#### START OF VIEW3D FIND FUNCTION
#def view3d_find(self, context, return_area = False ):
def view3d_find(context, return_area = False ):
    # returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    if return_area: return region, rv3d, v3d, area
                    return region, rv3d, v3d
    return None, None
#### END OF VIEW3D FIND FUNCTION

class chryzoid_operator(bpy.types.Operator):
    bl_label = "Operator"
    bl_idname = "chryzoid.operator"

##### Here I copy all the code from the F3 chryzoid...
    showColMats = False # for debug: show colors and materials
    # emission_mat = [] # commented this declaration out
    lineNr = 0
    
#    radius = 100 # The radius of the circle the points will sit on
#    radius2ThicknessRatio = 5000 # moved declaration of radius and thickness ratio to top
    mats = bpy.data.materials
    numPoints = 7 # The number of points to be distributed equidistantly on the circumference of the circle of radius defined below
    points = []
     # This is used to differentiate runs when clearLines_props.clearLinesBool is false and more than one set of lines is created
    runNumber = 1
    # The consecutive values, from index 1, of the array below have the length of a side from a point to a point index away from it
    sidesLen = []
    sidesLen.append(0) # Array of sides lengths [0] has 0, see note 3 lines above
    theta0 = tau / 2 * (1 / 2 + 1 / numPoints)
    lineSetPrefix = "00_"
    colorSchemePrefix = "00_"
    #linesFrom = 3 # replaced by numPointsFrom property above...
    #linesTo = 9 # replaced by numPointsTo property above...

    # Static variables to know the color scheme used
    # make it to an array for multiple runs color scheme attribution
    # When using the value, use them directly, since COLORSHEMES[X] = X!
    # The array is only used for its size
    ONE = 0
    RANDOM = 1
    SERIAL = 2
    LEVEL = 3
    LEVEL_SERIAL = 4
    POINT = 5
    COLORSCHEMES = [ONE, RANDOM, SERIAL, LEVEL, LEVEL_SERIAL, POINT]
    
    # Static variables below to know which index we have in the line name
    # The line names syntax is the following
    # AA_BB_L_CC_1p_DD_EE for periphery lines,thus the "_1p_", where p is for periphery 
    # and 1 so that the periphery lines come first in the Outliner
    # or 
    # AA_BB_L_CC_2i_DD_EE for inside lines, thus the "_2i_", where i is for inside
    # and 2 so that the inside lines come second in the Outliner
    #
    # AA is the run number
    # BB is the color scheme  number so that the schemes can be preserved 
    # when giving materials in more than one run
    # _L_ is there just to say that we have lines
    # CC is the number of points
    # _1p_ or _2i_ indicate whether it is periphery or inside lines, see 8 and 11 lines above
    # DD is the point from
    # EE is the line to
    
    LINESETPREFIX = 0
    COLORSCHEMEPREFIX = 1
    NUMLINE = 3
    POINTFROM = 5
    POINTTO = 6
    
    lineSetNumber = 0
    # Each element of levelsLogForMaterials has the numPoints for that level
    # for instance [3, 5, 7]
    levelsLogForMaterials = [] # doChryzoid will fill this array to indicate the levels
    colorUseFlag = LEVEL_SERIAL # use of colors flag 'one' for one color
    colors_and_strengths = [#((.008, .008, .008, 1), 50, "gray"),
                          ((1, 0, 0, 1), 50, "red"),
                          ((0, 1, 0, 1), 50, "green"),
                          ((0, 0, 1, 1), 50, "blue"),
                          ((1, 0, 1, 1), 50, "purple"),
                          ((0, 0.423268, 0.863157, 1), 50, "cyan"),
                          ((0.838799, 0, 0.262251, 1), 50, "magenta"),
                          ((1, 0.887923, 0, 1), 50, "yellow"),
                          ((1, 1, 1, 1), 50, "white")  ]


    ##### REMOVE OLD LINES FUNCTION
    def removeOldLines(self, context):
        objs = bpy.data.objects
        for obj in objs:
            if obj.name.find("_1p_") != -1 or obj.name.find("_2i_") != -1 or obj.name.find("ReferenceLine.") == 0:
                bpy.data.objects.remove(obj, do_unlink=True)
        override = bpy.context.copy()
        override["area.type"] = ['OUTLINER']
        override["display_mode"] = ['ORPHAN_DATA']
        # removes the unused data from memory
        # From https://blenderartists.org/t/blender-2-92-goes-in-not-responding-neverland/1299982/2
        # this would normally occur when you close and re-open file
        # the number 4 is an arbitrary number of times to repeaet the command
        # which allows for purging unused materials, textures, etc
        # that are currently linked to mesh data
        bpy.ops.outliner.orphans_purge(override, 4)
    ##### END OF REMOVE OLD LINES FUNCTION

    ##### START OF PURGE OLD MATERIALS FUNCTION, FROM https://blenderartists.org/t/deleting-all-materials-in-script/594160/2
    # the new function from nezumi.blend at https://blenderartists.org/t/blender-2-92-python-use-of-intproperties-crashes-addon/1298622/6
    # still crashes, let's try a new approach
    def purgeOldMaterials(self, context):
        for mat in bpy.data.materials:
            bpy.data.materials.remove(mat)
#    def purgeOldMaterials(self, context):
#        for mat in list(self.mats):
#            mat.remove(bpy.data.materials[0])
    # my old that crashed blender because self.mats has possibly changed address
#    def purgeOldMaterials(self, context):
#        for mat in self.mats:
#            self.mats.remove(bpy.data.materials[0])
    ##### END OF PURGE OLD MATERIALS FUNCTION

    ##### START OF CREATE SHADERS FUNCTION
    ### OBS em_matGiven is now an array of em_matGiven, use the current lineSetNumber on it
    # I pass emission_mat[x], not the original emission_mat
    # Nope, back to the old passing of the whole emission_mat
    def createShaders(self, context, em_matGiven):
        # EMISSION SHADER: CREATE AN EMISSION SHADER SO THAT WE CAN SEE THE LINE
        # EMISSION SHADER: NEW SHADER
        COLOR = 0
        STRENGTH = 1
        COLOR_NAME = 2
        global showColMats
        global lineSetPrefix
        
#        sizeGivenString = str(sizeGiven)
#        sizeGivenPrefix = ""
#        if sizeGiven <= 9:
#            sizeGivenPrefix = "0"
#        sizeGivenPrefix = sizeGivenPrefix + sizeGivenString
        #print("-----> 301 in create shaders and sizeGivenPrefix", sizeGivenPrefix)
        
        #print("-----> 294 in create shaders and I am going to add shaders to the next element in em_matGiven of size", len(em_matGiven))
        if self.showColMats == True:
            print("-------> 344 I have the following colors:")
            for i in range(len(colors_and_strengths)):
                print("------------> 346 ", colors_and_strengths[i])

        #global emission_mat # emission_mat is passed from execute
        nodes = []
        material_output = []
        node_emission = []
        links = []

        # create as many materials as we have colors
        #print("-----> 271 About to create as many materials as we have colors, that is", len(self.colors_and_strengths))
        for col_or in range(len(self.colors_and_strengths)):
            em_matGiven.append(bpy.data.materials.new(name = "_Emission_" + self.colors_and_strengths[col_or][COLOR_NAME]))
            #print("-----> 109 Added emission mat:", em_matGiven[len(em_matGiven) - 1])
            em_matGiven[col_or].use_nodes = True
            nodes.append(em_matGiven[col_or].node_tree.nodes)
            material_output.append(nodes[col_or].get('Material Output'))
            node_emission.append(nodes[col_or].new(type='ShaderNodeEmission'))
            node_emission[col_or].inputs[0].default_value = self.colors_and_strengths[col_or][COLOR] # RGB + Alpha
            node_emission[col_or].inputs[1].default_value = self.colors_and_strengths[col_or][STRENGTH] # strength
            links.append(em_matGiven[col_or].node_tree.links)
            new_link = links[col_or].new(node_emission[col_or].outputs[0], material_output[col_or].inputs[0])
        if self.showColMats == True:
            for i in range(len(em_matGiven)):
                print("Material:", em_matGiven[i])
                
        # remove BSDF From Materials (used to be a function
        for i in range(len(bpy.data.materials)):
            mat = bpy.data.materials[i]
            if mat.name.find("Principled BSDF") != -1:
                node_to_delete =  mat.node_tree.nodes['Principled BSDF']
                mat.node_tree.nodes.remove( node_to_delete )
        #print("-----> 377 at the end of create shaders and the next element in em_matGiven has now size", len(em_matGiven))
    ##### END OF CREATE SHADERS FUNCTION

    ##### START OF SHOW LINE DATA FUNCTION (ONLY FOR DEBUG)
    def showLineData(self, context, lineToShow):
        #return
        refLine = bpy.data.objects[lineToShow]
        print("-----> 384 \nLINE", lineToShow, "DATA:\nLocation:", refLine.location, "\nRotation:", refLine.rotation_euler, "\nScale:", refLine.scale)
    ##### END OF SHOW LINE DATA FUNCTION (ONLY FOR DEBUG)
        
    ##### START OF select Object By Name FUNCTION
    def selectObjectByName(self, context, objectToSelect):
        ## deselect all (just in case?) then select and activate Refe renceLine WITHOUT USING bpy.ops
        # from https://blenderartists.org/t/element-selected-in-outliner-and-i-dont-want-it-to-be/1296825/3
        for selected in bpy.context.selected_objects:
            selected.select_set(False)
        newObject = bpy.data.objects[objectToSelect] 
        newObject.select_set(True)
        bpy.context.view_layer.objects.active = newObject
    # other code to select only one object, using bpy.ops...
    # from https://blenderartists.org/t/element-selected-in-outliner-and-i-dont-want-it-to-be/1296825/3
    # don't run it, the one above works too
    #bpy.ops.object.select_all(action='DESELECT')
    #obj = bpy.data.objects["Refer0enceLine"] 
    #obj.select_set(True)
    #bpy.context.view_layer.objects.active = obj
    ##### END OF select Object By Name FUNCTION

    #### START OF DO COLORS BY LEVEL FUNCTION
    def doColorsByLevel(self, context, linesGiven, em_matGiven, levelOrLevelSerial):
        # Here I get only lines with AA_03 as starting name, since we are on the LEVEL scheme
        #os.system("cls")
        global levelsLogForMaterials
        # if levelsLogForMaterials is [3, 5, 7] we get the 3 from [0] and the 7 from [len() - 1
        # This way, we know how many levels to treat, from to to,
        # and how many lines there are per level, per n * (n - 1)/2
        firstLineNumPoints = self.levelsLogForMaterials[0]
        lastLineNumPoints = self.levelsLogForMaterials[len(self.levelsLogForMaterials) - 1]
        numLevels = lastLineNumPoints - firstLineNumPoints
        calcNumLines = 0
        if len(self.levelsLogForMaterials) == 1:
            # Assign a random color for each level
            matForThatLevel = random.randint(0, len(em_matGiven) - 1)
            for j in range(len(linesGiven)):
                linesGiven[calcNumLines + j].data.materials.append(em_matGiven[matForThatLevel])

        if len(self.levelsLogForMaterials) > 1:
            matForThatLevel = 0
            for i in range(len(self.levelsLogForMaterials)):
                # Assign a random color for each level
                if levelOrLevelSerial == self.LEVEL:
                    matForThatLevel = random.randint(0, len(em_matGiven) - 1)
                # or do it serial and Assign the next color for each level
                if levelOrLevelSerial == self.LEVEL_SERIAL:
                    matForThatLevel = (matForThatLevel + 1)# % len(em_matGiven)
                numLinesForThatLevel = int(self.levelsLogForMaterials[i] * (self.levelsLogForMaterials[i] - 1) / 2)
                for j in range(numLinesForThatLevel):
                    linesGiven[calcNumLines + 0].data.materials.append(em_matGiven[matForThatLevel % len(em_matGiven)])
                    calcNumLines += 1
                #calcNumLines += int(self.levelsLogForMaterials[i] * (self.levelsLogForMaterials[i] - 1) / 2)
    #### END OF DO COLORS BY LEVEL FUNCTION

    #### START OF DO COLORS BY POINT FUNCTION
    def doColorsByPoint(self, context, linesGiven, em_matGiven):
        # Assign a random color for each point from 0
        global levelsLogForMaterials
        lastPointToCheck = self.levelsLogForMaterials[len(self.levelsLogForMaterials) - 1]
        #print("-----> 423 PPPPPP in points and I have", len(linesGiven), "lines and log", self.levelsLogForMaterials, "--------> last poinit to check", lastPointToCheck)
        linesDone = []
        for i in range(len(linesGiven)):
            linesDone.append(-1)
        # The last element of linesDone, by line below, contains the actual number of lines done...
        linesDone.append(0)
        colorForThatPoint = random.randint(0, len(self.colors_and_strengths) - 1)
        colorForPreviousPoint = colorForThatPoint
        
        # START OF DO LINES EMANATING FROM THE 0 POINT
        pointToCheck = 0
        #print("-----> 434 line name split", linesGiven[i].name.split("_"))
        for i in range(len(linesGiven)):
            # a is the number of points b is the point to c is the point from
            a = int(linesGiven[i].name.split("_")[self.NUMLINE])
            b = int(linesGiven[i].name.split("_")[self.POINTTO])
            c = linesGiven[i].name.split("_")[self.POINTFROM]
            if (a == b) or (c == "00"):
                linesDone[i] = pointToCheck
                linesDone[len(linesDone) - 1] += 1
                linesGiven[i].data.materials.append(em_matGiven[colorForThatPoint])
        # END OF DO LINES EMANATING FROM THE 0 POINT
        
        # START OF DO LINES EMANATING FROM THE 1 POINT
        for i in range(1, lastPointToCheck):
            if linesDone[len(linesDone) - 1] == len(linesGiven):
                break
            colorForThatPoint = random.randint(0, len(self.colors_and_strengths) - 1)
            while colorForThatPoint == colorForPreviousPoint:
                colorForThatPoint = random.randint(0, len(self.colors_and_strengths) - 1)
            colorForPreviousPoint = colorForThatPoint
            for j in range(len(linesGiven)):
                # a is point from
                a = int(linesGiven[j].name.split("_")[self.POINTFROM])
                #b = int(linesGiven[j].name.split("_")[self.POINTTO])
                if linesDone[j] == -1:
                    if a == i:
                        linesDone[j] = i
                        linesGiven[j].data.materials.append(em_matGiven[colorForThatPoint])
                        linesDone[len(linesDone) - 1] += 1
    #### END OF DO COLORS BY POINT FUNCTION

    #### START OF APPLY SCHEME FUNCTION
    def applyScheme(self, context, linesToUse, schemeNumber, em_matGiven):
        #print("-----> 502 in apply one scheme and lines", linesToUse)
        colorToUse = random.randint(0, len(em_matGiven) - 1)
        for i in range(len(linesToUse)):
            linesToUse[i].data.materials.clear()
        # NOW APPLY
        if schemeNumber == self.ONE:
            for i in range(len(linesToUse)):
                linesToUse[i].data.materials.append(em_matGiven[colorToUse])

        if schemeNumber == self.RANDOM:
            for i in range(len(linesToUse)):
                linesToUse[i].data.materials.append(em_matGiven[random.randint(0, self.numPoints - 1)])

        if schemeNumber == self.SERIAL:
            colorToUse = 0;
            for i in range(len(linesToUse)):
                linesToUse[i].data.materials.append(em_matGiven[colorToUse])
                colorToUse = (colorToUse + 1) % len(em_matGiven)

        if schemeNumber == self.LEVEL:
            self.doColorsByLevel(context, linesToUse, em_matGiven, self.LEVEL)

        if schemeNumber == self.LEVEL_SERIAL:
            self.doColorsByLevel(context, linesToUse, em_matGiven, self.LEVEL_SERIAL)

        if schemeNumber == self.POINT:
            self.doColorsByPoint(context, linesToUse, em_matGiven)
    #### END OF APPLY SCHEME FUNCTION

    ### OBS I pass emission_mat[x], not the original emission_mat
    # Nope, back to passing the whole emission_mat
    def applyMaterialsToLines(self, context, em_matGiven):
        global colorUseFlag
        global lineSetPrefix
        colSchemeForLine = int(self.colorSchemePrefix[0:2])

        # FIRST, BUILD A LIST OF LINES

        # parse through all possible color schemes
        # Get the number of color schemes from the dropdown!
        # Nope, what you get is the length of the string!!!
        # Then make the scheme numbers to an array...
        scene = context.scene
        colorMode_props = scene.colorMode_properties
        # Here is the only place where COLORSCHEMES is used for its length
        # # All other places, use X instead of COLORSCHEME[X] SINCE COLORSCHEME[X] == X!
        numSchemes =  len(self.COLORSCHEMES)        
        #print("-----> 522 num schemes", numSchemes)
        
        # For each scheme, build the list of lines that have it
        for scheme in range(numSchemes):
            #print("-----> 488 SSSS Doing scheme", scheme)
            
            # make scheme # to a string with '_' at the end
            prefix = ""
            if scheme < 10:
                prefix = "0"
            schemeNumberString = "_" + prefix + str(scheme) + "_L"
            
            # get all the lines that have that scheme
            lines = []
            for j in range(len(bpy.data.objects)):
                if (bpy.data.objects[j].name.find(schemeNumberString) != -1):
                    lines.append(bpy.data.objects[j])
            # if any, apply the right scheme
            if len(lines) > 0:
                #print("-----> 541 I found", len(lines), "with", schemeNumberString, "as prefix calling applyScheme")
                self.applyScheme(context, lines, scheme, em_matGiven)
    #### END OF APPLY MATERIALS TO LINES FUNCTION

    ##### START OF POPULATE POINTS AND LINE LENGTHS FUNCTION
    def populatePointsAndLineLengths(self, context, numPointsGiven):
        global radius
        global sidesLen
        global theta0
        global points
        theta0 = tau / 2 * (1 / 2 + 1 / numPointsGiven)
        
        # purge points array
        points = []
        # purge sidesLen array EXCEPT 0 ELEMENT, WHICH IS 0!
        sidesLen = []
        sidesLen.append(0)
            
        # START OF BUILD POINTS ARRAY
        for i in range(numPointsGiven):
           # points.append((self.radius * cos(i * tau/numPointsGiven), self.radius * sin(i * tau/numPointsGiven), 0))
            points.append((radius * cos(i * tau/numPointsGiven), radius * sin(i * tau/numPointsGiven), 0))
        # END OF BUILD POINTS ARRAY

        # START OF BUILD SIDESLEN ARRAY FOR __EVEN__ numPointsGiven
        if numPointsGiven % 2 == 0:
            numPointsGivenOver2 = int (numPointsGiven/2)
            # Fill from 0 to numPointsGiven/2 excluded
            for i in range(1, numPointsGivenOver2):
                sidesLen.append(sqrt((points[i][0] - points[0][0]) * (points[i][0] - points[0][0]) + (points[i][1] - points[0][1]) * (points[i][1] - points[0][1])))
            # Fill numPointsGiven/2, the lone longest segment
            sidesLen.append(sqrt((points[numPointsGivenOver2][0] - points[0][0]) * (points[numPointsGivenOver2][0] - points[0][0]) + (points[numPointsGivenOver2][1] - points[0][1]) * (points[numPointsGivenOver2][1] - points[0][1])))
            # Fill numPointsGiven/2 + 1 to numPointsGiven - 1
            for i in range(numPointsGivenOver2 + 1, numPointsGiven - 0):
                sidesLen.append(sidesLen[numPointsGiven - i])
        # END OF BUILD SIDES LENGTHS ARRAY FOR EVEN numPointsGiven

        # START OF BUILD SIDESLEN ARRAY FOR __ODD__ numPointsGiven
        if numPointsGiven % 2 != 0:
            numPointsGivenOver2 = int (numPointsGiven / 2)

            # Fill from 0 to numPointsGiven/2 INCLUDED
            for i in range(1, numPointsGivenOver2 + 1):
                sidesLen.append(sqrt((points[i][0] - points[0][0]) * (points[i][0] - points[0][0]) + (points[i][1] - points[0][1]) * (points[i][1] - points[0][1])))

            # Fill numPointsGiven/2 + 1 to numPointsGiven - 1
            for i in range(numPointsGivenOver2 + 1, numPointsGiven):
                sidesLen.append(sidesLen[numPointsGiven - i])
        # END OF BUILD SIDESLEN ARRAY FOR __ODD__ numPointsGiven
    ##### END OF POPULATE POINTS AND LINE LENGTHS FUNCTION

# moved this function (view3d_find) to outside this class

    ##### START OF build Ref Line From CUBE FUNCTION
    def buildRefLineFromCube(self, context):
        global runNumber
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        #bpy.ops.transform.resize(value=(self.radius, self.radius / self.radius2ThicknessRatio, self.radius / self.radius2ThicknessRatio))
        bpy.ops.transform.resize(value=(radius, radius / radius2ThicknessRatio, radius / radius2ThicknessRatio))
        bpy.context.scene.cursor.location[0] = -radius / 2
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.context.scene.cursor.location[0] = 0
        bpy.context.object.location[0] = 0
        
        # waiting for override code to run the loopcuts...
        # Here is the long awaited code, does it work, now
        region, rv3d, v3d, area = view3d_find(context, True)

        override = {
            'scene'  : bpy.context.scene,
            'region' : region,
            'area'   : area,
            'space'  : v3d
        }
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.loopcut_slide(
            override,
            MESH_OT_loopcut = {
                "object_index" : 0,
                "number_cuts":550, 
                "smoothness":0, 
                "falloff":'SMOOTH', 
                "edge_index":4, 
                "mesh_select_mode_init":(True, False, False)
            }, 
            TRANSFORM_OT_edge_slide = {
                "value"             : 0, 
                "mirror"                : False, 
                "snap"                  : False, 
                "snap_target"           : 'CLOSEST', 
                "snap_point"            : (0, 0, 0), 
                "snap_align"            : False, 
                "snap_normal"           : (0, 0, 0), 
                "correct_uv"            : False, 
                "release_confirm"       : False, 
            }
        )
        bpy.context.object.name="ReferenceLine"
        for selected in bpy.context.selected_objects:
            print("-----> 700 JUST CREATED REFLINE, thus it is OBVIOUSLY selected", selected.name)
            print("-----> 701 called only when no ref line found in draw full lines...")
    ##### END OF build Ref Line From CUBE FUNCTION

    ##### START OF DRAWFULLLINE FUNCTION
    def drawFullLines(self, context, numPointsGiven):
        # Draw all lines
        
        # buildRe_fLine if it does not exist
        # as of now, the ref line must be selected if it has to work, and even then, it fucks up the lengths when we change numPoints...
        # As of a later now, the ref line is selected automatically if not selected
        # and if it does not exist, one is created.
        # Now you can pick the reference line from a dropdown menu...
        
        # Implementing dropdown to pick between more than one ref line...
        
        foundRefLine = False
        for i in range(len(bpy.data.objects)):
            if bpy.data.objects[i].name.find(context.scene.prop) == 0:
            #if bpy.data.objects[i].name == "ReferenceLine":
                #print("-----> 714!!!!! I found it:\"", bpy.data.objects[i].name)
                foundRefLine = True
                bpy.ops.object.select_all(action='DESELECT')
                #self.selectObjectByName(context, "ReferenceLine")  
                self.selectObjectByName(context, context.scene.prop)  
                break
        if foundRefLine == False:
            self.buildRefLineFromCube(context)
        
        # AT THIS POINT ReferenceLine IS SELECTED EXIT EDIT MODE
        #print("-----> 724 ref line selected is\"", bpy.ops.object.name)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # FIRST DRAW LINES ON PERIPHERY 0_1, 1_2, AND SO ON
        # OBS! THE REFERENCE LINE MUST BE SELECTED IF IT EXISTS ALREADY    
        self.colorSchemePrefix = "0" + str(self.colorUseFlag) + "_"
        for i in range(len(points)):
            bpy.context.scene.cursor.location=(0, 0, 0)
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0)})
            
            if numPointsGiven > 9:
                zeroPrefix = ''
            else:
                zeroPrefix = '0'
            if i > 9:
                zeroPrefixI = ''
            else:
                zeroPrefixI = '0'
            if (i + 1) > 9:
                zeroPrefixIPlus1 = ''
            else:
                zeroPrefixIPlus1 = '0'
            bpy.context.object.name = self.lineSetPrefix + self.colorSchemePrefix + "L_" + zeroPrefix + str(numPointsGiven) + "_" + "1p_" + zeroPrefixI + str(i) + "_" +  zeroPrefixIPlus1 + str(i + 1 % numPointsGiven)
            # AT THIS POINT WE HAVE THE RIGHT NAME Line_Periph_numPoints_m_n THE LINE OF CODE BELOW SHOWED IT
            bpy.context.object.location[0] = points[i][0]
            bpy.context.object.location[1] = points[i][1]
            if bpy.context.scene.chryzoid_properties.pos_z == True:
                bpy.context.object.location[2] = (numPointsGiven - 3) * bpy.context.scene.chryzoid_properties.z
            if bpy.context.scene.chryzoid_properties.pos_z == False:
                bpy.context.object.location[2] = (numPointsGiven - 3) * -bpy.context.scene.chryzoid_properties.z
            bpy.data.objects[bpy.context.object.name].rotation_euler[2] = 0
            bpy.context.object.scale[0] = sidesLen[1]
            ang = (theta0 + (i) * tau / numPointsGiven) % tau
            bpy.data.objects[bpy.context.object.name].rotation_euler[2] = ang
        # DONE DRAWING THE LINES ON PERIPHERY...
        # AT THIS POINT RefeLine_Periph_num_num-1_num IS SELECTED
        for i in range(len(points)): # OBS DISABLED IF 0 IN THE RANGE, FOR DEBUGGING...
            for j in range(i + 2, len(points) - 0):
                if numPointsGiven > 9:
                    zeroPrefix = ''
                else:
                    zeroPrefix = '0'
                if i > 9:
                    zeroPrefixI = ''
                else:
                    zeroPrefixI = '0'
                if j > 9:
                    zeroPrefixJ = ''
                else:
                    zeroPrefixJ = '0'
                if (j - i) == numPointsGiven - 1:
                    continue
                bpy.context.scene.cursor.location=(0, 0, 0)
                bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(-0, -0, 0)}) #
                bpy.context.selected_objects[0].name = self.lineSetPrefix + self.colorSchemePrefix + "L_" + zeroPrefix + str(numPointsGiven) + "_" + "2i_" + zeroPrefixI + str(i) + "_" + zeroPrefixJ + str(j)
                bpy.context.object.location[0] = points[i][0]
                bpy.context.object.location[1] = points[i][1]
                if bpy.context.scene.chryzoid_properties.pos_z == True:
                    bpy.context.object.location[2] = (numPointsGiven - 3) * bpy.context.scene.chryzoid_properties.z
                if bpy.context.scene.chryzoid_properties.pos_z == False:
                    bpy.context.object.location[2] = (numPointsGiven - 3) * -bpy.context.scene.chryzoid_properties.z
                bpy.data.objects[bpy.context.object.name].rotation_euler[2] = 0
                bpy.context.object.scale[0] = sidesLen[j - i]
                ang = (theta0 + i * (tau / numPointsGiven) + (j - i - 1) * (tau / (2 * numPointsGiven))) % tau
                bpy.data.objects[bpy.context.object.name].rotation_euler[2] = ang
            bpy.context.scene.cursor.location=(0, 0, 0)
    ##### END OF DRAWFULLLINE FUNCTION

    ##### START OF DO CHRYZOID FUNCTION
    def doChryzoid(self, context, numPointsGiven, colorSchemeGiven):
        self.colorUseFlag = colorSchemeGiven
        self.populatePointsAndLineLengths(context, numPointsGiven)
        self.drawFullLines(context, numPointsGiven) # DRAW LINES AFTER THEY HAVE BEEN SCALED. OBS IT CALLS build RefLine!
    ##### END OF DO CHRYZOID FUNCTION

    ##### START OF EXECUTE FUNCTION
    def execute(self, context):

        #os.system("cls")
        global COLORSCHEMES

        layout = self.layout
        scene = context.scene
        refline_props = scene.refline_properties
        colorMode_props = scene.colorMode_properties
        clearLines_props = scene.clearLines_properties
        chryzoid_props = scene.chryzoid_properties
        chryzode_props = scene.chryzode_properties
        
        global colorUseFlag
        global levelsLogForMaterials
        global lineSetPrefix
        global lineSetNumber
        
        ###### LET'S     ###### HAVE    ###### FUN    ###### NOW...
        startTime = time.time()
        startDate = datetime.now()

        if clearLines_props.clearLinesBool == True:
            self.removeOldLines(context)
        self.purgeOldMaterials(context)
        emission_mat = []
        self.createShaders(context, emission_mat)
        self.levelsLogForMaterials = [] # Reset the levels log for materials
        #print("\n-----> 842 At start of EXECUTE FOR chryzoid_operator about to do chryzoids from", bpy.context.scene.chryzoid_properties.numberFrom, "to", bpy.context.scene.chryzoid_properties.numberTo, "skipping", bpy.context.scene.chryzoid_properties.skip, "and colorUseFlag", self.colorUseFlag, "before setting it")
        if colorMode_props.colorModeEnum == 'ONE':
            self.colorUseFlag = self.COLORSCHEMES[self.ONE]
        if colorMode_props.colorModeEnum == 'RANDOM':
            self.colorUseFlag = self.COLORSCHEMES[self.RANDOM]
        if colorMode_props.colorModeEnum == 'SERIAL':
            self.colorUseFlag = self.COLORSCHEMES[self.SERIAL]
        if colorMode_props.colorModeEnum == 'LEVEL':
            self.colorUseFlag = self.COLORSCHEMES[self.LEVEL]
        if colorMode_props.colorModeEnum == 'POINT':
            self.colorUseFlag = self.COLORSCHEMES[self.POINT]
        # Get the prefix of the lines, that is the "XX_" that is before "L_"
        # The XX_ is there for all lines of one run to differentiate them from another run
        # to avoid ending with ".001" and so on on the next run
        self.lineSetPrefix = "00_"
        self.lineSetNumber = 0
        foundLinePrefix = False
        lineNameFound = ""
        lineSetNumberPadding = ""
        #allLinesFound = []
        for j in range(len(bpy.data.objects)):
            if bpy.data.objects[j].name.find("L_") != -1:
                self.lineSetNumber = int(bpy.data.objects[j].name[:2]) + 1
                lineNameFound = bpy.data.objects[j].name
                foundLinePrefix = True
        if self.lineSetNumber < 10:
            lineSetNumberPadding = "0"
        self.lineSetPrefix = lineSetNumberPadding + str(self.lineSetNumber) + "_"
        #print("-----> 760 At start of EXECUTE FOR chryzoid_operator lineSetNumber", self.lineSetNumber, "and prefix", self.lineSetPrefix)
            
        for i in range(bpy.context.scene.chryzoid_properties.numberFrom, bpy.context.scene.chryzoid_properties.numberTo + 1, bpy.context.scene.chryzoid_properties.skip):
            self.levelsLogForMaterials.append(i)
            tempstarttime = time.time()
            #print("----> 866 Doing chryzoid", i, "of from", bpy.context.scene.chryzoid_properties.numberFrom, "to", bpy.context.scene.chryzoid_properties.numberTo, "skip", bpy.context.scene.chryzoid_properties.skip)
            self.doChryzoid(context, i, self.colorUseFlag)
            tempendtime = time.time()
            print("-----> 869 Doing chryzoid", i, "of from", bpy.context.scene.chryzoid_properties.numberFrom, "to", bpy.context.scene.chryzoid_properties.numberTo, "skip", bpy.context.scene.chryzoid_properties.skip, "took", round((tempendtime - tempstarttime) * 1000), "ms")
            
            # MAKE SURE THAT REF LINES IS SELECTED AT START OF EACH RUN
            for selected in bpy.context.selected_objects:
                selected.select_set(False)

            #newObject = bpy.data.objects["ReferenceLine"] 
            newObject = bpy.data.objects[context.scene.prop] 
            newObject.select_set(True)
            bpy.context.view_layer.objects.active = newObject

        self.applyMaterialsToLines(context, emission_mat)

        endTime = time.time()
        print("-----> 883 At end of execute and", startDate)
        print("-----> 884 At end of execute and It took:", round((endTime - startTime) * 1000), "ms")
         
        self.selectObjectByName(context, context.scene.prop)
                
        return {'FINISHED'}
    ##### END OF EXECUTE FUNCTION

##### end of copy all the code from the F3 chryzoid... 
    
class chryzo_operator(bpy.types.Operator):
    bl_label = "Operator"
    bl_idname = "chryzo.operator"
    
    def execute(self, context):
        #os.system("cls")
        timenow = time.time()
        print("-----> 911 I executed CHRYZODE at", timenow, "and # of Points:", bpy.context.scene.chryzode_properties.numPoints, "and multiplier:", bpy.context.scene.chryzode_properties.multiplier)
        scene = context.scene
        refline_props = scene.refline_properties
        chryzoid_props = scene.chryzoid_properties
        chryzode_props = scene.chryzode_properties
        #if refline_props.refLineEnum == 'opt1':
            # that was a test
            #bpy.ops.mesh.primitive_cube_add()
        print("I pick this line", refline_props.refLineEnum)
        return {'FINISHED'}


# I wanted to call it deleteLine and it did not accept it!
class chryzo2_operator(bpy.types.Operator):
    bl_label = "Operator"
    bl_idname = "chryzo2.operator"
    
    def execute(self, context):
        #os.system("cls")
        timenow = time.time()
        print("-----> 931 I execute CHRYZODE2 at", timenow, "and # of Points:", bpy.context.scene.chryzode_properties.numPoints, "and multiplier:", bpy.context.scene.chryzode_properties.multiplier)
        scene = context.scene
        refline_props = scene.refline_properties
        chryzoid_props = scene.chryzoid_properties
        chryzode_props = scene.chryzode_properties
        #if refline_props.refLineEnum == 'opt1':
            # that was a test
            #bpy.ops.mesh.primitive_cube_add()
        print("-----> 939 I execute CHRYZODE2 at", timenow, " and I pick this line", refline_props.refLineEnum)
        lines = []
        for i in range(len(bpy.data.objects)):
            if (bpy.data.objects[i].name.find("_1p_") != -1 or bpy.data.objects[i].name.find("_2i_") != -1):
                lines.append(bpy.data.objects[i])
        #print("I got lines", lines)
        for obj in lines:
            bpy.data.objects.remove(obj, do_unlink=True)

        return {'FINISHED'}
#### end of chryzoid2_operator

       
#### build_refline_operator
class chryzo3_operator(bpy.types.Operator):
    bl_label = "Operator"
    bl_idname = "chryzo3.operator"
    
    def execute(self, context):
        lines_to_unlink = []

        chryzoid_operator.buildRefLineFromCube(self, context)
        for obj in bpy.context.scene.collection.objects:
            if obj.name.find("ReferenceLine") != -1:
                obj.name = obj.name.replace("ReferenceLine", "ReferenceLineNew")
        bpy.ops.object.editmode_toggle()
        coll_from = bpy.context.scene.collection
        coll_to = bpy.data.collections['Collection']
        for obj in bpy.context.scene.collection.objects:
            if obj.name.find("ReferenceLine") != -1:
                lines_to_unlink.append(obj)
        for obj in lines_to_unlink:
            coll_to.objects.link(obj)
        for obj in lines_to_unlink:
            coll_from.objects.unlink(obj)

        return {'FINISHED'}
#classes = [RefLineProperties, ColorModeProperties, ClearLinesProperties, ChryzoidProperties, ChryzodeProperties, ChryzoidPanel, ChryzodePanel, chryzoid_operator, chryzode_operator, chryzode2_operator]#, deleteLines_operator]

classes = [RefLineProperties, ColorModeProperties, ClearLinesProperties, ChryzoidProperties, ChryzodeProperties, ChryzoidPanel, chryzoid_operator, chryzo_operator, chryzo2_operator, chryzo3_operator]#, deleteLines_operator]

def register():
    for clas in classes:
        bpy.utils.register_class(clas)

    bpy.types.Scene.refline_properties = bpy.props.PointerProperty(type = RefLineProperties)
    bpy.types.Scene.colorMode_properties = bpy.props.PointerProperty(type = ColorModeProperties)
    bpy.types.Scene.clearLines_properties = bpy.props.PointerProperty(type = ClearLinesProperties)
    bpy.types.Scene.chryzoid_properties = bpy.props.PointerProperty(type = ChryzoidProperties)
    bpy.types.Scene.chryzode_properties = bpy.props.PointerProperty(type = ChryzodeProperties)
    bpy.types.Scene.prop = bpy.props.EnumProperty(name="Ref Line", items=items_prop, update=update_prop)


def unregister():
    for clas in classes:
        bpy.utils.unregister_class(clas)
    del bpy.types.Scene.refline_properties
    del bpy.types.Scene.colorMode_properties
    del bpy.types.Scene.chryzoid_properties
    del bpy.types.Scene.chryzode_properties
    del bpy.types.Scene.prop

if __name__ == "__main__":
    register()
