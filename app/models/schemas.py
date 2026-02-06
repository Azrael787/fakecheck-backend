diff --git a/app/models/schemas.py b/app/models/schemas.py
new file mode 100644
index 0000000000000000000000000000000000000000..0cad993f1279f42275ac5ef97b7009d3d1f7e51b
--- /dev/null
+++ b/app/models/schemas.py
@@ -0,0 +1,37 @@
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
