
from big_ol_pile_of_manim_imports import *
from active_projects.eop.reusable_imports import *
from active_projects.eop.chapter1.brick_row_scene import BrickRowScene

class EntireBrickWall(BrickRowScene):

    def construct(self):

        self.remove(self.get_primary_pi_creature())

        row_height = 0.3
        nb_rows = 20
        start_point = 3 * UP + 1 * LEFT
        
        rows = VMobject()
        rows.add(BrickRow(0, height = row_height))
        rows.move_to(start_point)
        self.add(rows)
            
        zero_counter = Integer(0).next_to(start_point + 0.5 * rows[0].width * RIGHT)
        nb_flips_text = TextMobject("\# of flips")
        nb_flips_text.next_to(zero_counter, RIGHT, buff = LARGE_BUFF)
        self.add(zero_counter, nb_flips_text)
        flip_counters = VGroup(zero_counter)

        for i in range(1, nb_rows + 1):
            rows.add(rows[-1].copy())
            self.bring_to_back(rows[-1])
            anims = [
                rows[-1].shift, row_height * DOWN,
                Animation(rows[-2])
            ]
            
            if i % 5 == 0:
                counter = Integer(i)
                counter.next_to(rows[-1].get_right() + row_height * DOWN, RIGHT)
                flip_counters.add(counter)
                anims.append(FadeIn(counter))

            self.play(*anims)

            self.play(SplitRectsInBrickWall(rows[-1]))
            rows.submobjects[-1] = self.merge_rects_by_subdiv(rows[-1])
            rows.submobjects[-1] = self.merge_rects_by_coloring(rows[-1])



        # draw indices under the last row for the number of tails
        tails_counters = VGroup()
        for (i, rect) in enumerate(rows[-1].rects):
            if i < 6 or i > 14:
                continue
            if i == 6:
                counter = TexMobject("\dots", color = COLOR_TAILS)
                counter.next_to(rect, DOWN, buff = 1.5 * MED_SMALL_BUFF)
            elif i == 14:
                counter = TexMobject("\dots", color = COLOR_TAILS)
                counter.next_to(rect, DOWN, buff = 1.5 * MED_SMALL_BUFF)
                counter.shift(0.2 * RIGHT)
            else:
                counter = Integer(i, color = COLOR_TAILS)
                counter.next_to(rect, DOWN)
            tails_counters.add(counter)

        nb_tails_text = TextMobject("\# of tails", color = COLOR_TAILS)
        nb_tails_text.next_to(tails_counters[-1], RIGHT, buff = LARGE_BUFF)

        self.play(
            LaggedStart(FadeIn, tails_counters),
            FadeIn(nb_tails_text)
        )

        # remove any hidden brick rows
        hidden_brick_rows = VGroup(*[mob for mob in self.mobjects
            if isinstance(mob, BrickRow) and not mob in rows
        ])
        self.remove(hidden_brick_rows)

        mobs_to_shift = VGroup(
            rows, flip_counters, tails_counters, nb_tails_text, 
        )
        self.play(mobs_to_shift.shift, 3 * UP)

        last_row_rect = SurroundingRectangle(rows[-1], buff = 0)
        last_row_rect.set_stroke(color = YELLOW, width = 6)

        self.play(
            rows.fade, 0.9,
            ShowCreation(last_row_rect)
        )

        def highlighted_brick(row = 20, nb_tails = 10):
            brick_copy = rows[row].rects[nb_tails].copy()
            brick_copy.set_fill(color = YELLOW, opacity = 0.8)
            prob_percentage = float(choose(row, nb_tails)) / 2**row * 100
            brick_label = DecimalNumber(prob_percentage, unit = "\%", num_decimal_places = 1, color = BLACK)
            brick_label.move_to(brick_copy)
            brick_label.scale_to_fit_height(0.8 * brick_copy.get_height())
            return VGroup(brick_copy, brick_label)

        highlighted_bricks = [
            highlighted_brick(row = 20, nb_tails = i)
            for i in range(20)
        ]

        self.play(
            FadeIn(highlighted_bricks[10])
        )

        self.play(
            FadeOut(highlighted_bricks[10]),
            FadeIn(highlighted_bricks[9]),
            FadeIn(highlighted_bricks[11]),
        )

        self.play(
            FadeOut(highlighted_bricks[9]),
            FadeOut(highlighted_bricks[11]),
            FadeIn(highlighted_bricks[8]),
            FadeIn(highlighted_bricks[12]),
        )





















