+from enum import Enum
+from pydantic import BaseModel
+from typing import Optional
+
+
+class AnalysisStatus(str, Enum):
+    pending = "pending"
+    processing = "processing"
+    completed = "completed"
+    failed = "failed"
+
+
+class AnalysisResult(BaseModel):
+    fake_probability: float
+    real_probability: float
+    label: str
+
+
+class AnalysisJob(BaseModel):
+    job_id: str
+    filename: str
+    content_type: Optional[str]
+    status: AnalysisStatus
+    result: Optional[AnalysisResult] = None
+    error: Optional[str] = None
+
+
+class AnalysisResponse(BaseModel):
+    job_id: str
+    status: AnalysisStatus
+
+
+class AnalysisStatusResponse(BaseModel):
+    job_id: str
+    status: AnalysisStatus
+    result: Optional[AnalysisResult]
+    error: Optional[str]
