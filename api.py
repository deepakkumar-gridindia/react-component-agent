import asyncio
import io
import os
import uuid
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel

import agent as agent_module

app = FastAPI(title="React Component Generator")
_executor = ThreadPoolExecutor(max_workers=4)

# job_id -> {logs, zip, done, error}
_jobs: dict = {}


@app.get("/", response_class=HTMLResponse)
def index():
    return (Path(__file__).parent / "static" / "index.html").read_text()


class GenerateRequest(BaseModel):
    json_schema: dict
    api_key: Optional[str] = None


def _run_job(job_id: str, schema: dict, api_key: str) -> None:
    job = _jobs[job_id]
    try:
        with TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            def log_fn(msg: str) -> None:
                job["logs"].append(str(msg))

            agent_module.run_agent(schema, output_dir, api_key=api_key, log_fn=log_fn)

            files = list(output_dir.iterdir())
            if not files:
                raise RuntimeError("Agent produced no output files")

            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                for f in files:
                    zf.write(f, f.name)
            job["zip"] = buf.getvalue()
    except Exception as exc:
        job["error"] = str(exc)
    finally:
        job["done"] = True


@app.post("/generate")
async def generate(req: GenerateRequest):
    api_key = req.api_key or os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="No Groq API key provided. Enter one in the UI or set GROQ_API_KEY on the server.",
        )

    job_id = uuid.uuid4().hex
    _jobs[job_id] = {"logs": [], "zip": None, "done": False, "error": None}

    loop = asyncio.get_event_loop()
    loop.run_in_executor(_executor, _run_job, job_id, req.json_schema, api_key)

    return {"job_id": job_id}


@app.get("/status/{job_id}")
def status(job_id: str, offset: int = 0):
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "done": job["done"],
        "error": job["error"],
        "logs": job["logs"][offset:],
        "ready": job["done"] and job["zip"] is not None,
    }


@app.get("/download/{job_id}")
def download(job_id: str):
    job = _jobs.get(job_id)
    if not job or not job["zip"]:
        raise HTTPException(status_code=404, detail="Not ready or not found")
    return Response(
        content=job["zip"],
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="components.zip"'},
    )
