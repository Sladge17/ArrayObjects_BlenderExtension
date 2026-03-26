from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, FloatProperty, BoolProperty

import bpy


class OBJECT_OT_object_multiplier(Operator):
    bl_idname = "object.object_multiplier"
    bl_label = "Object multiplier"
    bl_description = "Create array of objects"
    bl_options = {'REGISTER', 'UNDO'}

    x: BoolProperty(name="X")
    y: BoolProperty(name="Y")
    z: BoolProperty(name="Z")

    count_x: IntProperty(name="Count_X", min=0)
    count_y: IntProperty(name="Count_Y", min=0)
    count_z: IntProperty(name="Count_Z", min=0)

    value_x: FloatProperty(name="Value X")
    value_y: FloatProperty(name="Value Y")
    value_z: FloatProperty(name="Value Z")


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


    def draw(self, context):
        row_axis = self.layout.row()
        column_x = self.layout.column()
        column_y = self.layout.column()
        column_z = self.layout.column()

        row_axis.prop(self, 'x')
        row_axis.prop(self, 'y')
        row_axis.prop(self, 'z')

        if self.x:
            column_x.label(text="Axis X")
            column_x.prop(self, 'count_x')
            column_x.prop(self, 'value_x')

        if self.y:
            column_y.label(text="Axis Y")
            column_y.prop(self, 'count_y')
            column_y.prop(self, 'value_y')

        if self.z:
            column_z.label(text="Axis Z")
            column_z.prop(self, 'count_z')
            column_z.prop(self, 'value_z')


    def _get_object_copy(self, target_object):
        obj = bpy.data.objects.new(target_object.name, target_object.data.copy())
        obj.location = target_object.location
        obj.rotation_euler = target_object.rotation_euler
        obj.scale = target_object.scale
        return obj
    
    
    def _get_oblect_copies_x(self, target_objects):
        copies = []
        for target_object in target_objects:
            for i in range(1, self.count_x):
                obj = self._get_object_copy(target_object)
                obj.location.x += self.value_x * i
                bpy.data.collections['Collection'].objects.link(obj)
                copies.append(obj)

        return copies


    def _get_oblect_copies_y(self, target_objects):
        copies = []
        for target_object in target_objects:
            for i in range(1, self.count_y):
                obj = self._get_object_copy(target_object)
                obj.location.y += self.value_y * i
                bpy.data.collections['Collection'].objects.link(obj)
                copies.append(obj)

        return copies


    def _get_oblect_copies_z(self, target_objects):
        copies = []
        for target_object in target_objects:
            for i in range(1, self.count_z):
                obj = self._get_object_copy(target_object)
                obj.location.z += self.value_z * i
                bpy.data.collections['Collection'].objects.link(obj)
                copies.append(obj)

        return copies



    def execute(self, context):
        target_objects = [context.active_object]
        if self.x:
            target_objects += self._get_oblect_copies_x(target_objects)

        if self.y:
            target_objects += self._get_oblect_copies_y(target_objects)

        if self.z:
            target_objects += self._get_oblect_copies_z(target_objects)

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
