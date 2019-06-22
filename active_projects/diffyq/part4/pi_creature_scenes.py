from manimlib.imports import *


class WhyWouldYouCare(TeacherStudentsScene):
    def construct(self):
        self.student_says(
            "Who cares!",
            target_mode="sassy",
            student_index=2,
            added_anims=[self.teacher.change, "guilty"],
        )
        self.wait()
        self.play(
            RemovePiCreatureBubble(self.students[2]),
            self.teacher.change, "raise_right_hand",
            self.get_student_changes(
                "pondering", "erm", "thinking",
                look_at_arg=self.screen,
            )
        )
        self.look_at(self.screen)
        self.wait(5)


class HangOnThere(TeacherStudentsScene):
    def construct(self):
        student = self.students[2]

        axes1 = Axes(
            x_min=0,
            x_max=1,
            y_min=-1.5,
            y_max=1.5,
            x_axis_config={
                "tick_frequency": 0.25,
                "include_tip": False,
                "unit_size": 3,
            },
            y_axis_config={
                "tick_frequency": 0.5,
                "include_tip": False,
            },
        )
        axes1.set_stroke(width=2)
        axes2 = axes1.deepcopy()
        neq = TexMobject("\\neq")
        neq.scale(2)

        group = VGroup(axes1, neq, axes2)
        group.arrange(RIGHT)
        group.set_height(4)
        group.next_to(
            student.get_corner(UL), UP,
            buff=LARGE_BUFF,
        )

        step_graph = axes1.get_graph(
            lambda x: (1 if x < 0.5 else -1),
            discontinuities=[0.5],
        )
        step_graph.set_color(YELLOW)
        wave_graphs = VGroup(*[
            axes2.get_graph(
                lambda x: (4 / PI) * np.sum([
                    (u / n) * np.cos(n * PI * x)
                    for u, n in zip(
                        it.cycle([1, -1]),
                        range(1, max_n, 2),
                    )
                ]),
            )
            for max_n in range(3, 103, 2)
        ])
        wave_graphs.set_stroke(width=3)
        wave_graphs.set_color_by_gradient(WHITE, PINK)
        last_wave_graph = wave_graphs[-1]
        last_wave_graph.set_stroke(PINK, 2)
        wave_graphs.remove(last_wave_graph)
        # wave_graphs[-1].set_stroke(width=3)
        # wave_graphs[-1].set_stroke(BLACK, 5, background=True)
        group.add(step_graph)

        self.student_says(
            "Hang on\\\\hang on\\\\hang on...",
            target_mode="surprised",
            content_introduction_class=FadeIn,
            student_index=2,
            added_anims=[
                self.teacher.change, "guilty"
            ],
            run_time=1,
        )
        self.wait()
        self.play(
            RemovePiCreatureBubble(
                student,
                target_mode="raise_left_hand",
                look_at_arg=group,
            ),
            FadeInFromDown(group),
        )

        last_wg = VectorizedPoint()
        n_first_fades = 4
        for wg in wave_graphs[:n_first_fades]:
            self.play(
                last_wg.set_stroke, {"width": 0.1},
                FadeIn(wg),
            )
            last_wg = wg
        self.play(
            LaggedStart(
                *[
                    UpdateFromAlphaFunc(
                        wg,
                        lambda m, a: m.set_stroke(
                            width=(3 * there_and_back(a) + 0.1 * a)
                        ),
                    )
                    for wg in wave_graphs[n_first_fades:]
                ],
                run_time=5,
                lag_ratio=0.2,
            ),
            ApplyMethod(
                last_wg.set_stroke, {"width": 0.1},
                run_time=0.25,
            ),
            FadeIn(
                last_wave_graph,
                rate_func=squish_rate_func(smooth, 0.9, 1),
                run_time=5,
            ),
            self.teacher.change, "thinking",
        )
        self.change_student_modes(
            "confused", "confused", "angry"
        )
        self.wait(3)