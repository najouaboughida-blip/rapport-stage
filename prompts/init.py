"""
Package prompts - Gestion des prompts académiques
"""

from .academic_prompts import (
    ACADEMIC_PROMPTS_CONFIG,
    generate_section_prompt,
    generate_style_instructions
)

__all__ = [
    'ACADEMIC_PROMPTS_CONFIG',
    'generate_section_prompt',
    'generate_style_instructions'
]