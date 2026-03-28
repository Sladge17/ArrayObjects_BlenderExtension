from bpy.types import Operator, VIEW3D_PT_tools_active
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, FloatProperty, BoolProperty

import bpy


class OBJECT_OT_array_objects(Operator):
    bl_idname = "object.array_objects"
    bl_label = "Array objects"
    bl_description = "Create array of objects"
    bl_options = {'REGISTER', 'UNDO'}

    copy: BoolProperty(name="Copy")
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
        self.copy = True
        self.instance = False
        self.copy_prev = self.copy
        self.instance_prev = self.instance
        
        self.increment_x = True
        self.increment_y = True
        self.increment_z = True

        self.count_x = 1
        self.count_y = 1
        self.count_z = 1

        self.value_x = 0.0
        self.value_y = 0.0
        self.value_z = 0.0


    def check(self, context):
        if self.copy == False and self.copy_prev == True:
            self.copy = True

        if self.copy == True and self.copy_prev == False:
            self.copy_prev = True
            self.instance = False
            self.instance_prev = False

        if self.instance == False and self.instance_prev == True:
            self.instance = True

        if self.instance == True and self.instance_prev == False:
            self.instance_prev = True
            self.copy = False
            self.copy_prev = False


    def draw(self, context):
        row_instance = self.layout.row(align=True)
        row_instance.prop(
            self,
            'copy',
            text="Copy",
            toggle=1,
        )
        row_instance.prop(
            self,
            'instance',
            text="Instance",
            toggle=1,
        )

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



def add_button_array(self, context):
    row = self.layout.row()
    row.scale_x = 2.0
    row.scale_y = 2.0
    row.operator(
        OBJECT_OT_array_objects.bl_idname,
        text="",
        icon='MOD_ARRAY',
    )


def register():
    register_class(OBJECT_OT_array_objects)
    VIEW3D_PT_tools_active.append(add_button_array)


def unregister():
    VIEW3D_PT_tools_active.remove(add_button_array)
    unregister_class(OBJECT_OT_array_objects)



if __name__ == "__main__":
    register()
