""" Vacuum tube elements for schematic drawing.

Recommended usage:
    V1 = Tube('12AX7', heaters=True)
    V2 = Tube('EL34', heaters=True)
    # Access anchors: V1.a1, V1.k2, V2.g2, etc.

Available tube types: 12AX7, ECC83, EL34, KT66 (see TUBE_SPECS for more)
"""

import math
from .elements import Element, gap
from ..segments import Segment, SegmentArc, SegmentText

tr_d = 2.5
tr_r = 0.5 * tr_d

grid_len = 0.5 * tr_d

anode_h = 0.5 * tr_r
anode_len = math.sqrt(tr_r**2 - anode_h**2)

cathode_h = anode_h
cathode_len = math.sqrt(tr_r**2 - cathode_h**2)
cathode_gap = math.sqrt(tr_r**2 - (cathode_len / 2) ** 2)
cathode_tail = 1 / 2 * (cathode_gap - cathode_h)

half_overhang = 12.5

dual_tr_gap =  0.75 * tr_r
dual_tr_grid_offset = 0.25

pent_gap = dual_tr_gap


class VacuumTube(Element):
    """
    Parent class for all the tubes defined below.

    Args:
        pin_nums: Show pin numbers at each anchor
        heaters: Whether to draw heater filaments
    """

    def __init__(self, *d, pin_nums: dict = None, heaters: bool = False, **kwargs):
        super().__init__(*d, **kwargs)

        self.pin_nums = pin_nums
        self.heaters = heaters

    def draw_heaters(self):
        """Draw heater filaments"""
        # Check tube type by class name
        class_name = self.__class__.__name__
        
        # Calculate center position based on tube type
        if class_name == "DualTriode":
            center_x = (tr_d + dual_tr_gap) / 2
        elif class_name == "Pentode":
            center_x = tr_d / 2
        else:
            # Single Triode or Rectifier
            x_extent, _ = self.params["drop"]
            center_x = x_extent / 2
        
        # Draw heaters (same logic for all tube types)
        self.segments.append(Segment([(center_x - 0.2, -0.2), (center_x, 0.2)]))
        self.segments.append(Segment([(center_x + 0.2, -0.2), (center_x, 0.2)]))

    def draw_pin_num(self, location, num):
        self.segments.append(SegmentText(location, str(num)))


class Triode(VacuumTube):
    """Triode Vacuum Tube.

    Args:
        pin_nums: Show pin numbers at each anchor
        half: Draw only half of the tube. "left" for left half, "right" for right half.

    Anchors:
        * g (grid)
        * k (cathode)
        * a (anode)
    """

    def __init__(self, *d, half: str = None, **kwargs):
        super().__init__(*d, **kwargs)

        self.half = half

        half_sign = 1 if self.half == "right" else -1

        # Decide whether to draw a full circle, left half, or right half based on 'half' argument
        theta1, theta2 = (0, 360)  # Default to full circle
        if self.half == "left":
            theta1, theta2 = (90 - half_overhang, 270 + half_overhang)
        elif self.half == "right":
            theta1, theta2 = (270 - half_overhang, 90 + half_overhang)

        # Draw the triode as a circular or semicircular shape using SegmentArc
        self.segments.append(
            SegmentArc(
                center=(tr_r, tr_r),
                width=tr_d,
                height=tr_d,
                theta1=theta1,
                theta2=theta2,
            )
        )

        # Grid lead as a dotted line
        self.segments.append(
            Segment(
                [
                    ((tr_d - grid_len) / 2, tr_r),
                    ((tr_d - grid_len) / 2 + grid_len, tr_r),
                ],
                ls="--",
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r + half_sign * tr_r, tr_r),
                    ((tr_d + half_sign * grid_len) / 2 + half_sign * 0.1, tr_r),
                ]
            )
        )

        # Anode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - anode_len / 2, tr_r + anode_h),
                    (tr_r + anode_len / 2, tr_r + anode_h),
                ]
            )
        )
        self.segments.append(Segment([(tr_r, tr_r + anode_h), (tr_r, tr_d)]))

        # Cathode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - cathode_len / 2, tr_r - cathode_h),
                    (tr_r + cathode_len / 2, tr_r - cathode_h),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r - half_sign * cathode_len / 2, tr_r - cathode_h),
                    (
                        tr_r - half_sign * cathode_len / 2,
                        tr_r - cathode_h - cathode_tail,
                    ),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r + half_sign * cathode_len / 2, tr_r - cathode_h),
                    (tr_r + half_sign * cathode_len / 2, tr_r - cathode_gap),
                ]
            )
        )

        # Defining the anchor points
        self.anchors["g"] = (tr_r + half_sign * tr_r, tr_r)  # Grid
        self.anchors["k"] = (
            tr_r + half_sign * cathode_len / 2,
            tr_r - cathode_gap,
        )  # Cathode
        self.anchors["a"] = (tr_r, tr_d)  # Anode
        self.params["drop"] = (tr_d, 0)

        # Add pin numbers if provided
        if self.pin_nums is not None:
            self.draw_pin_num(
                ((tr_d - half_sign * grid_len) / 2 - half_sign * 0.2, tr_r),
                self.pin_nums["g"],
            )
            self.draw_pin_num(
                (tr_r - half_sign * 0.2, tr_r + anode_h + 0.3),
                self.pin_nums["a"],
            )
            self.draw_pin_num((tr_r, tr_r - cathode_h - 0.3), self.pin_nums["k"])

        if self.heaters:
            self.draw_heaters()


class DualTriode(VacuumTube):
    """Dual Triode Vacuum Tube.

    Args:
        pin_nums: Show pin numbers at each anchor

    Anchors:
        * g1 (grid of first triode)
        * g2 (grid of second triode)
        * k1 (cathode of first triode)
        * k2 (cathode of second triode)
        * a1 (anode of first triode)
        * a2 (anode of second triode)
    """

    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)

        # Draw the triode outline
        self.segments.append(
            SegmentArc(
                center=(tr_r, tr_r),
                width=tr_d,
                height=tr_d,
                theta1=90,
                theta2=270,
            )
        )

        self.segments.append(Segment([(tr_r, 0), (tr_r + dual_tr_gap, 0)]))

        self.segments.append(Segment([(tr_r, tr_d), (tr_r + dual_tr_gap, tr_d)]))

        self.segments.append(
            SegmentArc(
                center=(tr_r + dual_tr_gap, tr_r),
                width=tr_d,
                height=tr_d,
                theta1=270,
                theta2=90,
            )
        )

        # Grid lead as dotted lines
        self.segments.append(
            Segment(
                [
                    (dual_tr_grid_offset + (tr_d - grid_len) / 2, tr_r),
                    (
                        dual_tr_grid_offset + (tr_d - grid_len) / 2 + 0.5 * grid_len,
                        tr_r,
                    ),
                ],
                ls="--",
            )
        )

        self.segments.append(
            Segment(
                [
                    (
                        (tr_d + dual_tr_gap)
                        - (dual_tr_grid_offset + (tr_d - grid_len) / 2),
                        tr_r,
                    ),
                    (
                        (tr_d + dual_tr_gap)
                        - (
                            dual_tr_grid_offset + (tr_d - grid_len) / 2 + 0.5 * grid_len
                        ),
                        tr_r,
                    ),
                ],
                ls="--",
            )
        )

        self.segments.append(
            Segment(
                [
                    (
                        tr_d + dual_tr_gap - (grid_len / 2) + 0.1 - dual_tr_grid_offset,
                        tr_r,
                    ),
                    (tr_d + dual_tr_gap, tr_r),
                ]
            )
        )

        self.segments.append(
            Segment(
                [
                    (0, tr_r),
                    ((tr_d - grid_len) / 2 - 0.1 + dual_tr_grid_offset, tr_r),
                ]
            )
        )

        # Anode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - anode_len / 2, tr_r + anode_h),
                    (tr_r + anode_len / 2 + dual_tr_gap, tr_r + anode_h),
                ]
            )
        )
        self.segments.append(Segment([(tr_r, tr_r + anode_h), (tr_r, tr_d)]))
        self.segments.append(
            Segment([(tr_r + dual_tr_gap, tr_r + anode_h), (tr_r + dual_tr_gap, tr_d)])
        )

        # Cathode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - cathode_len / 2, tr_r - cathode_h),
                    (tr_r + cathode_len / 2 + dual_tr_gap, tr_r - cathode_h),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r - cathode_len / 2, tr_r - cathode_h),
                    (tr_r - cathode_len / 2, tr_r - cathode_gap),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r + cathode_len / 2 + dual_tr_gap, tr_r - cathode_h),
                    (tr_r + cathode_len / 2 + dual_tr_gap, tr_r - cathode_gap),
                ]
            )
        )

        ## Defining the anchor points
        ## Defining the anchor points
        # Grids
        self.anchors["g1"] = (0, tr_r)  # Grids
        self.anchors["g2"] = (tr_d + dual_tr_gap, tr_r)

        # Cathodes
        self.anchors["k1"] = (
            tr_r - cathode_len / 2,
            tr_r - cathode_gap,
        )
        self.anchors["k2"] = (
            tr_r + cathode_len / 2 + dual_tr_gap,
            tr_r - cathode_gap,
        )

        # Anodes
        self.anchors["a1"] = (tr_r, tr_d)
        self.anchors["a2"] = (tr_r + dual_tr_gap, tr_d)

        # Drop point at grid 1 for better positioning
        self.params["drop"] = (0, tr_r)

        # Add pin numbers if provided
        if self.pin_nums is not None:
            # Grids
            self.draw_pin_num(
                (0.3, tr_r + 0.2),
                self.pin_nums["g1"],
            )
            self.draw_pin_num(
                (tr_d + dual_tr_gap - 0.3, tr_r + 0.2),
                self.pin_nums["g2"],
            )

            # Anodes
            self.segments.append(
                SegmentText(
                    (tr_r - 0.2, tr_r + anode_h + 0.3),
                    str(self.pin_nums["a1"]),
                )
            )
            self.draw_pin_num(
                (tr_r + dual_tr_gap + 0.2, tr_r + anode_h + 0.3),
                self.pin_nums["a2"],
            )

            # Cathodes
            self.draw_pin_num(
                (tr_r - cathode_gap / 2 + 0.3, tr_r - cathode_h - 0.3),
                self.pin_nums["k1"],
            )
            self.draw_pin_num(
                (
                    tr_r + cathode_gap / 2 + dual_tr_gap - 0.3,
                    tr_r - cathode_h - 0.3,
                ),
                self.pin_nums["k2"],
            )

        if self.heaters:
            self.draw_heaters()


class Pentode(VacuumTube):
    """Pentode Vacuum Tube.

    Args:
        pin_nums: Show pin numbers at each anchor

    Anchors:
        * g1 (grid)
        * g2 (screen grid)
        * g3 (suppressor grid)
        * k (cathode)
        * a (anode)
    """

    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)

        # Draw the pentode outline
        self.segments.append(
            SegmentArc(
                center=(tr_r, tr_r),
                width=tr_d,
                height=tr_d,
                theta1=180,
                theta2=0,
            )
        )

        self.segments.append(
            Segment(
                [
                    (0, tr_r),
                    (0, tr_r + pent_gap),
                ]
            )
        )

        self.segments.append(
            Segment(
                [
                    (tr_d, tr_r),
                    (tr_d, tr_r + pent_gap),
                ]
            )
        )

        self.segments.append(
            SegmentArc(
                center=(tr_r, tr_r + pent_gap),
                width=tr_d,
                height=tr_d,
                theta1=0,
                theta2=180,
            )
        )

        # Grid lead as a dotted line
        self.segments.append(
            Segment(
                [
                    ((tr_d - grid_len) / 2, tr_r),
                    ((tr_d + grid_len) / 2, tr_r),
                ],
                ls="--",
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_d, tr_r),
                    ((tr_d + grid_len) / 2 + 0.1, tr_r),
                ]
            )
        )

        # Screen grid as a dotted line
        self.segments.append(
            Segment(
                [
                    ((tr_d - grid_len) / 2, tr_r + pent_gap / 2),
                    ((tr_d + grid_len) / 2, tr_r + pent_gap / 2),
                ],
                ls="--",
            )
        )
        self.segments.append(
            Segment(
                [
                    (0, tr_r + pent_gap / 2),
                    (grid_len / 2 - 0.1, tr_r + pent_gap / 2),
                ]
            )
        )

        # Suppressor grid as a dotted line
        self.segments.append(
            Segment(
                [
                    ((tr_d - grid_len) / 2, tr_r + pent_gap),
                    ((tr_d + grid_len) / 2, tr_r + pent_gap),
                ],
                ls="--",
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_d, tr_r + pent_gap),
                    ((tr_d + grid_len) / 2 + 0.1, tr_r + pent_gap),
                ]
            )
        )

        # Anode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - anode_len / 2, tr_r + pent_gap + anode_h),
                    (tr_r + anode_len / 2, tr_r + pent_gap + anode_h),
                ]
            )
        )
        self.segments.append(
            Segment([(tr_r, tr_r + pent_gap + anode_h), (tr_r, tr_d + pent_gap)])
        )

        # Cathode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - cathode_len / 2, tr_r - cathode_h),
                    (tr_r + cathode_len / 2, tr_r - cathode_h),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r + cathode_len / 2, tr_r - cathode_h),
                    (
                        tr_r + cathode_len / 2,
                        tr_r - cathode_h - cathode_tail,
                    ),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r - cathode_len / 2, tr_r - cathode_h),
                    (tr_r - cathode_len / 2, tr_r - cathode_gap),
                ]
            )
        )

        # Defining the anchor points
        self.anchors["g1"] = (0, tr_r)  # Grid
        self.anchors["g2"] = (0, tr_r + pent_gap / 2)  # Screen
        self.anchors["g3"] = (0, tr_r + pent_gap)  # Suppressor
        self.anchors["k"] = (
            tr_r - cathode_len / 2,
            tr_r - cathode_gap,
        )  # Cathode
        self.anchors["a"] = (tr_r, tr_d + pent_gap)  # Anode
        self.params["drop"] = (0, tr_r)

        # Add pin numbers if provided
        if self.pin_nums is not None:
            self.draw_pin_num(
                (tr_r - grid_len / 2 - 0.2, tr_r),
                self.pin_nums["g1"],
            )

            self.draw_pin_num(
                (tr_d - grid_len / 2 + 0.2, tr_r + pent_gap / 2),
                self.pin_nums["g2"],
            )

            self.draw_pin_num(
                (tr_r - grid_len / 2 - 0.2, tr_r + pent_gap),
                self.pin_nums["g3"],
            )

            self.draw_pin_num(
                (tr_r + 0.2, tr_r + pent_gap + anode_h + 0.2),
                self.pin_nums["a"],
            )

            x_offset = 0.2 if self.heaters else 0
            self.draw_pin_num(
                (tr_r + x_offset, tr_r - cathode_h - 0.3), self.pin_nums["k"]
            )

        if self.heaters:
            self.draw_heaters()


class RectifierTube(VacuumTube):
    """Dual-diode tube rectifier.

    Anchors:
        * a1 (anode 1)
        * a2 (anode 2)
        * k (cathode)
        * h1, h2 (heaters)
    """
    def __init__(self, *d, pin_nums=None, heaters=True, **kwargs):
        super().__init__(*d, pin_nums=pin_nums, heaters=heaters, **kwargs)
        # Draw a basic envelope and two diodes (positioned so cathode is at origin)
        # Envelope (circle)
        r = 1.0
        self.segments.append(SegmentArc(center=(r, r), width=2*r, height=2*r, theta1=0, theta2=360))
        # Diode 1 (left)
        self.segments.append(Segment([(0.5, 1.5), (1, 1)]))  # Anode 1 to cathode
        self.segments.append(Segment([(1, 1), (1.5, 1.5)]))  # Cathode to anode 2
        # Diode 2 (right)
        self.segments.append(Segment([(1.5, 0.5), (1, 1)]))
        self.segments.append(Segment([(1, 1), (0.5, 0.5)]))
        # Heater leads
        self.segments.append(Segment([(0.7, 0.2), (0.7, 0.5)]))
        self.segments.append(Segment([(1.3, 0.2), (1.3, 0.5)]))
        # Anchors (positioned so cathode is at origin)
        self.anchors["a1"] = (-0.5, 0.5)
        self.anchors["a2"] = (0.5, -0.5)
        self.anchors["k"] = (0, 0)  # Cathode at origin
        self.anchors["h1"] = (-0.3, -0.8)
        self.anchors["h2"] = (0.3, -0.8)
        self.params["drop"] = (1, 0)
        # Pin numbers if provided
        if pin_nums:
            self.draw_pin_num(self.anchors["a1"], pin_nums.get("a1", ""))
            self.draw_pin_num(self.anchors["a2"], pin_nums.get("a2", ""))
            self.draw_pin_num(self.anchors["k"], pin_nums.get("k", ""))
            self.draw_pin_num(self.anchors["h1"], pin_nums.get("h1", ""))
            self.draw_pin_num(self.anchors["h2"], pin_nums.get("h2", ""))


TUBE_SPECS = {
    "12AX7": {
        "class": DualTriode,
        "pin_nums": {"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6},
        "anchors": ["g1", "k1", "a1", "g2", "k2", "a2"],
    },
    "12AT7": {
        "class": DualTriode,
        "pin_nums": {"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6},
        "anchors": ["g1", "k1", "a1", "g2", "k2", "a2"],
    },
    "12AU7": {
        "class": DualTriode,
        "pin_nums": {"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6},
        "anchors": ["g1", "k1", "a1", "g2", "k2", "a2"],
    },
    "12AY7": {
        "class": DualTriode,
        "pin_nums": {"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6},
        "anchors": ["g1", "k1", "a1", "g2", "k2", "a2"],
    },
    "ECC83": {
        "class": DualTriode,
        "pin_nums": {"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6},
        "anchors": ["g1", "k1", "a1", "g2", "k2", "a2"],
    },
    "ECC82": {
        "class": DualTriode,
        "pin_nums": {"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6},
        "anchors": ["g1", "k1", "a1", "g2", "k2", "a2"],
    },
    "ECC81": {
        "class": DualTriode,
        "pin_nums": {"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6},
        "anchors": ["g1", "k1", "a1", "g2", "k2", "a2"],
    },
    "ECC80": {
        "class": DualTriode,
        "pin_nums": {"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6},
        "anchors": ["g1", "k1", "a1", "g2", "k2", "a2"],
    },
    "EL34": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": 1, "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "KT66": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "KT88": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "6550": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "6L6": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "6L6GC": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "6V6": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "6V6GT": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "EL84": {
        "class": Pentode,
        "pin_nums": {"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8},
        "anchors": ["g1", "g2", "g3", "a", "k"],
    },
    "5AR4": {
        "class": RectifierTube,
        "pin_nums": {"a1": 4, "a2": 6, "k": 8, "h1": 2, "h2": 8},
        "anchors": ["a1", "a2", "k", "h1", "h2"],
    },
    "GZ34": {
        "class": RectifierTube,
        "pin_nums": {"a1": 4, "a2": 6, "k": 8, "h1": 2, "h2": 8},
        "anchors": ["a1", "a2", "k", "h1", "h2"],
    },
    "5Y3": {
        "class": RectifierTube,
        "pin_nums": {"a1": 4, "a2": 6, "k": 8, "h1": 2, "h2": 8},
        "anchors": ["a1", "a2", "k", "h1", "h2"],
    },
    "EZ81": {
        "class": RectifierTube,
        "pin_nums": {"a1": 1, "a2": 7, "k": 3, "h1": 4, "h2": 5},
        "anchors": ["a1", "a2", "k", "h1", "h2"],
    },
}

def Tube(tube_type, heaters=False, show_pins=False, **kwargs):
    """General vacuum tube element factory function.

    Args:
        tube_type: e.g. '12AX7', 'EL34', etc.
        heaters: Draw heater filaments
        show_pins: Show pin numbers
        **kwargs: Passed to the underlying tube class

    Returns:
        Instance of the appropriate tube class (DualTriode, Pentode, etc.)

    Example:
        V1 = Tube('12AX7', heaters=True)
        V2 = Tube('EL34', heaters=True)
        # Access anchors: V1.a1, V1.k2, V2.g2, etc.
    """
    spec = TUBE_SPECS.get(tube_type.upper())
    if not spec:
        raise ValueError(f"Unknown tube type: {tube_type}")
    tube_cls = spec["class"]
    pin_nums = spec["pin_nums"] if show_pins else None
    return tube_cls(heaters=heaters, pin_nums=pin_nums, **kwargs)
