from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class RubricCriterion(BaseModel):
    id: str
    description: str
    max_marks: float


class Question(BaseModel):
    id: str
    text: str
    max_marks: float
    rubric: List[RubricCriterion]
    model_answer: str


class TaughtMaterial(BaseModel):
    raw_text: str
    allowed_libraries: List[str] = Field(default_factory=list)
    explicitly_taught_functions: List[str] = Field(default_factory=list)
    restricted_libraries: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class Assessment(BaseModel):
    title: str
    questions: List[Question]
    taught_material: TaughtMaterial


class CodeChunk(BaseModel):
    chunk_id: str
    chunk_type: Literal["import", "function", "class", "statement", "cell", "unknown"]
    start_line: int
    end_line: int
    content: str
    symbol_name: Optional[str] = None


class ParsedSubmission(BaseModel):
    language: str
    imports: List[str]
    functions: List[str]
    classes: List[str]
    chunks: List[CodeChunk]
    raw_code: str


class QuestionAlignment(BaseModel):
    question_id: str
    matched_chunk_ids: List[str]
    reasoning: str
    confidence: float


class ScopeFlag(BaseModel):
    question_id: str
    item: str
    item_type: Literal["library", "function", "pattern", "api"]
    evidence_chunk_ids: List[str]
    reason: str
    severity: Literal["info", "warning"] = "info"


class RubricScore(BaseModel):
    criterion_id: str
    awarded_marks: float
    reason: str


class QuestionGrade(BaseModel):
    question_id: str
    matched_chunk_ids: List[str]
    correctness_summary: str
    rubric_scores: List[RubricScore]
    total_awarded: float
    out_of_scope_flags: List[ScopeFlag]
    confidence: float
    needs_human_review: bool = False


class GradingReport(BaseModel):
    assessment_title: str
    per_question: List[QuestionGrade]
    total_awarded: float
    max_total: float
    summary: str