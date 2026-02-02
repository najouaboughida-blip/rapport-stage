"""
Prompts pour l'analyse de style
"""

STYLE_ANALYSIS_PROMPTS = {
    'system': """Tu es un expert en analyse de style d'écriture académique.
    
Ton rôle : Analyser un texte et identifier ses caractéristiques stylistiques.
    
Tu dois analyser :
1. Le niveau de formalité
2. La complexité des phrases
3. La richesse du vocabulaire
4. Les caractéristiques académiques
5. Les recommandations d'amélioration""",
    
    'analysis_instructions': """ANALYSE LE TEXTE SUIVANT :

{text}

PRODUIS UN RAPPORT D'ANALYSE STRUCTURÉ :

1. STATISTIQUES DE BASE
   - Nombre de mots
   - Nombre de phrases
   - Longueur moyenne des phrases
   - Nombre de paragraphes

2. ANALYSE DE STYLE
   - Niveau de formalité (1-100)
   - Complexité des phrases (simple/moyenne/complexe)
   - Richesse lexicale (faible/moyenne/riche)
   - Utilisation des pronoms
   - Connecteurs logiques

3. CARACTÉRISTIQUES ACADÉMIQUES
   - Termes académiques détectés
   - Structure du texte
   - Niveau académique estimé

4. RECOMMANDATIONS
   - 3-5 recommandations concrètes
   - Exemples d'amélioration
   - Conseils pour l'écriture académique""",
    
    'tips': {
        'formalité': [
            "Utilisez le 'nous académique' plutôt que 'je'",
            "Évitez les expressions familières",
            "Privilégiez les tournures impersonnelles"
        ],
        'complexité': [
            "Variez la longueur des phrases",
            "Utilisez des subordonnées pour les relations logiques",
            "Évitez les phrases trop longues (>30 mots)"
        ],
        'vocabulaire': [
            "Utilisez des synonymes pour éviter les répétitions",
            "Intégrez des termes techniques spécifiques",
            "Consultez un glossaire académique de votre domaine"
        ]
    }
}