
from pedemath.matrix import Matrix44
from pedemath.quat import invert_quat
from pedemath.quat import lerp_quat
from pedemath.quat import Quat
from pedemath.vec3 import Vec3
from pedemath.vec3 import neg_v3
from pedemath.vec3 import sub_v3


def invert_transform(transform):
    return Transform(neg_v3(transform.pos), invert_quat(transform.rot))


def lerp_transform(transform1, transform2, percent):

    dist_vec = sub_v3(transform2.pos, transform1.pos)
    dist_vec.scale(percent)

    rot = lerp_quat(transform1.rot, transform2.rot, percent)

    return Transform(transform1.pos + dist_vec, rot)


class Transform(object):
    """ Define a common api for a transform.

    # TODO: trying set and get, possibly move to attribute
    """

    def __init__(self, pos=None, rot=None):

        if not pos:
            pos = Vec3(0, 0, 0)

        self.pos = Vec3(*pos)

        if not rot:
            rot = Quat()

        self.rot = Quat(*rot)

        # Optional parent transform
        # self.parent = None

    def transform(self, target):
        """Transform the target and return it's new value.
        It may be a Vec3 point or a Transform"""

        if isinstance(target, Vec3):
            return self.pos + target
        elif isinstance(target, Transform):
            # TODO: maybe rotate the position as well?
            return Transform(self.pos + target.pos, target.rot * self.rot)
        else:
            raise Exception("Unhandled type %s" % type(target))

    def transform_in_place(self, point):
        # TODO: add in rotation
        point += self.pos

    def make_ident(self):

        self.pos.set(0, 0, 0)
        self.rot.make_ident()

    def is_ident(self):
        return (self.pos.x == 0 and self.pos.y == 0 and self.pos.z == 0 and
                self.rot.is_ident())

    def set_pos_rot(self, pos, rot):
        self.pos.set(*pos)
        self.rot.set(*rot)

    def set(self, transform):
        self.pos.set(*transform.pos)
        self.rot.set(*transform.rot)

    def __eq__(self, transform):
        # print "COMPARE:", self.pos , transform.pos , self.rot , transform.rot
        # print self.pos == transform.pos , self.rot == transform.rot
        return self.pos == transform.pos and self.rot == transform.rot

    def __getitem__(self, index):
        """Allow to be treated as an array [pos, rot]
        For example, at index 0, return pos.
        Raise IndexError if index is invalid.
        """

        if (index == 0):
            return self.pos
        elif (index == 1):
            return self.rot

        raise IndexError("Vector index out of range")

    def __setitem__(self, index, value):
        """Allow to be treated as an array [pos, rot]
        For example, at index 0, set pos to value.
        Return the value that is set.
        Raise IndexError if index is invalid.
        """

        if (index == 0):
            self.pos = value
            return self.pos
        elif (index == 1):
            self.rot = value
            return self.rot

        raise IndexError("Vector index out of range")

    def __len__(self):
        return 2

    def get_matrix44(self):
        """
        Create a matrix to represent the transform.

        Combine the rotation and translation with a matrix multiply:
            transform_matrix = rot_matrix * translation_matrix
        """

        trans_mat = Matrix44.from_trans(self.pos)
        mat = self.rot.as_matrix44()

        # Basically: matrix = rot matrix * trans matrix
        mat *= trans_mat

        return mat
