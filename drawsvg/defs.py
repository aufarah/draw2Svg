"""SVG element definitions that are intended to go between the <defs></defs>
tag.
"""

from .elements import DrawingElement, DrawingParentElement


class DrawingDef(DrawingParentElement):
    """Parent class of SVG nodes that must be direct children of <defs>."""
    def get_svg_defs(self):
        return (self,)

class DrawingDefSub(DrawingParentElement):
    """Parent class of SVG nodes that are meant to be descendants of a def
    element."""
    pass

class LinearGradient(DrawingDef):
    """A linear gradient to use as a fill or other color.

    Has <stop> nodes as children.

    See also:
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/linearGradient
    """
    TAG_NAME = 'linearGradient'
    def __init__(self, x1, y1, x2, y2, gradientUnits='userSpaceOnUse',
                 **kwargs):
        y_shift = 0
        if gradientUnits != 'userSpaceOnUse':
            y_shift = 1
        try: y1 = y_shift - y1
        except TypeError: pass
        try: y2 = y_shift - y2
        except TypeError: pass
        super().__init__(x1=x1, y1=y1, x2=x2, y2=y2,
                         gradientUnits=gradientUnits, **kwargs)
    def add_stop(self, offset, color, opacity=None, **kwargs):
        stop = GradientStop(offset=offset, stop_color=color,
                            stop_opacity=opacity, **kwargs)
        self.append(stop)
        return stop

class RadialGradient(DrawingDef):
    """A radial gradient to use as a fill or other color.

    Has <stop> nodes as children.

    See also:
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element/radialGradient
    """
    TAG_NAME = 'radialGradient'
    def __init__(self, cx, cy, r, gradientUnits='userSpaceOnUse', fy=None,
                 **kwargs):
        y_shift = 0
        if gradientUnits != 'userSpaceOnUse':
            y_shift = 1
        try: cy = y_shift - cy
        except TypeError: pass
        try: fy = y_shift - fy
        except TypeError: pass
        super().__init__(cx=cx, cy=cy, r=r, gradientUnits=gradientUnits,
                         fy=fy, **kwargs)
    def add_stop(self, offset, color, opacity=None, **kwargs):
        stop = GradientStop(offset=offset, stop_color=color,
                            stop_opacity=opacity, **kwargs)
        self.append(stop)

class GradientStop(DrawingDefSub):
    """A control point for a radial or linear gradient.

    See also: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/stop
    """
    TAG_NAME = 'stop'
    has_content = False

class ClipPath(DrawingDef):
    """A shape used to crop another element by not drawing outside of this
    shape.

    Has regular drawing elements as children.

    See also: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/clipPath
    """
    TAG_NAME = 'clipPath'

class Mask(DrawingDef):
    """A drawing where the gray value and transparency are used to control the
    transparency of another shape.

    Has regular drawing elements as children.

    See also: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/mask
    """
    TAG_NAME = 'mask'

class Filter(DrawingDef):
    """A filter to apply to geometry.

    For example a blur filter.

    See also: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/filter
    """
    TAG_NAME = 'filter'

class FilterItem(DrawingDefSub):
    """A child of Filter with any tag name.

    See also:
    https://developer.mozilla.org/en-US/docs/Web/SVG/Element#filter_primitive_elements
    """
    def __init__(self, tag_name, **args):
        super().__init__(**args)
        self.TAG_NAME = tag_name

class Marker(DrawingDef):
    """A small drawing that can be placed at the ends of (or along) a path.

    This can be used for arrow heads or points on a graph for example.

    By default, units are multiples of stroke width.

    See also: https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker
    """
    TAG_NAME = 'marker'
    def __init__(self, minx, miny, maxx, maxy, scale=1, orient='auto',
                 **kwargs):
        width = maxx - minx
        height = maxy - miny
        kwargs = {
            'markerWidth': width if scale == 1 else float(width) * scale,
            'markerHeight': height if scale == 1 else float(height) * scale,
            'viewBox': '{} {} {} {}'.format(minx, -maxy, width, height),
            'orient': orient,
            **kwargs,
        }
        super().__init__(**kwargs)
