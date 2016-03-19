# Copyright (c) 2016 Nuxi, https://nuxi.nl/
#
# This file is distributed under a 2-clause BSD license.
# See the LICENSE file for details.


class Layout:

    def __init__(self, size, align=None):
        if align is None:
            align = size
        if not isinstance(size, tuple):
            size = (size, size)
        if not isinstance(align, tuple):
            align = (align, align)
        self.size = size
        self.align = align
        self.offset = None

    @staticmethod
    def struct(members):
        if members == [] or any(m.layout is None for m in members):
            return None

        align = (max(m.layout.align[0] for m in members),
                 max(m.layout.align[1] for m in members))

        offset = (0, 0)
        for m in members:
            m.offset = (_align(offset[0], m.layout.align[0]),
                        _align(offset[1], m.layout.align[1]))
            offset = (m.offset[0] + m.layout.size[0],
                      m.offset[1] + m.layout.size[1])

        size = (_align(offset[0], align[0]),
                _align(offset[1], align[1]))

        return Layout(size, align)

    @staticmethod
    def array(type, count):
        if type.layout is None:
            return None

        size = (type.layout.size[0] * count,
                type.layout.size[1] * count)

        return Layout(size, type.layout.align)

    @staticmethod
    def union(members):
        if members == [] or any(m.layout is None for m in members):
            return None

        size = (max(m.layout.size[0] for m in members),
                max(m.layout.size[1] for m in members))

        align = (max(m.layout.align[0] for m in members),
                 max(m.layout.align[1] for m in members))

        return Layout(size, align)


def _align(size, align):
    misalignment = size % align
    if misalignment == 0:
        return size
    else:
        return size + align - misalignment