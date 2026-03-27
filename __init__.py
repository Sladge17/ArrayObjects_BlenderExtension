from bpy.types import Operator, Panel
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, FloatProperty, BoolProperty

import bpy


class OBJECT_OT_objects_array(Operator):
    bl_idname = "object.object_multiplier"
    bl_label = "Object multiplier"
    bl_description = "Create array of objects"
    bl_options = {'REGISTER', 'UNDO'}

    instance: BoolProperty(name="Instance")

    increment_x: BoolProperty(name="increment X", default=True)
    increment_y: BoolProperty(name="increment Y", default=True)
    increment_z: BoolProperty(name="increment Z", default=True)

    count_x: IntProperty(name="Count X", min=1, default=1)
    count_y: IntProperty(name="Count Y", min=1, default=1)
    count_z: IntProperty(name="Count Z", min=1, default=1)

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

        return True


    def __init__(self, context):
        super().__init__(context)

        self.increment_x = True
        self.increment_y = True
        self.increment_z = True

        self.count_x = 1
        self.count_y = 1
        self.count_z = 1

        self.value_x = 0.0
        self.value_y = 0.0
        self.value_z = 0.0


    def draw(self, context):
        self.layout.prop(self, 'instance')

        column_x = self.layout.column()
        column_y = self.layout.column()
        column_z = self.layout.column()

        column_x.label(text="Axis X")
        column_x.prop(self, 'increment_x')
        column_x.prop(self, 'count_x')
        column_x.prop(self, 'value_x')

        column_y.label(text="Axis Y")
        column_y.prop(self, 'increment_y')
        column_y.prop(self, 'count_y')
        column_y.prop(self, 'value_y')

        column_z.label(text="Axis Z")
        column_z.prop(self, 'increment_z')
        column_z.prop(self, 'count_z')
        column_z.prop(self, 'value_z')


    def _get_object_copy(self, target_object):
        if self.instance:
            obj = bpy.data.objects.new(target_object.name, target_object.data)
        else:
            obj = bpy.data.objects.new(target_object.name, target_object.data.copy())

        obj.location = target_object.location
        obj.rotation_euler = target_object.rotation_euler
        obj.scale = target_object.scale
        return obj
    
    
    def _get_oblect_copies_x(self, target_objects):
        copies = []
        if self.count_x == 1 or self.increment_x:
            increment_x = self.value_x
        else:
            increment_x = self.value_x / (self.count_x - 1)

        for target_object in target_objects:
            for i in range(1, self.count_x):
                obj = self._get_object_copy(target_object)
                obj.location.x += increment_x * i
                bpy.data.collections['Collection'].objects.link(obj)
                copies.append(obj)

        return copies


    def _get_oblect_copies_y(self, target_objects):
        copies = []
        if self.count_y == 1 or self.increment_y:
            increment_y = self.value_y
        else:
            increment_y = self.value_y / (self.count_y - 1)

        for target_object in target_objects:
            for i in range(1, self.count_y):
                obj = self._get_object_copy(target_object)
                obj.location.y += increment_y * i
                bpy.data.collections['Collection'].objects.link(obj)
                copies.append(obj)

        return copies


    def _get_oblect_copies_z(self, target_objects):
        copies = []
        if self.count_z == 1 or self.increment_z:
            increment_z = self.value_z
        else:
            increment_z = self.value_z / (self.count_z - 1)

        for target_object in target_objects:
            for i in range(1, self.count_z):
                obj = self._get_object_copy(target_object)
                obj.location.z += increment_z * i
                bpy.data.collections['Collection'].objects.link(obj)
                copies.append(obj)

        return copies


    def execute(self, context):
        target_objects = [context.active_object]
        target_objects += self._get_oblect_copies_x(target_objects)
        target_objects += self._get_oblect_copies_y(target_objects)
        target_objects += self._get_oblect_copies_z(target_objects)

        return {'FINISHED'}



class VIEW3D_PT_objects_array(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Array tools"
    bl_label = "Objects array"


    def draw(self, context):
        self.layout.operator(
            operator="object.object_multiplier",
            text="Set array",
        )



def register():
    register_class(OBJECT_OT_objects_array)
    register_class(VIEW3D_PT_objects_array)


def unregister():
    unregister_class(VIEW3D_PT_objects_array)
    unregister_class(OBJECT_OT_objects_array)



if __name__ == "__main__":
    register()
