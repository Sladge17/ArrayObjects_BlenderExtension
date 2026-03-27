import bpy

from bpy.props import FloatProperty, BoolProperty, EnumProperty



class OBJECT_OT_movement_XYZ(bpy.types.Operator):
    """Movement XYZ coord"""
    bl_idname = "object.movement_xyz"
    bl_label = "Movement XYZ"
    bl_description = "Movement XYZ coord"
    bl_options = {'REGISTER', 'UNDO'}

    direction: EnumProperty(
        items=[
            ("X", "X direction", "Description X direction"),
            ("Y", "Y direction", "Description Y direction"),
            ("Z", "Z direction", "Description Z direction"),
        ],
        default="X",
    )
    offset: FloatProperty()
    reverse: BoolProperty()


    def _get_sign(self):
        sign = 1
        if self.reverse:
            sign = -1

        return sign        


    @classmethod
    def poll(cls, context) -> bool:
        if not context.mode == 'OBJECT':
            cls.poll_message_set("Working mode is not OBJECT")
            return False
        
        if not len(context.selected_objects):
            cls.poll_message_set("Object not selected")
            return False

        return True


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        self.layout.prop(self, 'direction')
        self.layout.prop(self, 'offset')
        self.layout.prop(self, 'reverse')


    def execute(self, context):

        sign = self._get_sign()
        if self.direction == 'X':
            for obj in context.selected_objects:
                obj.location.x = obj.location.x + self.offset * sign

        if self.direction == 'Y':
            for obj in context.selected_objects:
                obj.location.y = obj.location.y + self.offset * sign

        if self.direction == 'Z':
            for obj in context.selected_objects:
                obj.location.z = obj.location.z + self.offset * sign

        self.report({'INFO'}, "Objects moved")
        return {'FINISHED'}




class VIEW3D_PT_movement_XYZ(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Example tool"
    bl_label = "Movement XYZ"


    def draw(self, context):
        self.layout.operator(
            operator="object.movement_xyz",
            text="Movement",
        )



def register():
    bpy.utils.register_class(OBJECT_OT_movement_XYZ)
    bpy.utils.register_class(VIEW3D_PT_movement_XYZ)



def unregister():
    bpy.utils.unregister_class(VIEW3D_PT_movement_XYZ)
    bpy.utils.unregister_class(OBJECT_OT_movement_XYZ)


if __name__ == "__main__":
    register()
