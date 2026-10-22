
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_pdf_report(
    target_role,
    detected_skills,
    selected_job,
    recommendations,
    roadmap
):

    # STEP 1: Create PDF in memory
    buffer = BytesIO()

    # STEP 2: Configure the document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=19 * mm,
        title="AI Resume Analysis Report"
    )

    # STEP 3: Define text styles
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="MainHeadingCustom",
        parent=styles["Title"],
        fontSize=18,
        leading=23,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#17324D"),
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name="SectionCustom",
        parent=styles["Heading2"],
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=13,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name="TextCustom",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=5
    ))

    styles.add(ParagraphStyle(
        name="NoteCustom",
        parent=styles["BodyText"],
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#475569")
    ))

    # STEP 4: Add report title
    story = [
        Paragraph(
            "AI Resume Analysis Report",
            styles["MainHeadingCustom"]
        ),
        Paragraph(
            "Educational career guidance - "
            "not a hiring decision.",
            styles["NoteCustom"]
        ),
        Spacer(1, 10),
        Paragraph(
            "<b>Target role:</b> "
            + escape(target_role),
            styles["TextCustom"]
        )
    ]

    # STEP 5: Add match score table
    table = Table([
        [
            Paragraph(
                "<b>TF-IDF cosine similarity</b>",
                styles["TextCustom"]
            ),
            Paragraph(
                "<b>Required-skill coverage</b>",
                styles["TextCustom"]
            )
        ],
        [
            f"{selected_job['similarity']:.4f}",
            f"{selected_job['skill_coverage_percent']:.1f}%"
        ]
    ], colWidths=[87 * mm, 87 * mm])

    table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#EAF1F6")
        ),
        (
            "BOX",
            (0, 0),
            (-1, -1),
            0.5,
            colors.HexColor("#CBD5E1")
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),
        (
            "ALIGN",
            (0, 1),
            (-1, -1),
            "CENTER"
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            8
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            8
        )
    ]))

    story.extend([
        Spacer(1, 10),
        table
    ])

    # STEP 6: Reusable report section
    def add_section(heading, entries, empty_message):

        story.append(Paragraph(
            escape(heading),
            styles["SectionCustom"]
        ))

        for entry in entries or [empty_message]:

            story.append(Paragraph(
                "- " + escape(str(entry)),
                styles["TextCustom"]
            ))

    # STEP 7: Add detected skills
    add_section(
        "Detected technical skills",
        detected_skills,
        "No technical skills detected."
    )

    # STEP 8: Add matched skills
    add_section(
        "Matched required skills",
        selected_job["matched_skills"],
        "No matching required skills detected."
    )

    # STEP 9: Add missing skills
    add_section(
        "Required skills not detected",
        selected_job["missing_skills"],
        "All listed skills were detected."
    )

    # STEP 10: Add recommended jobs
    formatted_recommendations = [
        f"{number}. {role['job_role']} - "
        f"similarity {role['similarity']:.4f}, "
        f"coverage {role['skill_coverage_percent']:.1f}%"
        for number, role in enumerate(
            recommendations,
            start=1
        )
    ]

    add_section(
        "Top job recommendations",
        formatted_recommendations,
        "No role shares a detected required skill."
    )

    # STEP 11: Add learning roadmap
    story.append(Paragraph(
        "Four-week learning roadmap",
        styles["SectionCustom"]
    ))

    if not roadmap:

        story.append(Paragraph(
            "No missing required skills were detected. "
            "Consider demonstrating them through a project.",
            styles["TextCustom"]
        ))

    else:

        for week in roadmap:

            story.append(Paragraph(
                f"<b>Week {week['week']}: "
                f"{escape(str(week['focus']))}</b>",
                styles["TextCustom"]
            ))

            for task in week["activities"]:

                story.append(Paragraph(
                    "- " + escape(str(task)),
                    styles["TextCustom"]
                ))

    # STEP 12: Add responsible-AI explanation
    story.extend([
        Spacer(1, 10),
        Paragraph(
            "Scores estimate overlap in documented skills, "
            "not hiring suitability. Missing keywords do "
            "not necessarily mean missing ability.",
            styles["NoteCustom"]
        )
    ])

    # STEP 13: Add page numbers
    def footer(canvas, document):

        canvas.saveState()
        canvas.setFont("Helvetica", 8)

        canvas.drawRightString(
            A4[0] - 18 * mm,
            11 * mm,
            f"Page {document.page}"
        )

        canvas.restoreState()

    # STEP 14: Build the PDF
    doc.build(
        story,
        onFirstPage=footer,
        onLaterPages=footer
    )

    # STEP 15: Return the PDF bytes
    return buffer.getvalue()
