"""
Générateur de rapports de stage avec analyse de style
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from .ai_generator import AIGenerator

class StageReportGenerator:
    """Générateur intelligent de rapports de stage ENSAO"""
    
    # Sections standard avec descriptions
    STANDARD_SECTIONS = [
        {
            'id': 'cover_page',
            'name': 'Page de couverture',
            'description': 'Page officielle avec toutes les informations',
            'required': True
        },
        {
            'id': 'thanks',
            'name': 'Remerciements',
            'description': 'Remerciements académiques et professionnels',
            'required': True
        },
        {
            'id': 'abstract',
            'name': 'Résumés',
            'description': 'Résumé français et abstract anglais',
            'required': True
        },
        {
            'id': 'introduction',
            'name': 'Introduction générale',
            'description': 'Contexte, problématique et objectifs',
            'required': True
        },
        {
            'id': 'company_presentation',
            'name': 'Présentation de l\'entreprise',
            'description': 'Description de l\'entreprise d\'accueil',
            'required': True
        },
        {
            'id': 'methodology',
            'name': 'Méthodologie de travail',
            'description': 'Approche, outils et organisation',
            'required': True
        },
        {
            'id': 'realization',
            'name': 'Réalisation technique',
            'description': 'Développement et implémentation',
            'required': True
        },
        {
            'id': 'results',
            'name': 'Résultats et discussion',
            'description': 'Analyse et validation des résultats',
            'required': True
        },
        {
            'id': 'conclusion',
            'name': 'Conclusion et perspectives',
            'description': 'Bilan du stage et perspectives',
            'required': True
        },
        {
            'id': 'bibliography',
            'name': 'Bibliographie',
            'description': 'Références bibliographiques',
            'required': True
        },
        {
            'id': 'annexes',
            'name': 'Annexes',
            'description': 'Documents complémentaires',
            'required': False
        }
    ]
    
    def __init__(self, 
                 student_info: Dict,
                 company_info: Dict,
                 reference_text: str = None,
                 options: Optional[Dict] = None):
        """
        Initialise le générateur de rapport
        
        Args:
            student_info: Informations de l'étudiant
            company_info: Informations de l'entreprise
            reference_text: Texte de référence pour l'analyse de style
            options: Options de génération
        """
        self.student = self._validate_student_info(student_info)
        self.company = self._validate_company_info(company_info)
        self.reference_text = reference_text
        self.options = options or {
            'writing_style': 'académique',
            'language': 'fr',
            'target_length': '60-80 pages',
            'academic_level': 'licence'
        }
        
        # ID unique pour ce rapport
        self.report_id = str(uuid.uuid4())[:8]
        
        # Initialiser le générateur IA
        self.ai_generator = AIGenerator(
            api_key=options.get('api_key') if options else None,
            reference_text=reference_text
        )
        
        # Stocker les sections générées
        self.sections = {}
        self.sections_metadata = {}
        
        # Statistiques
        self.stats = {
            'total_words': 0,
            'sections_generated': 0,
            'sections_edited': 0,
            'generation_time': 0,
            'last_updated': datetime.now().isoformat()
        }
    
    def _validate_student_info(self, student_info: Dict) -> Dict:
        """Valide et complète les informations étudiant"""
        required_fields = ['full_name', 'project_title', 'filiere']
        default_values = {
            'filiere': 'Génie Informatique',
            'academic_year': '2024-2025',
            'duration': '2 mois',
            'supervisor': 'Dr. NOM Prénom'
        }
        
        validated = student_info.copy()
        
        # Vérifier les champs requis
        for field in required_fields:
            if field not in validated or not validated[field]:
                raise ValueError(f"Le champ '{field}' est requis pour l'étudiant")
        
        # Appliquer les valeurs par défaut
        for field, default in default_values.items():
            if field not in validated or not validated[field]:
                validated[field] = default
        
        # Formater le nom
        if 'full_name' in validated:
            validated['full_name'] = validated['full_name'].strip().upper()
        
        return validated
    
    def _validate_company_info(self, company_info: Dict) -> Dict:
        """Valide et complète les informations entreprise"""
        default_values = {
            'sector': 'Informatique',
            'supervisor': 'M. NOM Prénom',
            'location': 'Non spécifiée'
        }
        
        validated = company_info.copy()
        
        # Vérifier le nom de l'entreprise
        if 'name' not in validated or not validated['name']:
            raise ValueError("Le nom de l'entreprise est requis")
        
        # Appliquer les valeurs par défaut
        for field, default in default_values.items():
            if field not in validated or not validated[field]:
                validated[field] = default
        
        return validated
    
    def generate_full_report(self) -> Dict:
        """
        Génère un rapport complet avec toutes les sections
        
        Returns:
            Dict avec le contenu et les métadonnées
        """
        start_time = datetime.now()
        
        report_data = {
            'report_id': self.report_id,
            'student': self.student,
            'company': self.company,
            'options': self.options,
            'generated_at': start_time.isoformat(),
            'sections': {},
            'metadata': {}
        }
        
        # Générer chaque section
        for section_info in self.STANDARD_SECTIONS:
            if section_info['required']:
                section_id = section_info['id']
                
                try:
                    result = self.generate_section(section_id)
                    
                    if result['success']:
                        report_data['sections'][section_id] = result['content']
                        report_data['metadata'][section_id] = result['metadata']
                        
                        # Mettre à jour les statistiques
                        self.stats['sections_generated'] += 1
                        self.stats['total_words'] += result['metadata'].get('word_count', 0)
                    else:
                        report_data['sections'][section_id] = f"<p>Erreur lors de la génération: {result.get('error', 'Inconnue')}</p>"
                        report_data['metadata'][section_id] = result['metadata']
                        
                except Exception as e:
                    error_msg = f"<p>Erreur critique: {str(e)[:200]}</p>"
                    report_data['sections'][section_id] = error_msg
                    report_data['metadata'][section_id] = {
                        'section': section_id,
                        'error': str(e),
                        'generated_at': datetime.now().isoformat()
                    }
        
        # Calculer le temps de génération
        end_time = datetime.now()
        generation_time = (end_time - start_time).total_seconds()
        
        report_data['generation_time'] = generation_time
        report_data['stats'] = self.stats.copy()
        report_data['stats']['generation_time'] = generation_time
        
        # Ajouter l'analyse de style
        report_data['style_analysis'] = self.ai_generator.get_style_analysis_report()
        
        return report_data
    
    def generate_section(self, section_id: str, custom_prompt: str = None) -> Dict:
        """
        Génère une section spécifique du rapport
        
        Args:
            section_id: Identifiant de la section
            custom_prompt: Prompt personnalisé (optionnel)
        
        Returns:
            Dict avec 'content' et 'metadata'
        """
        # Vérifier si la section existe
        section_info = next((s for s in self.STANDARD_SECTIONS if s['id'] == section_id), None)
        if not section_info:
            raise ValueError(f"Section '{section_id}' non reconnue")
        
        # Préparer le contexte
        context = {
            'student': self.student,
            'company': self.company,
            'options': self.options,
            'section': section_id
        }
        
        # Générer le contenu
        if custom_prompt:
            # Utiliser le prompt personnalisé
            result = self._generate_with_custom_prompt(section_id, custom_prompt, context)
        else:
            # Utiliser le générateur IA standard
            result = self.ai_generator.generate_section(section_id, context)
        
        # Stocker la section
        self.sections[section_id] = result['content']
        self.sections_metadata[section_id] = result['metadata']
        
        # Mettre à jour les statistiques
        self.stats['last_updated'] = datetime.now().isoformat()
        
        return result
    
    def _generate_with_custom_prompt(self, section_id: str, prompt: str, context: Dict) -> Dict:
        """Génère avec un prompt personnalisé"""
        try:
            # Ici, on pourrait adapter la logique pour utiliser un prompt personnalisé
            # Pour l'instant, on utilise la méthode standard
            return self.ai_generator.generate_section(section_id, context)
        except Exception as e:
            return {
                'content': f"<p>Erreur avec prompt personnalisé: {str(e)[:200]}</p>",
                'metadata': {
                    'section': section_id,
                    'error': str(e),
                    'custom_prompt_used': True,
                    'generated_at': datetime.now().isoformat()
                },
                'success': False
            }
    
    def edit_section(self, section_id: str, new_content: str) -> bool:
        """
        Modifie le contenu d'une section existante
        
        Args:
            section_id: Identifiant de la section
            new_content: Nouveau contenu
        
        Returns:
            True si succès
        """
        if section_id not in self.sections:
            raise ValueError(f"Section '{section_id}' n'existe pas")
        
        # Mettre à jour le contenu
        self.sections[section_id] = new_content
        
        # Mettre à jour les métadonnées
        if section_id in self.sections_metadata:
            self.sections_metadata[section_id]['edited'] = True
            self.sections_metadata[section_id]['edited_at'] = datetime.now().isoformat()
            self.sections_metadata[section_id]['word_count'] = len(new_content.split())
        else:
            self.sections_metadata[section_id] = {
                'section': section_id,
                'edited': True,
                'edited_at': datetime.now().isoformat(),
                'word_count': len(new_content.split())
            }
        
        # Mettre à jour les statistiques
        self.stats['sections_edited'] += 1
        self.stats['last_updated'] = datetime.now().isoformat()
        
        return True
    
    def get_section_content(self, section_id: str) -> str:
        """Retourne le contenu d'une section"""
        return self.sections.get(section_id, '')
    
    def get_section_metadata(self, section_id: str) -> Dict:
        """Retourne les métadonnées d'une section"""
        return self.sections_metadata.get(section_id, {})
    
    def get_report_summary(self) -> Dict:
        """Retourne un résumé du rapport"""
        return {
            'report_id': self.report_id,
            'student_name': self.student.get('full_name'),
            'project_title': self.student.get('project_title'),
            'company': self.company.get('name'),
            'filiere': self.student.get('filiere'),
            'sections_count': len(self.sections),
            'total_words': self.stats['total_words'],
            'sections_generated': self.stats['sections_generated'],
            'sections_edited': self.stats['sections_edited'],
            'last_updated': self.stats['last_updated']
        }
    
    def get_style_analysis(self) -> Dict:
        """Retourne l'analyse de style"""
        return self.ai_generator.get_style_analysis_report()
    
    def get_academic_tips(self) -> List[Dict]:
        """Retourne des conseils académiques"""
        return self.ai_generator.get_academic_tips()
    
    def validate_report_data(self) -> Dict:
        """
        Valide les données du rapport
        
        Returns:
            Dict avec validation results
        """
        errors = []
        warnings = []
        
        # Validation étudiant
        if len(self.student.get('full_name', '').strip()) < 5:
            errors.append("Nom étudiant trop court (minimum 5 caractères)")
        
        if len(self.student.get('project_title', '').strip()) < 10:
            errors.append("Titre du projet trop court (minimum 10 caractères)")
        
        # Validation entreprise
        if len(self.company.get('name', '').strip()) < 3:
            errors.append("Nom entreprise trop court")
        
        # Vérification des dates
        if 'start_date' in self.student and 'end_date' in self.student:
            try:
                start = datetime.strptime(self.student['start_date'], '%Y-%m-%d')
                end = datetime.strptime(self.student['end_date'], '%Y-%m-%d')
                if end < start:
                    errors.append("La date de fin doit être après la date de début")
            except ValueError:
                warnings.append("Format de date invalide, utiliser YYYY-MM-DD")
        
        # Vérification des sections requises
        required_sections = [s['id'] for s in self.STANDARD_SECTIONS if s['required']]
        missing_sections = [s for s in required_sections if s not in self.sections]
        
        if missing_sections:
            warnings.append(f"Sections manquantes: {', '.join(missing_sections)}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'sections_present': list(self.sections.keys()),
            'total_sections': len(self.sections)
        }
    
    def estimate_report_length(self) -> Dict:
        """Estime la longueur du rapport"""
        total_words = self.stats['total_words']
        
        # Estimation basée sur le nombre de mots
        # Environ 300 mots par page en format académique
        estimated_pages = max(15, round(total_words / 300))
        
        if estimated_pages < 30:
            length_category = 'court'
        elif estimated_pages < 60:
            length_category = 'moyen'
        else:
            length_category = 'long'
        
        return {
            'estimated_pages': estimated_pages,
            'estimated_words': total_words,
            'length_category': length_category,
            'sections_count': len(self.sections),
            'meets_requirements': estimated_pages >= 40  # Minimum pour un PFE
        }
    
    def export_to_dict(self) -> Dict:
        """Exporte le rapport complet sous forme de dictionnaire"""
        return {
            'report_id': self.report_id,
            'student': self.student,
            'company': self.company,
            'options': self.options,
            'sections': self.sections,
            'metadata': self.sections_metadata,
            'stats': self.stats,
            'style_analysis': self.get_style_analysis(),
            'validation': self.validate_report_data(),
            'exported_at': datetime.now().isoformat()
        }
    
    def import_from_dict(self, data: Dict) -> bool:
        """Importe un rapport depuis un dictionnaire"""
        try:
            self.report_id = data.get('report_id', self.report_id)
            self.student = data.get('student', self.student)
            self.company = data.get('company', self.company)
            self.options = data.get('options', self.options)
            self.sections = data.get('sections', self.sections)
            self.sections_metadata = data.get('metadata', self.sections_metadata)
            self.stats = data.get('stats', self.stats)
            
            # Recréer le générateur IA avec le texte de référence si disponible
            if 'reference_text' in data:
                self.reference_text = data['reference_text']
                self.ai_generator = AIGenerator(
                    api_key=self.options.get('api_key'),
                    reference_text=self.reference_text
                )
            
            return True
            
        except Exception as e:
            print(f"Erreur import: {str(e)}")
            return False