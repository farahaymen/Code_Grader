ALIGNMENT_PROMPT = """
You are grading a programming assessment.

Your task:
1. Read the assessment question.
2. Read the student's code chunks.
3. Identify which chunks answer the question.
4. Return only the chunk IDs that are relevant.
5. A chunk can be relevant even if the implementation differs from the model answer.

Question:
{question_text}

Model answer:
{model_answer}

Student code chunks:
{chunks_text}

Return JSON with:
{{
  "matched_chunk_ids": ["C1", "C2"],
  "reasoning": "brief explanation",
  "confidence": 0.0
}}
"""

GRADING_PROMPT = """
You are grading a student's answer for one programming question.

Grade by the rubric and question requirements, not by similarity to the model answer.
Alternative correct implementations should receive credit.

Question:
{question_text}

Rubric:
{rubric_text}

Model answer:
{model_answer}

Relevant student code:
{student_code}

Taught material summary:
{material_text}

Return JSON:
{{
  "correctness_summary": "short paragraph",
  "rubric_scores": [
    {{
      "criterion_id": "R1",
      "awarded_marks": 0,
      "reason": "..."
    }}
  ],
  "confidence": 0.0,
  "needs_human_review": false
}}
"""