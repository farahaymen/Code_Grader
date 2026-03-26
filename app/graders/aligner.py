import json
from app.schemas import Assessment, ParsedSubmission, QuestionAlignment
from app.llm.client import ask_llm_json
from app.llm.prompts import ALIGNMENT_PROMPT


def align_questions(assessment: Assessment, parsed: ParsedSubmission) -> list[QuestionAlignment]:
    results = []

    chunks_text = "\n\n".join(
        f"{c.chunk_id} | {c.chunk_type} | lines {c.start_line}-{c.end_line}\n{c.content}"
        for c in parsed.chunks
    )

    for q in assessment.questions:
        prompt = ALIGNMENT_PROMPT.format(
            question_text=q.text,
            model_answer=q.model_answer,
            chunks_text=chunks_text
        )
        response = ask_llm_json(prompt)

        results.append(QuestionAlignment(
            question_id=q.id,
            matched_chunk_ids=response["matched_chunk_ids"],
            reasoning=response["reasoning"],
            confidence=float(response["confidence"])
        ))

    return results