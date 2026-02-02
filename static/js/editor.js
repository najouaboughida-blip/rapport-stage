{% block extra_js %}
<script>
// ==================== VARIABLES GLOBALES ====================
let currentSection = null;
let sectionsData = {{ report.sections|tojson|safe }};
let structure = {{ structure|tojson|safe }};
let currentSectionIndex = -1;
let sectionIds = Object.keys(structure);
let isViewingCoverPage = true;

// Données de la page de garde - CORRECTION DE LA DATE
let coverPageData = {
    university: "UNIVERSITÉ MOHAMMED PREMIER",
    school: "École Nationale des Sciences Appliquées - Oujda",
    filiere: "{{ report.student.filiere|default('GÉNIE INFORMATIQUE')|upper }}",
    title: "RAPPORT DE STAGE DE FIN D'ÉTUDES",
    project_title: "{{ report.student.project_title|default('TITRE DU PROJET DE STAGE') }}",
    student_name: "{{ report.student.full_name|default('NOM Prénom')|upper }}",
    academic_supervisor: "{{ report.student.academic_supervisor|default('Dr. NOM Prénom') }}",
    company_supervisor: "{{ report.company.supervisor|default('M. NOM Prénom') }}",
    company_name: "{{ report.company.name|default('Entreprise') }}",
    company_name2: "{{ report.company.name|default('Entreprise') }}",
    duration: "{{ report.student.duration|default('2 mois') }}",
    academic_year: "{{ report.student.academic_year|default('2024-2025') }}",
    date: `Fait à Oujda, le ${new Date().toLocaleDateString('fr-FR')}`
};

// ==================== INITIALISATION ====================
$(document).ready(function() {
    console.log('🚀 Éditeur initialisé');
    
    // Initialiser la page de garde
    initCoverPage();
    
    // Charger la page de garde par défaut
    loadCoverPage();
    
    // Événements clavier
    $(document).on('keydown', function(e) {
        handleKeyDown(e);
    });
    
    // Mettre à jour les stats initiales
    updateAllStats();
    updateProgress();
});

// ==================== FONCTIONS DE BASE ====================

// Initialiser la page de garde
function initCoverPage() {
    console.log('📄 Initialisation page de garde');
    
    // CORRECTION : Remplir la date dynamiquement
    const today = new Date().toLocaleDateString('fr-FR');
    $('[data-field="date"]').text(`Fait à Oujda, le ${today}`);
    
    // Remplir les champs avec les données
    $('.cover-editable-field').each(function() {
        const field = $(this).data('field');
        if (coverPageData[field]) {
            $(this).text(coverPageData[field]);
        }
        
        // Ajouter l'événement input
        $(this).on('input', function() {
            const fieldName = $(this).data('field');
            coverPageData[fieldName] = $(this).text().trim();
            updateCoverWordCount();
            updateProgress();
        });
    });
}

// Charger la page de garde
function loadCoverPage() {
    console.log('🔍 Chargement page de garde');
    
    // Mettre à jour l'état
    isViewingCoverPage = true;
    currentSection = null;
    currentSectionIndex = -1;
    
    // Afficher/masquer les éléments
    $('#coverPageSection').show();
    $('#editorArea').hide();
    $('#editorStats').hide();
    $('#emptyState').hide();
    $('#previewSection').hide();
    
    // Mettre à jour le titre
    $('#currentSectionTitle').html('<i class="fas fa-file-contract me-2"></i> PAGE DE GARDE');
    $('#currentSectionDescription').text('Page titre officielle - Modifiable en direct');
    
    // Mettre à jour la sélection dans la sidebar
    $('.section-card').removeClass('active');
    $('#coverPageCard').addClass('active');
    
    // Mettre à jour les statistiques
    updateCoverWordCount();
    updateProgress();
}

// Charger une section régulière
function loadSection(sectionId) {
    console.log('📂 Chargement section:', sectionId);
    
    // Sauvegarder avant de changer
    if (isViewingCoverPage) {
        saveCoverPage(false);
    } else if (currentSection) {
        saveCurrentSection(false);
    }
    
    // Mettre à jour l'état
    isViewingCoverPage = false;
    currentSection = sectionId;
    currentSectionIndex = sectionIds.indexOf(sectionId);
    
    // Afficher/masquer les éléments
    $('#coverPageSection').hide();
    $('#editorArea').show();
    $('#editorStats').show();
    $('#emptyState').hide();
    $('#previewSection').hide();
    
    // Mettre à jour le titre
    const sectionInfo = structure[sectionId];
    $('#currentSectionTitle').text(sectionInfo.title);
    $('#currentSectionDescription').text(sectionInfo.description);
    
    // Charger le contenu
    let content = sectionsData[sectionId] || getDefaultContent(sectionId, sectionInfo);
    $('#editorArea').html(content);
    
    // Mettre à jour la sélection dans la sidebar
    $('.section-card').removeClass('active');
    $(`#card-${sectionId}`).addClass('active');
    
    // Activer l'édition
    $('#editorArea').attr('contenteditable', 'true');
    
    // Mettre à jour les statistiques
    updateWordCount();
    updateProgress();
    updateLastSaveTime();
}

// ==================== NAVIGATION ====================

function previousSection() {
    console.log('⬅️ Section précédente');
    
    if (isViewingCoverPage) {
        // De la page de garde vers la dernière section
        if (sectionIds.length > 0) {
            loadSection(sectionIds[sectionIds.length - 1]);
        }
    } else if (currentSectionIndex > 0) {
        // Vers la section précédente
        loadSection(sectionIds[currentSectionIndex - 1]);
    } else {
        // De la première section vers la page de garde
        loadCoverPage();
    }
}

function nextSection() {
    console.log('➡️ Section suivante');
    
    if (isViewingCoverPage) {
        // De la page de garde vers la première section
        if (sectionIds.length > 0) {
            loadSection(sectionIds[0]);
        }
    } else if (currentSectionIndex < sectionIds.length - 1) {
        // Vers la section suivante
        loadSection(sectionIds[currentSectionIndex + 1]);
    } else {
        // De la dernière section vers la page de garde
        loadCoverPage();
    }
}

// ==================== ÉDITION ====================

function formatText(command) {
    if (isViewingCoverPage) {
        // Pour la page de garde
        document.execCommand(command, false, null);
        updateCoverWordCount();
    } else {
        // Pour les sections régulières
        document.execCommand(command, false, null);
        updateWordCount();
    }
}

function insertList(type) {
    const command = type === 'ul' ? 'insertUnorderedList' : 'insertOrderedList';
    formatText(command);
}

function undoAction() {
    document.execCommand('undo');
    updateWordCount();
}

function redoAction() {
    document.execCommand('redo');
    updateWordCount();
}

// ==================== SAUVEGARDE ====================

function saveCurrent() {
    if (isViewingCoverPage) {
        saveCoverPage();
    } else {
        saveCurrentSection();
    }
}

function saveCoverPage(showAlert = true) {
    console.log('💾 Sauvegarde page de garde');
    
    // Collecter les données
    const data = {};
    $('.cover-editable-field').each(function() {
        const field = $(this).data('field');
        data[field] = $(this).text().trim();
    });
    
    // Simuler la sauvegarde (à remplacer par un appel API)
    $.ajax({
        url: `/api/update-cover-page/{{ report_id }}`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function(response) {
            if (response.success && showAlert) {
                showNotification('Page de garde sauvegardée', 'success');
            }
            updateCoverWordCount();
            updateProgress();
            updateLastSaveTime();
        },
        error: function() {
            if (showAlert) {
                showNotification('Erreur lors de la sauvegarde', 'error');
            }
        }
    });
}

function saveCurrentSection(showAlert = true) {
    if (!currentSection) return;
    
    console.log('💾 Sauvegarde section:', currentSection);
    
    const content = $('#editorArea').html();
    sectionsData[currentSection] = content;
    
    // Simuler la sauvegarde (à remplacer par un appel API)
    $.ajax({
        url: `/api/update-single-section/{{ report_id }}`,
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            section_name: currentSection,
            content: content
        }),
        success: function(response) {
            if (response.success && showAlert) {
                showNotification('Section sauvegardée', 'success');
            }
            updateWordCount();
            updateProgress();
            updateLastSaveTime();
        },
        error: function() {
            if (showAlert) {
                showNotification('Erreur lors de la sauvegarde', 'error');
            }
        }
    });
}

// ==================== COMPTAGE DE MOTS ====================

function updateWordCount() {
    if (!currentSection || isViewingCoverPage) return;
    
    const text = $('#editorArea').text();
    const words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
    
    // Mettre à jour la sidebar
    $(`#stats-${currentSection}`).text(words);
    
    // Mettre à jour les stats d'édition
    $('#wordCount').text(words);
    $('#readingTime').text(Math.ceil(words / 200));
    
    // Validation
    const sectionInfo = structure[currentSection];
    if (words < sectionInfo.min_words) {
        $(`#stats-${currentSection}`).css('color', '#E74C3C');
    } else if (words > sectionInfo.max_words) {
        $(`#stats-${currentSection}`).css('color', '#F39C12');
    } else {
        $(`#stats-${currentSection}`).css('color', '#27AE60');
    }
    
    updateProgress();
}

function updateCoverWordCount() {
    let totalWords = 0;
    $('.cover-editable-field').each(function() {
        const text = $(this).text();
        const words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
        totalWords += words;
    });
    $('#stats-cover').text(totalWords);
}

function updateAllStats() {
    // Mettre à jour toutes les sections
    for (const sectionId in sectionsData) {
        const content = sectionsData[sectionId] || '';
        const text = content.replace(/<[^>]+>/g, ' ');
        const words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
        $(`#stats-${sectionId}`).text(words);
    }
    
    // Mettre à jour la page de garde
    updateCoverWordCount();
    
    // Mettre à jour la progression
    updateProgress();
}

// ==================== PROGRESSION ====================

function updateProgress() {
    let completedSections = 0;
    let totalWords = 0;
    let totalMinWords = 0;
    
    // CORRECTION : Inclure la page de garde dans le calcul
    const totalSections = Object.keys(structure).length + 1; // +1 pour la page de garde
    
    // Page de garde (toujours considérée comme complète si elle a du contenu)
    let coverWords = 0;
    $('.cover-editable-field').each(function() {
        const text = $(this).text();
        const words = text.trim().split(/\s+/).filter(word => word.length > 0).length;
        coverWords += words;
    });
    totalWords += coverWords;
    
    if (coverWords > 10) { // Si la page de garde a au moins 10 mots
        completedSections++;
    }
    
    // Sections régulières
    for (const sectionId in structure) {
        const sectionInfo = structure[sectionId];
        
        // Compter les mots
        let wordCount = 0;
        if (sectionsData[sectionId]) {
            const text = sectionsData[sectionId].replace(/<[^>]+>/g, ' ');
            wordCount = text.trim().split(/\s+/).filter(word => word.length > 0).length;
        }
        
        totalWords += wordCount;
        totalMinWords += sectionInfo.min_words || 0;
        
        if (wordCount >= (sectionInfo.min_words || 50)) {
            completedSections++;
        }
    }
    
    const progress = Math.min(100, Math.round((completedSections / totalSections) * 100));
    
    // Mettre à jour l'interface
    $('#progressIndicator').text(`${progress}%`);
    $('#progressIndicator').removeClass('progress-complete progress-partial');
    $('#progressIndicator').addClass(progress >= 100 ? 'progress-complete' : 'progress-partial');
    
    // CORRECTION : AFFICHAGE CORRECT
    $('#progressText').html(`${completedSections}/${totalSections} sections complètes`);
    $('#wordProgressText').html(`${totalWords}/${totalMinWords} mots minimum atteints`);
    
    // Afficher/masquer le bouton de téléchargement
    if (progress >= 80) {
        $('#downloadBtn').show();
    } else {
        $('#downloadBtn').hide();
    }
}

// ==================== UTILITAIRES ====================

function updateLastSaveTime() {
    const now = new Date();
    const timeStr = now.toLocaleTimeString('fr-FR', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    $('#lastSave').text(`Dernière sauvegarde: ${timeStr}`);
}

function showPreview() {
    if (isViewingCoverPage) {
        $('#previewContent').html($('#coverPageEditable').clone().removeClass('cover-page-editable'));
    } else {
        $('#previewContent').html($('#editorArea').clone().removeClass('section-content-editor'));
    }
    $('#previewSection').show();
}

function hidePreview() {
    $('#previewSection').hide();
}

function resetCoverPage() {
    if (confirm('Réinitialiser la page de garde ?')) {
        initCoverPage();
        showNotification('Page de garde réinitialisée', 'info');
    }
}

function downloadReport() {
    showNotification('Téléchargement en cours...', 'info');
    window.location.href = `/api/download-report-pdf/{{ report_id }}`;
}

function showNotification(message, type = 'info') {
    const alertClass = {
        'success': 'alert-success',
        'error': 'alert-danger',
        'warning': 'alert-warning',
        'info': 'alert-info'
    }[type];
    
    const icon = {
        'success': 'check-circle',
        'error': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    }[type];
    
    const alert = $(`
        <div class="alert ${alertClass} alert-dismissible fade show position-fixed" 
             style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;">
            <div class="d-flex align-items-center">
                <i class="fas fa-${icon} me-2"></i>
                <div>${message}</div>
            </div>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `);
    
    $('body').append(alert);
    
    setTimeout(() => {
        alert.alert('close');
    }, 3000);
}

function getDefaultContent(sectionId, sectionInfo) {
    const defaults = {
        'remerciements': `<h2>REMERCIEMENTS</h2>
<p>Je tiens à exprimer ma gratitude à toutes les personnes qui ont contribué à la réalisation de ce travail...</p>`,
        
        'resume': `<h2>RÉSUMÉ</h2>
<p>Ce rapport présente les travaux réalisés lors de mon stage...</p>`,
        
        'introduction': `<h2>INTRODUCTION</h2>
<p>Cette introduction présente le contexte, la problématique et les objectifs du stage...</p>`
    };
    
    return defaults[sectionId] || `<p>Commencez à rédiger votre section ici...</p>`;
}

function handleKeyDown(e) {
    // Ctrl+S pour sauvegarder
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        saveCurrent();
    }
    
    // Ctrl+Z/Y pour undo/redo
    if (e.ctrlKey && e.key === 'z') {
        e.preventDefault();
        undoAction();
    }
    if (e.ctrlKey && e.key === 'y') {
        e.preventDefault();
        redoAction();
    }
}
</script>
{% endblock %}