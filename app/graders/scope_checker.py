from app.schemas import Assessment, ParsedSubmission, ScopeFlag


def check_out_of_scope_usage(assessment: Assessment, parsed: ParsedSubmission) -> list[ScopeFlag]:
    flags: list[ScopeFlag] = []

    allowed = set(assessment.taught_material.allowed_libraries)
    restricted = set(assessment.taught_material.restricted_libraries)

    for chunk in parsed.chunks:
        if chunk.chunk_type != "import":
            continue

        imported_items = [item.strip() for item in (chunk.symbol_name or "").split(",") if item.strip()]
        for item in imported_items:
            root_lib = item.split(".")[0]

            if root_lib in restricted:
                for q in assessment.questions:
                    flags.append(ScopeFlag(
                        question_id=q.id,
                        item=item,
                        item_type="library",
                        evidence_chunk_ids=[chunk.chunk_id],
                        reason=f"'{item}' is explicitly outside the taught material.",
                        severity="warning"
                    ))

            elif allowed and root_lib not in allowed:
                for q in assessment.questions:
                    flags.append(ScopeFlag(
                        question_id=q.id,
                        item=item,
                        item_type="library",
                        evidence_chunk_ids=[chunk.chunk_id],
                        reason=f"'{item}' was not found among explicitly allowed/taught libraries.",
                        severity="info"
                    ))

    return flags