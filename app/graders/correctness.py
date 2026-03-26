from app.schemas import (
    Assessment,
    ParsedSubmission,
    QuestionAlignment,
    QuestionGrade,
    RubricScore,
)
from app.llm.client import ask_llm_json
from app.llm.prompts import GRADING_PROMPT


def grade_questions(assessment: Assessment, parsed: ParsedSubmission, alignments, scope_flags) -> list[QuestionGrade]:
    grades = []

    for q in assessment.questions:
        alignment = next(a for a in alignments if a.question_id == q.id)
        matched_chunks = [c for c in parsed.chunks if c.chunk_id in alignment.matched_chunk_ids]
        matched_code = "\n\n".join(
            f"{c.chunk_id} | lines {c.start_line}-{c.end_line}\n{c.content}"
            for c in matched_chunks
        )

        rubric_text = "\n".join(
            f"{r.id}: {r.description} ({r.max_marks} marks)"
            for r in q.rubric
        )

        prompt = GRADING_PROMPT.format(
            question_text=q.text,
            rubric_text=rubric_text,
            model_answer=q.model_answer,
            student_code=matched_code,
            material_text=assessment.taught_material.raw_text[:4000]
        )

        response = ask_llm_json(prompt)

        rubric_scores = [
            RubricScore(
                criterion_id=item["criterion_id"],
                awarded_marks=float(item["awarded_marks"]),
                reason=item["reason"]
            )
            for item in response["rubric_scores"]
        ]

        question_scope_flags = [f for f in scope_flags if f.question_id == q.id]
        total_awarded = sum(item.awarded_marks for item in rubric_scores)

        grades.append(QuestionGrade(
            question_id=q.id,
            matched_chunk_ids=alignment.matched_chunk_ids,
            correctness_summary=response["correctness_summary"],
            rubric_scores=rubric_scores,
            total_awarded=min(total_awarded, q.max_marks),
            out_of_scope_flags=question_scope_flags,
            confidence=float(response["confidence"]),
            needs_human_review=bool(response["needs_human_review"])
        ))

    return grades