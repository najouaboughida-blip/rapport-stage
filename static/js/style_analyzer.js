/**
 * Analyseur de style d'écriture académique
 * Pour le Générateur Intelligent de Rapports Académiques ENSAO
 */

class StyleAnalyzer {
    constructor(options = {}) {
        this.options = {
            minTextLength: options.minTextLength || 100,
            apiEndpoint: options.apiEndpoint || '/api/analyze-style',
            showRealTimeAnalysis: options.showRealTimeAnalysis || true,
            language: options.language || 'fr'
        };
        
        // Dictionnaires pour l'analyse
        this.dictionaries = {
            formalIndicators: [
                'nous', 'il convient', 'souligner', 'notons que', 'par conséquent',
                'cependant', 'toutefois', 'néanmoins', 'en outre', 'par ailleurs',
                'ainsi', 'de ce fait', 'cela étant', 'dans le cadre de',
                'présenterons', 'détaillerons', 'exposerons', 'il importe',
                'il est nécessaire', 'il apparaît que', 'selon', 'conformément',
                'en référence à', 'en vue de', 'afin de', 'pour ce faire'
            ],
            informalIndicators: [
                'je', 'moi', 'perso', 'super', 'cool', 'trop', 'genre', 'grave',
                'je pense que', 'je crois que', 'je trouve que', 'j\'aime',
                'franchement', 'honnêtement', 'en fait', 'du coup', 'voilà',
                'bref', 'alors', 'bon', 'ben', 'hein'
            ],
            academicTerms: [
                'problématique', 'méthodologie', 'hypothèse', 'cadre théorique',
                'revue de littérature', 'état de l\'art', 'corpus', 'analyse',
                'synthèse', 'conclusion', 'perspective', 'recommandation',
                'évaluation', 'validation', 'implémentation', 'développement',
                'optimisation', 'architecture', 'algorithme', 'protocole',
                'expérimentation', 'résultat', 'discussion', 'limitation'
            ],
            transitionWords: [
                'premièrement', 'deuxièmement', 'troisièmement', 'en premier lieu',
                'en second lieu', 'd\'abord', 'ensuite', 'enfin', 'finalement',
                'par ailleurs', 'en outre', 'de plus', 'également', 'aussi',
                'cependant', 'toutefois', 'néanmoins', 'par contre', 'en revanche',
                'par conséquent', 'donc', 'ainsi', 'de ce fait', 'en conséquence',
                'par exemple', 'notamment', 'entre autres', 'c\'est-à-dire',
                'autrement dit', 'en d\'autres termes'
            ],
            complexStructures: [
                'qui', 'que', 'dont', 'où', 'lequel', 'laquelle', 'lesquels',
                'lorsque', 'puisque', 'parce que', 'alors que', 'tandis que',
                'bien que', 'quoique', 'afin que', 'pour que', 'de sorte que',
                'si bien que', 'au point que', 'à moins que', 'sauf si'
            ]
        };
        
        // État de l'analyse
        this.state = {
            text: '',
            analysis: null,
            isAnalyzing: false,
            lastAnalysisTime: null,
            realTimeTimeout: null
        };
        
        // Éléments DOM
        this.elements = {
            textArea: null,
            analyzeButton: null,
            resultsContainer: null,
            statsContainer: null,
            featuresContainer: null,
            recommendationsContainer: null
        };
        
        // Initialiser
        this.init();
    }
    
    init() {
        console.log('🔍 StyleAnalyzer initialisé');
        
        // Récupérer les références DOM
        this.elements.textArea = document.getElementById('referenceText');
        this.elements.analyzeButton = document.getElementById('analyzeButton');
        this.elements.resultsContainer = document.getElementById('analysisResults');
        this.elements.statsContainer = document.getElementById('statsContainer');
        this.elements.featuresContainer = document.getElementById('featuresContainer');
        this.elements.recommendationsContainer = document.getElementById('recommendationsContainer');
        
        // Configurer les événements
        this.setupEventListeners();
        
        // Vérifier si on doit charger un texte par défaut
        this.loadDefaultText();
    }
    
    setupEventListeners() {
        // Analyse sur clic du bouton
        if (this.elements.analyzeButton) {
            this.elements.analyzeButton.addEventListener('click', () => {
                this.analyze();
            });
        }
        
        // Analyse en temps réel (si activée)
        if (this.options.showRealTimeAnalysis && this.elements.textArea) {
            this.elements.textArea.addEventListener('input', () => {
                this.handleRealTimeAnalysis();
            });
        }
        
        // Sauvegarde automatique
        if (this.elements.textArea) {
            this.elements.textArea.addEventListener('blur', () => {
                this.saveToLocalStorage();
            });
        }
    }
    
    loadDefaultText() {
        // Essayer de charger depuis localStorage
        const savedText = localStorage.getItem('styleAnalyzerText');
        if (savedText && this.elements.textArea) {
            this.elements.textArea.value = savedText;
            this.state.text = savedText;
            this.updateTextStats();
        }
        
        // Charger un exemple si le texte est vide
        if ((!this.state.text || this.state.text.length < 10) && this.elements.textArea) {
            this.loadExampleText();
        }
    }
    
    loadExampleText() {
        const exampleText = `L'introduction générale du présent rapport s'inscrit dans le cadre du stage de fin d'études effectué au sein de l'entreprise Capgemini TS. Ce stage, d'une durée de deux mois, a pour objectif principal la refonte de l'architecture conversationnelle du WinBot, un chatbot destiné à améliorer l'expérience client de l'opérateur INWI.

Dans un premier temps, nous présenterons le contexte général du projet ainsi que la problématique rencontrée. Ensuite, nous détaillerons la méthodologie adoptée pour répondre à cette problématique. Enfin, nous exposerons les résultats obtenus et les perspectives d'amélioration.

Il convient de souligner que ce travail s'appuie sur une analyse approfondie des besoins fonctionnels et techniques, ainsi que sur une revue de la littérature relative aux systèmes conversationnels modernes. Notre approche méthodologique combine une analyse qualitative des besoins avec une évaluation quantitative des performances.`;
        
        if (this.elements.textArea) {
            this.elements.textArea.value = exampleText;
            this.state.text = exampleText;
            this.updateTextStats();
        }
    }
    
    handleRealTimeAnalysis() {
        // Limiter la fréquence d'analyse en temps réel
        if (this.state.realTimeTimeout) {
            clearTimeout(this.state.realTimeTimeout);
        }
        
        this.state.realTimeTimeout = setTimeout(() => {
            const text = this.elements.textArea.value;
            if (text.length > this.options.minTextLength) {
                this.performQuickAnalysis(text);
            }
        }, 1000);
    }
    
    analyze() {
        if (!this.elements.textArea) {
            console.error('Zone de texte non trouvée');
            return;
        }
        
        const text = this.elements.textArea.value.trim();
        this.state.text = text;
        
        // Validation
        if (text.length < this.options.minTextLength) {
            this.showError(`Le texte doit contenir au moins ${this.options.minTextLength} caractères pour l'analyse.`);
            return;
        }
        
        // Afficher l'état de chargement
        this.showLoading();
        
        // Effectuer l'analyse
        this.performAnalysis(text).then(analysis => {
            this.state.analysis = analysis;
            this.state.lastAnalysisTime = new Date();
            this.state.isAnalyzing = false;
            
            // Afficher les résultats
            this.displayResults(analysis);
            
            // Sauvegarder
            this.saveToLocalStorage();
            this.saveAnalysisToLocalStorage(analysis);
            
            // Notification
            this.showNotification('Analyse terminée avec succès', 'success');
        }).catch(error => {
            console.error('Erreur lors de l\'analyse:', error);
            this.showError('Une erreur est survenue lors de l\'analyse. Veuillez réessayer.');
            this.state.isAnalyzing = false;
            this.hideLoading();
        });
    }
    
    async performAnalysis(text) {
        this.state.isAnalyzing = true;
        
        try {
            // Essayer l'API serveur d'abord
            if (this.options.apiEndpoint) {
                const response = await fetch(this.options.apiEndpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ text: text })
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.success && data.analysis) {
                        return data.analysis;
                    }
                }
            }
            
            // Fallback à l'analyse locale
            return this.performLocalAnalysis(text);
            
        } catch (error) {
            console.warn('API non disponible, utilisation de l\'analyse locale:', error);
            return this.performLocalAnalysis(text);
        }
    }
    
    performLocalAnalysis(text) {
        console.log('🔧 Analyse locale en cours...');
        
        // Statistiques de base
        const words = text.trim().split(/\s+/).filter(w => w.length > 0);
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const paragraphs = text.split(/\n\s*\n/).filter(p => p.trim().length > 0);
        
        // Calculs
        const wordCount = words.length;
        const sentenceCount = sentences.length;
        const paragraphCount = paragraphs.length;
        const avgSentenceLength = sentenceCount > 0 ? wordCount / sentenceCount : 0;
        const avgParagraphLength = paragraphCount > 0 ? wordCount / paragraphCount : 0;
        
        // Analyse de style
        const formalityScore = this.calculateFormalityScore(text);
        const complexityScore = this.calculateComplexityScore(text);
        const vocabularyScore = this.calculateVocabularyScore(text);
        const structureScore = this.calculateStructureScore(text);
        
        // Caractéristiques détectées
        const detectedFeatures = this.detectFeatures(text);
        
        // Recommandations
        const recommendations = this.generateRecommendations({
            wordCount,
            avgSentenceLength,
            formalityScore,
            complexityScore,
            vocabularyScore,
            detectedFeatures
        });
        
        // Score global
        const overallScore = Math.round((
            formalityScore + 
            complexityScore + 
            vocabularyScore + 
            structureScore
        ) / 4);
        
        return {
            summary: {
                wordCount,
                sentenceCount,
                paragraphCount,
                avgSentenceLength: Math.round(avgSentenceLength * 10) / 10,
                avgParagraphLength: Math.round(avgParagraphLength * 10) / 10,
                overallScore,
                formalityScore,
                complexityScore,
                vocabularyScore,
                structureScore
            },
            features: detectedFeatures,
            recommendations: recommendations,
            detailedAnalysis: {
                wordStats: this.analyzeWordUsage(text),
                sentenceStats: this.analyzeSentenceStructure(text),
                readabilityScore: this.calculateReadabilityScore(text),
                academicTermCount: this.countAcademicTerms(text),
                transitionWordCount: this.countTransitionWords(text)
            },
            timestamp: new Date().toISOString()
        };
    }
    
    performQuickAnalysis(text) {
        // Analyse légère pour le temps réel
        const wordCount = text.trim().split(/\s+/).filter(w => w.length > 0).length;
        const formalityScore = this.calculateFormalityScore(text);
        
        // Mettre à jour les statistiques en temps réel
        this.updateTextStats();
        
        // Afficher un score préliminaire si le texte est suffisamment long
        if (wordCount > 50) {
            this.showQuickScore(formalityScore);
        }
    }
    
    calculateFormalityScore(text) {
        const textLower = text.toLowerCase();
        let formalCount = 0;
        let informalCount = 0;
        
        // Compter les indicateurs formels
        this.dictionaries.formalIndicators.forEach(indicator => {
            const regex = new RegExp(`\\b${indicator}\\b`, 'gi');
            formalCount += (textLower.match(regex) || []).length;
        });
        
        // Compter les indicateurs informels
        this.dictionaries.informalIndicators.forEach(indicator => {
            const regex = new RegExp(`\\b${indicator}\\b`, 'gi');
            informalCount += (textLower.match(regex) || []).length;
        });
        
        // Calculer le score (0-100)
        const total = formalCount + informalCount;
        if (total === 0) return 50;
        
        let score = (formalCount / total) * 100;
        
        // Ajuster basé sur l'utilisation du "nous" vs "je"
        const nousCount = (textLower.match(/\bnous\b/g) || []).length;
        const jeCount = (textLower.match(/\bje\b/g) || []).length;
        
        if (nousCount > jeCount * 2) {
            score += 10;
        } else if (jeCount > nousCount * 2) {
            score -= 15;
        }
        
        // Limiter entre 0 et 100
        return Math.max(0, Math.min(100, Math.round(score)));
    }
    
    calculateComplexityScore(text) {
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        if (sentences.length === 0) return 50;
        
        let complexStructures = 0;
        let totalWords = 0;
        
        sentences.forEach(sentence => {
            const words = sentence.trim().split(/\s+/);
            totalWords += words.length;
            
            // Vérifier les structures complexes
            const sentenceLower = sentence.toLowerCase();
            this.dictionaries.complexStructures.forEach(structure => {
                if (sentenceLower.includes(structure)) {
                    complexStructures++;
                }
            });
        });
        
        // Score basé sur la longueur moyenne des phrases et les structures complexes
        const avgSentenceLength = totalWords / sentences.length;
        const complexityRatio = complexStructures / sentences.length;
        
        let score = 50;
        
        if (avgSentenceLength > 25) score += 20;
        else if (avgSentenceLength > 20) score += 10;
        else if (avgSentenceLength < 10) score -= 10;
        
        if (complexityRatio > 0.5) score += 20;
        else if (complexityRatio > 0.3) score += 10;
        
        return Math.max(0, Math.min(100, score));
    }
    
    calculateVocabularyScore(text) {
        const words = text.toLowerCase().split(/\s+/).filter(w => w.length > 0);
        const uniqueWords = new Set(words);
        
        // Richesse lexicale
        const lexicalRichness = uniqueWords.size / words.length;
        
        // Termes académiques
        const academicTerms = this.countAcademicTerms(text);
        const academicRatio = academicTerms / words.length;
        
        // Calcul du score
        let score = 50;
        
        if (lexicalRichness > 0.7) score += 25;
        else if (lexicalRichness > 0.5) score += 10;
        else if (lexicalRichness < 0.3) score -= 15;
        
        if (academicRatio > 0.05) score += 15;
        else if (academicRatio > 0.02) score += 5;
        
        return Math.max(0, Math.min(100, Math.round(score)));
    }
    
    calculateStructureScore(text) {
        const paragraphs = text.split(/\n\s*\n/).filter(p => p.trim().length > 0);
        let structureScore = 50;
        
        // Vérifier la présence d'éléments structurels
        const hasHeadings = /^(#+|\d+\.|\*+)/m.test(text);
        const hasLists = /^\s*[\-\*\+]\s|\d+\.\s/.test(text);
        const hasTransitions = this.countTransitionWords(text) > 3;
        
        if (hasHeadings) structureScore += 10;
        if (hasLists) structureScore += 5;
        if (hasTransitions) structureScore += 15;
        
        // Vérifier la longueur des paragraphes
        const avgParagraphLength = paragraphs.reduce((sum, p) => {
            return sum + p.trim().split(/\s+/).length;
        }, 0) / Math.max(paragraphs.length, 1);
        
        if (avgParagraphLength > 100) structureScore -= 10;
        else if (avgParagraphLength < 30) structureScore -= 5;
        else if (avgParagraphLength >= 50 && avgParagraphLength <= 100) structureScore += 10;
        
        return Math.max(0, Math.min(100, structureScore));
    }
    
    calculateReadabilityScore(text) {
        // Adaptation du Flesch Reading Ease pour le français
        const words = text.trim().split(/\s+/).filter(w => w.length > 0);
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const syllables = this.countSyllables(text);
        
        if (words.length === 0 || sentences.length === 0) return 50;
        
        const avgSentenceLength = words.length / sentences.length;
        const avgSyllablesPerWord = syllables / words.length;
        
        // Formule simplifiée pour le français
        let score = 206.835 - (1.015 * avgSentenceLength) - (84.6 * avgSyllablesPerWord);
        
        // Ajuster pour une échelle 0-100
        score = Math.max(0, Math.min(100, score));
        
        return Math.round(score);
    }
    
    countSyllables(text) {
        // Estimation simple du nombre de syllabes en français
        const vowels = /[aeiouyàâäéèêëîïôöùûü]/gi;
        const matches = text.match(vowels);
        return matches ? matches.length : 0;
    }
    
    countAcademicTerms(text) {
        const textLower = text.toLowerCase();
        let count = 0;
        
        this.dictionaries.academicTerms.forEach(term => {
            const regex = new RegExp(`\\b${term}\\b`, 'gi');
            count += (textLower.match(regex) || []).length;
        });
        
        return count;
    }
    
    countTransitionWords(text) {
        const textLower = text.toLowerCase();
        let count = 0;
        
        this.dictionaries.transitionWords.forEach(word => {
            const regex = new RegExp(`\\b${word}\\b`, 'gi');
            count += (textLower.match(regex) || []).length;
        });
        
        return count;
    }
    
    detectFeatures(text) {
        const features = [];
        const textLower = text.toLowerCase();
        
        // Style d'écriture
        if (this.countTransitionWords(text) > 5) {
            features.push('Utilisation fréquente de connecteurs logiques');
        }
        
        if (this.countAcademicTerms(text) > 10) {
            features.push('Vocabulaire académique riche');
        }
        
        const nousCount = (textLower.match(/\bnous\b/g) || []).length;
        const jeCount = (textLower.match(/\bje\b/g) || []).length;
        if (nousCount > jeCount * 3) {
            features.push('Style impersonnel (prédominance du "nous")');
        } else if (jeCount > nousCount) {
            features.push('Style personnel (utilisation du "je")');
        }
        
        // Structure
        if (/^(#+|\d+\.|\*+)/m.test(text)) {
            features.push('Structure hiérarchique avec titres');
        }
        
        if (/^\s*[\-\*\+]\s|\d+\.\s/.test(text)) {
            features.push('Présence de listes');
        }
        
        const paragraphCount = text.split(/\n\s*\n/).filter(p => p.trim().length > 0).length;
        if (paragraphCount > 10) {
            features.push('Structure paragraphes bien découpée');
        }
        
        // Complexité
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const avgLength = sentences.reduce((sum, s) => sum + s.trim().split(/\s+/).length, 0) / sentences.length;
        
        if (avgLength > 25) {
            features.push('Phrases complexes et détaillées');
        } else if (avgLength < 15) {
            features.push('Phrases courtes et directes');
        }
        
        return features.slice(0, 6); // Limiter à 6 caractéristiques
    }
    
    analyzeWordUsage(text) {
        const words = text.toLowerCase().split(/\s+/).filter(w => w.length > 0);
        const wordFreq = {};
        
        // Compter la fréquence des mots
        words.forEach(word => {
            // Nettoyer le mot
            const cleanWord = word.replace(/[.,!?;:()\[\]{}'"«»]/g, '');
            if (cleanWord.length > 3) { // Ignorer les mots trop courts
                wordFreq[cleanWord] = (wordFreq[cleanWord] || 0) + 1;
            }
        });
        
        // Trier par fréquence
        const sortedWords = Object.entries(wordFreq)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 10); // Top 10
        
        return sortedWords;
    }
    
    analyzeSentenceStructure(text) {
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        
        if (sentences.length === 0) {
            return {
                count: 0,
                avgLength: 0,
                lengthDistribution: []
            };
        }
        
        const lengths = sentences.map(s => s.trim().split(/\s+/).length);
        const avgLength = lengths.reduce((a, b) => a + b) / lengths.length;
        
        // Distribution des longueurs
        const lengthDistribution = {
            short: lengths.filter(l => l < 10).length,
            medium: lengths.filter(l => l >= 10 && l <= 25).length,
            long: lengths.filter(l => l > 25).length
        };
        
        return {
            count: sentences.length,
            avgLength: Math.round(avgLength * 10) / 10,
            lengthDistribution: lengthDistribution
        };
    }
    
    generateRecommendations(stats) {
        const recommendations = [];
        
        // Recommandations basées sur la formalité
        if (stats.formalityScore < 40) {
            recommendations.push({
                type: 'formality',
                priority: 'high',
                title: 'Améliorer la formalité',
                description: 'Votre style est trop informel pour un rapport académique.',
                suggestions: [
                    'Remplacez "je" par "nous" ou utilisez des tournures impersonnelles',
                    'Évitez les expressions familières et les mots de liaison informels',
                    'Utilisez davantage de connecteurs logiques académiques'
                ]
            });
        } else if (stats.formalityScore < 60) {
            recommendations.push({
                type: 'formality',
                priority: 'medium',
                title: 'Affiner le style académique',
                description: 'Votre style pourrait être plus formel.',
                suggestions: [
                    'Augmentez l\'utilisation du "nous académique"',
                    'Ajoutez des expressions comme "il convient de souligner"',
                    'Structurez vos phrases avec des subordonnées'
                ]
            });
        }
        
        // Recommandations basées sur la longueur des phrases
        if (stats.avgSentenceLength > 30) {
            recommendations.push({
                type: 'structure',
                priority: 'high',
                title: 'Simplifier les phrases',
                description: 'Vos phrases sont trop longues, ce qui peut nuire à la lisibilité.',
                suggestions: [
                    'Divisez les phrases de plus de 30 mots en phrases plus courtes',
                    'Utilisez des points-virgules pour séparer les idées connexes',
                    'Réorganisez les phrases complexes en plusieurs phrases simples'
                ]
            });
        } else if (stats.avgSentenceLength < 15) {
            recommendations.push({
                type: 'structure',
                priority: 'medium',
                title: 'Enrichir les phrases',
                description: 'Vos phrases sont trop courtes, ce qui peut donner un style haché.',
                suggestions: [
                    'Combinez certaines phrases courtes avec des conjonctions',
                    'Développez vos idées avec plus de détails',
                    'Utilisez des propositions relatives pour ajouter de l\'information'
                ]
            });
        }
        
        // Recommandations basées sur le vocabulaire
        if (stats.vocabularyScore < 40) {
            recommendations.push({
                type: 'vocabulary',
                priority: 'medium',
                title: 'Enrichir le vocabulaire',
                description: 'Votre vocabulaire pourrait être plus varié et technique.',
                suggestions: [
                    'Utilisez plus de synonymes pour éviter les répétitions',
                    'Intégrez des termes techniques spécifiques à votre domaine',
                    'Consultez un glossaire académique pour votre discipline'
                ]
            });
        }
        
        // Recommandations générales
        if (stats.wordCount < 300) {
            recommendations.push({
                type: 'general',
                priority: 'low',
                title: 'Développer le contenu',
                description: 'Votre texte est relativement court.',
                suggestions: [
                    'Ajoutez plus de détails et d\'explications',
                    'Développez chaque point avec des exemples concrets',
                    'Incluez des références théoriques ou pratiques'
                ]
            });
        }
        
        // Trier par priorité
        recommendations.sort((a, b) => {
            const priorityOrder = { high: 0, medium: 1, low: 2 };
            return priorityOrder[a.priority] - priorityOrder[b.priority];
        });
        
        return recommendations.slice(0, 5); // Limiter à 5 recommandations
    }
    
    displayResults(analysis) {
        if (!this.elements.resultsContainer) return;
        
        // Afficher le conteneur de résultats
        this.elements.resultsContainer.style.display = 'block';
        
        // Mettre à jour les statistiques
        this.displayStats(analysis.summary);
        
        // Mettre à jour les caractéristiques
        this.displayFeatures(analysis.features);
        
        // Mettre à jour les recommandations
        this.displayRecommendations(analysis.recommendations);
        
        // Mettre à jour l'analyse détaillée
        this.displayDetailedAnalysis(analysis.detailedAnalysis);
        
        // Cacher le chargement
        this.hideLoading();
        
        // Scroll vers les résultats
        this.elements.resultsContainer.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
    
    displayStats(stats) {
        if (!this.elements.statsContainer) return;
        
        const html = `
            <div class="row">
                <div class="col-md-3 mb-4">
                    <div class="stat-card text-center">
                        <div class="stat-value">${stats.wordCount}</div>
                        <div class="stat-label">Mots</div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card text-center">
                        <div class="stat-value">${stats.sentenceCount}</div>
                        <div class="stat-label">Phrases</div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card text-center">
                        <div class="stat-value">${stats.avgSentenceLength}</div>
                        <div class="stat-label">Mots/phrase</div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card text-center">
                        <div class="stat-value">${stats.overallScore}/100</div>
                        <div class="stat-label">Score global</div>
                    </div>
                </div>
            </div>
            
            <div class="row mb-4">
                <div class="col-12">
                    <h6>Répartition des scores</h6>
                    <div class="progress-group">
                        <div class="d-flex justify-content-between mb-1">
                            <span>Formalité</span>
                            <span>${stats.formalityScore}/100</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar" style="width: ${stats.formalityScore}%"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-1">
                            <span>Complexité</span>
                            <span>${stats.complexityScore}/100</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-success" style="width: ${stats.complexityScore}%"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-1">
                            <span>Vocabulaire</span>
                            <span>${stats.vocabularyScore}/100</span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar bg-info" style="width: ${stats.vocabularyScore}%"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between mb-1">
                            <span>Structure</span>
                            <span>${stats.structureScore}/100</span>
                        </div>
                        <div class="progress">
                            <div class="progress-bar bg-warning" style="width: ${stats.structureScore}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.elements.statsContainer.innerHTML = html;
    }
    
    displayFeatures(features) {
        if (!this.elements.featuresContainer || !features) return;
        
        let html = '';
        
        if (features.length > 0) {
            html = '<h6>Caractéristiques détectées</h6><div class="row">';
            
            features.forEach((feature, index) => {
                html += `
                    <div class="col-md-6 mb-2">
                        <div class="feature-item">
                            <i class="fas fa-check-circle text-success me-2"></i>
                            ${feature}
                        </div>
                    </div>
                `;
            });
            
            html += '</div>';
        } else {
            html = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    Aucune caractéristique spécifique n'a été détectée. Votre style est neutre.
                </div>
            `;
        }
        
        this.elements.featuresContainer.innerHTML = html;
    }
    
    displayRecommendations(recommendations) {
        if (!this.elements.recommendationsContainer || !recommendations) return;
        
        let html = '<h6>Recommandations d\'amélioration</h6>';
        
        if (recommendations.length > 0) {
            recommendations.forEach(rec => {
                const priorityClass = {
                    high: 'danger',
                    medium: 'warning',
                    low: 'info'
                }[rec.priority];
                
                html += `
                    <div class="recommendation-card mb-3 border-left-3 border-${priorityClass}">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <h6 class="mb-0">
                                <i class="fas fa-exclamation-circle text-${priorityClass} me-2"></i>
                                ${rec.title}
                            </h6>
                            <span class="badge bg-${priorityClass}">${rec.priority}</span>
                        </div>
                        <p class="text-muted mb-2">${rec.description}</p>
                        <ul class="mb-0">
                            ${rec.suggestions.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                    </div>
                `;
            });
        } else {
            html += `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle me-2"></i>
                    Votre style d'écriture est bien adapté aux rapports académiques. Aucune recommandation majeure.
                </div>
            `;
        }
        
        this.elements.recommendationsContainer.innerHTML = html;
    }
    
    displayDetailedAnalysis(details) {
        // Cette méthode pourrait être étendue pour afficher plus de détails
        console.log('Analyse détaillée:', details);
    }
    
    updateTextStats() {
        if (!this.elements.textArea) return;
        
        const text = this.elements.textArea.value;
        const words = text.trim().split(/\s+/).filter(w => w.length > 0).length;
        const chars = text.length;
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0).length;
        
        // Mettre à jour les compteurs dans l'interface
        const wordCountElement = document.getElementById('wordCount');
        const charCountElement = document.getElementById('charCount');
        const sentenceCountElement = document.getElementById('sentenceCount');
        
        if (wordCountElement) wordCountElement.textContent = words;
        if (charCountElement) charCountElement.textContent = chars;
        if (sentenceCountElement) sentenceCountElement.textContent = sentences;
    }
    
    showQuickScore(score) {
        // Afficher un score rapide dans l'interface
        const quickScoreElement = document.getElementById('quickScore');
        if (!quickScoreElement) {
            // Créer l'élément s'il n'existe pas
            const div = document.createElement('div');
            div.id = 'quickScore';
            div.className = 'alert alert-info mt-2';
            div.style.display = 'none';
            div.innerHTML = `
                <i class="fas fa-chart-line me-2"></i>
                Score de formalité préliminaire: <strong>${score}/100</strong>
                <small class="ms-2">(Analyse en temps réel)</small>
            `;
            
            if (this.elements.textArea && this.elements.textArea.parentNode) {
                this.elements.textArea.parentNode.appendChild(div);
            }
        }
        
        const element = document.getElementById('quickScore');
        if (element) {
            element.querySelector('strong').textContent = `${score}/100`;
            element.style.display = 'block';
            
            // Cacher après quelques secondes
            setTimeout(() => {
                element.style.display = 'none';
            }, 5000);
        }
    }
    
    showLoading() {
        // Afficher un indicateur de chargement
        const loadingElement = document.getElementById('analysisLoading');
        if (loadingElement) {
            loadingElement.style.display = 'block';
        }
        
        // Désactiver le bouton d'analyse
        if (this.elements.analyzeButton) {
            this.elements.analyzeButton.disabled = true;
            const originalText = this.elements.analyzeButton.innerHTML;
            this.elements.analyzeButton.innerHTML = `
                <i class="fas fa-spinner fa-spin me-2"></i>
                Analyse en cours...
            `;
            
            // Stocker le texte original pour le restaurer plus tard
            this.elements.analyzeButton.dataset.originalText = originalText;
        }
    }
    
    hideLoading() {
        // Cacher l'indicateur de chargement
        const loadingElement = document.getElementById('analysisLoading');
        if (loadingElement) {
            loadingElement.style.display = 'none';
        }
        
        // Réactiver le bouton d'analyse
        if (this.elements.analyzeButton) {
            this.elements.analyzeButton.disabled = false;
            const originalText = this.elements.analyzeButton.dataset.originalText;
            if (originalText) {
                this.elements.analyzeButton.innerHTML = originalText;
            }
        }
    }
    
    showError(message) {
        // Afficher un message d'erreur
        const errorElement = document.getElementById('analysisError');
        if (!errorElement) {
            const div = document.createElement('div');
            div.id = 'analysisError';
            div.className = 'alert alert-danger alert-dismissible fade show';
            div.innerHTML = `
                <i class="fas fa-exclamation-triangle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            if (this.elements.textArea && this.elements.textArea.parentNode) {
                this.elements.textArea.parentNode.insertBefore(div, this.elements.textArea);
            }
        } else {
            errorElement.querySelector('i').nextSibling.textContent = message;
            errorElement.style.display = 'block';
        }
    }
    
    showNotification(message, type = 'info') {
        // Créer une notification
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            max-width: 400px;
        `;
        
        const icon = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        }[type] || 'info-circle';
        
        notification.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-${icon} me-2"></i>
                <div>${message}</div>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }
    
    saveToLocalStorage() {
        if (this.elements.textArea) {
            localStorage.setItem('styleAnalyzerText', this.elements.textArea.value);
        }
    }
    
    saveAnalysisToLocalStorage(analysis) {
        if (analysis) {
            localStorage.setItem('lastStyleAnalysis', JSON.stringify(analysis));
        }
    }
    
    loadLastAnalysis() {
        const savedAnalysis = localStorage.getItem('lastStyleAnalysis');
        if (savedAnalysis) {
            try {
                const analysis = JSON.parse(savedAnalysis);
                this.state.analysis = analysis;
                this.displayResults(analysis);
                return true;
            } catch (e) {
                console.warn('Erreur lors du chargement de l\'analyse sauvegardée:', e);
            }
        }
        return false;
    }
    
    exportAnalysis(format = 'json') {
        if (!this.state.analysis) {
            this.showError('Aucune analyse à exporter');
            return;
        }
        
        let data, filename, mimeType;
        
        switch(format) {
            case 'json':
                data = JSON.stringify(this.state.analysis, null, 2);
                filename = `analyse_style_${Date.now()}.json`;
                mimeType = 'application/json';
                break;
                
            case 'txt':
                data = this.formatAnalysisAsText(this.state.analysis);
                filename = `analyse_style_${Date.now()}.txt`;
                mimeType = 'text/plain';
                break;
                
            default:
                this.showError('Format d\'export non supporté');
                return;
        }
        
        // Télécharger le fichier
        const blob = new Blob([data], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.click();
        URL.revokeObjectURL(url);
        
        this.showNotification('Analyse exportée avec succès', 'success');
    }
    
    formatAnalysisAsText(analysis) {
        let text = `ANALYSE DE STYLE ACADÉMIQUE\n`;
        text += `============================\n\n`;
        
        // Résumé
        text += `RÉSUMÉ\n`;
        text += `------\n`;
        text += `Mots: ${analysis.summary.wordCount}\n`;
        text += `Phrases: ${analysis.summary.sentenceCount}\n`;
        text += `Mots par phrase: ${analysis.summary.avgSentenceLength}\n`;
        text += `Score global: ${analysis.summary.overallScore}/100\n\n`;
        
        // Scores détaillés
        text += `SCORES DÉTAILLÉS\n`;
        text += `----------------\n`;
        text += `Formalité: ${analysis.summary.formalityScore}/100\n`;
        text += `Complexité: ${analysis.summary.complexityScore}/100\n`;
        text += `Vocabulaire: ${analysis.summary.vocabularyScore}/100\n`;
        text += `Structure: ${analysis.summary.structureScore}/100\n\n`;
        
        // Caractéristiques
        if (analysis.features && analysis.features.length > 0) {
            text += `CARACTÉRISTIQUES DÉTECTÉES\n`;
            text += `-------------------------\n`;
            analysis.features.forEach(feature => {
                text += `• ${feature}\n`;
            });
            text += `\n`;
        }
        
        // Recommandations
        if (analysis.recommendations && analysis.recommendations.length > 0) {
            text += `RECOMMANDATIONS\n`;
            text += `---------------\n`;
            analysis.recommendations.forEach(rec => {
                text += `[${rec.priority.toUpperCase()}] ${rec.title}\n`;
                text += `${rec.description}\n`;
                rec.suggestions.forEach(suggestion => {
                    text += `  - ${suggestion}\n`;
                });
                text += `\n`;
            });
        }
        
        // Métadonnées
        if (analysis.timestamp) {
            const date = new Date(analysis.timestamp);
            text += `\nAnalyse générée le: ${date.toLocaleString('fr-FR')}\n`;
        }
        
        return text;
    }
    
    destroy() {
        // Nettoyage
        if (this.state.realTimeTimeout) {
            clearTimeout(this.state.realTimeTimeout);
        }
        
        console.log('🗑️ StyleAnalyzer détruit');
    }
}

// Export pour utilisation globale
window.StyleAnalyzer = StyleAnalyzer;

// Initialisation automatique
document.addEventListener('DOMContentLoaded', function() {
    // Vérifier si nous sommes sur la page d'analyse de style
    const textArea = document.getElementById('referenceText');
    if (textArea) {
        // Initialiser l'analyseur
        window.styleAnalyzer = new StyleAnalyzer({
            minTextLength: 100,
            showRealTimeAnalysis: true,
            language: 'fr'
        });
        
        // Ajouter des boutons d'export si nécessaire
        addExportButtons();
    }
});

function addExportButtons() {
    const container = document.querySelector('.analysis-container');
    if (!container) return;
    
    const buttonGroup = document.createElement('div');
    buttonGroup.className = 'export-buttons mt-3 d-flex gap-2';
    buttonGroup.innerHTML = `
        <button class="btn btn-sm btn-outline-primary" onclick="exportAnalysis('json')">
            <i class="fas fa-file-code me-1"></i>JSON
        </button>
        <button class="btn btn-sm btn-outline-secondary" onclick="exportAnalysis('txt')">
            <i class="fas fa-file-alt me-1"></i>TXT
        </button>
        <button class="btn btn-sm btn-outline-info" onclick="copyAnalysis()">
            <i class="fas fa-copy me-1"></i>Copier
        </button>
    `;
    
    container.appendChild(buttonGroup);
}

function exportAnalysis(format) {
    if (window.styleAnalyzer) {
        window.styleAnalyzer.exportAnalysis(format);
    }
}

function copyAnalysis() {
    if (window.styleAnalyzer && window.styleAnalyzer.state.analysis) {
        const text = window.styleAnalyzer.formatAnalysisAsText(window.styleAnalyzer.state.analysis);
        navigator.clipboard.writeText(text).then(() => {
            if (window.styleAnalyzer) {
                window.styleAnalyzer.showNotification('Analyse copiée dans le presse-papier', 'success');
            }
        });
    }
}