"""Split the AI4SE_Playground repository into function-level chunks.

Every function or method becomes one chunk. Class-level code that is not a
method (class line, docstring, class attributes) becomes a "class" chunk, and
module-level code (docstring, imports, constants) becomes a "module" chunk.
Each chunk's text starts with a short header naming its file, its class with
bases, and the attributes that class's __init__ sets.

Output: chunks.json next to this script.
"""

import ast
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent / "AI4SE_Playground"
OUT = HERE / "chunks.json"

FUNC_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


def start_line(node):
    """First line of a node, including its decorators."""
    lines = [node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])]
    return min(lines)


def segment(lines, first, last):
    """Source lines first..last (1-based, inclusive)."""
    return "\n".join(lines[first - 1:last])


def class_context(node):
    """Header lines for a class: its bases and the attributes __init__ sets.

    Every method chunk carries these, so any retrieved method shows the real
    attribute names (e.g. ``_base``), not just the method body.
    """
    bases = ", ".join(ast.unparse(b) for b in node.bases)
    lines = f"# class: {node.name}({bases})" if bases else f"# class: {node.name}"
    attrs = []
    for item in node.body:
        if isinstance(item, FUNC_TYPES) and item.name == "__init__":
            for sub in ast.walk(item):
                targets = sub.targets if isinstance(sub, ast.Assign) else [getattr(sub, "target", None)]
                for t in targets:
                    if (isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
                            and t.value.id == "self" and t.attr not in attrs):
                        attrs.append(t.attr)
    if attrs:
        lines += "\n# attributes: " + ", ".join(attrs)
    return lines


def make_chunk(rel, role, kind, cls, name, first, last, code, context=None):
    header = f"# file: {rel}"
    if context:
        header += f"\n{context}"
    elif cls:
        header += f"\n# class: {cls}"
    return {
        "file": rel,
        "role": role,
        "kind": kind,
        "class": cls,
        "name": name,
        "start_line": first,
        "end_line": last,
        "text": f"{header}\n{code}",
    }


def chunk_file(path):
    rel = path.relative_to(REPO).as_posix()
    role = "test" if "tests" in path.parts else "source"
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    tree = ast.parse(source)
    chunks = []
    module_parts = []
    module_span = []

    for node in tree.body:
        first, last = start_line(node), node.end_lineno
        if isinstance(node, FUNC_TYPES):
            chunks.append(make_chunk(rel, role, "function", None, node.name,
                                     first, last, segment(lines, first, last)))
        elif isinstance(node, ast.ClassDef):
            chunks.extend(chunk_class(node, rel, role, lines))
        else:
            module_parts.append(segment(lines, first, last))
            module_span += [first, last]

    if module_parts:
        chunks.insert(0, make_chunk(rel, role, "module", None, path.stem,
                                    min(module_span), max(module_span),
                                    "\n".join(module_parts)))
    return chunks


def chunk_class(node, rel, role, lines):
    methods = [n for n in node.body if isinstance(n, FUNC_TYPES)]
    others = [n for n in node.body if not isinstance(n, FUNC_TYPES)]

    # Class chunk: the "class X(...):" line(s) plus every non-method statement.
    first = start_line(node)
    head_end = node.body[0].lineno - 1
    parts = [segment(lines, first, head_end)]
    last = head_end
    for n in others:
        parts.append(segment(lines, start_line(n), n.end_lineno))
        last = max(last, n.end_lineno)
    context = class_context(node)
    chunks = []
    # A bare "class X(Base):" line says nothing the method headers don't.
    if others:
        chunks.append(make_chunk(rel, role, "class", node.name, node.name,
                                 first, last, "\n".join(parts), context))

    for m in methods:
        m_first, m_last = start_line(m), m.end_lineno
        chunks.append(make_chunk(rel, role, "method", node.name, m.name,
                                 m_first, m_last, segment(lines, m_first, m_last), context))
    return chunks


def main():
    chunks = []
    for path in sorted(REPO.rglob("*.py")):
        chunks.extend(chunk_file(path))
    for i, chunk in enumerate(chunks):
        chunk["id"] = i

    OUT.write_text(json.dumps(chunks, indent=2), encoding="utf-8")

    sizes = [c["text"].count("\n") + 1 for c in chunks]
    kinds = {}
    for c in chunks:
        key = f'{c["role"]}/{c["kind"]}'
        kinds[key] = kinds.get(key, 0) + 1
    print(f"{len(chunks)} chunks written to {OUT.name}")
    print("by role/kind:", kinds)
    print(f"lines per chunk (incl. header): min {min(sizes)}, max {max(sizes)}, "
          f"mean {sum(sizes) / len(sizes):.1f}")
    print("chars per chunk: max", max(len(c["text"]) for c in chunks))


if __name__ == "__main__":
    main()
