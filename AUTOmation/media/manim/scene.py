#!/usr/bin/env python3
"""
AUTOmation Pipeline Flow — Manim scene

Shows the content automation pipeline:
  Recording -> Transcript -> Scene Plan -> Animation -> Social Post

Usage:
    source media/manim/manim-env/bin/activate
    manim scene.py AutomationFlow -pql

Flags:
    -p    preview (open the video)
    -q l    low quality (fast render)
    -ql   (same as -q l)
"""

from manim import *


class AutomationFlow(Scene):
    """Animated pipeline: Recording -> Transcript -> Scene Plan -> Animation -> Social Post"""

    def construct(self):
        # Title
        title = Text("AUTOmation Pipeline", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Pipeline stages
        stages = [
            "Recording",
            "Transcript",
            "Scene Plan",
            "Animation",
            "Social Post",
        ]

        # Colors for each stage
        colors = [BLUE_D, TEAL_D, GOLD_D, PINK, GREEN_D]

        # Create boxes for each stage
        boxes = []
        labels = []
        arrows = []

        for i, (stage, color) in enumerate(zip(stages, colors)):
            box = RoundedRectangle(
                corner_radius=0.3,
                width=3,
                height=1.2,
                color=color,
                fill_opacity=0.2,
            )
            box.move_to(DOWN * 1.5 + UP * (2 - i * 0.8))
            label = Text(stage, font_size=20, color=color)
            label.move_to(box.get_center())

            boxes.append(box)
            labels.append(label)

        # Draw first box and label
        self.play(FadeIn(boxes[0]), Write(labels[0]))
        self.wait(0.3)

        # Draw arrows and remaining boxes sequentially
        for i in range(1, len(stages)):
            arrow = Arrow(
                start=boxes[i - 1].get_bottom(),
                end=boxes[i].get_top(),
                color=WHITE,
                stroke_width=2,
            )
            arrows.append(arrow)
            self.play(GrowArrow(arrow))
            self.play(FadeIn(boxes[i]), Write(labels[i]))
            self.wait(0.3)

        # Highlight all stages in sequence
        for i, box in enumerate(boxes):
            self.play(
                box.animate.set_fill_opacity(0.5),
                labels[i].animate.scale(1.2),
            )
            self.wait(0.5)
            self.play(
                box.animate.set_fill_opacity(0.2),
                labels[i].animate.scale(1.0),
            )

        # Fade out
        self.wait(1)
        self.play(
            *[FadeOut(arrow) for arrow in arrows],
            *[FadeOut(box) for box in boxes],
            *[FadeOut(label) for label in labels],
        )
        self.play(FadeOut(title))
        self.wait(1)
