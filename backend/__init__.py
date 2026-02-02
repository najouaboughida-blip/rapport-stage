"""
Backend modules for the intelligent academic report generator.
"""

from .ai_generator import AIGenerator, AcademicPromptGenerator
from .stage_generator import StageReportGenerator
from .pdf_generator import PDFGenerator, generate_quick_pdf
from .word_generator import WordGenerator, generate_quick_docx

__all__ = [
    'AIGenerator',
    'AcademicPromptGenerator',
    'StageReportGenerator',
    'PDFGenerator',
    'WordGenerator',
    'generate_quick_pdf',
    'generate_quick_docx'
]