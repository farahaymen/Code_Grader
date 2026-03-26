from fastapi import FastAPI
from pydantic import BaseModel
from app.schemas import Assessment
from app.pipeline import run_grading_pipeline

app = FastAPI(title="Code Grader MVP")


class GradeRequest(BaseModel):
    assessment: Assessment
    student_code: str


@app.post("/grade")
def grade_submission(request: GradeRequest):
    report = run_grading_pipeline(
        assessment=request.assessment,
        student_code=request.student_code
    )
    return report.model_dump()