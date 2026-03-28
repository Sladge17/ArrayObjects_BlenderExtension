from bpy.types import Operator, VIEW3D_PT_tools_active
from bpy.utils import register_class, unregister_class
from bpy.props import IntProperty, FloatProperty, BoolProperty

import bpy


class OBJECT_OT_array_objects(Operator):
    bl_idname = "object.array_objects"
    bl_label = "Array objects"
    bl_description = "Create array of selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    copy: BoolProperty(name="Copy")
    instance: BoolProperty(name="Instance")

    increment_x: BoolProperty(name="increment X")
    total_x: BoolProperty(name="total X")
    count_x: IntProperty(name="Count X", min=1)
    value_x: FloatProperty(name="Value X")

    increment_y: BoolProperty(name="increment Y")
    total_y: BoolProperty(name="total Y")
    count_y: IntProperty(name="Count Y", min=1)
    value_y: FloatProperty(name="Value Y")

    increment_z: BoolProperty(name="increment Z")
    total_z: BoolProperty(name="total Z")
    count_z: IntProperty(name="Count Z", min=1)
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
        self.total_x = False
        self.increment_x_prev = self.increment_x
        self.total_x_prev = self.total_x
        self.count_x = 1
        self.value_x = 0.0

        self.increment_y = True
        self.total_y = False
        self.increment_y_prev = self.increment_y
        self.total_y_prev = self.total_y
        self.count_y = 1
        self.value_y = 0.0

        self.increment_z = True
        self.total_z = False
        self.increment_z_prev = self.increment_z
        self.total_z_prev = self.total_z
        self.count_z = 1
        self.value_z = 0.0


    def _check_copy_instance(self):
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


    def _check_increment_total_x(self):
        if self.increment_x == False and self.increment_x_prev == True:
            self.increment_x = True

        if self.increment_x == True and self.increment_x_prev == False:
            self.increment_x_prev = True
            self.total_x = False
            self.total_x_prev = False

        if self.total_x == False and self.total_x_prev == True:
            self.total_x = True

        if self.total_x == True and self.total_x_prev == False:
            self.total_x_prev = True
            self.increment_x = False
            self.increment_x_prev = False


    def _check_increment_total_y(self):
        if self.increment_y == False and self.increment_y_prev == True:
            self.increment_y = True

        if self.increment_y == True and self.increment_y_prev == False:
            self.increment_y_prev = True
            self.total_y = False
            self.total_y_prev = False

        if self.total_y == False and self.total_y_prev == True:
            self.total_y = True

        if self.total_y == True and self.total_y_prev == False:
            self.total_y_prev = True
            self.increment_y = False
            self.increment_y_prev = False


    def _check_increment_total_z(self):
        if self.increment_z == False and self.increment_z_prev == True:
            self.increment_z = True

        if self.increment_z == True and self.increment_z_prev == False:
            self.increment_z_prev = True
            self.total_z = False
            self.total_z_prev = False

        if self.total_z == False and self.total_z_prev == True:
            self.total_z = True

        if self.total_z == True and self.total_z_prev == False:
            self.total_z_prev = True
            self.increment_z = False
            self.increment_z_prev = False


    def check(self, context):
        self._check_copy_instance()
        self._check_increment_total_x()
        self._check_increment_total_y()
        self._check_increment_total_z()


    def draw(self, context):
        row_copy_instance = self.layout.row(align=True)
        row_copy_instance.prop(
            self,
            'copy',
            text="Copy",
            toggle=1,
        )
        row_copy_instance.prop(
            self,
            'instance',
            text="Instance",
            toggle=1,
        )


        box_x = self.layout.box()
        box_x.label(text="Axis X")
        row_increment_total_x = box_x.row(align=True)
        row_increment_total_x.prop(
            self,
            'increment_x',
            text="Increment",
            toggle=1,
        )
        row_increment_total_x.prop(
            self,
            'total_x',
            text="Tolal",
            toggle=1,
        )
        box_x.prop(self, 'count_x', text="Count")
        box_x.prop(self, 'value_x', text="Value")

        box_y = self.layout.box()
        box_y.label(text="Axis Y")
        row_increment_total_y = box_y.row(align=True)
        row_increment_total_y.prop(
            self,
            'increment_y',
            text="Increment",
            toggle=1,
        )
        row_increment_total_y.prop(
            self,
            'total_y',
            text="Tolal",
            toggle=1,
        )
        box_y.prop(self, 'count_y', text="Count")
        box_y.prop(self, 'value_y', text="Value")

        box_z = self.layout.box()
        box_z.label(text="Axis Z")
        row_increment_total_z = box_z.row(align=True)
        row_increment_total_z.prop(
            self,
            'increment_z',
            text="Increment",
            toggle=1,
        )
        row_increment_total_z.prop(
            self,
            'total_z',
            text="Tolal",
            toggle=1,
        )
        box_z.prop(self, 'count_z', text="Count")
        box_z.prop(self, 'value_z', text="Value")


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
