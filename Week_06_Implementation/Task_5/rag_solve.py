"""Solve the missing_code.json tasks with the RAG pipeline from Tasks 2-4.

For each task: embed the task text, take the top 5 chunks (Task 4), send task +
chunks to the LLM, and write the returned method over the stub in the target
file. The stub is located with ast and only its lines are replaced.

Needs WEEK_6_API_KEY in the environment or in a .env file in a parent folder.
"""

import ast
import json
import os
import re
import sys
import textwrap
from pathlib import Path

from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

WEEK = Path(__file__).resolve().parent.parent
REPO = WEEK / "AI4SE_Playground"
TASKS = WEEK / "Assignments" / "missing_code.json"
sys.path.insert(0, str(WEEK / "Task_4"))
from match_chunks import embed, ids_for, match  # noqa: E402

MODEL = "gpt-6-luna"
TOP_N = 5
MAX_ATTEMPTS = 3

SYSTEM = (
    "You implement one missing Python method in an existing code base. "
    "You get the task and some related code from the repository. "
    "Reply with only the complete method definition (decorators if any, def line, "
    "docstring, body) in a single ```python block. Do not include the class "
    "statement, imports or any other code."
)

load_dotenv(find_dotenv(usecwd=True))
client = OpenAI(api_key=os.environ["WEEK_6_API_KEY"])


def build_prompt(task_text, chunks):
    context = "\n\n".join(
        f"--- chunk {i} ({c['role']}) ---\n{c['text']}" for i, (_, c) in enumerate(chunks, 1)
    )
    return f"Task:\n{task_text}\n\nRelated code from the repository:\n\n{context}"


def ask_llm(prompt, method):
    """Return the generated method as dedented source, validated with ast."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        )
        reply = response.choices[0].message.content or ""
        block = re.search(r"```(?:python)?\n(.*?)```", reply, re.S)
        code = textwrap.dedent(block.group(1) if block else reply).strip("\n")
        try:
            tree = ast.parse(code)
            func = tree.body[0]
            if len(tree.body) == 1 and isinstance(func, ast.FunctionDef) and func.name == method:
                return code, func
            problem = "reply is not exactly one def of the right name"
        except SyntaxError as error:
            problem = f"syntax error: {error}"
        print(f"    attempt {attempt}: {problem}")
    raise RuntimeError(f"no usable code for {method}")


def find_stub(tree, cls, method):
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == cls:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method:
                    return item
    raise LookupError(f"{cls}.{method} not found")


def write_method(path, cls, method, code, func):
    """Replace the stub's lines with ``code``; returns False if it was already done."""
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines(keepends=True)
    stub = find_stub(ast.parse(source), cls, method)
    if not (len(stub.body) == 1 and isinstance(stub.body[0], ast.Pass)):
        return False

    # Keep the stub's decorators unless the model wrote its own.
    first = min([stub.lineno] + [d.lineno for d in stub.decorator_list]) if func.decorator_list else stub.lineno
    indent = re.match(r"\s*", lines[stub.lineno - 1]).group(0)
    new = textwrap.indent(code, indent) + "\n"
    updated = "".join(lines[:first - 1]) + new + "".join(lines[stub.end_lineno:])
    ast.parse(updated)  # never leave a broken file behind
    path.write_text(updated, encoding="utf-8")
    return True


def solve(task_text, file, cls, method):
    """Run the RAG pipeline for one textual task and write the result into ``file``."""
    query = embed([task_text])[0]
    chunks = match(query, n=TOP_N, exclude=ids_for(file, cls, method))
    for score, c in chunks:
        print(f"    {score:.3f} {c['file']} {c['class'] or ''}.{c['name']}")
    code, func = ask_llm(build_prompt(task_text, chunks), method)
    if write_method(REPO / file, cls, method, code, func):
        print(f"    wrote {len(code.splitlines())} lines")
    else:
        print("    skipped: method is no longer a stub")


def main():
    for task in json.loads(TASKS.read_text(encoding="utf-8")):
        doc = task["docstring"].strip().strip('"').strip()
        text = (f'In {task["file"]}, implement the method `{task["method"]}` of class '
                f'`{task["class"]}`. It should do this: {doc}')
        print(f'{task["class"]}.{task["method"]}')
        solve(text, task["file"], task["class"], task["method"])


if __name__ == "__main__":
    main()
