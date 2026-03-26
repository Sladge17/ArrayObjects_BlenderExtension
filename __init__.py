from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, FloatProperty, BoolProperty

import bpy


class OBJECT_OT_object_multiplier(Operator):
    bl_idname = "object.object_multiplier"
    bl_label = "Object multiplier"
    bl_description = "Create array of objects"
    bl_options = {'REGISTER', 'UNDO'}

    count: IntProperty(name="Count", min=0)
    value: FloatProperty(name="Value")
    x: BoolProperty(name="X")


    @classmethod
    def poll(cls, context) -> bool:
        if not context.mode == 'OBJECT':
            cls.poll_message_set("Working mode is not OBJECT")
            return False
        
        if not len(context.selected_objects):
            cls.poll_message_set("Object not selected")
            return False

        cls.count = 0
        cls.value = 0.0
        return True


    def __init__(self, context):
        super().__init__(context)
        self.count = 0
        self.value = 0.0


    def execute(self, context):
        selected_object = context.selected_objects[0]
        for i in range(self.count):
            obj = bpy.data.objects.new(selected_object.name, selected_object.data.copy())
            obj.location = selected_object.location
            obj.rotation_euler = selected_object.rotation_euler
            obj.scale = selected_object.scale
            obj.location.x += self.value * (i + 1)
            bpy.data.collections['Collection'].objects.link(obj)

        return {'FINISHED'}



class VIEW3D_PT_object_multiplier(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Array tools"
    bl_label = "Object multiplier"


    def draw(self, context):
        self.layout.operator(
            operator="object.object_multiplier",
            text="Set array",
        )



def register():
    register_class(OBJECT_OT_object_multiplier)
    register_class(VIEW3D_PT_object_multiplier)


def unregister():
    unregister_class(VIEW3D_PT_object_multiplier)
    unregister_class(OBJECT_OT_object_multiplier)



if __name__ == "__main__":
    register()
