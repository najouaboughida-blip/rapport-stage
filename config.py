"""
Configuration de l'application
"""

import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    # Clé secrète Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'academic-report-generator-ensa-oujda-2024'
    
    # Configuration OpenAI
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = "gpt-3.5-turbo"  # ou "gpt-4" si disponible
    OPENAI_TEMPERATURE = 0.7
    OPENAI_MAX_TOKENS = 1500
    
    # Configuration PDF
    PDF_PAGE_SIZE = 'A4'
    PDF_MARGINS = {
        'top': 2.5,    # cm
        'bottom': 2.5,
        'left': 2.5,
        'right': 2.5
    }
    
    # Configuration Word
    WORD_FONT_NAME = 'Times New Roman'
    WORD_FONT_SIZE = 11
    WORD_LINE_SPACING = 1.5
    
    # Chemins des fichiers
    UPLOAD_FOLDER = 'uploads'
    GENERATED_FOLDER = 'generated'
    TEMP_FOLDER = 'temp'
    
    # Tailles maximales
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    MAX_REFERENCE_TEXT = 5000  # caractères
    
    # Sessions
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Fonctionnalités
    ENABLE_STYLE_ANALYSIS = True
    ENABLE_AI_GENERATION = True
    ENABLE_REAL_OPENAI = True  # Mettre à False pour mode simulation
    
    @staticmethod
    def init_app(app):
        """Initialise l'application avec la configuration"""
        # Créer les dossiers nécessaires
        for folder in [app.config['UPLOAD_FOLDER'], 
                      app.config['GENERATED_FOLDER'], 
                      app.config['TEMP_FOLDER']]:
            if not os.path.exists(folder):
                os.makedirs(folder)
        
        # Configurer les limites
        app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
    TESTING = False
    ENABLE_REAL_OPENAI = False  # Mode simulation en développement

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    TESTING = False
    ENABLE_REAL_OPENAI = True

class TestingConfig(Config):
    """Configuration pour les tests"""
    DEBUG = False
    TESTING = True
    ENABLE_REAL_OPENAI = False

# Mapping des configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}