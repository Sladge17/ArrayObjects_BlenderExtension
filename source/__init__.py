from bpy.types import VIEW3D_PT_tools_active
from bpy.utils import register_class, unregister_class

from .operator_array_objects import OBJECT_OT_array_objects



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
