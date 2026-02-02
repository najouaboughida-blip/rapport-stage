"""
Prompts académiques complets pour le générateur ENSAO
"""

ACADEMIC_PROMPTS_CONFIG = {
    'system_base': """Tu es un expert en rédaction académique pour rapports de stage ENSAO.
    
TON IDENTITÉ :
- Assistant académique spécialisé
- Connaisseur des normes ENSA Oujda
- Rédacteur formel et technique

TES CONTRAINTES :
1. Utiliser le "nous académique" systématiquement
2. Phrases de 15-30 mots en moyenne
3. Structure paragraphes claire (5-8 lignes)
4. Vocabulaire technique adapté au domaine
5. Pas de style personnel ou informel
6. Respect des normes académiques françaises

TON OBJECTIF : Produire un texte académique, structuré, précis et professionnel.""",
    
    'section_specific': {
        'cover_page': {
            'instruction': """GÉNÈRE UNE PAGE DE GARDE ACADÉMIQUE

INFORMATIONS À INCLURE (dans l'ordre) :
1. [LOGO] UNIVERSITÉ MOHAMMED PREMIER
2. École Nationale des Sciences Appliquées - Oujda
3. FILIÈRE : {filiere}
4. "RAPPORT DE STAGE DE FIN D'ÉTUDES"
5. TITRE : "{project_title}"
6. "Présenté par :" {full_name}
7. "Encadré par :" {academic_supervisor} (ENSAO)
   "                 {company_supervisor} ({company_name})
8. "Année universitaire :" {academic_year}

FORMAT : HTML centré, sans texte continu, polices académiques""",
            
            'variables': ['filiere', 'project_title', 'full_name', 
                         'academic_supervisor', 'company_supervisor', 
                         'company_name', 'academic_year']
        },
        
        'thanks': {
            'instruction': """RÉDIGE LA SECTION "REMERCIEMENTS"

STRUCTURE ACADÉMIQUE :
1. Remerciement général (optionnel : à Allah)
2. Remerciement à la famille
3. Remerciement à l'encadrant académique (ENSAO)
4. Remerciement à l'encadrant professionnel (entreprise)
5. Remerciement à l'entreprise d'accueil
6. Remerciement aux collègues/collaborateurs
7. Remerciement au jury (optionnel)
8. Signature et date

STYLE :
- Utiliser le "nous" académique
- Ton respectueux et formel
- Phrases complètes (pas de listes)
- 1 page maximum
- Signature : "Fait à Oujda, le [date]" + nom""",
            
            'variables': ['full_name', 'academic_supervisor', 
                         'company_supervisor', 'company_name']
        },
        
        'abstract': {
            'instruction': """GÉNÈRE LES RÉSUMÉS ACADÉMIQUES

A. RÉSUMÉ EN FRANÇAIS (200-250 mots)
Structure :
- Contexte du stage ({company_name}, durée {duration})
- Problématique abordée
- Méthodologie employée
- Résultats principaux obtenus
- Conclusions majeures
- Mots-clés (5-8 termes techniques)

B. ABSTRACT IN ENGLISH (200-250 words)
Même structure en anglais académique.

CONTRAINTES :
- Texte continu (pas de listes)
- Style synthétique mais complet
- Pas de détails techniques approfondis
- Vocabulaire académique standard""",
            
            'variables': ['company_name', 'duration', 'project_title']
        },
        
        'introduction': {
            'instruction': """RÉDIGE L'INTRODUCTION GÉNÉRALE

STRUCTURE ACADÉMIQUE STRICTE :

1. CONTEXTE GÉNÉRALE (1-2 paragraphes)
   - Domaine {sector} et son importance
   - Spécificité du cas étudié
   - Justification scientifique

2. CADRE DU STAGE (1 paragraphe)
   - Présentation de {company_name}
   - Contexte organisationnel
   - Mission et positionnement

3. PROBLÉMATIQUE (1-2 paragraphes)
   - État de l'art sommaire
   - Problème identifié
   - Question de recherche centrale
   - Enjeux scientifiques/professionnels

4. OBJECTIFS DU TRAVAIL (1 paragraphe)
   - Objectif général
   - Objectifs spécifiques (3-5)
   - Contribution attendue

5. MÉTHODOLOGIE GLOBALE (1 paragraphe)
   - Approche générale
   - Méthodes principales
   - Justification sommaire

6. PLAN DU RAPPORT (1 paragraphe)
   - Annonce des chapitres
   - Logique de progression
   - Structure adoptée

LONGUEUR : 600-800 mots
STYLE : Formel, argumenté, académique""",
            
            'variables': ['company_name', 'sector', 'project_title']
        },
        
        'methodology': {
            'instruction': """RÉDIGE LE CHAPITRE "MÉTHODOLOGIE"

SECTIONS REQUISES :

1. APPROCHE MÉTHODOLOGIQUE GLOBALE
   - Cadre épistémologique
   - Justification des choix méthodologiques
   - Alternatives considérées et écartées

2. DÉMARCHE ADOPTÉE
   - Phasage du projet
   - Étapes et livrables
   - Critères de validation
   - Calendrier sommaire

3. OUTILS ET TECHNOLOGIES
   - Stack technique complète
   - Justification des choix techniques
   - Environnement de développement
   - Outils de gestion et suivi

4. ORGANISATION DU TRAVAIL
   - Rôles et responsabilités
   - Processus de communication
   - Gestion documentaire
   - Méthodes de collaboration

5. CONSIDÉRATIONS ÉTHIQUES ET LIMITES
   - Aspects éthiques considérés
   - Limitations méthodologiques
   - Contraintes identifiées
   - Stratégies d'atténuation

STYLE : Technique, justificatif, précis
LONGUEUR : 1000-1200 mots""",
            
            'variables': []
        }
    },
    
    'style_adaptations': {
        'high_formality': {
            'name': 'Très formel',
            'characteristics': [
                'Utilisation exclusive du "nous académique"',
                'Phrases complexes avec subordonnées',
                'Vocabulaire technique avancé',
                'Structure rigoureuse',
                'Ton impersonnel et objectif'
            ],
            'phrases': [
                'Il convient de souligner que',
                'Il apparaît nécessaire de',
                'Nous nous proposons d\'examiner',
                'Il importe de préciser que',
                'À cet égard, nous pouvons constater que'
            ]
        },
        
        'medium_formality': {
            'name': 'Formel académique',
            'characteristics': [
                'Utilisation majoritaire du "nous"',
                'Phrases de complexité moyenne',
                'Vocabulaire technique standard',
                'Structure académique classique',
                'Ton professionnel'
            ],
            'phrases': [
                'Nous présentons dans cette section',
                'Il est important de noter que',
                'Cette approche permet de',
                'Les résultats obtenus montrent que',
                'En conclusion, nous pouvons dire que'
            ]
        },
        
        'technical': {
            'name': 'Technique',
            'characteristics': [
                'Précision terminologique',
                'Description détaillée des procédés',
                'Justification technique des choix',
                'Références aux normes et standards',
                'Focus sur l\'implémentation'
            ],
            'phrases': [
                'L\'architecture mise en place repose sur',
                'L\'algorithme implémenté permet de',
                'La solution technique retenue consiste à',
                'Les performances obtenues démontrent',
                'L\'optimisation réalisée a permis de'
            ]
        }
    }
}

def generate_section_prompt(section_name: str, student_info: dict, company_info: dict, 
                          style_analysis: dict = None) -> str:
    """
    Génère un prompt complet pour une section spécifique
    """
    # Récupérer le template de la section
    section_template = ACADEMIC_PROMPTS_CONFIG['section_specific'].get(
        section_name,
        ACADEMIC_PROMPTS_CONFIG['section_specific']['introduction']
    )
    
    instruction = section_template['instruction']
    
    # Remplacer les variables
    variables = {
        'full_name': student_info.get('full_name', 'NOM Prénom'),
        'filiere': student_info.get('filiere', 'Génie Informatique'),
        'project_title': student_info.get('project_title', 'Titre du projet'),
        'academic_supervisor': student_info.get('supervisor', 'Dr. NOM Prénom'),
        'duration': student_info.get('duration', '2 mois'),
        'academic_year': student_info.get('academic_year', '2024-2025'),
        'company_name': company_info.get('name', 'Entreprise'),
        'company_supervisor': company_info.get('supervisor', 'M. NOM Prénom'),
        'sector': company_info.get('sector', 'Informatique')
    }
    
    for key, value in variables.items():
        instruction = instruction.replace(f'{{{key}}}', value)
    
    # Ajouter les instructions de style si disponible
    if style_analysis:
        style_instructions = generate_style_instructions(style_analysis)
        instruction = f"{style_instructions}\n\n{instruction}"
    
    # Ajouter la base système
    system_base = ACADEMIC_PROMPTS_CONFIG['system_base']
    
    return f"""{system_base}

{instruction}

FORMATAGE FINAL :
- Utiliser des balises HTML simples (h2, h3, p, ul/li si nécessaire)
- Pas de Markdown (**bold** ou *italic*)
- Structure académique stricte
- Pas de commentaires ou métadonnées supplémentaires
- Générer uniquement le contenu textuel de la section"""

def generate_style_instructions(style_analysis: dict) -> str:
    """Génère des instructions de style basées sur l'analyse"""
    if not style_analysis or 'summary' not in style_analysis:
        return "STYLE : Académique formel standard"
    
    summary = style_analysis['summary']
    
    instructions = ["INSTRUCTIONS DE STYLE (basées sur l'analyse) :"]
    
    # Niveau de formalité
    formality = summary.get('formality_score', 50)
    if formality >= 80:
        instructions.append("- STYLE : Très formel (utilisation exclusive du 'nous académique')")
    elif formality >= 60:
        instructions.append("- STYLE : Formel académique (utilisation majoritaire du 'nous')")
    else:
        instructions.append("- STYLE : Formel standard")
    
    # Complexité des phrases
    complexity = summary.get('complexity', 'moyenne')
    if complexity == 'complexe':
        instructions.append("- PHRASES : Complexes avec subordonnées (20-35 mots)")
    elif complexity == 'simple':
        instructions.append("- PHRASES : Simples et directes (15-25 mots)")
    else:
        instructions.append("- PHRASES : Complexité moyenne (18-28 mots)")
    
    # Vocabulaire
    vocabulary = summary.get('vocabulary', 'moyenne')
    if vocabulary == 'riche':
        instructions.append("- VOCABULAIRE : Technique et varié")
    else:
        instructions.append("- VOCABULAIRE : Académique standard")
    
    # Caractéristiques spécifiques
    features = style_analysis.get('detailed_analysis', {}).get('academic_indicators', [])
    if features:
        instructions.append("- CARACTÉRISTIQUES À REPRODUIRE :")
        for feature in features[:3]:
            instructions.append(f"  * {feature}")
    
    return "\n".join(instructions)