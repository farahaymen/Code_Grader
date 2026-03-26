from app.schemas import Assessment, GradingReport
from app.analyzers.python_parser import parse_python_submission
from app.graders.aligner import align_questions
from app.graders.scope_checker import check_out_of_scope_usage
from app.graders.correctness import grade_questions


def run_grading_pipeline(assessment: Assessment, student_code: str) -> GradingReport:
    parsed = parse_python_submission(student_code)
    scope_flags = check_out_of_scope_usage(assessment, parsed)
    alignments = align_questions(assessment, parsed)
    per_question = grade_questions(assessment, parsed, alignments, scope_flags)

    total_awarded = sum(q.total_awarded for q in per_question)
    max_total = sum(q.max_marks for q in assessment.questions)

    summary = (
        f"Submission graded across {len(per_question)} questions. "
        f"Total score: {total_awarded}/{max_total}."
    )

    return GradingReport(
        assessment_title=assessment.title,
        per_question=per_question,
        total_awarded=total_awarded,
        max_total=max_total,
        summary=summary
    )