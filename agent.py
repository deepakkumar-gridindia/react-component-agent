#!/usr/bin/env python3
"""
React Component Generator Agent

Generates production-ready React/TypeScript components from JSON schemas
using Groq (llama-3.3-70b) with tool use to write files to disk.

Usage:
  python agent.py <schema.json> [output-dir]
  python agent.py -                          # read schema from stdin
  python agent.py                            # use built-in example schema
"""

import json
import os
import re
import sys
import time
import uuid
from groq import Groq, RateLimitError, BadRequestError
from pathlib import Path


def _load_env() -> None:
    if os.environ.get("GROQ_API_KEY"):
        return
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env()
_default_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

MODEL_DEFAULT = "llama-3.1-8b-instant"   # high rate-limit free tier model
MODEL_LARGE   = "llama-3.3-70b-versatile"  # best quality, lower rate limits

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "write_component",
            "description": (
                "Write a React component or TypeScript file to disk. "
                "Use this for every file you generate: types, components, index barrel."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename to write, e.g. UserProfile.tsx or types.ts",
                    },
                    "content": {
                        "type": "string",
                        "description": "Complete file content — TypeScript/TSX source code",
                    },
                },
                "required": ["filename", "content"],
            },
        },
    }
]

SYSTEM_PROMPT = """You are an expert React and TypeScript developer. Given a JSON schema you will:

1. **Analyse** the schema: identify types, required fields, enums, nested objects, arrays.
2. **Generate** complete, production-ready files:
   - `types.ts`  — TypeScript interfaces / type aliases that mirror the schema exactly.
   - `<Name>Card.tsx`  — A read-only display component that renders one record.
   - `<Name>Form.tsx`  — A controlled form component (useState) for creating/editing a record.
   - `<Name>List.tsx`  — A list/table component that accepts an array of records.
   - `index.ts`  — barrel export re-exporting everything above.
3. **Write every file** immediately using the `write_component` tool — do not print code in prose.

Coding standards:
- Functional components with typed props (interface Props { … }).
- Tailwind CSS utility classes for all styling — no inline styles, no CSS modules.
- Enum fields → <select> in forms, coloured badge in display.
- Arrays of primitives → comma-separated tags; arrays of objects → nested list.
- Nested objects → a dedicated sub-section or sub-component.
- Mark required fields with an asterisk (*) in form labels.
- Graceful null/undefined handling (optional chaining, fallback text "—").
- JSDoc comments on every exported symbol.
- No external UI libraries beyond React itself."""

# Matches the <function=name>{...}</function> format some models emit instead of tool_calls
_FUNC_TAG_RE = re.compile(r"<function=(\w+)>(.*?)</function>", re.DOTALL)


def _parse_function_tags(text: str) -> list[dict]:
    """Parse inline <function=name>{...}</function> tags into a normalised call list."""
    calls = []
    for m in _FUNC_TAG_RE.finditer(text):
        name, args_str = m.group(1), m.group(2).strip()
        try:
            args = json.loads(args_str)
            calls.append({"id": f"call_{uuid.uuid4().hex[:8]}", "name": name, "args": args})
        except json.JSONDecodeError:
            pass
    return calls


def _trim_history(messages: list[dict]) -> list[dict]:
    """Strip file content from past assistant tool-call arguments to keep context small."""
    result = []
    for i, msg in enumerate(messages):
        is_last = i == len(messages) - 1
        if not is_last and msg.get("role") == "assistant" and msg.get("tool_calls"):
            slim_calls = []
            for tc in msg["tool_calls"]:
                try:
                    args = json.loads(tc["function"]["arguments"])
                    slim_args = json.dumps({"filename": args.get("filename", "?")})
                except Exception:
                    slim_args = tc["function"]["arguments"]
                slim_calls.append(
                    {**tc, "function": {**tc["function"], "arguments": slim_args}}
                )
            result.append({**msg, "tool_calls": slim_calls})
        else:
            result.append(msg)
    return result


def write_component(output_dir: Path, filename: str, content: str) -> str:
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return f"Wrote {filepath}"


def run_agent(
    schema: dict,
    output_dir: Path,
    api_key: str | None = None,
    log_fn=print,
    model: str | None = None,
) -> None:
    groq_client = Groq(api_key=api_key or os.environ.get("GROQ_API_KEY", ""))
    model = model or MODEL_DEFAULT
    schema_str = json.dumps(schema, indent=2)
    component_name = schema.get("title", "Component").replace(" ", "")

    log_fn(f"Agent starting — output → {output_dir}/\n")
    written: list[str] = []

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                f"Generate React components for this JSON schema. "
                f"Use `{component_name}` as the base name for all components.\n\n"
                f"```json\n{schema_str}\n```"
            ),
        },
    ]

    for _ in range(15):
        for attempt in range(4):
            try:
                response = groq_client.chat.completions.create(
                    model=model,
                    max_tokens=4096,
                    tools=TOOLS,
                    messages=_trim_history(messages),
                )
                break
            except RateLimitError as e:
                if attempt == 3:
                    raise
                wait = 30 * (attempt + 1)
                log_fn(f"  Rate limited — waiting {wait}s...")
                time.sleep(wait)
            except BadRequestError as e:
                log_fn(f"\nBad request: {e}\n")
                raise

        msg = response.choices[0].message

        # ── Detect inline <function=...> tags (fallback for models that skip tool_calls) ──
        inline_calls = _parse_function_tags(msg.content or "")
        if inline_calls and not msg.tool_calls:
            # Reconstruct a clean text (strip the tags) and synthetic tool_calls
            clean_text = _FUNC_TAG_RE.sub("", msg.content or "").strip()
            if clean_text:
                log_fn(clean_text)

            # Build synthetic tool_calls so the rest of the loop is identical
            synthetic_calls = [
                {
                    "id": c["id"],
                    "type": "function",
                    "function": {
                        "name": c["name"],
                        "arguments": json.dumps(c["args"]),
                    },
                }
                for c in inline_calls
            ]
            messages.append(
                {
                    "role": "assistant",
                    "content": clean_text or None,
                    "tool_calls": synthetic_calls,
                }
            )
            tool_call_items = [
                type("TC", (), {"id": c["id"], "function": type("F", (), {
                    "name": c["name"],
                    "arguments": json.dumps(c["args"]),
                })()})()
                for c in inline_calls
            ]
        else:
            if msg.content:
                log_fn(msg.content)

            assistant_msg: dict = {"role": "assistant", "content": msg.content}
            if msg.tool_calls:
                assistant_msg["tool_calls"] = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    }
                    for tc in msg.tool_calls
                ]
            messages.append(assistant_msg)

            if not msg.tool_calls:
                break

            tool_call_items = msg.tool_calls

        # Execute tools
        for tc in tool_call_items:
            args = json.loads(tc.function.arguments)
            if tc.function.name == "write_component":
                result = write_component(output_dir, args["filename"], args["content"])
                written.append(args["filename"])
                log_fn(f"  ✓ {args['filename']}")
            else:
                result = f"Unknown tool: {tc.function.name}"

            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    log_fn(f"\n{'─' * 50}")
    log_fn(f"Done — {len(written)} file(s) written to {output_dir}/")
    for f in written:
        log_fn(f"  {output_dir}/{f}")


# ── Example schema used when no argument is supplied ─────────────────────────

EXAMPLE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Employee",
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "department": {
            "type": "string",
            "enum": ["Engineering", "Design", "Marketing", "HR", "Finance"],
        },
        "role": {"type": "string", "enum": ["junior", "mid", "senior", "lead", "manager"]},
        "salary": {"type": "number", "minimum": 0},
        "startDate": {"type": "string", "format": "date"},
        "isActive": {"type": "boolean"},
        "address": {
            "type": "object",
            "properties": {
                "street": {"type": "string"},
                "city": {"type": "string"},
                "country": {"type": "string"},
            },
            "required": ["city", "country"],
        },
        "skills": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["id", "firstName", "lastName", "email", "department", "role"],
}


def main() -> None:
    if len(sys.argv) == 1:
        print("No schema supplied — using built-in Employee example.\n")
        schema = EXAMPLE_SCHEMA
        output_dir = Path("generated_components")
    elif sys.argv[1] == "-":
        schema = json.loads(sys.stdin.read())
        output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("generated_components")
    else:
        schema_path = Path(sys.argv[1])
        if not schema_path.exists():
            print(f"Error: file not found — {schema_path}", file=sys.stderr)
            sys.exit(1)
        schema = json.loads(schema_path.read_text())
        output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("generated_components")

    run_agent(schema, output_dir)


if __name__ == "__main__":
    main()
