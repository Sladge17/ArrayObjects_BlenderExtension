import bpy


class OBJECT_OT_object_multiplyer(bpy.types.Operator):
    """Processing useless nodes!!!"""
    bl_idname = "object.object_multiplyer"
    bl_label = "Object multiplyer"
    bl_description = "Processing useless nodes)))"
    bl_options = {'REGISTER'}


    def _clear_scene(self) -> None:
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj, do_unlink=True)

        bpy.ops.outliner.orphans_purge()


    def _add_cube(self, position: list = None) -> None:
        vertices = [
            [-1.0, -1.0, 1.0],
            [-1.0, 1.0, 1.0],
            [-1.0, -1.0, -1.0],
            [-1.0, 1.0, -1.0],
            [1.0, -1.0, 1.0],
            [1.0, 1.0, 1.0],
            [1.0, -1.0, -1.0],
            [1.0, 1.0, -1.0],
        ]

        edges = []

        faces = [
            [0, 1, 3],
            [0, 3, 2],
            [2, 3, 7],
            [2, 7, 6],
            [6, 7, 5],
            [6, 5, 4],
            [4, 5, 1],
            [4, 1, 0],
            [2, 6, 4],
            [2, 4, 0],
            [7, 3, 1],
            [7, 1, 5],
        ]

        mesh_cube = bpy.data.meshes.new(name="MeshCube")
        mesh_cube.from_pydata(
            vertices=vertices,
            edges=edges,
            faces=faces,
        )

        object_cube = bpy.data.objects.new(
            name="ObjectCube",
            object_data=mesh_cube,
        )

        bpy.data.collections['Collection'].objects.link(object=object_cube)


    def execute(self, context):
        self._clear_scene()
        self._add_cube()
        return {'FINISHED'}



def register():
    bpy.utils.register_class(OBJECT_OT_object_multiplyer)



def unregister():
    bpy.utils.unregister_class(OBJECT_OT_object_multiplyer)


if __name__ == "__main__":
    register()
