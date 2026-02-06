+import uuid
+from typing import Dict, Optional
+
+from fastapi import UploadFile
+
+from app.models.schemas import AnalysisJob, AnalysisResult, AnalysisStatus
+
+_JOBS: Dict[str, AnalysisJob] = {}
+
+
+def create_job(filename: str, content_type: Optional[str]) -> AnalysisJob:
+    job_id = str(uuid.uuid4())
+    job = AnalysisJob(
+        job_id=job_id,
+        filename=filename,
+        content_type=content_type,
+        status=AnalysisStatus.pending,
+    )
+    _JOBS[job_id] = job
+    return job
+
+
+def get_job(job_id: str) -> Optional[AnalysisJob]:
+    return _JOBS.get(job_id)
+
+
+def analyze_file(job_id: str, file: UploadFile) -> None:
+    job = _JOBS[job_id]
+    job.status = AnalysisStatus.processing
+    try:
+        _ = file.file.read()
+        fake_probability = 0.5
+        result = AnalysisResult(
+            fake_probability=fake_probability,
+            real_probability=1 - fake_probability,
+            label="fake" if fake_probability >= 0.5 else "real",
+        )
+        job.result = result
+        job.status = AnalysisStatus.completed
+    except Exception as exc:
+        job.status = AnalysisStatus.failed
+        job.error = str(exc)
