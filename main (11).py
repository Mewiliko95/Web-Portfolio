import flet as ft
import base64
import os


def get_icon(name: str):
    icons = getattr(ft, "Icons", None) or getattr(ft, "icons")
    return getattr(icons, name)


def load_image_base64(path: str) -> str:
    # Try multiple path candidates and extensions
    base_candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), path),
        os.path.join(os.getcwd(), path),
        path,
    ]
    # Also try common image extensions if no extension given
    extensions = ["", ".jpeg", ".jpg", ".png", ".JPG", ".JPEG", ".PNG"]
    candidates = []
    for base in base_candidates:
        candidates.append(base)
        if not any(base.lower().endswith(ext.lower()) for ext in [".jpeg", ".jpg", ".png"]):
            for ext in extensions[1:]:
                candidates.append(base + ext)

    for abs_path in candidates:
        if os.path.exists(abs_path):
            try:
                with open(abs_path, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception as e:
                print(f"[ERROR] Could not read {abs_path}: {e}")
    print(f"[ERROR] Image not found: {path}")
    return ""


def main(page: ft.Page):
    page.title = "Ball Mill Load — Johanna Mewiliko Neyandje"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#c2185b"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 0

    primary   = "#ffffff"
    secondary = "#ff69b4"
    card      = "#ff69b4"
    panel     = "#d63384"
    text      = "#1a0a2e"
    subtext   = "#4a1030"

    # ── Load profile picture as base64 so it always shows ────────────────────
    profile_b64 = load_image_base64("assets/profile.jpeg")
    profile_src = f"data:image/jpeg;base64,{profile_b64}" if profile_b64 else ""

    def symmetric_padding(horizontal: int, vertical: int):
        return ft.Padding(horizontal, vertical, horizontal, vertical)

    def border_all(width: int, color: str):
        side = ft.BorderSide(width=width, color=color)
        return ft.Border(top=side, right=side, bottom=side, left=side)

    async def open_route(route: str):
        await page.push_route(route)

    def nav_link(label: str, section_key: str):
        route = "/" if section_key == "home" else f"/{section_key}"
        return ft.Button(
            label,
            color=text,
            bgcolor=panel,
            elevation=0,
            height=36,
            on_click=lambda _: page.run_task(open_route, route),
            style=ft.ButtonStyle(
                padding=ft.Padding(8, 6, 8, 6),
                text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
            ),
        )

    def section_title(label: str, title: str):
        return ft.Column(
            spacing=8,
            controls=[
                ft.Text(label, size=14, color=primary, weight=ft.FontWeight.BOLD),
                ft.Text(title, size=42, weight=ft.FontWeight.BOLD, color=text),
            ],
        )

    def feature_card(title: str, description: str, icon_name: str):
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=28,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Icon(get_icon(icon_name), size=38, color=primary),
                    ft.Text(title, size=22, weight=ft.FontWeight.BOLD, color=text),
                    ft.Text(description, size=16, color=subtext),
                ],
            ),
        )

    def stat_card(number: str, label: str):
        return ft.Container(
            bgcolor=card,
            padding=26,
            border_radius=12,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(number, size=38, weight=ft.FontWeight.BOLD, color=primary),
                    ft.Text(label, size=17, color=subtext),
                ],
            ),
        )

    # ── CERTIFICATES (actual uploads) ─────────────────────────────────────────
    certificates = [
        {
            "title": "MATLAB Onramp",
            "date": "19 March 2026",
            "description": "Completed 100% of the MathWorks MATLAB Onramp self-paced training course.",
            "image_path": "assets/certificates/MATLAB Onramp",
            "tag": "Onramp",
        },
        {
            "title": "Machine Learning Onramp",
            "date": "20 March 2026",
            "description": "Completed 100% of the MathWorks Machine Learning Onramp self-paced training course.",
            "image_path": "assets/certificates/Machine Learning Onramp",
            "tag": "Onramp",
        },
        {
            "title": "Simulink Onramp",
            "date": "27 April 2026",
            "description": "Completed 100% of the MathWorks Simulink Onramp self-paced training course.",
            "image_path": "assets/certificates/Simulink Onramp",
            "tag": "Onramp",
        },
        {
            "title": "Explore Data with MATLAB Plots",
            "date": "23 April 2026",
            "description": "Completed 100% of the Explore Data with MATLAB Plots course.",
            "image_path": "assets/certificates/Explore Data with MATLAB Plots",
            "tag": "Course",
        },
        {
            "title": "Make and Manipulate Matrices",
            "date": "3 April 2026",
            "description": "Completed 100% of the Make and Manipulate Matrices course.",
            "image_path": "assets/certificates/Make and Manipulate Matrices",
            "tag": "Course",
        },
        {
            "title": "Calculations with Vectors and Matrices",
            "date": "23 March 2026",
            "description": "Completed 100% of the Calculations with Vectors and Matrices course.",
            "image_path": "assets/certificates/Calculations with Vectors and Matrices",
            "tag": "Course",
        },
        {
            "title": "Deep Learning Onramp",
            "date": "18 April 2026",
            "description": "Completed 100% of the MathWorks Deep Learning Onramp self-paced training course.",
            "image_path": "assets/certificates/Deep Learning Onramp",
            "tag": "Onramp",
        },
    ]

    cert_dialog = ft.AlertDialog(
        modal=True,
        bgcolor=card,
        actions=[
            ft.TextButton(
                "Close",
                style=ft.ButtonStyle(color=primary),
                on_click=lambda _: close_dialog(),
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def close_dialog():
        cert_dialog.open = False
        page.update()

    def open_cert(cert: dict):
        b64 = load_image_base64(cert["image_path"])

        cert_dialog.title = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4,
            controls=[
                ft.Text(cert["title"], size=20, weight=ft.FontWeight.BOLD,
                        color=primary, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Completed: {cert['date']}", size=14,
                        color=subtext, text_align=ft.TextAlign.CENTER),
            ],
        )

        cert_dialog.content = ft.Container(
            width=700,
            height=470,
            alignment=ft.Alignment.CENTER,
            content=ft.Image(
                src=f"data:image/jpeg;base64,{b64}",
                fit=ft.BoxFit.CONTAIN,
                width=680,
                height=460,
            ) if b64 else ft.Text("Image not found", color="red"),
        )

        cert_dialog.open = True
        if cert_dialog not in page.overlay:
            page.overlay.append(cert_dialog)
        page.update()

    def tag_color(tag: str) -> str:
        return {
            "Onramp":        "#00d9ff",
            "Learning Path": "#7b2cbf",
            "Course":        "#00b894",
        }.get(tag, primary)

    def cert_card(cert: dict):
        tc = tag_color(cert["tag"])
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=22,
            border=border_all(1, secondary),
            expand=True,
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Container(
                        bgcolor="#e91e8c",
                        border_radius=20,
                        padding=ft.Padding(10, 4, 10, 4),
                        border=border_all(1, tc),
                        content=ft.Text(
                            cert["tag"],
                            size=11,
                            color=tc,
                            weight=ft.FontWeight.BOLD,
                        ),
                        alignment=ft.Alignment.CENTER_LEFT,
                    ),
                    ft.Icon(get_icon("VERIFIED"), size=34, color=primary),
                    ft.Text(cert["title"], size=17, weight=ft.FontWeight.BOLD, color=text),
                    ft.Text(cert["description"], size=13, color=subtext),
                    ft.Text(cert["date"], size=12, color=primary, italic=True),
                    ft.ElevatedButton(
                        "View Certificate",
                        bgcolor=primary,
                        color="#000000",
                        on_click=lambda _, c=cert: open_cert(c),
                        style=ft.ButtonStyle(
                            padding=ft.Padding(10, 6, 10, 6),
                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
                        ),
                    ),
                ],
            ),
        )

    nav_items = [
        ("HOME",     "home"),
        ("ABOUT",    "about"),
        ("TIMELINE", "timeline"),
        ("MATLAB",   "matlab"),
        ("HISTORY",  "history"),
        ("BLOG",     "blog"),
        ("GITHUB",   "github"),
        ("CONTACT",  "contact"),
    ]
    page.appbar = ft.AppBar(
        title=ft.Text("Ball Mill Load", size=28, weight=ft.FontWeight.BOLD, color=primary),
        bgcolor=panel,
        toolbar_height=76,
        actions=[nav_link(label, key) for label, key in nav_items],
        actions_padding=ft.Padding(0, 0, 28, 0),
    )

    # ─── HERO ────────────────────────────────────────────────────────────────
    hero_section = ft.Container(
        key="home",
        padding=symmetric_padding(horizontal=50, vertical=60),
        content=ft.ResponsiveRow(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    spacing=20,
                    controls=[
                        ft.Text("WELCOME", size=18, color=secondary, weight=ft.FontWeight.BOLD),
                        ft.Text("Johanna Mewiliko Neyandje", size=52, weight=ft.FontWeight.BOLD, color=text),
                        ft.Text(
                            "GitHub Manager · Ball Mill Load · UNAM Mining Student, 3rd Year Extended",
                            size=22, color=subtext,
                        ),
                        ft.Row(
                            spacing=16,
                            wrap=True,
                            controls=[
                                ft.Button("Hire Me", bgcolor=primary, color="#000000",
                                          on_click=lambda _: page.run_task(open_route, "/contact")),
                                ft.Button("View Projects",
                                          style=ft.ButtonStyle(color=ft.Colors.WHITE),
                                          on_click=lambda _: page.run_task(open_route, "/timeline")),
                            ],
                        ),
                    ],
                ),
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=340, height=340, border_radius=170,
                            border=border_all(5, primary),
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=profile_src,
                                width=340, height=340,
                                fit=ft.BoxFit.COVER,
                            ) if profile_src else ft.Container(width=340, height=340, bgcolor=panel),
                        )
                    ],
                ),
            ],
        ),
    )

    features = ft.Container(
        padding=symmetric_padding(horizontal=40, vertical=30),
        content=ft.ResponsiveRow(
            run_spacing=20,
            controls=[
                ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                    "GitHub Management",
                    "Responsible for managing the team's GitHub repository — creating branches, "
                    "reviewing pull requests, resolving merge conflicts, and maintaining a clean commit history throughout the project.",
                    "CODE"
                )]),
                ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                    "Stress Analysis Engine",
                    "Ball Mill Load calculates structural stress on mill supports using σ = F/A, "
                    "classifying results as Safe (<50 MPa), Warning (50–80 MPa), or Critical (>80 MPa).",
                    "CALCULATE"
                )]),
                ft.Column(col={"md": 4, "sm": 12, "xs": 12}, controls=[feature_card(
                    "Safety & Load Planning",
                    "Helps mining engineers quickly estimate whether the applied load on a ball mill support "
                    "is within safe limits — preventing structural damage and costly downtime.",
                    "ENGINEERING"
                )]),
            ],
        ),
    )

    # ─── ABOUT ───────────────────────────────────────────────────────────────
    about_section = ft.Container(
        key="about",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.ResponsiveRow(
            run_spacing=24,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    controls=[
                        ft.Container(
                            width=480, height=360, border_radius=12,
                            border=border_all(3, primary),
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                            content=ft.Image(
                                src=profile_src,
                                width=480, height=360,
                                fit=ft.BoxFit.COVER,
                            ) if profile_src else ft.Container(width=480, height=360, bgcolor=panel),
                        )
                    ],
                ),
                ft.Column(
                    col={"md": 6, "sm": 12, "xs": 12},
                    spacing=20,
                    controls=[
                        section_title("ABOUT ME", "GitHub Manager & Mining Engineering Student"),
                        ft.Text(
                            "I am a third-year extended program Mining Engineering student at UNAM. "
                            "As part of my Computer Programming I module, I contributed to building Ball Mill Load — "
                            "a mobile app that calculates structural stress on ball mill supports to determine whether loads are Safe, Warning, or Critical.",
                            size=18, color=subtext,
                        ),
                        ft.Text(
                            "My role as GitHub Manager meant I was responsible for the entire version control workflow: "
                            "setting up the repository, managing branches, reviewing and merging pull requests, "
                            "and ensuring the team's code history remained clean and traceable throughout the project.",
                            size=18, color=subtext,
                        ),
                        ft.Container(
                            bgcolor="#b0003a",
                            border_radius=10,
                            padding=ft.Padding(18, 14, 18, 14),
                            border=border_all(1, "#ffffff"),
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Row(spacing=10, controls=[
                                        ft.Icon(get_icon("INFO"), size=20, color="#ffffff"),
                                        ft.Text("A Note on Group Contributions", size=15,
                                                weight=ft.FontWeight.BOLD, color="#ffffff"),
                                    ]),
                                    ft.Text(
                                        "During this semester project, our group faced coordination challenges due to "
                                        "conflicting assessment schedules across different modules. Our Project Manager "
                                        "took responsibility for ensuring the project was delivered on time by leading "
                                        "the technical implementation herself. As a result, the commit history primarily "
                                        "reflects her activity.",
                                        size=14, color="#f8bbd9",
                                    ),
                                    ft.Text(
                                        "All group members contributed through their designated roles. As GitHub Manager, "
                                        "I maintained the repository structure, managed branches, and supported the team "
                                        "throughout. This reflects the reality of many real-world engineering projects, "
                                        "where one team member often drives the core implementation while others contribute "
                                        "in essential supporting roles. Rather than risk errors and wasted time, we aligned "
                                        "behind our Project Manager to keep the project moving forward.",
                                        size=14, color="#f8bbd9",
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )

    stats = ft.Container(
        padding=symmetric_padding(horizontal=40, vertical=30),
        content=ft.ResponsiveRow(
            run_spacing=20,
            controls=[
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("1",  "Project")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("8",  "Commits")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("3",  "Pull Requests")]),
                ft.Column(col={"md": 3, "sm": 6, "xs": 12}, controls=[stat_card("7",  "Certificates")]),
            ],
        ),
    )

    # ─── TIMELINE ────────────────────────────────────────────────────────────
    timeline_cards = [
        (
            "Week 1–2 (02–13 Mar): Project Ideation & Repository Setup",
            "Our team came together to brainstorm a practical engineering app. After evaluating several ideas, "
            "we settled on Ball Mill Load — a mobile app to help mining engineers quickly assess whether the load "
            "on a ball mill support is safe, using the core formula σ = F/A. "
            "I was assigned the role of GitHub Manager. I created the GitHub repository (UNAM-I3691CP), "
            "set up the folder structure (/src, /docs, /designs, /assets), added all team members as collaborators, "
            "wrote the initial README.md, and shared the repository URL with Mr. Abisai by end of Week 2."
        ),
        (
            "Week 3–4 (16–27 Mar): Pitch Week & Idea Registration",
            "Our group presented three app ideas to Mr. Abisai during Pitch Week. "
            "Ball Mill Load was the idea selected and officially registered. "
            "As GitHub Manager, I committed the Signed Idea Registration Form and initial pitch notes to the /docs folder "
            "and created a dedicated feature branch structure ready for the SRS phase. "
            "Branch protection rules were applied to main to prevent unreviewed pushes."
        ),
        (
            "Week 5–6 (30 Mar–10 Apr): SRS Phase — Requirements & Firebase Model",
            "The team began writing the System Requirements Specification (SRS). "
            "I managed the /docs folder on GitHub, ensuring that each section committed by the Documentation Lead "
            "was reviewed and merged cleanly. I resolved merge conflicts between SRS drafts pushed by different team members "
            "and maintained a consistent file naming convention throughout the document folder."
        ),
        (
            "Week 7–8 (13–25 Apr): SRS Finalisation & Submission",
            "The team completed the SRS — including non-functional requirements and use case diagrams. "
            "I performed a final review of all /docs commits before the 25 April 23:59 deadline, "
            "ensured the final PDF (GroupName_SRS_I3691CP.pdf) was committed to GitHub and submitted on the UNAM portal. "
            "I also audited the repository to confirm all team members had at least 2 meaningful commits in the SRS phase."
        ),
        (
            "Week 9–10 (27 Apr–08 May): Prototype Phase — Figma Screens",
            "As the UI/UX Lead worked in Figma, I managed the /designs folder on GitHub. "
            "I committed the first batch of exported PNG screens (onboarding, login, dashboard) and set up "
            "a consistent naming convention for all design exports. "
            "I reviewed pull requests from the UI/UX Lead and ensured all screen exports were properly "
            "organised and linked to their corresponding functional requirements."
        ),
        (
            "Week 11–12 (11–30 May): Prototype Completion & Submission",
            "All remaining Figma screens were exported and committed to /designs. "
            "I prepared the GitHub repository for the prototype submission deadline (30 May 23:59) — "
            "verifying that the shareable Figma link, exported PNGs, and design rationale document "
            "were all committed and organised. I also ran a test EAS Build in Week 12 to identify "
            "any configuration issues before the final submission week."
        ),
        (
            "Week 13–14 (01–13 Jun): Progress Demo, Final Sprint & APK Submission",
            "During the progress demo (Week 13), I ensured the GitHub repository showed a meaningful "
            "multi-author commit history for Mr. Abisai's review. In the final sprint (Week 14), "
            "I merged all remaining feature branches into main, reviewed the final codebase, "
            "and managed the EAS Build process to produce the installable Android APK. "
            "The complete final submission package — APK, updated SRS, User Manual, Figma link, "
            "Individual Contribution Report, and Group Declaration Form — was submitted by 13 June 23:59."
        ),
    ]

    timeline_section = ft.Container(
        key="timeline",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Text("Project Timeline", size=42, weight=ft.FontWeight.BOLD, color=text),
                *[
                    ft.Container(
                        bgcolor=card, padding=24, border_radius=12, border=border_all(1, primary),
                        content=ft.Column(spacing=8, controls=[
                            ft.Text(week, size=23, weight=ft.FontWeight.BOLD, color=primary),
                            ft.Text(description, color=subtext, size=16),
                        ]),
                    )
                    for week, description in timeline_cards
                ],
            ],
        ),
    )

    # ─── MATLAB SECTION ──────────────────────────────────────────────────────
    matlab_section = ft.Container(
        key="matlab",
        bgcolor=panel,
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=28,
            controls=[
                ft.Text("MATLAB Achievement Hub", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text(
                    "All 7 MathWorks certificates earned by Johanna Mewiliko Neyandje — click any card to view the full certificate.",
                    size=16, color=subtext,
                ),
                ft.Text("Onramp Certificates", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[0])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[1])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[2])]),
                    ],
                ),
                ft.Text("MATLAB Courses", size=20, weight=ft.FontWeight.BOLD, color=primary),
                ft.ResponsiveRow(
                    run_spacing=20,
                    controls=[
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[3])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[4])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[5])]),
                        ft.Column(col={"md": 4, "sm": 6, "xs": 12}, controls=[cert_card(certificates[6])]),
                    ],
                ),
            ],
        ),
    )

    # ─── BLAST HISTORY SECTION ───────────────────────────────────────────────
    history_records = [
        {
            "id": "BML-001",
            "date": "2 May 2026",
            "site": "UNAM Lab — Test Session A",
            "load_kg": "5,000 kg",
            "area": "0.12 m²",
            "force": "49,050 N",
            "stress": "408.75 kPa (0.41 MPa)",
            "material": "Mild Steel",
            "result": "SAFE",
        },
        {
            "id": "BML-002",
            "date": "9 May 2026",
            "site": "UNAM Lab — Test Session B",
            "load_kg": "18,000 kg",
            "area": "0.05 m²",
            "force": "176,580 N",
            "stress": "3.53 MPa",
            "material": "Cast Iron",
            "result": "WARNING",
        },
        {
            "id": "BML-003",
            "date": "16 May 2026",
            "site": "UNAM Lab — Test Session C",
            "load_kg": "45,000 kg",
            "area": "0.03 m²",
            "force": "441,450 N",
            "stress": "14.72 MPa",
            "material": "Mild Steel",
            "result": "CRITICAL",
        },
    ]

    def danger_color(level: str) -> str:
        return {
            "SAFE":     "#00b894",
            "WARNING":  "#fdcb6e",
            "CRITICAL": "#d63031",
        }.get(level, primary)

    def history_card(rec: dict):
        dc = danger_color(rec["result"])
        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=24,
            border=border_all(1, secondary),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(rec["id"], size=18, weight=ft.FontWeight.BOLD, color=primary),
                            ft.Container(
                                bgcolor=dc,
                                border_radius=20,
                                padding=ft.Padding(12, 4, 12, 4),
                                content=ft.Text(
                                    rec["result"], size=12,
                                    color="#000000", weight=ft.FontWeight.BOLD,
                                ),
                            ),
                        ],
                    ),
                    ft.Text(f"📅 {rec['date']}  |  📍 {rec['site']}", size=13, color=subtext),
                    ft.Divider(color="#1a0a2e", thickness=1),
                    ft.ResponsiveRow(
                        run_spacing=6,
                        controls=[
                            ft.Column(col={"md": 4, "xs": 12}, controls=[
                                ft.Text(f"Load:         {rec['load_kg']}", size=13, color=text),
                                ft.Text(f"Support Area: {rec['area']}", size=13, color=text),
                                ft.Text(f"Force (F=mg): {rec['force']}", size=13, color=text),
                            ]),
                            ft.Column(col={"md": 4, "xs": 12}, controls=[
                                ft.Text(f"Stress (σ=F/A): {rec['stress']}", size=13, color=text),
                                ft.Text(f"Material:       {rec['material']}", size=13, color=text),
                            ]),
                            ft.Column(col={"md": 4, "xs": 12}, controls=[
                                ft.Text(f"Result:  {rec['result']}", size=13, color=dc,
                                        weight=ft.FontWeight.BOLD),
                            ]),
                        ],
                    ),
                ],
            ),
        )

    history_section = ft.Container(
        key="history",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=24,
            controls=[
                ft.Text("Load Analysis History", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text(
                    "Ball Mill Load keeps a complete, auditable record of every stress analysis session. "
                    "Each entry captures all inputs and outputs so mining engineers can review, "
                    "compare, and learn from past calculations. Managed by Johanna Mewiliko Neyandje.",
                    size=16, color=subtext,
                ),
                *[history_card(r) for r in history_records],
            ],
        ),
    )

    # ─── BLOG ────────────────────────────────────────────────────────────────
    blog_section = ft.Container(
        key="blog",
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=24,
            controls=[
                ft.Text("Technical Blog", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text("Confidence in Concepts — written technical explanations with video inserts.",
                        size=16, color=subtext),
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Icon(get_icon("CODE"), size=38, color=primary),
                            ft.Text("Confidence in Python OOP", size=22,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "Object Oriented Programming (OOP) is a programming approach that "
                                "organises code into classes and objects. A class is like a blueprint "
                                "and an object is an instance of that blueprint. In Ball Mill Load, "
                                "we created classes such as StressSession that holds properties like "
                                "load, support area, material type, calculated stress, and safety result.",
                                size=15, color=subtext,
                            ),
                            ft.Text(
                                "The three main pillars of OOP are inheritance, encapsulation and "
                                "polymorphism. Inheritance allows a child class to reuse code from a "
                                "parent class. Encapsulation hides internal data from outside access. "
                                "Polymorphism allows different classes to be used through the same "
                                "interface. We applied these concepts throughout the Ball Mill Load project.",
                                size=15, color=subtext,
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=card,
                    border_radius=12,
                    padding=28,
                    border=border_all(1, secondary),
                    content=ft.Column(
                        spacing=14,
                        controls=[
                            ft.Icon(get_icon("STORAGE"), size=38, color=primary),
                            ft.Text("Understanding Data Structures", size=22,
                                    weight=ft.FontWeight.BOLD, color=text),
                            ft.Text(
                                "Data structures are ways of organising and storing data in a program "
                                "so that it can be accessed and modified efficiently. In Ball Mill Load, "
                                "we use lists and dictionaries to store blast history records "
                                "fetched from Firestore before displaying them to the user.",
                                size=15, color=subtext,
                            ),
                            ft.Text(
                                "A stack follows Last In First Out (LIFO) — useful for undo operations. "
                                "A queue follows First In First Out (FIFO) — like a sequence of blast events. "
                                "In the history module, we store blast records as dictionaries inside a list, "
                                "making it easy to filter by date, site, or danger level.",
                                size=15, color=subtext,
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=card,
                    padding=28,
                    border_radius=12,
                    border=border_all(1, primary),
                    content=ft.Column(
                        spacing=16,
                        controls=[
                            ft.Icon(get_icon("FUNCTIONS"), size=38, color=primary),
                            ft.Text("Ball Mill Load — Mathematical Notation", size=28,
                                    weight=ft.FontWeight.BOLD, color=primary),
                            ft.Text(
                                "The core of Ball Mill Load is stress analysis. Below are the key formulas "
                                "used to determine whether a ball mill support is safe:",
                                size=15, color=subtext,
                            ),
                            ft.Text("① Convert Load to Force", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Text("F = m × g", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Where m = mass in kg, g = 9.81 m/s² (gravitational acceleration). "
                                "This converts the load weight into a force in Newtons (N).",
                                size=13, color=subtext, italic=True),
                            ft.Divider(color="#1a0a2e"),
                            ft.Text("② Calculate Stress on Support", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Text("σ = F / A", size=17, color=text, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "Where σ = stress (Pa or MPa), F = force (N), A = support area (m²). "
                                "This is the fundamental stress formula.",
                                size=13, color=subtext, italic=True),
                            ft.Divider(color="#1a0a2e"),
                            ft.Text("③ Safety Classification", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Text("Safe:     σ < 50 MPa", size=17, color="#00b894", weight=ft.FontWeight.BOLD),
                            ft.Text("Warning:  50 MPa ≤ σ ≤ 80 MPa", size=17, color="#fdcb6e", weight=ft.FontWeight.BOLD),
                            ft.Text("Critical: σ > 80 MPa", size=17, color="#d63031", weight=ft.FontWeight.BOLD),
                            ft.Divider(color="#1a0a2e"),
                            ft.Text("④ Final Result (Core Formula)", size=16, color=primary, weight=ft.FontWeight.BOLD),
                            ft.Container(
                                bgcolor="#e91e8c",
                                border_radius=10,
                                padding=ft.Padding(20, 14, 20, 14),
                                border=border_all(1, primary),
                                content=ft.Text(
                                    "σ = (m × g) / A",
                                    size=22, color=primary, weight=ft.FontWeight.BOLD,
                                ),
                            ),
                            ft.Text(
                                "This single formula tells the engineer exactly how much stress the ball mill support is experiencing. "
                                "If the result exceeds safe thresholds for the material, the app flags it as Warning or Critical "
                                "so corrective action can be taken before structural damage or costly downtime occurs. "
                                "All sessions are recorded in the Ball Mill Load history for future reference.",
                                size=14, color=subtext,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    # ─── MEDIA BOX HELPER ────────────────────────────────────────────────────
    def open_local_video(path: str):
        try:
            if os.name == "nt":
                os.startfile(path)
            else:
                import webbrowser
                webbrowser.open(f"file://{path}")
        except Exception as e:
            print(f"[ERROR] Cannot open video file: {e}")

    def media_box(title: str, description: str, icon_name: str,
                  image_path: str = "", video_url: str = "", local_video_path: str = ""):
        if image_path:
            b64 = load_image_base64(image_path)
            media_content = ft.Image(
                src=f"data:image/jpeg;base64,{b64}",
                fit=ft.BoxFit.CONTAIN,
                width=460,
                height=260,
                border_radius=8,
            ) if b64 else ft.Text("Image not found", color="red", size=13)
        elif local_video_path:
            # Resolve absolute path for local video file
            abs_video = os.path.join(os.path.dirname(os.path.abspath(__file__)), local_video_path)
            if not os.path.exists(abs_video):
                abs_video = os.path.join(os.getcwd(), local_video_path)
            media_content = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=14,
                controls=[
                    ft.Icon(get_icon("PLAY_CIRCLE"), size=54, color=primary),
                    ft.Text("Local video asset ready", size=14, color=subtext, italic=True),
                    ft.Button(
                        "▶ Open Video File",
                        bgcolor=primary,
                        color="#000000",
                        on_click=lambda _, p=abs_video: open_local_video(p),
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD),
                        ),
                    ),
                ],
            )
        elif video_url:
            media_content = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
                controls=[
                    ft.Icon(get_icon("PLAY_CIRCLE"), size=54, color=primary),
                    ft.Text("Video evidence attached", size=13, color=subtext),
                    ft.ElevatedButton(
                        "▶ Watch Video",
                        bgcolor=primary,
                        color="#000000",
                        on_click=lambda _, u=video_url: __import__('webbrowser').open(u),
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=13, weight=ft.FontWeight.BOLD)),
                    ),
                ],
            )
        else:
            media_content = ft.Container(
                width=460, height=240, border_radius=8,
                border=ft.Border(
                    top=ft.BorderSide(2, "#444444"), bottom=ft.BorderSide(2, "#444444"),
                    left=ft.BorderSide(2, "#444444"), right=ft.BorderSide(2, "#444444"),
                ),
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.Icon(get_icon("UPLOAD_FILE"), size=50, color="#555555"),
                        ft.Text("Upload your evidence here", size=14, color="#777777"),
                        ft.Text("screenshot · video · image", size=12, color="#555555", italic=True),
                    ],
                ),
            )

        return ft.Container(
            bgcolor=card,
            border_radius=12,
            padding=24,
            border=border_all(1, secondary),
            content=ft.Column(
                spacing=14,
                controls=[
                    ft.Row(spacing=12, controls=[
                        ft.Icon(get_icon(icon_name), size=32, color=primary),
                        ft.Text(title, size=19, weight=ft.FontWeight.BOLD, color=text),
                    ]),
                    ft.Text(description, size=13, color=subtext),
                    ft.Divider(color="#1a0a2e", thickness=1),
                    media_content,
                ],
            ),
        )

    # ─── GITHUB SECTION ──────────────────────────────────────────────────────
    github_section = ft.Container(
        key="github",
        bgcolor=panel,
        padding=symmetric_padding(horizontal=50, vertical=50),
        content=ft.Column(
            spacing=28,
            controls=[
                ft.Text("GitHub Evidence", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text(
                    "GitHub contributions for Ball Mill Load are displayed below. "
                    "To add evidence, set image_path='assets/your_file.jpg' or "
                    "video_url='https://youtube.com/...' inside each box in the code.",
                    size=15, color=subtext,
                ),
                media_box(
                    title="Commit History",
                    description="Screenshots of GitHub commits to the Ball Mill Load repository, "
                                "showing weekly contributions and repository management over the project period.",
                    icon_name="HISTORY",
                    image_path="",
                    video_url="",
                ),
                media_box(
                    title="Pull Request & Merge",
                    description="Evidence of pull requests being reviewed and successfully merged "
                                "into the main Ball Mill Load branch as GitHub Manager.",
                    icon_name="MERGE_TYPE",
                    image_path="",
                    video_url="",
                ),
                media_box(
                    title="App Demo & Stress Result Feature",
                    description="A live walkthrough of Ball Mill Load running — showing load inputs, stress calculation, "
                                "Safe/Warning/Critical result, and the history record being saved in real time.",
                    icon_name="INSIGHTS",
                    image_path="",
                    video_url="",
                    local_video_path="assets/WIN_20260615_15_28_28_Pro.mp4",
                ),
            ],
        ),
    )

    # ─── CONTACT ─────────────────────────────────────────────────────────────
    contact_section = ft.Container(
        key="contact",
        padding=symmetric_padding(horizontal=50, vertical=60),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Text("Contact Me", size=42, weight=ft.FontWeight.BOLD, color=text),
                ft.Text("Available for freelance work and engineering projects.", size=18, color=subtext,
                        text_align=ft.TextAlign.CENTER),
                ft.TextField(width=500, label="Your Name",  bgcolor=card, border_color=primary, color=text),
                ft.TextField(width=500, label="Your Email", bgcolor=card, border_color=primary, color=text),
                ft.TextField(width=500, min_lines=4, max_lines=6, multiline=True, label="Message",
                             bgcolor=card, border_color=primary, color=text),
                ft.Button("Send Message", bgcolor=primary, color="#000000"),
            ],
        ),
    )

    footer = ft.Container(
        padding=30,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(
            "© 2026 Ball Mill Load — Johanna Mewiliko Neyandje (GitHub Manager) · All Rights Reserved",
            color=subtext,
        ),
    )

    pages = {
        "home":     [hero_section, features],
        "about":    [about_section, stats],
        "timeline": [timeline_section],
        "matlab":   [matlab_section],
        "history":  [history_section],
        "blog":     [blog_section],
        "github":   [github_section],
        "contact":  [contact_section],
    }

    def render_route(_=None):
        section  = page.route.strip("/") or "home"
        controls = pages.get(section, pages["home"])
        page.controls.clear()
        page.add(ft.Column(spacing=0, controls=[*controls, footer]))
        page.update()

    page.on_route_change = render_route
    render_route()


if __name__ == "__main__":
    ft.run(main, web_renderer=ft.WebRenderer.CANVAS_KIT, assets_dir="assets")
