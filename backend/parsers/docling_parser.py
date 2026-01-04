from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
import pandas as pd
from typing import List, Dict, Any

class DoclingParser:
    def __init__(self):
        self.pipeline_options = PdfPipelineOptions()
        self.pipeline_options.do_ocr = True
        self.pipeline_options.do_table_structure = True
        self.pipeline_options.table_structure_options.do_cell_matching = True

        self.converter = DocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=self.pipeline_options)
            }
        )

    def process(self, file_path: str) -> Dict[str, Any]:
        """
        Parses the PDF once and returns both structured chunks and table metadata.
        """
        try:
            doc = self.converter.convert(file_path).document
        except Exception as e:
            print(f"Docling conversion failed: {e}")
            return {"chunks": [], "tables": []}

        chunks = []
        tables_data = []

        # Iterate through pages
        for page_num, page in doc.pages.items():
            
            # 1. Text Elements
            for element in page.text_elements:
                bbox = [
                    element.bbox.l, # x0
                    element.bbox.t, # y0
                    element.bbox.r, # x1
                    element.bbox.b  # y1
                ]
                
                role = "content"
                # Check label string safely
                if hasattr(element, "label") and ("HEADER" in str(element.label).upper() or "TITLE" in str(element.label).upper()):
                    role = "heading"

                chunks.append({
                    "text": element.text,
                    "page": page_num,
                    "bbox": bbox,
                    "type": "text",
                    "role": role
                })

            # 2. Table Elements
            for table in page.tables:
                # bounding box
                bbox = [
                    table.bbox.l,
                    table.bbox.t,
                    table.bbox.r,
                    table.bbox.b
                ]
                
                # Phase 4: Decoupled Retrieval
                # 1. Generate DataFrame for valid summaries
                df = table.export_to_dataframe()
                
                # 2. Create Search Summary (Headers + First 3 rows)
                header_str = ", ".join([str(h) for h in df.columns.tolist()])
                preview_rows = df.head(3).to_string(index=False)
                search_summary = f"Table regarding: {header_str}.\nPreview:\n{preview_rows}"
                
                # 3. Full Content for RAG Context
                table_md = table.export_to_markdown()
                
                chunks.append({
                    "text": search_summary,      # Used for Embedding/Search
                    "full_content": table_md,    # Used for LLM Generation
                    "page": page_num,
                    "bbox": bbox,
                    "type": "table",
                    "role": "table"
                })

                # DataFrame for Metadata Store
                df = table.export_to_dataframe()
                tables_data.append({
                    "page": page_num,
                    "data": df.values.tolist(), # Convert to list for JSON serialization
                    "headers": df.columns.tolist(),
                    "rows": len(df),
                    "cols": len(df.columns),
                    "bbox": bbox
                })

        return {
            "chunks": chunks,
            "tables": tables_data
        }
