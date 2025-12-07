<template>
    <div class="detail-container">
        <!-- Back Button -->
        <button class="back-btn" @click="goBack">
            ← Wróć
        </button>

        <!-- Header Section -->
        <div class="header-section">
            <div class="header-top">
                <h1 class="item-title">{{ item.title }}</h1>
                <span class="item-id">{{ item.number }}</span>
            </div>

            <div class="header-meta">
                <div class="meta-item">
                    <span class="meta-label">Utworzono:</span>
                    <span class="meta-value">{{ formatDate(item.createdDate) }}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Ostatnia zmiana:</span>
                    <span class="meta-value">{{ formatDate(item.modifiedDate) }}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Autor:</span>
                    <span class="meta-value">{{ item.author }}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Dodane przez:</span>
                    <span class="meta-value">{{ item.postedBy }}</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">Partia polityczna:</span>
                    <span class="meta-value">{{ item.politicalParty }}</span>
                </div>
            </div>

            <div class="tags-section">
                <span v-for="tag in item.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>

            <div class="abstract-section">
                <h3>Streszczenie</h3>
                <p>{{ item.abstract }}</p>
            </div>

            <div class="download-section">
                <button class="download-btn sub-btn" @click="subscribeItem()">
                    🔔 Subskrybuj zmiany
                </button>
                <button class="download-btn pdf-btn" @click="downloadFile(item.pdfUrl, 'pdf')">
                    📄 Pobierz PDF
                </button>
                <button class="download-btn doc-btn" @click="downloadFile(item.docUrl, 'doc')">
                    📋 Pobierz DOC
                </button>
            </div>
        </div>

        <!-- Main Content Section -->
        <div class="content-section">
            <!-- States Timeline -->
            <div class="states-panel">
                <h3>Etapy projektu</h3>
                <div class="states-list">
                    <button v-for="state in item.states" :key="state.id" @click="selectState(state)" :class="[
                        'state-btn',
                        { active: selectedState?.id === state.id },
                        { completed: state.completed },
                        { inactive: !state.completed && selectedState?.id !== state.id }
                    ]" :disabled="!state.completed && selectedState?.id !== state.id">
                        <span class="state-name">{{ state.name }}</span>
                        <span v-if="state.completed" class="state-badge">✓</span>
                        <span v-else class="state-badge">⊘</span>
                    </button>
                </div>
            </div>

            <!-- State Details Panel -->
            <div class="state-details-panel">
                <h4>Szczegóły etapu: {{ selectedState?.name }}</h4>

                <div class="details-item">
                    <span class="details-label">Data wejścia w etap:</span>
                    <span class="details-value">{{ formatDate(selectedState?.enterDate) }}</span>
                </div>

                <div class="details-item">
                    <span class="details-label">Autor:</span>
                    <span class="details-value">{{ selectedState?.author }}</span>
                </div>

                <div class="details-item">
                    <span class="details-label">Dodane przez:</span>
                    <span class="details-value">{{ selectedState?.postedBy }}</span>
                </div>

                <div class="details-item">
                    <span class="details-label">Partia polityczna:</span>
                    <span class="details-value">{{ selectedState?.politicalParty }}</span>
                </div>

                <div class="details-abstract">
                    <h5>Streszczenie zmian</h5>
                    <p>{{ selectedState?.abstract }}</p>
                </div>

                <div v-if="selectedState?.notes" class="details-notes">
                    <h5>Wyjaśnienie</h5>
                    <p>{{ selectedState?.notes }}</p>
                </div>
            </div>

        </div>

        <!-- PDF Viewer and State Details -->
        <div class="viewer-section">

            <!-- Dropdown toolbar above PDF viewer -->
            <div class="viewer-toolbar">
                <div v-for="type in dropdownTypes" :key="type" class="dropdown">
                    <button class="dropdown-btn" @click.stop="toggleDropdown(type)">
                        {{ dropdownLabels[type] }}
                        <span class="caret">▼</span>
                    </button>
                    <ul v-if="dropdownOpen[type]" class="dropdown-menu">
                        <li v-for="option in dropdownOptions[type]" :key="option" @click.stop="selectDropdownOption(type, option)">
                            {{ option }}
                        </li>
                    </ul>
                </div>
            </div>

            <!-- PDF Viewer -->
            <div class="pdf-viewer-wrapper">
                <div class="viewer-header">
                    <h3>Podgląd etapu {{ selectedState?.name }}</h3>
                    <div class="viewer-download-buttons">
                        <button class="download-btn pdf-btn small"
                            @click="downloadStateFile(selectedState?.pdfUrl, 'pdf')">
                            📄 PDF
                        </button>
                        <button class="download-btn doc-btn small"
                            @click="downloadStateFile(selectedState?.docUrl, 'doc')">
                            📋 DOC
                        </button>
                    </div>
                </div>

                <!-- PDF Placeholder (in real app, use vue-pdf-embed or similar) -->
                <div class="pdf-placeholder">
                    <div class="pdf-preview">
                        <iframe v-if="isPdf(currentPreview)" :src="currentPreview" class="pdf-frame" title="PDF podgląd"></iframe>
                        <img v-else :src="currentPreview" :alt="selectedState?.name" class="pdf-image">
                    </div>
                    <p class="pdf-hint">Podgląd dokumentu: {{ selectedState?.documentName }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import dokumentPdf from '@/assets/dokument.pdf'
import dokument2Pdf from '@/assets/dokument2_stripped_colored.pdf'
import wyjasnieniaPdf from '@/assets/wyjasnienia.pdf'
import uwagiPdf from '@/assets/uwagi.pdf'
import stanowiskoPdf from '@/assets/stanowisko.pdf'
import ustaleniaPdf from '@/assets/ustalenia.pdf'

// Placeholder image for PDF preview
const placeholderImage = 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22400%22 height=%22500%22 viewBox=%220 0 400 500%22%3E%3Crect fill=%22%23f5f5f5%22 width=%22400%22 height=%22500%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 font-family=%22Arial%22 font-size=%2224%22 fill=%22%23999%22%3EPodgląd dokumentu%3C/text%3E%3C/svg%3E'

// Sample Item Data
const item = ref({
    id: 1,
    number: 'UD-2024-001',
    title: 'Ustawa o zmianie ustawy o ochronie danych osobowych',
    createdDate: '2024-12-01',
    modifiedDate: '2024-12-05',
    author: 'Dr. Piotr Kowalski',
    postedBy: 'Anna Nowak (Urzędnik)',
    politicalParty: 'Platforma Obywatelska',
    tags: ['#ochrona-danych', '#privacy', '#RODO'],
    abstract: 'Projekt ustawy wprowadza kompleksowe zmiany w zakresie przetwarzania danych osobowych w administracji publicznej. Głównym celem jest wzmocnienie ochrony praw obywateli oraz uproszczenie procedur administracyjnych związanych z przetwarzaniem danych.',
    pdfUrl: '/documents/UD-2024-001.pdf',
    docUrl: '/documents/UD-2024-001.docx',
    states: [
        {
            id: 1,
            name: 'Wstępne opracowanie',
            completed: true,
            enterDate: '2024-12-01',
            author: 'Dr. Piotr Kowalski',
            postedBy: 'Anna Nowak',
            politicalParty: 'Platforma Obywatelska',
            abstract: 'Etap obejmuje wstępne przeanalizowanie problemu i przygotowanie koncepcji projektu ustawy.',
            notes: 'Przeprowadzono konsultacje z ekspertami z zakresu ochrony danych.',
            documentName: 'Koncepcja_projektu_UD-2024-001.pdf',
            pdfUrl: '/documents/states/UD-2024-001-stage-1.pdf',
            docUrl: '/documents/states/UD-2024-001-stage-1.docx',
            preview: dokumentPdf
        },
        {
            id: 2,
            name: 'Komisja legislacyjna',
            completed: false,
            enterDate: '2024-12-02',
            author: 'Prof. Maria Lewandowska',
            postedBy: 'Marek Wiśniewski',
            politicalParty: 'Prawo i Sprawiedliwość',
            abstract: 'Etap obejmuje ocenę projektu przez Komisję Legislacyjną. Przeanalizowano zgodność z prawem międzynarodowym i unijnym.',
            notes: 'Komisja zaproponowała 5 poprawek do projektu.',
            documentName: 'Opinia_komisji_legislacyjnej.pdf',
            pdfUrl: '/documents/states/UD-2024-001-stage-2.pdf',
            docUrl: '/documents/states/UD-2024-001-stage-2.docx',
            preview: 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%22400%22 height=%22500%22 viewBox=%220 0 400 500%22%3E%3Crect fill=%22%23f3e5f5%22 width=%22400%22 height=%22500%22/%3E%3Ctext x=%2250%25%22 y=%2215%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 font-family=%22Arial%22 font-size=%2220%22 fill=%22%237b1fa2%22 font-weight=%22bold%22%3EKomisja legislacyjna%3C/text%3E%3C/svg%3E'
        },
        {
            id: 3,
            name: 'Sejm - pierwsza lektura',
            completed: true,
            enterDate: '2024-12-03',
            author: 'Poseł Jan Nowak',
            postedBy: 'Piotr Lewandowski',
            politicalParty: 'Polska 2050',
            abstract: 'Projekt został przedstawiony na posiedzeniu Sejmu i poddany pierwszej lekturze. Debata przebiegła konstruktywnie.',
            notes: 'Zgłoszono 12 poprawek do projektu.',
            documentName: 'Protokol_pierwsza_lektura.pdf',
            pdfUrl: '/documents/states/UD-2024-001-stage-3.pdf',
            docUrl: '/documents/states/UD-2024-001-stage-3.docx',
            preview: dokument2Pdf
        },
        {
            id: 4,
            name: 'Komisja sejmowa',
            completed: false,
            enterDate: null,
            author: null,
            postedBy: null,
            politicalParty: null,
            abstract: 'Etap obejmuje szczegółową ocenę projektu przez właściwą komisję sejmową.',
            notes: null,
            documentName: 'Brak dokumentu',
            pdfUrl: null,
            docUrl: null,
            preview: null
        },
        {
            id: 5,
            name: 'Sejm - druga lektura',
            completed: false,
            enterDate: null,
            author: null,
            postedBy: null,
            politicalParty: null,
            abstract: 'Druga lektura projektu na posiedzeniu Sejmu.',
            notes: null,
            documentName: 'Brak dokumentu',
            pdfUrl: null,
            docUrl: null,
            preview: null
        },
        {
            id: 6,
            name: 'Senat',
            completed: false,
            enterDate: null,
            author: null,
            postedBy: null,
            politicalParty: null,
            abstract: 'Projekt przesyłany do Senatu na rozpatrzenie.',
            notes: null,
            documentName: 'Brak dokumentu',
            pdfUrl: null,
            docUrl: null,
            preview: null
        }
    ]
})

// Selected state (default to first state)
const selectedState = ref(item.value.states[0])

// Dropdown configuration
const dropdownTypes = ['ustawa', 'uwaga', 'odniesienie', 'ustalenie']

const dropdownOptions = {
    ustawa: ['Ustawa', 'Dodatek A', 'Dodatek B', 'Wyjaśnienie A', 'Wyjaśnienie B'],
    uwaga: ['Uwaga ogólna', 'Uwaga legislacyjna', 'Uwaga redakcyjna', 'Uwaga techniczna'],
    odniesienie: ['Odniesienie do art. 1', 'Odniesienie do dyrektywy UE', 'Odniesienie do orzecznictwa', 'Odniesienie do konsultacji'],
    ustalenie: ['Ustalenie komisji', 'Ustalenie proceduralne', 'Ustalenie harmonogramu', 'Ustalenie finansowe']
}

const defaultDropdownLabels = {
    ustawa: 'Ustawa',
    uwaga: 'Uwaga',
    odniesienie: 'Odniesienie',
    ustalenie: 'Ustalenie'
}

const dropdownLabels = ref({ ...defaultDropdownLabels })

const dropdownOpen = ref({
    ustawa: false,
    uwaga: false,
    odniesienie: false,
    ustalenie: false
})

// Override preview when dropdowns are used
const overridePreview = ref(null)

// Current preview source (override > selected state > placeholder)
const currentPreview = computed(() => overridePreview.value || selectedState.value?.preview || placeholderImage)

// Helper functions
const formatDate = (dateString) => {
    if (!dateString) return 'Nieznana'
    const options = { year: 'numeric', month: 'long', day: 'numeric' }
    return new Date(dateString).toLocaleDateString('pl-PL', options)
}

const selectState = (state) => {
    selectedState.value = state
    // Reset preview to state default (equivalent to selecting "Ustawa")
    overridePreview.value = null
    dropdownLabels.value = { ...defaultDropdownLabels }
    dropdownOpen.value = {
        ustawa: false,
        uwaga: false,
        odniesienie: false,
        ustalenie: false
    }
}

const isPdf = (src) => {
    if (!src) return false
    return src.toLowerCase().endsWith('.pdf')
}

const subscribeItem = () => {
    alert('Subskrypcja zmian dla tego projektu została aktywowana.')
}

const downloadFile = (url, type) => {
    if (!url) {
        alert(`Plik ${type.toUpperCase()} nie jest dostępny`)
        return
    }
    // In real app, this would download the actual file
    console.log(`Downloading ${type} from ${url}`)
    // Simulate download
    const link = document.createElement('a')
    link.href = url
    link.download = `document.${type === 'pdf' ? 'pdf' : 'docx'}`
    link.click()
}

const downloadStateFile = (url, type) => {
    if (!url) {
        alert(`Plik ${type.toUpperCase()} dla tego etapu nie jest dostępny`)
        return
    }
    console.log(`Downloading state ${type} from ${url}`)
    const link = document.createElement('a')
    link.href = url
    link.download = `stage-document.${type === 'pdf' ? 'pdf' : 'docx'}`
    link.click()
}

const toggleDropdown = (type) => {
    dropdownOpen.value = {
        ...dropdownOpen.value,
        [type]: !dropdownOpen.value[type]
    }
}

const selectDropdownOption = (type, option) => {
    // Reset other labels to defaults, set current to selected option
    dropdownLabels.value = {
        ...defaultDropdownLabels,
        [type]: option
    }

    // Set preview based on selection
    switch (type) {
        case 'ustawa':
            overridePreview.value = option === 'Ustawa' ? null : wyjasnieniaPdf
            break
        case 'uwaga':
            overridePreview.value = uwagiPdf
            break
        case 'odniesienie':
            overridePreview.value = stanowiskoPdf
            break
        case 'ustalenie':
            overridePreview.value = ustaleniaPdf
            break
        default:
            overridePreview.value = null
    }

    // Close all dropdowns
    dropdownOpen.value = {
        ustawa: false,
        uwaga: false,
        odniesienie: false,
        ustalenie: false
    }
}

const goBack = () => {
    window.history.back()
}
</script>

<style scoped>
* {
    box-sizing: border-box;
}

.detail-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f5f5f5;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    gap: 30px;
}

/* Back Button */
.back-btn {
    align-self: flex-start;
    padding: 10px 16px;
    background-color: white;
    border: 2px solid #e0e0e0;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    color: #333;
    transition: all 0.3s ease;
}

.back-btn:hover {
    background-color: #f5f5f5;
    border-color: #DC143C;
    color: #DC143C;
    transform: translateX(-3px);
}

/* Header Section */
.header-section {
    background-color: white;
    padding: 30px;
    border-radius: 8px;
    /* margin-bottom: 30px; */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-top {
    display: flex;
    justify-content: space-between;
    align-items: start;
    margin-bottom: 20px;
}

.item-title {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    color: #333;
    flex: 1;
    line-height: 1.3;
}

.item-id {
    background-color: #e8f5e9;
    color: #2e7d32;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    white-space: nowrap;
    margin-left: 15px;
}

.header-meta {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
    padding-bottom: 25px;
    border-bottom: 1px solid #e0e0e0;
}

.meta-item {
    display: flex;
    flex-direction: column;
}

.meta-label {
    font-size: 12px;
    font-weight: 600;
    color: #999;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.meta-value {
    font-size: 16px;
    color: #333;
    font-weight: 500;
}

/* Tags */
.tags-section {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 25px;
}

.tag {
    display: inline-block;
    background-color: #e3f2fd;
    color: #1976d2;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
}

/* Abstract */
.abstract-section {
    margin-bottom: 25px;
}

.abstract-section h3 {
    margin: 0 0 12px 0;
    font-size: 16px;
    color: #333;
    font-weight: 600;
}

.abstract-section p {
    margin: 0;
    color: #666;
    line-height: 1.6;
    font-size: 15px;
}

/* Download Buttons */
.download-section {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

.download-btn {
    padding: 12px 24px;
    border: 2px solid #e0e0e0;
    border-radius: 6px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 600;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.download-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.pdf-btn {
    background-color: #ffebee;
    color: #c62828;
    border-color: #ef5350;
}

.pdf-btn:hover {
    background-color: #ffcdd2;
    border-color: #e53935;
}

.doc-btn {
    background-color: #e3f2fd;
    color: #1565c0;
    border-color: #42a5f5;
}

.doc-btn:hover {
    background-color: #bbdefb;
    border-color: #1e88e5;
}

.sub-btn {
    background-color: #fff3e0;
    color: #ef6c00;
    border-color: #ffb74d;
}

.sub-btn:hover {
    background-color: #ffe0b2;
    border-color: #ffa726;
}

.download-btn.small {
    padding: 8px 16px;
    font-size: 13px;
}

/* Content Section */
.content-section {
    display: grid;
    grid-template-columns: 250px 1fr;
    gap: 20px;
}

/* States Panel */
.states-panel {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    height: fit-content;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.states-panel h3 {
    margin: 0 0 15px 0;
    font-size: 16px;
    color: #333;
    font-weight: 600;
}

.states-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.state-btn {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 14px;
    border: 2px solid #e0e0e0;
    background-color: white;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: #666;
    transition: all 0.3s ease;
    text-align: left;
}

.state-btn:hover:not(:disabled) {
  border-color: #DC143C;
  background-color: #f1f8f6;
}.state-btn.active {
  background-color: #DC143C;
  color: white;
  border-color: #DC143C;
}.state-btn.inactive:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.state-btn.completed {
  border-color: #FF6B6B;
}.state-name {
    flex: 1;
}

.state-badge {
    font-size: 16px;
}

/* Viewer Section */
.viewer-section {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
}

.viewer-toolbar {
    display: flex;
    gap: 12px;
    margin-bottom: 5px;
    flex-wrap: wrap;
}

.dropdown {
    position: relative;
}

.dropdown-btn {
    padding: 12px 18px;
    border: 2px solid #e0e0e0;
    background-color: #fff;
    border-radius: 8px;
    cursor: pointer;
    font-size: 15px;
    font-weight: 700;
    color: #333;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    transition: all 0.2s ease;
}

.dropdown-btn:hover {
    border-color: #DC143C;
    color: #DC143C;
    box-shadow: 0 2px 8px rgba(220, 20, 60, 0.15);
}

.caret {
    font-size: 12px;
    color: inherit;
}

.dropdown-menu {
    position: absolute;
    top: 105%;
    left: 0;
    min-width: 180px;
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 6px 0;
    z-index: 10;
}

.dropdown-menu li {
    list-style: none;
    padding: 10px 14px;
    font-size: 14px;
    color: #333;
    cursor: pointer;
    transition: background 0.2s ease, color 0.2s ease;
}

.dropdown-menu li:hover {
    background: #ffe8ed;
    color: #DC143C;
}

/* PDF Viewer */
.pdf-viewer-wrapper {
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
}

.viewer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px;
    border-bottom: 1px solid #e0e0e0;
    background-color: #fafafa;
}

.viewer-header h3 {
    margin: 0;
    font-size: 16px;
    color: #333;
    font-weight: 600;
}

.viewer-download-buttons {
    display: flex;
    gap: 8px;
}

.pdf-placeholder {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40px 20px;
    background-color: #f9f9f9;
    min-height: 500px;
}

.pdf-preview {
    width: 100%;
    max-width: 100%;
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.pdf-image {
    max-width: 100%;
    max-height: 400px;
    border-radius: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.pdf-frame {
    width: 100%;
    height: 500px;
    border: none;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.pdf-hint {
    color: #999;
    font-size: 14px;
    margin: 0;
    text-align: center;
}

/* State Details Panel */
.state-details-panel {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    overflow-y: auto;
    max-height: calc(100vh - 300px);
}

.state-details-panel h4 {
  margin: 0 0 20px 0;
  font-size: 15px;
  color: #333;
  font-weight: 600;
  border-bottom: 2px solid #DC143C;
  padding-bottom: 12px;
}.details-item {
    display: flex;
    flex-direction: column;
    margin-bottom: 16px;
}

.details-label {
    font-size: 12px;
    font-weight: 600;
    color: #999;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.details-value {
    font-size: 14px;
    color: #333;
    font-weight: 500;
}

.details-abstract,
.details-notes {
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #e0e0e0;
}

.details-abstract h5,
.details-notes h5 {
    margin: 0 0 10px 0;
    font-size: 13px;
    color: #333;
    font-weight: 600;
}

.details-abstract p,
.details-notes p {
    margin: 0;
    font-size: 13px;
    color: #666;
    line-height: 1.5;
}

/* Responsive */
@media (max-width: 1024px) {
    .content-section {
        grid-template-columns: 1fr;
    }

    .viewer-section {
        grid-template-columns: 1fr;
    }

    .state-details-panel {
        max-height: none;
    }
}

@media (max-width: 768px) {
    .detail-container {
        padding: 10px;
    }

    .header-section {
        padding: 15px;
    }

    .header-top {
        flex-direction: column;
    }

    .item-id {
        margin-left: 0;
        margin-top: 10px;
    }

    .header-meta {
        grid-template-columns: 1fr;
    }

    .content-section {
        grid-template-columns: 1fr;
    }

    .states-panel {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    }

    .states-list {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 10px;
    }

    .download-section {
        flex-direction: column;
    }

    .download-btn {
        width: 100%;
    }
}
</style>
