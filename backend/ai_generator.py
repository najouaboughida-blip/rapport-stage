"""
Générateur IA avec analyse de style académique intelligent - VERSION COMPLÈTE
"""

import json
import re
import random
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import time
import numpy as np

class AcademicPromptGenerator:
    """Générateur intelligent de prompts académiques avec analyse de style avancée"""
    
    def __init__(self, reference_text: str = None, style_data: Dict = None):
        """
        Initialise le générateur avec un texte de référence
        
        Args:
            reference_text: Texte de référence pour l'analyse de style
            style_data: Données de style pré-analysées
        """
        self.reference_text = reference_text
        self.style_data = style_data or self._analyze_style() if reference_text else {}
        self.academic_level = self._determine_academic_level()
        
        # Base de données de phrases académiques
        self.academic_phrases_db = self._load_academic_phrases()
        
        # Configurations de style
        self.style_configs = {
            'très_formel': {
                'pronoun': 'nous',
                'sentence_length': (20, 35),
                'complexity': 'élevée',
                'vocabulary': 'technique_avancé',
                'phrases': [
                    'Il convient de souligner que',
                    'Il apparaît nécessaire de',
                    'Nous nous proposons d\'examiner',
                    'Il importe de préciser que'
                ]
            },
            'académique_formel': {
                'pronoun': 'nous',
                'sentence_length': (18, 28),
                'complexity': 'moyenne',
                'vocabulary': 'technique',
                'phrases': [
                    'Nous présentons dans cette section',
                    'Il est important de noter que',
                    'Cette approche permet de',
                    'Les résultats obtenus montrent que'
                ]
            },
            'professionnel': {
                'pronoun': 'nous',
                'sentence_length': (15, 25),
                'complexity': 'modérée',
                'vocabulary': 'professionnel',
                'phrases': [
                    'Le projet vise à',
                    'La solution mise en place',
                    'L\'analyse réalisée a permis',
                    'Les objectifs principaux sont'
                ]
            }
        }
    
    def _load_academic_phrases(self) -> Dict[str, List[str]]:
        """Charge la base de données de phrases académiques"""
        return {
            'introduction': [
                "Dans le cadre de notre stage de fin d'études effectué au sein de",
                "Ce rapport s'inscrit dans la continuité des travaux réalisés pendant",
                "L'objectif principal de ce mémoire est de présenter",
                "Il convient de souligner que cette étude se focalise sur",
                "Notre travail s'inscrit dans le domaine de"
            ],
            'transition': [
                "Par ailleurs, il est important de noter que",
                "Dans cette perspective, nous pouvons constater que",
                "En ce qui concerne",
                "À cet égard, il est nécessaire de préciser que",
                "Dans un second temps, nous aborderons"
            ],
            'analysis': [
                "L'analyse réalisée a permis de mettre en évidence",
                "Les résultats obtenus démontrent que",
                "Il ressort de cette étude que",
                "L'examen approfondi révèle que",
                "Les données collectées indiquent que"
            ],
            'conclusion': [
                "En définitive, cette étude a permis de mettre en évidence",
                "Pour conclure, nous pouvons affirmer que",
                "En somme, les résultats obtenus démontrent que",
                "En guise de conclusion, il apparaît que",
                "Au terme de ce travail, nous pouvons retenir que"
            ],
            'methodology': [
                "La méthodologie adoptée repose sur",
                "L'approche choisie consiste à",
                "Le protocole expérimental mis en place",
                "Les outils méthodologiques utilisés incluent",
                "La démarche suivie a été"
            ]
        }
    
    def _analyze_style(self) -> Dict:
        """Analyse approfondie du style d'écriture"""
        if not self.reference_text or len(self.reference_text.strip()) < 50:
            return self._get_default_style()
        
        text = self.reference_text.strip()
        
        # Analyses principales
        word_analysis = self._analyze_words(text)
        sentence_analysis = self._analyze_sentences(text)
        structure_analysis = self._analyze_structure(text)
        vocabulary_analysis = self._analyze_vocabulary(text)
        
        # Scores composites
        formality_score = self._calculate_formality_score(text, word_analysis)
        complexity_score = self._calculate_complexity_score(sentence_analysis)
        academic_score = self._calculate_academic_score(vocabulary_analysis)
        
        # Rapport complet
        analysis = {
            'basic_stats': {
                'word_count': word_analysis['total_words'],
                'sentence_count': sentence_analysis['total_sentences'],
                'paragraph_count': structure_analysis['paragraph_count'],
                'avg_word_length': word_analysis['avg_word_length'],
                'avg_sentence_length': sentence_analysis['avg_length'],
                'avg_paragraph_length': structure_analysis['avg_paragraph_length']
            },
            'style_scores': {
                'formality_score': formality_score,
                'complexity_score': complexity_score,
                'academic_score': academic_score,
                'readability_score': self._calculate_readability_score(text),
                'cohesion_score': self._calculate_cohesion_score(text)
            },
            'linguistic_features': {
                'pronoun_usage': word_analysis['pronoun_distribution'],
                'verb_tenses': word_analysis['verb_tenses'],
                'sentence_types': sentence_analysis['sentence_types'],
                'transition_words': structure_analysis['transition_words'],
                'academic_indicators': vocabulary_analysis['academic_indicators']
            },
            'vocabulary_analysis': {
                'richness_score': vocabulary_analysis['richness_score'],
                'technical_terms': vocabulary_analysis['technical_terms'],
                'academic_terms': vocabulary_analysis['academic_terms'],
                'most_used_words': vocabulary_analysis['most_frequent'][:10]
            },
            'structural_patterns': {
                'paragraph_structure': structure_analysis['paragraph_patterns'],
                'section_organization': structure_analysis['section_patterns'],
                'argumentation_pattern': structure_analysis['argument_pattern']
            },
            'recommendations': self._generate_style_recommendations(
                formality_score, complexity_score, academic_score,
                word_analysis, sentence_analysis
            )
        }
        
        return analysis
    
    def _analyze_words(self, text: str) -> Dict:
        """Analyse des mots"""
        words = re.findall(r'\b\w+\b', text.lower())
        
        analysis = {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
            'pronoun_distribution': self._analyze_pronouns(text),
            'verb_tenses': self._analyze_verb_tenses(text),
            'word_frequency': self._calculate_word_frequency(words)
        }
        
        return analysis
    
    def _analyze_pronouns(self, text: str) -> Dict:
        """Analyse de l'usage des pronoms"""
        pronouns = {
            'nous': len(re.findall(r'\bnous\b', text.lower())),
            'je': len(re.findall(r'\bje\b', text.lower())),
            'il': len(re.findall(r'\bil\b', text.lower())),
            'elle': len(re.findall(r'\belle\b', text.lower())),
            'on': len(re.findall(r'\bon\b', text.lower()))
        }
        
        total = sum(pronouns.values())
        if total > 0:
            return {k: v/total for k, v in pronouns.items()}
        return pronouns
    
    def _analyze_verb_tenses(self, text: str) -> Dict:
        """Analyse des temps verbaux"""
        # Simplifié - analyse basée sur les terminaisons
        tenses = {
            'présent': len(re.findall(r'\b(?:est|sont|fait|font|peut|doit|veut)\b', text.lower())),
            'passé': len(re.findall(r'\b(?:était|fut|fit|furent|avait|eut)\b', text.lower())),
            'futur': len(re.findall(r'\b(?:sera|fera|devra|pourra)\b', text.lower())),
            'conditionnel': len(re.findall(r'\b(?:serait|ferait|devrait|pourrait)\b', text.lower()))
        }
        
        return tenses
    
    def _analyze_sentences(self, text: str) -> Dict:
        """Analyse des phrases"""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        if not sentences:
            return {
                'total_sentences': 0,
                'avg_length': 0,
                'sentence_types': {},
                'complexity_distribution': {}
            }
        
        lengths = [len(s.split()) for s in sentences]
        
        analysis = {
            'total_sentences': len(sentences),
            'avg_length': np.mean(lengths),
            'std_length': np.std(lengths) if len(lengths) > 1 else 0,
            'sentence_types': self._classify_sentence_types(sentences),
            'complexity_distribution': self._analyze_sentence_complexity(sentences)
        }
        
        return analysis
    
    def _classify_sentence_types(self, sentences: List[str]) -> Dict:
        """Classe les types de phrases"""
        types = {
            'simple': 0,
            'complexe': 0,
            'composée': 0
        }
        
        for sentence in sentences:
            words = sentence.split()
            if len(words) < 15:
                types['simple'] += 1
            elif ',' in sentence or ';' in sentence:
                types['complexe'] += 1
            else:
                types['composée'] += 1
        
        total = len(sentences)
        if total > 0:
            return {k: v/total for k, v in types.items()}
        return types
    
    def _analyze_sentence_complexity(self, sentences: List[str]) -> Dict:
        """Analyse la complexité des phrases"""
        complexity_indicators = [
            ('subordonnées', r'\b(?:qui|que|dont|où|si|quand|comme|parce que)\b'),
            ('conjonctions', r'\b(?:et|ou|mais|donc|or|ni|car)\b'),
            ('relative', r'\b(?:lequel|laquelle|duquel|auquel)\b')
        ]
        
        results = {}
        for name, pattern in complexity_indicators:
            count = sum(len(re.findall(pattern, s.lower())) for s in sentences)
            results[name] = count / len(sentences) if sentences else 0
        
        return results
    
    def _analyze_structure(self, text: str) -> Dict:
        """Analyse la structure du texte"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        analysis = {
            'paragraph_count': len(paragraphs),
            'avg_paragraph_length': np.mean([len(p.split()) for p in paragraphs]) if paragraphs else 0,
            'transition_words': self._count_transition_words(text),
            'paragraph_patterns': self._analyze_paragraph_patterns(paragraphs),
            'section_patterns': self._detect_section_patterns(text),
            'argument_pattern': self._detect_argument_pattern(text)
        }
        
        return analysis
    
    def _count_transition_words(self, text: str) -> List[Tuple[str, int]]:
        """Compte les mots de transition"""
        transition_words = [
            'premièrement', 'deuxièmement', 'troisièmement',
            'd\'abord', 'ensuite', 'enfin',
            'par ailleurs', 'en outre', 'de plus',
            'cependant', 'toutefois', 'néanmoins',
            'par conséquent', 'donc', 'ainsi',
            'par exemple', 'notamment', 'entre autres'
        ]
        
        counts = []
        text_lower = text.lower()
        for word in transition_words:
            count = len(re.findall(r'\b' + word + r'\b', text_lower))
            if count > 0:
                counts.append((word, count))
        
        return sorted(counts, key=lambda x: x[1], reverse=True)[:10]
    
    def _analyze_vocabulary(self, text: str) -> Dict:
        """Analyse du vocabulaire"""
        words = re.findall(r'\b\w+\b', text.lower())
        unique_words = set(words)
        
        # Termes académiques
        academic_terms = self._extract_academic_terms(text)
        technical_terms = self._extract_technical_terms(text)
        
        analysis = {
            'richness_score': len(unique_words) / len(words) if words else 0,
            'academic_terms': academic_terms,
            'technical_terms': technical_terms,
            'academic_indicators': self._detect_academic_indicators(text),
            'most_frequent': self._get_most_frequent_words(words, 20),
            'lexical_density': self._calculate_lexical_density(words)
        }
        
        return analysis
    
    def _extract_academic_terms(self, text: str) -> List[str]:
        """Extrait les termes académiques"""
        academic_patterns = [
            r'\b(?:problématique|hypothèse|méthodologie|cadre théorique)\b',
            r'\b(?:revue de littérature|état de l\'art|corpus d\'étude)\b',
            r'\b(?:analyse|synthèse|discussion|conclusion|perspective)\b',
            r'\b(?:expérimentation|validation|évaluation|optimisation)\b'
        ]
        
        terms = []
        text_lower = text.lower()
        for pattern in academic_patterns:
            terms.extend(re.findall(pattern, text_lower))
        
        return list(set(terms))[:15]
    
    def _calculate_formality_score(self, text: str, word_analysis: Dict) -> float:
        """Calcule le score de formalité"""
        formal_indicators = [
            'nous', 'il convient', 'souligner', 'notons que', 'par conséquent',
            'cependant', 'toutefois', 'néanmoins', 'en outre', 'par ailleurs'
        ]
        
        informal_indicators = [
            'je', 'moi', 'perso', 'super', 'cool', 'trop', 'genre',
            'je pense que', 'je crois que', 'je trouve que', 'j\'aime'
        ]
        
        text_lower = text.lower()
        formal_count = sum(len(re.findall(r'\b' + ind + r'\b', text_lower)) 
                          for ind in formal_indicators)
        informal_count = sum(len(re.findall(r'\b' + ind + r'\b', text_lower)) 
                           for ind in informal_indicators)
        
        # Poids de l'usage des pronoms
        pronoun_dist = word_analysis.get('pronoun_distribution', {})
        nous_ratio = pronoun_dist.get('nous', 0)
        je_ratio = pronoun_dist.get('je', 0)
        
        # Calcul du score
        total = formal_count + informal_count
        base_score = (formal_count / total * 100) if total > 0 else 50
        
        # Ajustement basé sur les pronoms
        if nous_ratio > je_ratio * 2:
            base_score += 15
        elif je_ratio > nous_ratio:
            base_score -= 10
        
        return min(100, max(0, base_score))
    
    def _calculate_complexity_score(self, sentence_analysis: Dict) -> float:
        """Calcule le score de complexité"""
        avg_length = sentence_analysis.get('avg_length', 20)
        sentence_types = sentence_analysis.get('sentence_types', {})
        
        # Score basé sur la longueur moyenne
        length_score = min(100, (avg_length / 30) * 100)
        
        # Score basé sur la complexité des phrases
        complex_ratio = sentence_types.get('complexe', 0)
        complexity_score = complex_ratio * 100
        
        # Score composite
        return (length_score * 0.6 + complexity_score * 0.4)
    
    def _calculate_academic_score(self, vocabulary_analysis: Dict) -> float:
        """Calcule le score académique"""
        academic_terms = len(vocabulary_analysis.get('academic_terms', []))
        technical_terms = len(vocabulary_analysis.get('technical_terms', []))
        richness = vocabulary_analysis.get('richness_score', 0)
        
        # Score basé sur les termes académiques
        term_score = min(100, (academic_terms + technical_terms) * 10)
        
        # Score basé sur la richesse lexicale
        richness_score = richness * 100
        
        return (term_score * 0.7 + richness_score * 0.3)
    
    def _calculate_readability_score(self, text: str) -> float:
        """Calcule le score de lisibilité (adaptation Flesch pour le français)"""
        words = re.findall(r'\b\w+\b', text)
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        if not words or not sentences:
            return 50
        
        # Nombre de syllabes approximatif
        vowels = 'aeiouyàâäéèêëîïôöùûü'
        syllables = sum(1 for char in text.lower() if char in vowels)
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        # Formule simplifiée
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        
        return max(0, min(100, score))
    
    def _calculate_cohesion_score(self, text: str) -> float:
        """Calcule le score de cohésion"""
        transition_words = self._count_transition_words(text)
        total_transitions = sum(count for _, count in transition_words)
        
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return 50
        
        # Score basé sur la densité des mots de transition
        transition_density = (total_transitions / len(words)) * 1000
        
        return min(100, transition_density * 10)
    
    def _generate_style_recommendations(self, formality_score: float, 
                                      complexity_score: float, 
                                      academic_score: float,
                                      word_analysis: Dict,
                                      sentence_analysis: Dict) -> List[Dict]:
        """Génère des recommandations de style"""
        recommendations = []
        
        # Recommandations sur la formalité
        if formality_score < 40:
            recommendations.append({
                'category': 'style',
                'priority': 'high',
                'title': 'Améliorer la formalité',
                'description': 'Le style est trop informel pour un rapport académique.',
                'suggestions': [
                    'Remplacer "je" par "nous" ou utiliser des tournures impersonnelles',
                    'Éviter les expressions familières',
                    'Utiliser plus de connecteurs logiques formels'
                ]
            })
        elif formality_score < 60:
            recommendations.append({
                'category': 'style',
                'priority': 'medium',
                'title': 'Affiner le style académique',
                'description': 'Le style pourrait être plus formel.',
                'suggestions': [
                    'Augmenter l\'utilisation du "nous académique"',
                    'Ajouter des expressions comme "il convient de souligner"',
                    'Structurer les phrases avec des subordonnées'
                ]
            })
        
        # Recommandations sur la complexité
        avg_length = sentence_analysis.get('avg_length', 20)
        if avg_length > 30:
            recommendations.append({
                'category': 'structure',
                'priority': 'high',
                'title': 'Simplifier les phrases',
                'description': 'Les phrases sont trop longes, ce qui nuit à la lisibilité.',
                'suggestions': [
                    'Diviser les phrases de plus de 30 mots',
                    'Utiliser des points-virgules pour séparer les idées',
                    'Réorganiser les phrases complexes'
                ]
            })
        elif avg_length < 15:
            recommendations.append({
                'category': 'structure',
                'priority': 'medium',
                'title': 'Enrichir les phrases',
                'description': 'Les phrases sont trop courtes, ce qui donne un style haché.',
                'suggestions': [
                    'Combiner des phrases courtes avec des conjonctions',
                    'Développer les idées avec plus de détails',
                    'Utiliser des propositions relatives'
                ]
            })
        
        # Recommandations sur le vocabulaire
        if academic_score < 40:
            recommendations.append({
                'category': 'vocabulaire',
                'priority': 'medium',
                'title': 'Enrichir le vocabulaire',
                'description': 'Le vocabulaire pourrait être plus varié et technique.',
                'suggestions': [
                    'Utiliser plus de synonymes',
                    'Intégrer des termes techniques spécifiques',
                    'Consulter un glossaire académique'
                ]
            })
        
        return recommendations
    
    def _get_default_style(self) -> Dict:
        """Retourne une analyse de style par défaut"""
        return {
            'basic_stats': {
                'word_count': 0,
                'sentence_count': 0,
                'paragraph_count': 0,
                'avg_word_length': 5,
                'avg_sentence_length': 20,
                'avg_paragraph_length': 100
            },
            'style_scores': {
                'formality_score': 70,
                'complexity_score': 60,
                'academic_score': 65,
                'readability_score': 65,
                'cohesion_score': 60
            },
            'linguistic_features': {
                'pronoun_usage': {'nous': 0.8, 'je': 0.1, 'il': 0.1},
                'verb_tenses': {'présent': 0.7, 'passé': 0.2, 'futur': 0.1},
                'sentence_types': {'simple': 0.4, 'complexe': 0.4, 'composée': 0.2},
                'transition_words': [('premièrement', 1), ('ensuite', 1), ('enfin', 1)],
                'academic_indicators': ['analyse', 'méthodologie', 'conclusion']
            },
            'vocabulary_analysis': {
                'richness_score': 0.6,
                'technical_terms': ['système', 'application', 'développement'],
                'academic_terms': ['problématique', 'méthodologie', 'résultats'],
                'most_used_words': [('le', 10), ('la', 8), ('et', 7)]
            },
            'structural_patterns': {
                'paragraph_structure': 'standard',
                'section_organization': 'logique',
                'argumentation_pattern': 'déductive'
            },
            'recommendations': []
        }
    
    def _determine_academic_level(self) -> str:
        """Détermine le niveau académique"""
        if not self.reference_text:
            return 'licence'
        
        word_count = len(self.reference_text.split())
        if word_count > 1000:
            return 'master'
        elif word_count > 500:
            return 'licence_avancée'
        else:
            return 'licence'
    
    def get_style_report(self) -> Dict:
        """Retourne un rapport complet d'analyse de style"""
        if not self.style_data:
            return {
                'status': 'no_analysis',
                'message': 'Aucune analyse disponible. Fournissez un texte de référence.',
                'timestamp': datetime.now().isoformat()
            }
        
        # Résumé simplifié pour l'interface
        summary = {
            'academic_level': self.academic_level,
            'formality_score': self.style_data['style_scores']['formality_score'],
            'formality_level': self._get_formality_level(
                self.style_data['style_scores']['formality_score']
            ),
            'complexity': self._get_complexity_level(
                self.style_data['style_scores']['complexity_score']
            ),
            'vocabulary': self._get_vocabulary_level(
                self.style_data['vocabulary_analysis']['richness_score']
            ),
            'readability': self._get_readability_level(
                self.style_data['style_scores']['readability_score']
            ),
            'technical_terms_count': len(
                self.style_data['vocabulary_analysis']['technical_terms']
            )
        }
        
        return {
            'status': 'complete',
            'summary': summary,
            'detailed_analysis': self.style_data,
            'recommendations': self.style_data.get('recommendations', []),
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_formality_level(self, score: float) -> str:
        if score >= 80:
            return 'très formel'
        elif score >= 60:
            return 'formel'
        elif score >= 40:
            return 'modéré'
        else:
            return 'informel'
    
    def _get_complexity_level(self, score: float) -> str:
        if score >= 70:
            return 'complexe'
        elif score >= 50:
            return 'moyenne'
        else:
            return 'simple'
    
    def _get_vocabulary_level(self, richness: float) -> str:
        if richness >= 0.7:
            return 'riche'
        elif richness >= 0.5:
            return 'moyenne'
        else:
            return 'limitée'
    
    def _get_readability_level(self, score: float) -> str:
        if score >= 70:
            return 'excellente'
        elif score >= 50:
            return 'bonne'
        else:
            return 'difficile'
    
    def generate_prompt_for_section(self, section: str, context: Dict) -> str:
        """
        Génère un prompt académique personnalisé pour une section
        
        Args:
            section: Section du rapport (cover_page, introduction, etc.)
            context: Contexte avec infos étudiant/entreprise
        
        Returns:
            Prompt académique détaillé
        """
        # Base académique selon le niveau
        base_prompt = self._get_base_academic_prompt()
        
        # Instructions de style basées sur l'analyse
        style_instructions = self._get_style_instructions()
        
        # Informations contextuelles
        context_info = self._format_context_info(context)
        
        # Instructions spécifiques à la section
        section_instructions = self._get_section_instructions(section, context)
        
        # Contraintes de formatage
        formatting_constraints = self._get_formatting_constraints(section)
        
        # Assembler le prompt
        prompt = f"""{base_prompt}

{style_instructions}

{context_info}

{section_instructions}

{formatting_constraints}

GÉNÈRE UNIQUEMENT LE CONTENU TEXTUEL DE LA SECTION, SANS COMMENTAIRES NI MÉTADONNÉES.
"""
        
        return prompt.strip()
    
    def _get_base_academic_prompt(self) -> str:
        """Retourne la base académique du prompt"""
        if self.academic_level == 'master':
            return """TU ES UN EXPERT ACADÉMIQUE DE NIVEAU MASTER, SPÉCIALISÉ DANS LA RÉDACTION DE MÉMOIRES DE RECHERCHE.

TON ÉCRITURE DOIT ÊTRE :
1. Rigoureuse et scientifiquement fondée
2. Structurée avec une argumentation solide
3. Riche en références théoriques pertinentes
4. Critique et analytique
5. Conforme aux normes académiques les plus strictes

TA MISSION : Produire un texte académique d'excellence, adapté à un public universitaire exigeant."""
        else:
            return """TU ES UN ASSISTANT ACADÉMIQUE EXPERT EN RÉDACTION DE RAPPORTS DE STAGE.

TON ÉCRITURE DOIT :
1. Respecter le style académique formel
2. Utiliser le "nous académique" systématiquement
3. Être claire, structurée et cohérente
4. Éviter les répétitions et les listes excessives
5. Suivre les normes de rédaction universitaires

TA MISSION : Produire un texte académique professionnel, adapté à un rapport de stage."""
    
    def _get_style_instructions(self) -> str:
        """Génère les instructions de style basées sur l'analyse"""
        if not self.style_data or self.style_data.get('status') == 'no_analysis':
            return """STYLE À UTILISER : Académique formel standard

Caractéristiques :
- Phrases de 18-25 mots en moyenne
- Vocabulaire technique adapté
- Connecteurs logiques modérés
- Structure paragraphes claire (5-8 lignes)
- Utilisation exclusive du "nous académique\""""
        
        summary = self.style_data.get('summary', {})
        detailed = self.style_data.get('detailed_analysis', {})
        
        instructions = f"""STYLE À REPRODUIRE (basé sur l'analyse) :

1. NIVEAU DE FORMALITÉ : {summary.get('formality_level', 'formel')}
   - Score : {summary.get('formality_score', 70)}/100
   - Conséquence : {"Utiliser exclusivement le 'nous académique'" if summary.get('formality_score', 70) > 75 else "Style formel standard"}

2. COMPLEXITÉ DES PHRASES : {summary.get('complexity', 'moyenne')}
   - Longueur recommandée : {detailed.get('basic_stats', {}).get('avg_sentence_length', 20)} mots en moyenne
   - Type : {"Phrases complexes avec subordonnées" if summary.get('complexity') == 'complexe' else "Phrases de complexité moyenne"}

3. VOCABULAIRE : {summary.get('vocabulary', 'moyenne')}
   - {"Utiliser un vocabulaire riche et varié" if summary.get('vocabulary') == 'riche' else "Vocabulaire académique standard"}
   - Termes techniques recommandés : {', '.join(detailed.get('vocabulary_analysis', {}).get('technical_terms', ['standard']))[:100]}

4. INDICATEURS ACADÉMIQUES DÉTECTÉS :
"""
        
        indicators = detailed.get('linguistic_features', {}).get('academic_indicators', [])
        if indicators:
            for indicator in indicators[:3]:
                instructions += f"   - Intégrer : '{indicator}'\n"
        else:
            instructions += "   - Aucun indicateur spécifique détecté\n"
        
        # Recommandations
        recommendations = self.style_data.get('recommendations', [])
        if recommendations:
            instructions += "\n5. RECOMMANDATIONS À INTÉGRER :\n"
            for rec in recommendations[:2]:
                instructions += f"   - {rec.get('suggestion', rec.get('title', ''))}\n"
        
        return instructions
    
    def _format_context_info(self, context: Dict) -> str:
        """Formate les informations contextuelles"""
        student = context.get('student', {})
        company = context.get('company', {})
        options = context.get('options', {})
        
        return f"""INFORMATIONS DU RAPPORT :

ÉTUDIANT :
- Nom complet : {student.get('full_name', 'NOM Prénom')}
- Filière : {student.get('filiere', 'Génie Informatique')}
- Titre du projet : "{student.get('project_title', 'Projet technique')}"
- Durée du stage : {student.get('duration', '2 mois')}
- Année universitaire : {student.get('academic_year', '2024-2025')}
- Encadrant académique : {student.get('supervisor', 'Dr. NOM Prénom')}

ENTREPRISE :
- Nom : {company.get('name', 'Entreprise')}
- Secteur d'activité : {company.get('sector', 'Informatique')}
- Encadrant professionnel : {company.get('supervisor', 'M. NOM Prénom')}
- Localisation : {company.get('location', 'Non spécifiée')}

OPTIONS DE RÉDACTION :
- Style demandé : {options.get('writing_style', 'académique_formel')}
- Longueur cible : {options.get('target_length', '60-80 pages')}
- Niveau académique : {options.get('academic_level', self.academic_level)}
"""
    
    def _get_section_instructions(self, section: str, context: Dict) -> str:
        """Retourne les instructions spécifiques à chaque section"""
        student = context.get('student', {})
        company = context.get('company', {})
        
        section_templates = {
            'cover_page': self._get_cover_page_template(student, company),
            'thanks': self._get_thanks_template(student, company),
            'abstract': self._get_abstract_template(student, company),
            'introduction': self._get_introduction_template(student, company),
            'methodology': self._get_methodology_template(student, company),
            'conclusion': self._get_conclusion_template(student, company)
        }
        
        return section_templates.get(section, self._get_default_template(student, company))
    
    def _get_cover_page_template(self, student: Dict, company: Dict) -> str:
        return f"""TU DOIS GÉNÉRER UNE PAGE DE GARDE ACADÉMIQUE PROFESSIONNELLE.

INFORMATIONS À INCLURE (DANS L'ORDRE) :
1. [LOGO] UNIVERSITÉ MOHAMMED PREMIER
2. ÉCOLE NATIONALE DES SCIENCES APPLIQUÉES - OUJDA
3. FILIÈRE : {student.get('filiere', 'Génie Informatique')}
4. "RAPPORT DE STAGE DE FIN D'ÉTUDES"
5. TITRE : "{student.get('project_title', 'Titre du projet')}"
6. "Présenté par :" {student.get('full_name', 'NOM Prénom')}
7. "Encadré par :" {student.get('supervisor', 'Dr. NOM Prénom')} (académique)
   "                 {company.get('supervisor', 'M. NOM Prénom')} ({company.get('name', 'Entreprise')})
8. "Année universitaire :" {student.get('academic_year', '2024-2025')}

FORMAT EXIGÉ :
- HTML centré verticalement et horizontalement
- Sans texte continu (structure visuelle)
- Polices académiques (Times New Roman implicitement)
- Taille de police dégressive (titre plus grand)
- Aucun commentaire supplémentaire"""
    
    def _get_thanks_template(self, student: Dict, company: Dict) -> str:
        return f"""TU DOIS RÉDIGER LA SECTION "REMERCIEMENTS".

STRUCTURE ACADÉMIQUE STRICTE :
1. Remerciement général (optionnel : expression de gratitude)
2. Remerciement à la famille pour le soutien
3. Remerciement à l'encadrant académique {student.get('supervisor', 'Dr. NOM')} pour son encadrement
4. Remerciement à l'encadrant professionnel {company.get('supervisor', 'M. NOM')} pour son accompagnement
5. Remerciement à l'entreprise {company.get('name', '')} pour l'accueil
6. Remerciement aux collègues et collaborateurs
7. Remerciement au jury (optionnel)
8. Signature : "Fait à Oujda, le [date actuelle]" + "{student.get('full_name', 'NOM Prénom')}"

STYLE EXIGÉ :
- Utiliser le "nous" académique
- Ton respectueux et formel
- Phrases complètes (pas de listes à puces)
- 1 page maximum
- Texte fluide et cohérent"""
    
    def _get_abstract_template(self, student: Dict, company: Dict) -> str:
        return f"""TU DOIS GÉNÉRER LES RÉSUMÉS ACADÉMIQUES.

A. RÉSUMÉ EN FRANÇAIS (200-250 mots exactement)
Structure obligatoire :
- Contexte : Stage chez {company.get('name', 'l\'entreprise')}, projet "{student.get('project_title', '')}"
- Problématique abordée
- Méthodologie employée
- Résultats principaux obtenus
- Conclusions majeures
- Mots-clés (5-8 termes techniques pertinents)

B. ABSTRACT IN ENGLISH (200-250 words exactly)
Same structure in academic English.

CONTRAINTES :
- Texte continu, pas de listes
- Style synthétique mais complet
- Pas de détails techniques approfondis
- Vocabulaire académique standard
- Deux sections distinctes clairement identifiées"""
    
    def _get_introduction_template(self, student: Dict, company: Dict) -> str:
        return f"""TU DOIS RÉDIGER L'INTRODUCTION GÉNÉRALE DU RAPPORT.

STRUCTURE ACADÉMIQUE STRICTE À SUIVRE :

1. CONTEXTE GÉNÉRAL (1-2 paragraphes)
   - Partir du domaine {company.get('sector', 'informatique')} en général
   - Rétrécir progressivement vers le cas spécifique
   - Justifier l'importance scientifique et professionnelle du sujet

2. CADRE DU STAGE (1 paragraphe)
   - Présentation de {company.get('name', 'l\'entreprise d\'accueil')}
   - Contexte organisationnel et sectoriel
   - Positionnement précis du stage et du projet

3. PROBLÉMATIQUE (1-2 paragraphes)
   - Situation initiale vs situation souhaitée
   - Problème identifié et ses enjeux
   - Question de recherche centrale
   - Pertinence scientifique et pratique

4. OBJECTIFS (1 paragraphe)
   - Objectif général du travail
   - Objectifs spécifiques (3-5 objectifs clairs)
   - Contribution attendue au domaine

5. MÉTHODOLOGIE SOMMAIRE (1 paragraphe)
   - Approche générale adoptée
   - Méthodes principales utilisées
   - Justification sommaire des choix

6. PLAN DU RAPPORT (1 paragraphe)
   - Annonce des chapitres avec leur contenu
   - Logique de progression argumentative
   - Structure adoptée et son intérêt

LONGUEUR : 600-800 mots
STYLE : Formel, argumenté, progressif, académique"""
    
    def _get_methodology_template(self, student: Dict, company: Dict) -> str:
        return f"""TU DOIS RÉDIGER LE CHAPITRE "MÉTHODOLOGIE".

SECTIONS REQUISES :

1. APPROCHE MÉTHODOLOGIQUE GLOBALE
   - Cadre épistémologique de la recherche
   - Justification des choix méthodologiques
   - Alternatives considérées et raisons de leur rejet

2. DÉMARCHE ADOPTÉE
   - Phasage détaillé du projet
   - Étapes successives et leurs livrables
   - Critères de validation à chaque étape
   - Calendrier sommaire d'exécution

3. OUTILS ET TECHNOLOGIES
   - Stack technique complète utilisée
   - Justification détaillée des choix techniques
   - Environnement de développement et de test
   - Outils de gestion, suivi et documentation

4. ORGANISATION DU TRAVAIL
   - Rôles et responsabilités de chaque acteur
   - Processus de communication et de coordination
   - Gestion documentaire et versionning
   - Méthodes de collaboration et de revue

5. CONSIDÉRATIONS ÉTHIQUES ET LIMITES
   - Aspects éthiques pris en compte
   - Limitations méthodologiques identifiées
   - Contraintes techniques et organisationnelles
   - Stratégies d'atténuation mises en place

STYLE : Technique, justificatif, précis, structuré
LONGUEUR : 1000-1200 mots
PRÉCISION : Décrire concrètement ce qui a été fait, pas seulement la théorie"""
    
    def _get_conclusion_template(self, student: Dict, company: Dict) -> str:
        return f"""TU DOIS RÉDIGER LA CONCLUSION GÉNÉRALE.

STRUCTURE À SUIVRE :

1. SYNTHÈSE DES TRAVAUX RÉALISÉS
   - Rappel du contexte et des objectifs
   - Résumé des principales réalisations
   - Mise en perspective des contributions

2. RÉPONSE À LA PROBLÉMATIQUE
   - Réponse apportée à la question de recherche
   - Validation des hypothèses formulées
   - Apports principaux au domaine

3. LIMITATIONS ET DIFFICULTÉS
   - Limitations méthodologiques rencontrées
   - Difficultés techniques et organisationnelles
   - Contraintes non levées

4. PERSPECTIVES ET RECOMMANDATIONS
   - Évolutions possibles du travail
   - Recommandations pour des travaux futurs
   - Applications potentielles dans d'autres contextes

5. BILAN PERSONNEL ET PROFESSIONNEL
   - Acquis techniques et méthodologiques
   - Compétences professionnelles développées
   - Apports de cette expérience au parcours

STYLE : Synthétique, réflexif, prospectif, professionnel
LONGUEUR : 500-700 mots
TON : Équilibré entre objectivité scientifique et réflexion personnelle"""
    
    def _get_default_template(self, student: Dict, company: Dict) -> str:
        return f"""TU DOIS RÉDIGER UNE SECTION ACADÉMIQUE.

EXIGENCES GÉNÉRALES :
- Structure claire avec introduction, développement, conclusion
- Argumentation logique et progressive
- Vocabulaire technique adapté au domaine
- Citations et références si nécessaires
- Ton académique et professionnel

CONTEXTE :
- Étudiant : {student.get('full_name', '')}
- Projet : {student.get('project_title', '')}
- Entreprise : {company.get('name', '')}

LONGUEUR : 500-800 mots
STYLE : Académique formel, structuré, précis"""
    
    def _get_formatting_constraints(self, section: str) -> str:
        """Retourne les contraintes de formatage"""
        return """FORMATAGE EXIGÉ (HTML simple) :

STRUCTURE :
<h2>Titre principal de la section</h2>
<h3>Sous-section si nécessaire</h3>
<p>Paragraphe de texte continu avec plusieurs phrases formant une idée complète.</p>
<ul><li>Liste à puces si nécessaire</li><li>Élément de liste</li></ul>

CONTRAINTES STRICTES :
- PAS de Markdown (**gras** ou *italique*)
- PAS de LaTeX ou formules complexes
- PAS de métadonnées ou commentaires
- UNIQUEMENT le contenu textuel formaté en HTML simple
- Balises autorisées : h2, h3, h4, p, ul, li, strong, em
- Structure académique stricte"""
    
    def get_academic_tips(self) -> List[Dict]:
        """Retourne des conseils académiques basés sur l'analyse"""
        tips = []
        
        if not self.style_data:
            return [
                {
                    'title': 'Style académique de base',
                    'content': 'Utilisez le "nous académique" et évitez le "je".',
                    'examples': ['Remplacer "Je pense que" par "Nous constatons que"']
                }
            ]
        
        detailed = self.style_data.get('detailed_analysis', {})
        linguistic = detailed.get('linguistic_features', {})
        
        # Conseils sur les pronoms
        pronoun_usage = linguistic.get('pronoun_usage', {})
        if pronoun_usage.get('je', 0) > 0.2:
            tips.append({
                'title': 'Utilisation excessive du "je"',
                'content': 'Privilégiez le "nous académique" pour plus de formalité.',
                'examples': [
                    '"Je pense que" → "Nous considérons que"',
                    '"J\'ai réalisé" → "Nous avons réalisé"'
                ]
            })
        
        # Conseils sur la structure
        basic_stats = detailed.get('basic_stats', {})
        avg_sentence_length = basic_stats.get('avg_sentence_length', 20)
        
        if avg_sentence_length > 30:
            tips.append({
                'title': 'Phrases trop longues',
                'content': 'Divisez les phrases longues pour améliorer la lisibilité.',
                'examples': [
                    'Diviser : "Le système qui a été développé pour résoudre le problème complexe de gestion des données qui était identifié lors de l\'analyse préliminaire"',
                    'En : "Le système a été développé pour résoudre un problème complexe de gestion des données. Ce problème avait été identifié lors de l\'analyse préliminaire."'
                ]
            })
        
        # Conseils sur le vocabulaire
        vocabulary = detailed.get('vocabulary_analysis', {})
        if vocabulary.get('richness_score', 0) < 0.5:
            tips.append({
                'title': 'Vocabulaire peu varié',
                'content': 'Utilisez plus de synonymes et de termes spécifiques.',
                'examples': [
                    '"Faire" → "Réaliser", "Implémenter", "Développer"',
                    '"Problème" → "Problématique", "Défi", "Enjeu"'
                ]
            })
        
        return tips[:5]  # Limiter à 5 conseils

class AIGenerator:
    """Générateur de contenu IA avec gestion des prompts académiques"""
    
    def __init__(self, api_key: str = None, reference_text: str = None):
        """
        Initialise le générateur IA
        
        Args:
            api_key: Clé API OpenAI (optionnelle)
            reference_text: Texte de référence pour l'analyse de style
        """
        self.api_key = api_key
        self.reference_text = reference_text
        
        # Initialiser le générateur de prompts
        self.prompt_generator = AcademicPromptGenerator(reference_text)
        
        # Détecter le mode (réel ou simulation)
        self.use_real_ai = False
        if api_key and api_key != "votre_clé_api_openai_ici" and len(api_key) > 20:
            self.use_real_ai = True
            try:
                import openai
                self.client = openai.OpenAI(api_key=api_key)
                print("✅ Mode réel OpenAI activé")
            except Exception as e:
                print(f"⚠️ Erreur OpenAI (mode simulation): {str(e)[:100]}")
                self.use_real_ai = False
        else:
            print("✅ Mode simulation activé")
            self.use_real_ai = False
    
    def generate_section(self, section: str, context: Dict) -> Dict:
        """
        Génère une section du rapport avec style académique
        
        Args:
            section: Nom de la section
            context: Contexte avec infos étudiant/entreprise
        
        Returns:
            Dict avec 'content' et 'metadata'
        """
        try:
            # Générer le prompt académique
            prompt = self.prompt_generator.generate_prompt_for_section(section, context)
            
            if self.use_real_ai:
                content = self._generate_with_openai(prompt, section)
            else:
                content = self._generate_simulated(section, context)
            
            # Métadonnées
            metadata = {
                'section': section,
                'generated_at': datetime.now().isoformat(),
                'style_analysis': self.prompt_generator.get_style_report(),
                'word_count': len(content.split()) if content else 0,
                'prompt_length': len(prompt),
                'academic_tips': self.prompt_generator.get_academic_tips()
            }
            
            return {
                'content': content,
                'metadata': metadata,
                'success': True
            }
            
        except Exception as e:
            print(f"⚠️ Erreur génération section {section}: {str(e)[:100]}")
            
            # Fallback à la génération simulée
            content = self._generate_simulated(section, context)
            
            return {
                'content': content,
                'metadata': {
                    'section': section,
                    'generated_at': datetime.now().isoformat(),
                    'error': str(e),
                    'word_count': len(content.split()) if content else 0
                },
                'success': False
            }
    
    def _generate_with_openai(self, prompt: str, section: str) -> str:
        """Génère avec OpenAI"""
        try:
            import openai
            
            # Préparer le message système
            system_message = """Tu es un assistant académique expert. Tu génères du contenu de rapport 
            de stage en respectant strictement le style académique et les instructions fournies."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.3
            )
            
            content = response.choices[0].message.content
            
            # Nettoyer et formater le contenu
            return self._clean_generated_content(content, section)
            
        except Exception as e:
            print(f"⚠️ OpenAI error: {str(e)[:100]}")
            raise e
    
    def _generate_simulated(self, section: str, context: Dict) -> str:
        """Génère du contenu simulé de haute qualité"""
        print(f"🔧 Génération simulée: {section}")
        
        student = context.get('student', {})
        company = context.get('company', {})
        
        # Utiliser les templates du prompt generator
        return self.prompt_generator._get_section_instructions(section, context)
    
    def _clean_generated_content(self, content: str, section: str) -> str:
        """Nettoie et formate le contenu généré"""
        if not content:
            return "<p>Contenu non disponible</p>"
        
        # Supprimer les marqueurs de prompt
        content = content.replace('```html', '').replace('```', '').strip()
        
        # Convertir le markdown en HTML simple
        content = content.replace('**', '<strong>').replace('**', '</strong>')
        content = content.replace('*', '<em>').replace('*', '</em>')
        
        # Gérer les sauts de ligne
        content = content.replace('\n\n', '</p><p>')
        content = content.replace('\n', '<br>')
        
        # S'assurer qu'il y a des balises HTML
        if not content.startswith('<'):
            content = f'<p>{content}</p>'
        
        # Ajouter un titre de section si absent
        if section != 'cover_page' and '<h2' not in content:
            section_title = section.replace('_', ' ').title()
            content = f'<h2>{section_title}</h2>{content}'
        
        return content
    
    def get_style_analysis_report(self) -> Dict:
        """Retourne le rapport d'analyse de style"""
        return self.prompt_generator.get_style_report()
    
    def get_academic_tips(self) -> List[Dict]:
        """Retourne des conseils académiques"""
        return self.prompt_generator.get_academic_tips()