import ast
from typing import List
from app.schemas import CodeChunk, ParsedSubmission


def get_source_segment(lines: List[str], start_line: int, end_line: int) -> str:
    return "\n".join(lines[start_line - 1:end_line])


def parse_python_submission(code: str) -> ParsedSubmission:
    tree = ast.parse(code)
    lines = code.splitlines()

    imports = []
    functions = []
    classes = []
    chunks = []

    chunk_counter = 1

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
            imports.extend(names)
            chunks.append(CodeChunk(
                chunk_id=f"C{chunk_counter}",
                chunk_type="import",
                start_line=node.lineno,
                end_line=getattr(node, "end_lineno", node.lineno),
                content=get_source_segment(lines, node.lineno, getattr(node, "end_lineno", node.lineno)),
                symbol_name=", ".join(names)
            ))
            chunk_counter += 1

        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = [f"{module}.{alias.name}" for alias in node.names]
            imports.extend(names)
            chunks.append(CodeChunk(
                chunk_id=f"C{chunk_counter}",
                chunk_type="import",
                start_line=node.lineno,
                end_line=getattr(node, "end_lineno", node.lineno),
                content=get_source_segment(lines, node.lineno, getattr(node, "end_lineno", node.lineno)),
                symbol_name=", ".join(names)
            ))
            chunk_counter += 1

        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            chunks.append(CodeChunk(
                chunk_id=f"C{chunk_counter}",
                chunk_type="function",
                start_line=node.lineno,
                end_line=getattr(node, "end_lineno", node.lineno),
                content=get_source_segment(lines, node.lineno, getattr(node, "end_lineno", node.lineno)),
                symbol_name=node.name
            ))
            chunk_counter += 1

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
            chunks.append(CodeChunk(
                chunk_id=f"C{chunk_counter}",
                chunk_type="class",
                start_line=node.lineno,
                end_line=getattr(node, "end_lineno", node.lineno),
                content=get_source_segment(lines, node.lineno, getattr(node, "end_lineno", node.lineno)),
                symbol_name=node.name
            ))
            chunk_counter += 1

        else:
            chunks.append(CodeChunk(
                chunk_id=f"C{chunk_counter}",
                chunk_type="statement",
                start_line=node.lineno,
                end_line=getattr(node, "end_lineno", node.lineno),
                content=get_source_segment(lines, node.lineno, getattr(node, "end_lineno", node.lineno)),
                symbol_name=None
            ))
            chunk_counter += 1

    return ParsedSubmission(
        language="python",
        imports=sorted(set(imports)),
        functions=functions,
        classes=classes,
        chunks=chunks,
        raw_code=code
    )