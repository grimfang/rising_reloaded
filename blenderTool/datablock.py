import bpy


### Addon info ###
bl_info = \
    {
        "name" : "Logic Block",
        "author" : "MJ-meo-dmt <mjmeodmt@gmail.com>",
        "version" : (1, 0, 0),
        "blender" : (2, 6, 7),
        "location" : "Properties > Object > Add Datablock",
        "description" :
            "Creates a 'datablock' to attach to the object.(use with: panda3d tags)",
        "warning" : "",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Game Engine",
    }
#################
  
class TypeSamplerPanel(bpy.types.Panel):
    bl_label = "Add Datablock"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
  
    def draw(self, context):
        scn = bpy.context.scene
        scnType = bpy.types.Scene
        layout = self.layout
        row = layout.row()
        col = row.column()
           
        ## SELECTION ##
        col.prop( scn, "dropDownProp" )
        
        ## CHECK PLAYER TYPE SELECTION ##
        if bpy.context.scene.dropDownProp == "playerType":
            col.prop( scn, "datablock_id" )
            col.prop( scn, "datablock_name" )
            col.prop( scn, "dropDownControl" )
            col.prop( scn, "datablock_model" )
            col.prop( scn, "datablock_height" )
            col.prop( scn, "datablock_radius" )
            col.prop( scn, "datablock_runSpeed" )
            col.prop( scn, "datablock_walkSpeed" )
            col.prop( scn, "datablock_turnSpeed" )
            col.prop( scn, "datablock_isDynamic" )
            col.prop( scn, "datablock_attachScript" )
        
        
        ## CHECK LEVEL TYPE SELECTION ##
        if bpy.context.scene.dropDownProp == "levelType":
            col.prop( scn, "dropDownLevelType" ) # Subtype
            col.prop( scn, "datablock_id" )
            col.prop( scn, "datablock_name" )
            col.prop( scn, "datablock_isDynamic" )
            col.prop( scn, "datablock_useBulletPlane" )
            col.prop( scn, "datablock_attachScript" )
        
        
        ## CHECK OBJECT TYPE SELECTION ##
        if bpy.context.scene.dropDownProp == "objectType":
            col.prop( scn, "datablock_id" )
            col.prop( scn, "datablock_name" )
            col.prop( scn, "datablock_model" )
            col.prop( scn, "datablock_isDynamic" )
            col.prop( scn, "datablock_attachScript" )
        
        ## CHECK LIGHT TYPE SELECTION ##
        if bpy.context.scene.dropDownProp == "lightType":
            col.prop( scn, "dropDownLight" ) # Subtype
            if bpy.context.scene.dropDownLight == "pointType":
                col.prop( scn, "datablock_id" )
                col.prop( scn, "datablock_name" )
                col.prop( scn, "datablock_model" )
                col.prop( scn, "datablock_isDynamic" )
                col.prop( scn, "datablock_attachScript" )
                col.prop(scn, "datablock_color")
            
            if bpy.context.scene.dropDownLight == "directType":
                col.prop( scn, "datablock_id" )
                col.prop( scn, "datablock_name" )
                col.prop( scn, "datablock_attachScript" )
                col.prop(scn, "datablock_color")
                
            if bpy.context.scene.dropDownLight == "ambientType":
                col.prop( scn, "datablock_id" )
                col.prop( scn, "datablock_name" )
                col.prop( scn, "datablock_attachScript" )
                col.prop(scn, "datablock_color")
                
            if bpy.context.scene.dropDownLight == "spotType":
                col.prop( scn, "datablock_id" )
                col.prop( scn, "datablock_name" )
                col.prop( scn, "datablock_model" )
                col.prop( scn, "datablock_isDynamic" )
                col.prop( scn, "datablock_attachScript" )
                col.prop(scn, "datablock_color")
                col.prop( scn, "datablock_lookAt" )
        
        
        col.operator( "bpt.sample_op" )

  
class SampleOperator(bpy.types.Operator):
  
    bl_idname = "bpt.sample_op"
    bl_label = "Add Datablock to Object"
  
    def invoke(self, context, event ):
        # This will need some work.. because you can add doubles...
        #bpy.ops.object.game_property_new(type='FLOAT', name="")
        # Try to add something for adding a datablock to all selected objects
        # and then get the name of the objects and fill them into the name field
        datablockType = bpy.context.scene.dropDownProp
        lightType = bpy.context.scene.dropDownLight
        levelSubType = bpy.context.scene.dropDownLevelType
        activeObject = context.active_object
        
        # Check which datablock type is selected
        if datablockType == "playerType":
            # Write the datablock like in logic editor
            bpy.ops.object.game_property_new(type='STRING', name="player")
            bpy.ops.object.game_property_new(type='INT', name="id")
            bpy.ops.object.game_property_new(type='STRING', name="controlType")
            bpy.ops.object.game_property_new(type='STRING', name="model")
            bpy.ops.object.game_property_new(type='FLOAT', name="height")
            bpy.ops.object.game_property_new(type='FLOAT', name="radius")
            bpy.ops.object.game_property_new(type='FLOAT', name="runSpeed")
            bpy.ops.object.game_property_new(type='FLOAT', name="walkSpeed")
            bpy.ops.object.game_property_new(type='FLOAT', name="turnSpeed")
            bpy.ops.object.game_property_new(type='BOOL', name="isDynamic")
            bpy.ops.object.game_property_new(type='STRING', name="script")
            
            # now add the values to them
            dict = activeObject.game.properties   
            dict['player'].value = bpy.context.scene.datablock_name
            dict['id'].value = bpy.context.scene.datablock_id
            dict['controlType'].value = bpy.context.scene.dropDownControl
            dict['model'].value = bpy.context.scene.datablock_model
            dict['height'].value = bpy.context.scene.datablock_height
            dict['radius'].value = bpy.context.scene.datablock_radius
            dict['runSpeed'].value = bpy.context.scene.datablock_runSpeed
            dict['walkSpeed'].value = bpy.context.scene.datablock_walkSpeed
            dict['turnSpeed'].value = bpy.context.scene.datablock_turnSpeed
            dict['isDynamic'].value = bpy.context.scene.datablock_isDynamic
            dict['script'].value = bpy.context.scene.datablock_attachScript
            
        elif datablockType == "levelType":
            # Write the datablock like in logic editor
            bpy.ops.object.game_property_new(type='STRING', name="level")
            bpy.ops.object.game_property_new(type='INT', name="id")
            bpy.ops.object.game_property_new(type='STRING', name="subType")
            bpy.ops.object.game_property_new(type='BOOL', name="isDynamic")
            bpy.ops.object.game_property_new(type='BOOL', name="useBulletPlane")
            bpy.ops.object.game_property_new(type='STRING', name="script")
            
            # now add the values to them
            dict = activeObject.game.properties   
            dict['level'].value = bpy.context.scene.datablock_name
            dict['id'].value = bpy.context.scene.datablock_id
            dict['subType'].value = levelSubType
            dict['isDynamic'].value = bpy.context.scene.datablock_isDynamic
            dict['useBulletPlane'].value = bpy.context.scene.datablock_useBulletPlane
            dict['script'].value = bpy.context.scene.datablock_attachScript
            
        elif datablockType == "objectType":
            # Write the datablock like in logic editor
            bpy.ops.object.game_property_new(type='STRING', name="object")
            bpy.ops.object.game_property_new(type='INT', name="id")
            bpy.ops.object.game_property_new(type='STRING', name="model")
            bpy.ops.object.game_property_new(type='BOOL', name="isDynamic")
            bpy.ops.object.game_property_new(type='STRING', name="script")
            
            # now add the values to them
            dict = activeObject.game.properties   
            dict['object'].value = bpy.context.scene.datablock_name
            dict['id'].value = bpy.context.scene.datablock_id
            dict['model'].value = bpy.context.scene.datablock_model
            dict['isDynamic'].value = bpy.context.scene.datablock_isDynamic
            dict['script'].value = bpy.context.scene.datablock_attachScript
            
        elif datablockType == "lightType":
            # POINT LIGHT PROP STUFF
            if lightType == "pointType":
                # Write the datablock like in logic editor
                bpy.ops.object.game_property_new(type='STRING', name="light")
                bpy.ops.object.game_property_new(type='STRING', name="subType")
                bpy.ops.object.game_property_new(type='INT', name="id")
                bpy.ops.object.game_property_new(type='STRING', name="model")
                bpy.ops.object.game_property_new(type='BOOL', name="isDynamic")
                bpy.ops.object.game_property_new(type='STRING', name="script")
                bpy.ops.object.game_property_new(type='STRING', name="color")
            
                # now add the values to them
                dict = activeObject.game.properties   
                dict['light'].value = bpy.context.scene.datablock_name
                dict['subType'].value = lightType
                dict['id'].value = bpy.context.scene.datablock_id
                dict['model'].value = bpy.context.scene.datablock_model
                dict['isDynamic'].value = bpy.context.scene.datablock_isDynamic
                dict['script'].value = bpy.context.scene.datablock_attachScript
                dict['color'].value = bpy.context.scene.datablock_color
            
            # DIRECTIONAL LIGHT PROP STUFF
            if lightType == "directType":
                # Write the datablock like in logic editor
                bpy.ops.object.game_property_new(type='STRING', name="light")
                bpy.ops.object.game_property_new(type='STRING', name="subType")
                bpy.ops.object.game_property_new(type='INT', name="id")
                bpy.ops.object.game_property_new(type='STRING', name="script")
                bpy.ops.object.game_property_new(type='STRING', name="color")
            
                # now add the values to them
                dict = activeObject.game.properties   
                dict['light'].value = bpy.context.scene.datablock_name
                dict['subType'].value = lightType
                dict['id'].value = bpy.context.scene.datablock_id
                dict['script'].value = bpy.context.scene.datablock_attachScript
                dict['color'].value = bpy.context.scene.datablock_color
            
            # AMBIENT LIGHT PROP STUFF
            if lightType == "ambientType":
                # Write the datablock like in logic editor
                bpy.ops.object.game_property_new(type='STRING', name="light")
                bpy.ops.object.game_property_new(type='STRING', name="subType")
                bpy.ops.object.game_property_new(type='INT', name="id")
                bpy.ops.object.game_property_new(type='STRING', name="script")
                bpy.ops.object.game_property_new(type='STRING', name="color")
            
                # now add the values to them
                dict = activeObject.game.properties   
                dict['light'].value = bpy.context.scene.datablock_name
                dict['subType'].value = lightType
                dict['id'].value = bpy.context.scene.datablock_id
                dict['script'].value = bpy.context.scene.datablock_attachScript
                dict['color'].value = bpy.context.scene.datablock_color
            
            # SPOT LIGHT PROP STUFF
            if lightType == "spotType":
                # Write the datablock like in logic editor
                bpy.ops.object.game_property_new(type='STRING', name="light")
                bpy.ops.object.game_property_new(type='STRING', name="subType")
                bpy.ops.object.game_property_new(type='INT', name="id")
                bpy.ops.object.game_property_new(type='STRING', name="model")
                bpy.ops.object.game_property_new(type='BOOL', name="isDynamic")
                bpy.ops.object.game_property_new(type='STRING', name="script")
                bpy.ops.object.game_property_new(type='STRING', name="color")
                bpy.ops.object.game_property_new(type='STRING', name="lookAt")
            
                # now add the values to them
                dict = activeObject.game.properties   
                dict['light'].value = bpy.context.scene.datablock_name
                dict['subType'].value = lightType
                dict['id'].value = bpy.context.scene.datablock_id
                dict['model'].value = bpy.context.scene.datablock_model
                dict['isDynamic'].value = bpy.context.scene.datablock_isDynamic
                dict['script'].value = bpy.context.scene.datablock_attachScript
                dict['color'].value = bpy.context.scene.datablock_color
                dict['lookAt'].value = bpy.context.scene.datablock_lookAt
            
        return {'FINISHED'}


def register():
    bpy.utils.register_class( TypeSamplerPanel )
    bpy.utils.register_class( SampleOperator )
 
 
def unregister():
    bpy.utils.register_class( TypeSamplerPanel )
    bpy.utils.register_class( SampleOperator )
 
 
if __name__ == "__main__":
    register()
  
if __name__ == '__main__':
    scnType = bpy.types.Scene
    # single value properties.
    StringProperty = bpy.props.StringProperty
    FloatProperty = bpy.props.FloatProperty
    IntProperty = bpy.props.IntProperty
    BoolProperty = bpy.props.BoolProperty
    
    ## DONO IF THERE IS A BETTER WAY IM STILL UBER NOOB WITH THIS>>> ##
    
    
    ### PLAYER TYPE DATABLOCK ###
    
    ## ID
    scnType.datablock_id = IntProperty( name = "Id",
                                       default = 0, min = 0, max = 1000,
                                    description = "Player Id" )
    
    ## NAME
    scnType.datablock_name = StringProperty(  name="Name",
                                            default=" ",
                                description = "Player Name")
    
    ## MODEL
    scnType.datablock_model = StringProperty(  name="Model File",
                                            default=" ",
                                description = "External Model File to be used instead")
    
    ## isDYNAMIC
    scnType.datablock_isDynamic = BoolProperty( name="isDynamic",
                                         description = "Is the object dynamic?",
                                         default=False )
                                         
    ## useBulletPlane
    scnType.datablock_useBulletPlane = BoolProperty( name="useBulletPlane",
                                         description = "Use Bullet Plane(infinite)",
                                         default=False )
    
    ## SCRIPT
    scnType.datablock_attachScript = StringProperty(  name="Attach Script",
                                            default=" ",
                                description = "Attach a custom script to this object.")
                                
    ## COLOR
    scnType.datablock_color = StringProperty(  name="Light Color",
                                            default="1.0 1.0 1.0 1.0",
                                description = "Adjust the color for the light. 0.0-1.0")
                                
    ## LOOKAT
    scnType.datablock_lookAt = StringProperty(  name="Light lookAt",
                                            default=" ",
                                description = "Set the light to lookAt something. Could be a object")
    
    ## HEIGHT - Player specific
    scnType.datablock_height = FloatProperty( name = "Height",
                                      default = 1.75, min = 0.0, max=3.0,
                                    description = "Set the height of your player" )
                                    
    ## RADIUS - Player specific
    scnType.datablock_radius = FloatProperty( name = "Radius",
                                      default = 0.4, min = 0.0, max=1.0,
                                    description = "Set the Radius of your player" )
    
    ## RUN SPEED - Player specific
    scnType.datablock_runSpeed = FloatProperty( name = "Run Speed",
                                      default = 6.0, min = 0.0, max=100.0,
                                    description = "Set the Run Speed of your player" )
                                    
    ## WALK SPEED - Player specific
    scnType.datablock_walkSpeed = FloatProperty( name = "Walk Speed",
                                      default = 3.0, min = 0.0, max=100.0,
                                    description = "Set the Walk Speed of your player" )
                                    
    ## TURN SPEED - Player specific
    scnType.datablock_turnSpeed = FloatProperty( name = "Turn Speed",
                                      default = 150.0, min = 0.0, max=1000.0,
                                    description = "Set the Walk Speed of your player" )

    # triplet setup.... ( return value, name, description )
    EnumProperty = bpy.props.EnumProperty
    datablockTypes= [("playerType", "Player", "Player Type Datablock"),
                    ("levelType", "Level", "Level Type Datablock"),
                    ("objectType", "Object", "Object Type Datablock"),
                    ("lightType", "Light", "Light Type Datablock")]
                    
    enumProp = EnumProperty( name = "Datablock Type", items = datablockTypes,
                    description = "Choose a Datablock" )
    
    scnType.dropDownProp = enumProp
    
    ## Control type selection:
    # basicControlType0 = basic_control_1st_person
    controlTypes = [("controlType0", "FPS Control Style", "FPS Control style"),
                    ("controlType1", "3RD Person Style", "3RD Person Control Style")]
                    
    controlType = EnumProperty( name = "Control Type", items = controlTypes,
                    description = "Choose a Control Type for the Player" )
  
    scnType.dropDownControl = controlType
    
    ## Light type selection:
    # point, direct, ambient, spot
    lightTypes = [("pointType", "Point Light", "Point Light Type"),
                    ("directType", "Directional Light", "Directional Light Type"),
                    ("ambientType", "Ambient Light", "Ambient Light Type"),
                    ("spotType", "Spot Light", "Spot Light Type")]
                    
    lightControlType = EnumProperty( name = "Light Type", items = lightTypes,
                    description = "Choose a Light Type" )
  
    scnType.dropDownLight = lightControlType
    
    ## Level Type
    # Wall, Ground
    levelSubTypes = [("wallType", "Wall", "Make this object a Wall"),
                    ("groundType", "Ground", "Make this object a ground")]
                    
    LevelSubControlType = EnumProperty( name = "Level Type", items = levelSubTypes,
                    description = "Choose a Level Type" )
  
    scnType.dropDownLevelType = LevelSubControlType
