import io
import pandas as pd
from typing import Optional


class DocumentProcessor:
    """Extracts and prepares text content from uploaded files."""

    SUPPORTED_TYPES = {
        "text/plain": "_process_txt",
        "text/csv": "_process_csv",
        "application/csv": "_process_csv",
        "application/pdf": "_process_pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "_process_docx",
        "application/json": "_process_json",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "_process_xlsx",
        "application/vnd.ms-excel": "_process_xlsx",
    }

    def process(self, uploaded_file) -> str:
        """Process an uploaded Streamlit file and return extracted text."""
        file_bytes = uploaded_file.read()
        mime = uploaded_file.type
        name = uploaded_file.name.lower()

        # Fallback detection by extension
        if mime not in self.SUPPORTED_TYPES:
            if name.endswith(".csv"):
                mime = "text/csv"
            elif name.endswith(".txt"):
                mime = "text/plain"
            elif name.endswith(".pdf"):
                mime = "application/pdf"
            elif name.endswith(".docx"):
                mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            elif name.endswith(".json"):
                mime = "application/json"
            elif name.endswith((".xlsx", ".xls")):
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        handler_name = self.SUPPORTED_TYPES.get(mime)
        if handler_name:
            handler = getattr(self, handler_name)
            return handler(file_bytes, uploaded_file.name)
        return f"[Unsupported file type: {mime}. Raw content preview]\n{file_bytes[:500].decode('utf-8', errors='replace')}"

    def _process_txt(self, data: bytes, name: str) -> str:
        text = data.decode("utf-8", errors="replace")
        return f"=== FILE: {name} ===\n{text}\n"

    def _process_csv(self, data: bytes, name: str) -> str:
        try:
            df = pd.read_csv(io.BytesIO(data))
            summary_lines = [f"=== FILE: {name} ==="]
            summary_lines.append(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
            summary_lines.append(f"Columns: {', '.join(df.columns.tolist())}")
            summary_lines.append("\nData Types:")
            for col, dtype in df.dtypes.items():
                summary_lines.append(f"  {col}: {dtype}")

            # Numeric summary
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            if numeric_cols:
                summary_lines.append("\nNumeric Summary:")
                desc = df[numeric_cols].describe().round(2)
                summary_lines.append(desc.to_string())

            # Top reviews / text columns
            text_cols = df.select_dtypes(include="object").columns.tolist()
            for col in text_cols[:3]:
                top_vals = df[col].value_counts().head(10)
                summary_lines.append(f"\nTop values in '{col}':")
                summary_lines.append(top_vals.to_string())

            # Sample rows
            summary_lines.append(f"\nSample Rows (first 20):")
            summary_lines.append(df.head(20).to_string(index=False))

            return "\n".join(summary_lines) + "\n"
        except Exception as e:
            return f"=== FILE: {name} ===\nError parsing CSV: {e}\n{data[:1000].decode('utf-8', errors='replace')}\n"

    def _process_pdf(self, data: bytes, name: str) -> str:
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(data))
            pages = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages.append(f"[Page {i+1}]\n{text}")
            combined = "\n\n".join(pages)
            return f"=== FILE: {name} ===\n{combined}\n"
        except ImportError:
            return f"=== FILE: {name} ===\n[PDF processing requires PyPDF2. Install with: pip install PyPDF2]\n"
        except Exception as e:
            return f"=== FILE: {name} ===\nError parsing PDF: {e}\n"

    def _process_docx(self, data: bytes, name: str) -> str:
        try:
            from docx import Document
            doc = Document(io.BytesIO(data))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return f"=== FILE: {name} ===\n" + "\n".join(paragraphs) + "\n"
        except ImportError:
            return f"=== FILE: {name} ===\n[DOCX processing requires python-docx. Install with: pip install python-docx]\n"
        except Exception as e:
            return f"=== FILE: {name} ===\nError parsing DOCX: {e}\n"

    def _process_json(self, data: bytes, name: str) -> str:
        import json
        try:
            parsed = json.loads(data.decode("utf-8", errors="replace"))
            pretty = json.dumps(parsed, indent=2)
            return f"=== FILE: {name} ===\n{pretty}\n"
        except Exception as e:
            return f"=== FILE: {name} ===\nError parsing JSON: {e}\n{data[:1000].decode('utf-8', errors='replace')}\n"

    def _process_xlsx(self, data: bytes, name: str) -> str:
        try:
            xl = pd.ExcelFile(io.BytesIO(data))
            parts = [f"=== FILE: {name} ==="]
            for sheet in xl.sheet_names:
                df = xl.parse(sheet)
                parts.append(f"\n--- Sheet: {sheet} ---")
                parts.append(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
                parts.append(df.head(20).to_string(index=False))
            return "\n".join(parts) + "\n"
        except Exception as e:
            return f"=== FILE: {name} ===\nError parsing XLSX: {e}\n"

    @staticmethod
    def truncate(text: str, max_chars: int = 12000) -> str:
        """Truncate text to fit within token limits while preserving structure."""
        if len(text) <= max_chars:
            return text
        half = max_chars // 2
        return text[:half] + "\n\n[... content truncated for brevity ...]\n\n" + text[-half:]
