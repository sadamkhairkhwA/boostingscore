"""Map practice level (1–3) to feedback language complexity (CEFR-style)."""


def feedback_language_instruction(level: int) -> str:
    """
    Instruction appended to AI system prompts so written feedback matches learner level.
    Level 1 ≈ A2–B1 simple English; 2 ≈ B1–B2; 3 ≈ B2+ / exam-ready terminology OK.
    """
    if level <= 1:
        return (
            "\n\nFEEDBACK LANGUAGE (required): The student is on practice LEVEL 1 "
            "(about CEFR A2–B1). Write ALL explanations in very simple English: short "
            "sentences, common everyday words, and easy structure. If you use a test word "
            "(like 'cohesion' or 'overview'), immediately explain it in simple words. "
            "No difficult jargon. Sound friendly and clear."
        )
    if level == 2:
        return (
            "\n\nFEEDBACK LANGUAGE (required): The student is on practice LEVEL 2 "
            "(about CEFR B1–B2). Use clear, natural English. You may use some IELTS words "
            "but add a short simple explanation the first time (e.g. in parentheses)."
        )
    return (
        "\n\nFEEDBACK LANGUAGE (required): The student is on practice LEVEL 3 (B2+). "
        "You may use normal IELTS / examiner vocabulary and fuller detail."
    )
