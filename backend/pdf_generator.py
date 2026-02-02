"""
Générateur de rapports PDF pour mémoires de stage
Version professionnelle avec support multi-pages et mise en forme académique
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, ListFlowable, ListItem
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm, inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable

import base64
from io import BytesIO
import re


class PDFGenerator:
    """Générateur de rapports PDF académiques avec mise en forme professionnelle"""
    
    def __init__(self, output_path: str = "rapport_stage.pdf", options: Optional[Dict] = None):
        """
        Initialise le générateur PDF
        
        Args:
            output_path: Chemin du fichier PDF de sortie
            options: Options de configuration
        """
        self.output_path = output_path
        self.options = options or {}
        
        # Configuration des polices et styles
        self.styles = getSampleStyleSheet()
        self.default_font = 'Helvetica'
        self.default_font_bold = 'Helvetica-Bold'
        self.default_font_italic = 'Helvetica-Oblique'
        
        # Couleurs académiques
        self.colors = {
            'primary': colors.HexColor('#2C3E50'),      # Bleu foncé
            'secondary': colors.HexColor('#3498DB'),    # Bleu
            'accent': colors.HexColor('#2980B9'),       # Bleu moyen
            'light': colors.HexColor('#ECF0F1'),        # Gris clair
            'text': colors.HexColor('#2C3E50'),         # Texte foncé
            'highlight': colors.HexColor('#E74C3C')     # Rouge pour highlights
        }
        
        # Initialiser les styles personnalisés
        self._init_custom_styles()
        
        # Informations du document
        self.title = "Rapport de Stage de Fin d'Études"
        self.author = "Étudiant ENSAO"
        self.subject = "Mémoire de Projet de Fin d'Études"
        self.keywords = "stage, rapport, mémoire, ENSAO, ingénieur"
        
        # Compteur de pages
        self.page_count = 0
    
    def _init_custom_styles(self):
        """Initialise les styles personnalisés pour le rapport académique"""
        
        # Style pour le titre principal
        self.styles.add(ParagraphStyle(
            name='MainTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=30,
            fontName=self.default_font_bold
        ))
        
        # Style pour les titres de chapitre
        self.styles.add(ParagraphStyle(
            name='ChapterTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=self.colors['secondary'],
            alignment=TA_LEFT,
            spaceBefore=40,
            spaceAfter=20,
            fontName=self.default_font_bold,
            borderWidth=1,
            borderColor=self.colors['accent'],
            borderPadding=(5, 5, 5, 5),
            leftIndent=0
        ))
        
        # Style pour les sous-titres
        self.styles.add(ParagraphStyle(
            name='SubTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.colors['accent'],
            alignment=TA_LEFT,
            spaceBefore=25,
            spaceAfter=12,
            fontName=self.default_font_bold,
            leftIndent=10
        ))
        
        # Style pour les sous-sous-titres
        self.styles.add(ParagraphStyle(
            name='SubSubTitle',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=self.colors['primary'],
            alignment=TA_LEFT,
            spaceBefore=20,
            spaceAfter=10,
            fontName=self.default_font_bold,
            leftIndent=20
        ))
        
        # Style pour le texte normal justifié
        self.styles.add(ParagraphStyle(
            name='NormalJustified',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.colors['text'],
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=14,
            fontName=self.default_font,
            wordWrap='CJK'
        ))
        
        # Style pour le texte normal aligné à gauche
        self.styles.add(ParagraphStyle(
            name='NormalLeft',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.colors['text'],
            alignment=TA_LEFT,
            spaceAfter=10,
            leading=14,
            fontName=self.default_font
        ))
        
        # Style pour les citations
        self.styles.add(ParagraphStyle(
            name='Quote',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_JUSTIFY,
            leftIndent=20,
            rightIndent=20,
            spaceBefore=10,
            spaceAfter=10,
            fontName=self.default_font_italic,
            borderWidth=1,
            borderColor=colors.HexColor('#BDC3C7'),
            borderPadding=5,
            backColor=colors.HexColor('#F8F9F9')
        ))
        
        # Style pour les listes
        self.styles.add(ParagraphStyle(
            name='ListBullet',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.colors['text'],
            alignment=TA_LEFT,
            leftIndent=20,
            spaceAfter=5,
            bulletIndent=10,
            fontName=self.default_font
        ))
        
        # Style pour les notes de bas de page
        self.styles.add(ParagraphStyle(
            name='Footnote',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#95A5A6'),
            alignment=TA_JUSTIFY,
            spaceBefore=5,
            spaceAfter=5,
            fontName=self.default_font
        ))
    
    def _header_footer(self, canvas, doc):
        """Génère l'en-tête et le pied de page"""
        
        # En-tête
        canvas.saveState()
        
        # Ligne de séparation en-tête
        canvas.setStrokeColor(self.colors['light'])
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.height + doc.topMargin - 20, 
                   doc.width + doc.leftMargin, doc.height + doc.topMargin - 20)
        
        # Logo université (texte simulé)
        canvas.setFont(self.default_font_bold, 9)
        canvas.setFillColor(self.colors['primary'])
        canvas.drawString(doc.leftMargin, doc.height + doc.topMargin - 15, 
                         "Université Mohammed Premier - ENSAO Oujda")
        
        # Numéro de page
        canvas.setFont(self.default_font, 9)
        canvas.setFillColor(self.colors['text'])
        page_text = f"Page {canvas.getPageNumber()}"
        canvas.drawRightString(doc.width + doc.leftMargin - 20, 
                             doc.height + doc.topMargin - 15, 
                             page_text)
        
        canvas.restoreState()
        
        # Pied de page
        canvas.saveState()
        
        # Ligne de séparation pied de page
        canvas.setStrokeColor(self.colors['light'])
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, doc.bottomMargin, 
                   doc.width + doc.leftMargin, doc.bottomMargin)
        
        # Informations pied de page
        canvas.setFont(self.default_font, 8)
        canvas.setFillColor(colors.HexColor('#95A5A6'))
        
        # Date et copyright
        date_str = datetime.now().strftime("%d/%m/%Y")
        footer_left = f"Généré le {date_str}"
        footer_center = "Mémoire de Projet de Fin d'Études"
        footer_right = "© ENSAO - Tous droits réservés"
        
        canvas.drawString(doc.leftMargin, doc.bottomMargin - 12, footer_left)
        canvas.drawCentredString(doc.width/2 + doc.leftMargin, doc.bottomMargin - 12, footer_center)
        canvas.drawRightString(doc.width + doc.leftMargin, doc.bottomMargin - 12, footer_right)
        
        canvas.restoreState()
    
    def create_cover_page(self, data: Dict) -> List[Flowable]:
        """Crée la page de couverture académique"""
        
        story = []
        
        # Espacement initial
        story.append(Spacer(1, 4*cm))
        
        # Logo université (texte simulé)
        title_style = ParagraphStyle(
            name='CoverUniversity',
            parent=self.styles['Title'],
            fontSize=16,
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            spaceAfter=10,
            fontName=self.default_font_bold
        )
        story.append(Paragraph("UNIVERSITÉ MOHAMMED PREMIER", title_style))
        
        # Nom de l'école
        school_style = ParagraphStyle(
            name='CoverSchool',
            parent=self.styles['Heading1'],
            fontSize=14,
            textColor=self.colors['secondary'],
            alignment=TA_CENTER,
            spaceAfter=5,
            fontName=self.default_font_bold
        )
        story.append(Paragraph("ÉCOLE NATIONALE DES SCIENCES APPLIQUÉES - OUJDA", school_style))
        
        # Filière
        filiere_style = ParagraphStyle(
            name='CoverFiliere',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName=self.default_font
        )
        story.append(Paragraph(data.get('filiere', 'GÉNIE INFORMATIQUE'), filiere_style))
        
        # Séparateur
        story.append(Spacer(1, 2*cm))
        
        # Type de rapport
        rapport_style = ParagraphStyle(
            name='CoverRapport',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.colors['primary'],
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName=self.default_font_bold
        )
        story.append(Paragraph("RAPPORT DE STAGE DE FIN D'ÉTUDES", rapport_style))
        
        # Titre du projet
        project_style = ParagraphStyle(
            name='CoverProject',
            parent=self.styles['Title'],
            fontSize=20,
            textColor=self.colors['accent'],
            alignment=TA_CENTER,
            spaceAfter=30,
            fontName=self.default_font_bold,
            borderWidth=1,
            borderColor=self.colors['accent'],
            borderPadding=10,
            backColor=colors.HexColor('#F8F9F9')
        )
        project_title = data.get('project_title', 'TITRE DU PROJET')
        story.append(Paragraph(f'"{project_title}"', project_style))
        
        # Séparateur
        story.append(Spacer(1, 3*cm))
        
        # Informations étudiant
        info_style = ParagraphStyle(
            name='CoverInfo',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.colors['text'],
            alignment=TA_CENTER,
            spaceAfter=8,
            fontName=self.default_font
        )
        
        # Présenté par
        student_name = data.get('student_name', 'NOM Prénom')
        story.append(Paragraph(f"<b>Présenté par :</b> {student_name}", info_style))
        
        # Encadré par
        academic_supervisor = data.get('academic_supervisor', 'Dr. NOM Prénom')
        company_supervisor = data.get('company_supervisor', 'M. NOM Prénom')
        story.append(Paragraph(f"<b>Encadré par :</b> {academic_supervisor} (ENSAO)", info_style))
        story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{company_supervisor} (Entreprise)", info_style))
        
        # Entreprise
        company_name = data.get('company_name', 'NOM DE L\'ENTREPRISE')
        story.append(Paragraph(f"<b>Entreprise d'accueil :</b> {company_name}", info_style))
        
        # Durée
        duration = data.get('duration', '2 mois')
        story.append(Paragraph(f"<b>Durée du stage :</b> {duration}", info_style))
        
        # Année universitaire
        academic_year = data.get('academic_year', '2024-2025')
        story.append(Paragraph(f"<b>Année universitaire :</b> {academic_year}", info_style))
        
        # Séparateur final
        story.append(Spacer(1, 4*cm))
        
        # Mention finale
        final_style = ParagraphStyle(
            name='CoverFinal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#95A5A6'),
            alignment=TA_CENTER,
            spaceAfter=0,
            fontName=self.default_font_italic
        )
        story.append(Paragraph("Mémoire de Projet de Fin d'Études", final_style))
        story.append(Paragraph("Présenté en vue de l'obtention du Diplôme d'Ingénieur d'État", final_style))
        
        # Saut de page
        story.append(PageBreak())
        
        return story
    
    def create_thanks_page(self, data: Dict) -> List[Flowable]:
        """Crée la page de remerciements"""
        
        story = []
        
        # Titre de la page
        story.append(Paragraph("REMERCIEMENTS", self.styles['ChapterTitle']))
        story.append(Spacer(1, 1*cm))
        
        # Contenu des remerciements
        thanks_content = data.get('thanks_content', 
            """Je tiens à exprimer ma profonde gratitude à toutes les personnes qui ont contribué de près ou de loin à la réalisation de ce stage et à l'élaboration de ce mémoire.

En premier lieu, je souhaite remercier mon encadrant académique, <b>{academic_supervisor}</b>, pour son encadrement précieux, sa disponibilité et ses conseils avisés tout au long de ce projet.

Je remercie chaleureusement mon encadrant en entreprise, <b>{company_supervisor}</b>, pour m'avoir accueilli au sein de <b>{company_name}</b>, pour sa confiance et son accompagnement professionnel durant toute la période du stage.

Mes remerciements s'adressent également à l'ensemble de l'équipe de <b>{company_name}</b> pour leur accueil chaleureux, leur soutien technique et l'ambiance de travail conviviale.

Je tiens à exprimer ma reconnaissance aux enseignants de l'École Nationale des Sciences Appliquées d'Oujda pour la qualité de la formation reçue durant ces années d'études.

Enfin, je dédie ce travail à ma famille pour son soutien indéfectible, ses encouragements constants et tous les sacrifices consentis pour ma réussite académique.

C'est avec une pensée particulière que je remercie tous ceux qui, de près ou de loin, ont contribué à l'aboutissement de ce travail."""
        )
        
        # Remplacer les variables
        thanks_content = thanks_content.format(
            academic_supervisor=data.get('academic_supervisor', 'Dr. NOM Prénom'),
            company_supervisor=data.get('company_supervisor', 'M. NOM Prénom'),
            company_name=data.get('company_name', 'l\'entreprise')
        )
        
        # Ajouter le contenu
        paragraphs = thanks_content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para, self.styles['NormalJustified']))
                story.append(Spacer(1, 0.5*cm))
        
        # Signature
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("Fait à Oujda, le " + datetime.now().strftime("%d %B %Y"), 
                             self.styles['NormalLeft']))
        story.append(Spacer(1, 1*cm))
        story.append(Paragraph(data.get('student_name', 'NOM Prénom'), 
                             ParagraphStyle(
                                 name='Signature',
                                 parent=self.styles['Normal'],
                                 fontSize=12,
                                 alignment=TA_RIGHT,
                                 fontName=self.default_font_bold
                             )))
        
        # Saut de page
        story.append(PageBreak())
        
        return story
    
    def create_abstract_page(self, data: Dict) -> List[Flowable]:
        """Crée la page de résumé/abstract"""
        
        story = []
        
        # Résumé en français
        story.append(Paragraph("RÉSUMÉ", self.styles['ChapterTitle']))
        story.append(Spacer(1, 0.5*cm))
        
        french_abstract = data.get('french_abstract', 
            """Ce rapport présente les travaux réalisés dans le cadre d'un stage de fin d'études effectué au sein de {company_name}. D'une durée de {duration}, ce stage avait pour objectif principal {project_objective}.

La problématique abordée concerne {problem_description}. Pour y répondre, nous avons adopté une méthodologie basée sur {methodology}.

Les résultats obtenus démontrent {main_results}. Ces travaux ont permis de {achievements}.

Ce stage a constitué une expérience professionnelle enrichissante, permettant de mettre en pratique les connaissances théoriques acquises durant la formation d'ingénieur en {filiere} à l'ENSAO."""
        )
        
        # Remplacer les variables
        french_abstract = french_abstract.format(
            company_name=data.get('company_name', 'l\'entreprise'),
            duration=data.get('duration', 'deux mois'),
            project_objective=data.get('project_objective', 'la réalisation d\'un projet technique'),
            problem_description=data.get('problem_description', 'l\'optimisation des processus'),
            methodology=data.get('methodology', 'une approche agile'),
            main_results=data.get('main_results', 'une amélioration significative'),
            achievements=data.get('achievements', 'valider les compétences acquises'),
            filiere=data.get('filiere', 'Génie Informatique')
        )
        
        story.append(Paragraph(french_abstract, self.styles['NormalJustified']))
        
        # Mots-clés
        story.append(Spacer(1, 1*cm))
        keywords = data.get('keywords', 'stage, rapport, mémoire, ENSAO, ingénieur, projet')
        story.append(Paragraph(f"<b>Mots-clés :</b> {keywords}", self.styles['NormalLeft']))
        
        # Saut pour l'abstract en anglais
        story.append(Spacer(1, 2*cm))
        
        # Abstract in English
        story.append(Paragraph("ABSTRACT", self.styles['ChapterTitle']))
        story.append(Spacer(1, 0.5*cm))
        
        english_abstract = data.get('english_abstract',
            """This report presents the work carried out as part of a final year internship at {company_name}. Lasting {duration}, this internship had as its main objective {project_objective_eng}.

The problem addressed concerns {problem_description_eng}. To address it, we adopted a methodology based on {methodology_eng}.

The results obtained demonstrate {main_results_eng}. This work enabled us to {achievements_eng}.

This internship was a rewarding professional experience, allowing us to put into practice the theoretical knowledge acquired during the {filiere_eng} engineering program at ENSAO."""
        )
        
        story.append(Paragraph(english_abstract, self.styles['NormalJustified']))
        
        # Keywords
        story.append(Spacer(1, 1*cm))
        keywords_eng = data.get('keywords_eng', 'internship, report, thesis, ENSAO, engineer, project')
        story.append(Paragraph(f"<b>Keywords:</b> {keywords_eng}", self.styles['NormalLeft']))
        
        # Saut de page
        story.append(PageBreak())
        
        return story
    
    def create_table_of_contents(self, data: Dict) -> List[Flowable]:
        """Crée la table des matières"""
        
        story = []
        
        # Titre
        story.append(Paragraph("TABLE DES MATIÈRES", self.styles['ChapterTitle']))
        story.append(Spacer(1, 1*cm))
        
        # Chapitres principaux
        chapters = data.get('chapters', [
            {'title': 'INTRODUCTION GÉNÉRALE', 'page': 1},
            {'title': 'PRÉSENTATION DE L\'ENTREPRISE', 'page': 5},
            {'title': 'MÉTHODOLOGIE DE TRAVAIL', 'page': 10},
            {'title': 'RÉALISATION TECHNIQUE', 'page': 15},
            {'title': 'RÉSULTATS ET DISCUSSION', 'page': 25},
            {'title': 'CONCLUSION ET PERSPECTIVES', 'page': 30},
            {'title': 'BIBLIOGRAPHIE', 'page': 35},
            {'title': 'ANNEXES', 'page': 37}
        ])
        
        # Ajouter chaque chapitre
        for chapter in chapters:
            # Créer une ligne avec des points de suite
            title = chapter['title']
            page_num = chapter['page']
            
            # Créer un tableau pour aligner le titre et le numéro de page
            table_data = [[
                Paragraph(title, ParagraphStyle(
                    name='TOCEntry',
                    parent=self.styles['Normal'],
                    fontSize=11,
                    textColor=self.colors['text'],
                    leftIndent=0,
                    spaceAfter=5,
                    fontName=self.default_font
                )),
                Paragraph(str(page_num), ParagraphStyle(
                    name='TOCPage',
                    parent=self.styles['Normal'],
                    fontSize=11,
                    textColor=self.colors['text'],
                    alignment=TA_RIGHT,
                    spaceAfter=5,
                    fontName=self.default_font
                ))
            ]]
            
            table = Table(table_data, colWidths=[doc.width * 0.9, doc.width * 0.1])
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.2*cm))
        
        # Saut de page
        story.append(PageBreak())
        
        return story
    
    def create_chapter(self, chapter_data: Dict) -> List[Flowable]:
        """Crée un chapitre complet"""
        
        story = []
        
        # Titre du chapitre
        title = chapter_data.get('title', 'Chapitre')
        story.append(Paragraph(title, self.styles['ChapterTitle']))
        
        # Introduction du chapitre
        intro = chapter_data.get('introduction', '')
        if intro:
            story.append(Paragraph(intro, self.styles['NormalJustified']))
            story.append(Spacer(1, 0.5*cm))
        
        # Sections du chapitre
        sections = chapter_data.get('sections', [])
        for i, section in enumerate(sections):
            # Titre de la section
            section_title = section.get('title', f'Section {i+1}')
            story.append(Paragraph(section_title, self.styles['SubTitle']))
            
            # Contenu de la section
            content = section.get('content', '')
            if isinstance(content, list):
                for item in content:
                    if item.startswith('• ') or item.startswith('- '):
                        # Élément de liste
                        story.append(Paragraph(item[2:], self.styles['ListBullet']))
                    else:
                        # Paragraphe normal
                        story.append(Paragraph(item, self.styles['NormalJustified']))
                        story.append(Spacer(1, 0.3*cm))
            else:
                # Contenu textuel simple
                paragraphs = content.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para, self.styles['NormalJustified']))
                        story.append(Spacer(1, 0.3*cm))
            
            # Espacement entre les sections
            if i < len(sections) - 1:
                story.append(Spacer(1, 0.5*cm))
        
        # Conclusion du chapitre
        conclusion = chapter_data.get('conclusion', '')
        if conclusion:
            story.append(Spacer(1, 1*cm))
            story.append(Paragraph("<b>Conclusion du chapitre</b>", self.styles['SubSubTitle']))
            story.append(Paragraph(conclusion, self.styles['NormalJustified']))
        
        # Saut de page (sauf pour le dernier chapitre)
        if chapter_data.get('add_page_break', True):
            story.append(PageBreak())
        
        return story
    
    def generate_full_report(self, data: Dict) -> Dict[str, Any]:
        """
        Génère un rapport PDF complet avec toutes les sections
        
        Args:
            data: Données du rapport
            
        Returns:
            Dictionnaire avec le statut et les informations du PDF
        """
        try:
            # Créer le document
            doc = SimpleDocTemplate(
                self.output_path,
                pagesize=A4,
                topMargin=2.5*cm,
                bottomMargin=2.5*cm,
                leftMargin=2.5*cm,
                rightMargin=2.5*cm,
                title=data.get('title', self.title),
                author=data.get('author', self.author),
                subject=data.get('subject', self.subject),
                keywords=data.get('keywords', self.keywords)
            )
            
            # Construire l'histoire (story) du document
            story = []
            
            # 1. Page de couverture
            print("📄 Génération de la page de couverture...")
            story.extend(self.create_cover_page(data))
            
            # 2. Page de remerciements
            print("🙏 Génération des remerciements...")
            story.extend(self.create_thanks_page(data))
            
            # 3. Résumé/Abstract
            print("📝 Génération du résumé...")
            story.extend(self.create_abstract_page(data))
            
            # 4. Table des matières
            print("📑 Génération de la table des matières...")
            story.extend(self.create_table_of_contents(data))
            
            # 5. Chapitres du rapport
            chapters_data = data.get('chapters_data', [])
            if not chapters_data:
                # Chapitres par défaut si non fournis
                chapters_data = [
                    {
                        'title': 'INTRODUCTION GÉNÉRALE',
                        'introduction': 'Ce chapitre présente le contexte général du stage, les objectifs poursuivis et la structure du rapport.',
                        'sections': [
                            {
                                'title': '1.1 Contexte du stage',
                                'content': [
                                    'Le stage s\'est déroulé au sein de l\'entreprise ' + data.get('company_name', '') + '.',
                                    'Durée : ' + data.get('duration', '') + '.',
                                    'Encadrement : ' + data.get('academic_supervisor', '') + ' (ENSAO) et ' + data.get('company_supervisor', '') + ' (entreprise).'
                                ]
                            },
                            {
                                'title': '1.2 Objectifs du projet',
                                'content': 'Les objectifs principaux étaient de ' + data.get('project_objective', 'réaliser un projet technique') + '.'
                            }
                        ],
                        'conclusion': 'Cette introduction a permis de poser le cadre général du stage et de présenter les objectifs poursuivis.',
                        'add_page_break': True
                    }
                ]
            
            for i, chapter in enumerate(chapters_data):
                print(f"📖 Génération du chapitre {i+1}...")
                story.extend(self.create_chapter(chapter))
            
            # 6. Bibliographie
            print("📚 Génération de la bibliographie...")
            bibliography = data.get('bibliography', [
                'ISO 690 - Norme internationale pour les références bibliographiques',
                'R. Pressman, "Ingénierie du logiciel", 2010',
                'J. Rumbaugh, "UML : Modélisation et conception orientée objet", 2007'
            ])
            
            story.append(Paragraph("BIBLIOGRAPHIE", self.styles['ChapterTitle']))
            story.append(Spacer(1, 1*cm))
            
            for ref in bibliography:
                story.append(Paragraph(f"• {ref}", self.styles['ListBullet']))
            
            # 7. Annexes
            print("📎 Génération des annexes...")
            story.append(PageBreak())
            story.append(Paragraph("ANNEXES", self.styles['ChapterTitle']))
            story.append(Spacer(1, 1*cm))
            
            annexes = data.get('annexes', [
                'Annexe 1 : Organigramme de l\'entreprise',
                'Annexe 2 : Planning du projet',
                'Annexe 3 : Documentation technique'
            ])
            
            for annexe in annexes:
                story.append(Paragraph(annexe, self.styles['NormalLeft']))
                story.append(Spacer(1, 0.5*cm))
            
            # Générer le PDF avec en-tête et pied de page
            print("⚡ Génération du PDF final...")
            doc.build(story, onFirstPage=self._header_footer, onLaterPages=self._header_footer)
            
            # Vérifier que le fichier a été créé
            if os.path.exists(self.output_path):
                file_size = os.path.getsize(self.output_path)
                print(f"✅ PDF généré avec succès : {self.output_path} ({file_size:,} octets)")
                
                return {
                    'success': True,
                    'path': os.path.abspath(self.output_path),
                    'file_size': file_size,
                    'generated_at': datetime.now().isoformat(),
                    'message': 'Rapport PDF généré avec succès'
                }
            else:
                return {
                    'success': False,
                    'error': 'Fichier non créé',
                    'message': 'Le fichier PDF n\'a pas été créé'
                }
                
        except Exception as e:
            print(f"❌ Erreur lors de la génération du PDF: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': f'Erreur lors de la génération du PDF: {str(e)[:100]}'
            }
    
    def generate_quick_pdf(self, content: str, title: str = "Rapport") -> Dict[str, Any]:
        """
        Génère un PDF rapide à partir d'un contenu texte simple
        
        Args:
            content: Contenu textuel
            title: Titre du document
            
        Returns:
            Dictionnaire avec le statut et les informations du PDF
        """
        try:
            # Créer le document simple
            doc = SimpleDocTemplate(
                self.output_path,
                pagesize=A4,
                topMargin=2*cm,
                bottomMargin=2*cm,
                leftMargin=2.5*cm,
                rightMargin=2.5*cm,
                title=title
            )
            
            story = []
            
            # Titre
            story.append(Paragraph(title, self.styles['Title']))
            story.append(Spacer(1, 1*cm))
            
            # Contenu
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para, self.styles['Normal']))
                    story.append(Spacer(1, 0.5*cm))
            
            # Générer le PDF
            doc.build(story)
            
            if os.path.exists(self.output_path):
                return {
                    'success': True,
                    'path': self.output_path,
                    'message': 'PDF rapide généré avec succès'
                }
            else:
                return {
                    'success': False,
                    'error': 'Fichier non créé'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def generate_quick_pdf(content: str, output_path: str = "output.pdf", 
                       title: str = "Document") -> Dict[str, Any]:
    """
    Fonction utilitaire pour générer un PDF rapide
    
    Args:
        content: Contenu textuel
        output_path: Chemin du fichier de sortie
        title: Titre du document
        
    Returns:
        Dictionnaire avec le statut et les informations
    """
    try:
        generator = PDFGenerator(output_path)
        return generator.generate_quick_pdf(content, title)
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de la génération du PDF rapide'
        }


def generate_full_report_pdf(data: Dict, output_path: str = "rapport_complet.pdf") -> Dict[str, Any]:
    """
    Fonction utilitaire pour générer un rapport PDF complet
    
    Args:
        data: Données du rapport
        output_path: Chemin du fichier de sortie
        
    Returns:
        Dictionnaire avec le statut et les informations
    """
    try:
        generator = PDFGenerator(output_path)
        return generator.generate_full_report(data)
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'message': 'Erreur lors de la génération du rapport complet'
        }


# Exemple d'utilisation
if __name__ == "__main__":
    # Données d'exemple
    sample_data = {
        'title': "Rapport de Stage de Fin d'Études",
        'filiere': "Génie Informatique",
        'project_title': "Développement d'une Application Web pour la Gestion de Projets",
        'student_name': "Mohammed ALAMI",
        'academic_supervisor': "Dr. Ahmed BENANI",
        'company_supervisor': "M. Karim EL FASSI",
        'company_name': "TechSolutions SARL",
        'duration': "2 mois (Juillet-Août 2024)",
        'academic_year': "2023-2024",
        'project_objective': "développer une application web complète pour la gestion de projets",
        'problem_description': "la gestion manuelle des projets dans l'entreprise",
        'methodology': "une approche Agile Scrum",
        'main_results': "une amélioration de 40% de l'efficacité de gestion",
        'achievements': "automatiser les processus de suivi et de reporting",
        'keywords': "stage, rapport, mémoire, ENSAO, ingénieur, projet, développement web, gestion de projets",
        'keywords_eng': "internship, report, thesis, ENSAO, engineer, project, web development, project management",
        
        'chapters_data': [
            {
                'title': 'INTRODUCTION GÉNÉRALE',
                'introduction': 'Ce chapitre présente le contexte, les objectifs et la structure du rapport.',
                'sections': [
                    {
                        'title': '1.1 Contexte du stage',
                        'content': [
                            'Le stage s\'est déroulé chez TechSolutions SARL, une entreprise spécialisée dans le développement de solutions logicielles.',
                            'Durée : 2 mois (Juillet-Août 2024).',
                            'Objectif principal : Développer une application web pour la gestion de projets.'
                        ]
                    },
                    {
                        'title': '1.2 Objectifs spécifiques',
                        'content': [
                            'Analyser les besoins de l\'entreprise',
                            'Concevoir l\'architecture de l\'application',
                            'Développer les fonctionnalités principales',
                            'Tester et valider la solution',
                            'Documenter le projet'
                        ]
                    }
                ],
                'conclusion': 'Cette introduction a permis de définir le cadre et les objectifs du stage.',
                'add_page_break': True
            }
        ]
    }
    
    # Générer le PDF
    print("🚀 Démarrage de la génération du PDF...")
    result = generate_full_report_pdf(sample_data, "exemple_rapport.pdf")
    
    if result['success']:
        print(f"✅ Succès ! PDF généré : {result['path']}")
        print(f"📏 Taille : {result.get('file_size', 0):,} octets")
    else:
        print(f"❌ Échec : {result.get('message', 'Erreur inconnue')}")