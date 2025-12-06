<template>
  <div class="panel-container">
    <!-- Top Navigation Bar -->
    <nav class="top-nav">
      <div class="nav-left">
        <h2 class="app-title">Panel Użytkownika</h2>
      </div>
      <div class="nav-center">
        <span class="connection-status">
          🔒 Bezpieczne połączenie w sieci LAN
        </span>
      </div>
      <div class="nav-right">
        <div class="user-info">
          <span class="user-name">{{ currentUser.name }}</span>
          <span class="user-role">{{ currentUser.role }}</span>
        </div>
        <button class="colorblind-mode-btn" @click="toggleColorblindMode"
          :title="isColorblindMode ? 'Wyłącz tryb dla daltonisty' : 'Włącz tryb dla daltonisty'">
          {{ isColorblindMode ? '👁 Tryb normalny' : '🎨 Tryb dla daltonisty' }}
        </button>
        <button class="dark-mode-btn" :class="{ active: isDarkMode }" @click="toggleDarkMode"
          :title="isDarkMode ? 'Wyłącz tryb nocny' : 'Włącz tryb nocny'">
          <span class="contrast-icon">A</span>
        </button>
        <button class="logout-btn" @click="logout">
          Wyloguj się
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <div class="panel-content">
      <!-- Statistics Section -->
      <section class="statistics-section">
        <h3>Statystyka projektów</h3>
        <div class="stats-grid">
          <div v-for="stat in itemStats" :key="stat.stage" class="stat-card"
            :style="{ backgroundImage: stat.gradient }">
            <div class="stat-number">{{ stat.count }}</div>
            <div class="stat-label">{{ stat.stage }}</div>
          </div>
        </div>
      </section>

      <!-- Items Requiring Action Section -->
      <section class="action-items-section">
        <h3>Projekty oczekujące na Twoją decyzję</h3>

        <div v-if="actionItems.length === 0" class="no-items">
          Brak projektów wymagających Twojej decyzji
        </div>

        <div v-else class="action-items-list">
          <div v-for="item in actionItems" :key="item.id" class="action-item-card">
            <!-- Item Header with Actions -->
            <div class="item-header-row">
              <div class="item-title-section">
                <h4 class="item-title">{{ item.title }}</h4>
                <span class="item-number">{{ item.number }}</span>
              </div>
              <div class="item-actions">
                <button class="action-btn accept-btn" @click="acceptItem(item.id)">
                  ✓ Zaakceptuj
                </button>
                <button class="action-btn cancel-btn" @click="cancelItem(item.id)">
                  ✕ Odrzuć
                </button>
                <button class="action-btn details-btn" @click="goToDetails(item.id)">
                  → Szczegóły
                </button>
              </div>
            </div>

            <!-- Item Information -->
            <div class="item-info">
              <div class="info-row">
                <span class="info-label">Status:</span>
                <span class="info-value">{{ item.currentStage }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Próba:</span>
                <span class="info-value">{{ item.initiative }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Data wpracowania:</span>
                <span class="info-value">{{ formatDate(item.date) }}</span>
              </div>
            </div>

            <!-- Item Description -->
            <p class="item-description">{{ item.description }}</p>

            <!-- Item Tags -->
            <div class="item-tags">
              <span v-for="tag in item.tags" :key="tag" class="tag">{{ tag }}</span>
            </div>

            <!-- Item Footer -->
            <div class="item-footer">
              <span class="added-by">Dodane przez: {{ item.addedBy }}</span>
              <span class="priority" :class="'priority-' + item.priority">
                {{ item.priority === 'high' ? '⚠ Wysoki priorytet' : item.priority === 'medium' ? '→ Średni priorytet' :
                '✓ Niski priorytet' }}
              </span>
            </div>
          </div>
        </div>
      </section>

      <!-- Administrative Errands Section -->
      <section class="administrative-errands-section">
        <h3>Sprawy urzędowe</h3>

        <div v-if="administrativeErrands.length === 0" class="no-items">
          Brak spraw urzędowych
        </div>

        <div v-else class="errands-list">
          <div v-for="errand in administrativeErrands" :key="errand.id" class="errand-card">
            <!-- Errand Header -->
            <div class="errand-header">
              <div class="errand-title-section">
                <h4 class="errand-title">{{ errand.title }}</h4>
                <span class="errand-id">{{ errand.number }}</span>
              </div>
              <button class="action-btn details-btn" @click="goToErrandDetails(errand.id)">
                → Szczegóły
              </button>
            </div>

            <!-- Errand Information -->
            <div class="errand-info">
              <div class="info-row">
                <span class="info-label">Status:</span>
                <span class="info-value">{{ errand.status }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Instytucja:</span>
                <span class="info-value">{{ errand.institution }}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Ostatnia modyfikacja:</span>
                <span class="info-value">{{ formatDate(errand.modifiedDate) }}</span>
              </div>
            </div>

            <!-- Progress Bar -->
            <div class="errand-progress-wrapper">
              <div class="progress-label">
                <span>Postęp</span>
                <span>{{ errand.progress }}%</span>
              </div>
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: errand.progress + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import router from '@/router'
import { ref, computed } from 'vue'

// Colorblind mode state
const isColorblindMode = ref(false)

// Dark mode state
const isDarkMode = ref(false)

// Current logged in user
const currentUser = ref({
  name: 'Dr. Jan Kowalski',
  role: 'Komisja legislacyjna',
  userId: 'user-001'
})

// Sample action items (items awaiting user's decision)
const actionItemsData = ref([
  {
    id: 1,
    title: 'Ustawa o zmianie ustawy o ochronie danych osobowych',
    number: 'UD-2024-001',
    currentStage: 'Komisja legislacyjna',
    initiative: 'Rada Ministrów',
    tags: ['#ochrona-danych', '#privacy', '#RODO'],
    date: '2024-12-01',
    description: 'Projekt wprowadza zmiany w zakresie przetwarzania danych osobowych w administracji publicznej.',
    addedBy: 'Anna Nowak (Urzędnik)',
    priority: 'high'
  },
  {
    id: 3,
    title: 'Ustawa o odnawialnych źródłach energii',
    number: 'UD-2024-002',
    currentStage: 'Komisja legislacyjna',
    initiative: 'Grupa posłów (150 podpisów)',
    tags: ['#energia', '#OZE', '#klimat'],
    date: '2024-11-20',
    description: 'Reforma systemu wsparcia dla energii odnawialnej.',
    addedBy: 'Piotr Kowalski (Urzędnik)',
    priority: 'medium'
  },
  {
    id: 4,
    title: 'Ustawa o zmianach w systemie edukacji',
    number: 'UD-2024-003',
    initiative: 'Ministerstwo Edukacji',
    tags: ['#edukacja', '#reforma', '#szkoła'],
    date: '2024-11-15',
    description: 'Modernizacja systemu edukacji publicznej.',
    addedBy: 'Maria Lewandowska (Urzędnik)',
    priority: 'low',
    currentStage: 'Komisja legislacyjna'
  }
])

// All items (for statistics)
const allItems = ref([
  {
    id: 1,
    stage: 'Wstępne opracowanie',
    tab: 'Projekty'
  },
  {
    id: 2,
    stage: 'Komisja legislacyjna',
    tab: 'Projekty'
  },
  {
    id: 3,
    stage: 'Sejm - pierwsza lektura',
    tab: 'Bieżące'
  },
  {
    id: 4,
    stage: 'Komisja sejmowa',
    tab: 'Bieżące'
  },
  {
    id: 5,
    stage: 'Sejm - druga lektura',
    tab: 'Bieżące'
  },
  {
    id: 6,
    stage: 'Senat',
    tab: 'Zatwierdzone'
  }
])

// Calculate statistics (exclude last stage)
const itemStats = computed(() => {
  const stageColors = {
    'Wstępne opracowanie': { gradient: 'linear-gradient(135deg, #4CAF50, #81C784)', bg: '#e8f5e9', text: '#2e7d32' },
    'Komisja legislacyjna': { gradient: 'linear-gradient(135deg, #2196F3, #64B5F6)', bg: '#e3f2fd', text: '#1565c0' },
    'Sejm - pierwsza lektura': { gradient: 'linear-gradient(135deg, #FF9800, #FFB74D)', bg: '#fff3e0', text: '#e65100' },
    'Komisja sejmowa': { gradient: 'linear-gradient(135deg, #9C27B0, #BA68C8)', bg: '#f3e5f5', text: '#6a1b9a' },
    'Sejm - druga lektura': { gradient: 'linear-gradient(135deg, #F44336, #EF5350)', bg: '#ffebee', text: '#c62828' }
  }

  return ['Wstępne opracowanie', 'Komisja legislacyjna', 'Sejm - pierwsza lektura', 'Komisja sejmowa', 'Sejm - druga lektura'].map(stage => {
    // In real app, count actual items in database
    const counts = {
      'Wstępne opracowanie': 5,
      'Komisja legislacyjna': 8,
      'Sejm - pierwsza lektura': 3,
      'Komisja sejmowa': 2,
      'Sejm - druga lektura': 1
    }

    return {
      stage: stage,
      count: counts[stage] || 0,
      ...stageColors[stage]
    }
  })
})

// Action items for current user
const actionItems = computed(() => {
  return actionItemsData.value
})

// Sample administrative errands data
const administrativeErrandsData = ref([
  {
    id: 101,
    number: 'PAR-2024-001',
    title: 'Wniosek o wydanie paszportu',
    institution: 'Urząd Miasta Warszawa',
    status: 'W trakcie przetwarzania',
    modifiedDate: '2024-12-10',
    progress: 45
  },
  {
    id: 102,
    number: 'PAR-2024-002',
    title: 'Zmiana danych w ewidencji mieszkańców',
    institution: 'Urząd Gminy Piaseczno',
    status: 'Oczekuje dokumentów',
    modifiedDate: '2024-12-05',
    progress: 20
  },
  {
    id: 103,
    number: 'PAR-2024-003',
    title: 'Zaświadczenie o niezaleganiu z podatkami',
    institution: 'Urząd Skarbowy Warszawa',
    status: 'Gotowe do odbioru',
    modifiedDate: '2024-12-12',
    progress: 100
  },
  {
    id: 104,
    number: 'PAR-2024-004',
    title: 'Prawo jazdy - przedłużenie ważności',
    institution: 'Wydział Transportu Urzędu Miasta',
    status: 'W trakcie przetwarzania',
    modifiedDate: '2024-12-08',
    progress: 65
  }
])

// Administrative errands for current user
const administrativeErrands = computed(() => {
  return administrativeErrandsData.value
})

// Helper functions
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('pl-PL', options)
}

const acceptItem = (itemId) => {
  console.log(`Item ${itemId} accepted`)
  alert(`Projekt ${itemId} został zaakceptowany`)
  // Remove from list
  const index = actionItemsData.value.findIndex(item => item.id === itemId)
  if (index > -1) {
    actionItemsData.value.splice(index, 1)
  }
}

const cancelItem = (itemId) => {
  console.log(`Item ${itemId} cancelled`)
  alert(`Projekt ${itemId} został odrzucony`)
  // Remove from list
  const index = actionItemsData.value.findIndex(item => item.id === itemId)
  if (index > -1) {
    actionItemsData.value.splice(index, 1)
  }
}

const goToDetails = (itemId) => {
  console.log(`Navigate to details for item ${itemId}`)
  // Navigate to detail view
  router.push(`/item/${itemId}`)
}

const goToErrandDetails = (errandId) => {
  console.log(`Navigate to details for errand ${errandId}`)
  // Navigate to errand detail view
  router.push(`/errand/${errandId}`)
}

const logout = () => {
  console.log('User logged out')
  alert('Wylogowano pomyślnie')
  // In real app, clear session and redirect to login
  window.location.href = '/login'
}

const toggleColorblindMode = () => {
  isColorblindMode.value = !isColorblindMode.value
  if (isColorblindMode.value) {
    document.documentElement.classList.add('colorblind-mode')
  } else {
    document.documentElement.classList.remove('colorblind-mode')
  }
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark-mode')
  } else {
    document.documentElement.classList.remove('dark-mode')
  }
}
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.panel-container {
  min-height: 100vh;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
}

/* Top Navigation Bar */
.top-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background-color: white;
  font-family: "Times New Roman", Times, serif;
  border-bottom: 2px solid #DC143C;
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.nav-left {
  flex: 0 0 auto;
}

.app-title {
  margin: 0;
  font-size: 24px;
  font-family: Times New Roman;
  font-weight: 700;
  color: #333;
}

.nav-center {
  flex: 1;
  text-align: center;
}

.connection-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #ffe8e8;
  color: #c62828;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 20px;
  flex: 0 0 auto;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-align: right;
}

.user-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.user-role {
  font-size: 12px;
  color: #999;
}

.logout-btn {
  padding: 10px 20px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #d32f2f;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.3);
}

/* Colorblind Mode Button */
.colorblind-mode-btn {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.colorblind-mode-btn:hover {
  background-color: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);

  /* Dark Mode Button */
  .dark-mode-btn {
    padding: 10px 20px;
    background-color: black;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .dark-mode-btn:hover {
    background-color: #555555;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(51, 51, 51, 0.3);
  }

  /* Contrast icon styling */
  .contrast-icon {
    font-size: 18px;
    font-weight: bold;
    letter-spacing: 2px;
  }

  /* When dark mode is active, highlight the icon */
  .dark-mode-btn.active .contrast-icon {
    color: #FFFF00;
    background: rgba(255, 255, 0, 0.2);
    padding: 2px 6px;
    border-radius: 3px;
  }
}

/* Colorblind Mode Palette */
:root.colorblind-mode {
  --color-primary: #0173B2;
  --color-accent: #DE8F05;
  --color-danger: #CC78BC;
  --color-success: #CA9161;
  --color-info: #29335C;
}

/* Disable colorblind mode for these tiles - keep black background */
:root.dark-mode.colorblind-mode .stat-card {
  background: #000000 !important;
  color: #FFFF00 !important;
}

/* Colorblind mode only (without dark mode) */
:root.colorblind-mode .stat-card:nth-child(1) {
  background: linear-gradient(135deg, #0173B2, #56CCEF) !important;
}

:root.colorblind-mode .stat-card:nth-child(2) {
  background: linear-gradient(135deg, #DE8F05, #F4B860) !important;
}

:root.colorblind-mode .stat-card:nth-child(3) {
  background: linear-gradient(135deg, #CC78BC, #E8C5E0) !important;
}

:root.colorblind-mode .stat-card:nth-child(4) {
  background: linear-gradient(135deg, #CA9161, #E5B8A2) !important;
}

:root.colorblind-mode .stat-card:nth-child(5) {
  background: linear-gradient(135deg, #29335C, #5E548E) !important;
}

:root.colorblind-mode .accept-btn {
  border-color: #0173B2;
  color: #0173B2;
  background-color: #E8F4F8;
}

:root.colorblind-mode .accept-btn:hover {
  background-color: #CCE5F0;
  border-color: #0173B2;
}

:root.colorblind-mode .cancel-btn {
  border-color: #CC78BC;
  color: #CC78BC;
  background-color: #F3E5F0;
}

:root.colorblind-mode .cancel-btn:hover {
  background-color: #E8D0E5;
  border-color: #CC78BC;
}

:root.colorblind-mode .details-btn {
  border-color: #DE8F05;
  color: #DE8F05;
  background-color: #FEF5E8;
}

:root.colorblind-mode .details-btn:hover {
  background-color: #FFF0D0;
  border-color: #DE8F05;
}

:root.colorblind-mode .priority-high {
  background-color: #F3E5F0;
  color: #CC78BC;
}

:root.colorblind-mode .priority-medium {
  background-color: #FEF5E8;
  color: #DE8F05;
}

:root.colorblind-mode .priority-low {
  background-color: #E8F4F8;
  color: #0173B2;
}

:root.colorblind-mode .tag {
  background-color: #E8F4F8;
  color: #0173B2;
}

:root.colorblind-mode .connection-status {

  /* Dark Mode Palette */
  :root.dark-mode {
    --bg-primary: #1a1a1a;
    --bg-secondary: #2d2d2d;
    --text-primary: #e0e0e0;
    --text-secondary: #b0b0b0;
    --border-color: #404040;
  }

  :root.dark-mode .panel-container {
    background-color: var(--bg-primary);
  }

  :root.dark-mode .top-nav {
    background-color: var(--bg-secondary);
    border-bottom-color: #8B0000;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 1000 !important;
  }

  :root.dark-mode .app-title {
    color: var(--text-primary);
  }

  :root.dark-mode .connection-status {
    background-color: #000000 !important;
    color: #FFFF00 !important;
  }

  :root.dark-mode.colorblind-mode .connection-status {
    background-color: #000000 !important;
    color: #FFFF00 !important;
  }

  :root.dark-mode .user-name {
    color: var(--text-primary);
  }

  :root.dark-mode .user-role {
    color: var(--text-secondary);
  }

  :root.dark-mode .statistics-section,
  :root.dark-mode .action-items-section {
    background-color: var(--bg-secondary);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  :root.dark-mode .statistics-section h3,
  :root.dark-mode .action-items-section h3 {
    color: var(--text-primary);
  }

  :root.dark-mode .stat-card {
    background-image: none !important;
    background-color: #000000 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }

  :root.dark-mode .action-item-card {
    border-color: var(--border-color);
    background-color: var(--bg-secondary);
  }

  :root.dark-mode .action-item-card:hover {
    border-color: #4CAF50;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  :root.dark-mode .item-title {
    color: var(--text-primary);
  }

  :root.dark-mode .item-number {
    background-color: #2a4a2a;
    color: #90ee90;
  }

  :root.dark-mode .action-btn {
    /* background-color: var(--bg-secondary); */
    color: var(--text-primary);
    border-color: var(--border-color);
  }

  :root.dark-mode .accept-btn {
    border-color: #4CAF50;
    color: #90ee90;
    /* background-color: black; */
  }

  :root.dark-mode .cancel-btn {
    border-color: #f44336;
    color: #ff6b6b;
    /* background-color: black; */
  }

  :root.dark-mode .details-btn {
    border-color: #1976d2;
    color: #64B5F6;
    /* background-color: black; */
  }

  :root.dark-mode .item-info {
    border-top-color: var(--border-color);
    border-bottom-color: var(--border-color);
  }

  :root.dark-mode .info-label {
    color: var(--text-secondary);
  }

  :root.dark-mode .info-value {
    color: var(--text-primary);
  }

  :root.dark-mode .item-description {
    color: var(--text-secondary);
  }

  :root.dark-mode .tag {
    background-color: #1a3a52;
    color: #64B5F6;
  }

  :root.dark-mode .item-footer {
    border-top-color: var(--border-color);
    color: var(--text-secondary);
  }

  :root.dark-mode .priority {
    color: white;
    background-color: black;
  }

  :root.dark-mode .priority-high {
    background-color: black;
    color: #ff6b6b;
  }

  :root.dark-mode .priority-medium {
    background-color: black;
    color: #ffb347;
  }

  :root.dark-mode .priority-low {
    background-color: black;
    color: #90ee90;
  }

  :root.dark-mode .no-items {
    color: var(--text-secondary);
  }

  background-color: #F3E5F0;
  color: #CC78BC;
}

/* Panel Content */
.panel-content {
  flex: 1;
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  margin-top: 80px;
}

/* Statistics Section */
.statistics-section {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.statistics-section h3 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.stat-card {
  background-size: cover;
  background-position: center;
  color: white;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(76, 175, 80, 0.4);
}

.stat-number {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  font-weight: 600;
  text-align: center;
  line-height: 1.3;
}

/* Action Items Section */
.action-items-section {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.action-items-section h3 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.no-items {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 16px;
}

.action-items-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.action-item-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

.action-item-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #4CAF50;
}

/* Item Header Row */
.item-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  gap: 15px;
}

.item-title-section {
  display: flex;
  gap: 10px;
  align-items: center;
  flex: 1;
}

.item-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  flex: 1;
}

.item-number {
  background-color: #e8f5e9;
  color: #2e7d32;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

/* Item Actions */
.item-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.action-btn {
  padding: 8px 14px;
  border: 2px solid #e0e0e0;
  background-color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.accept-btn {
  border-color: #4CAF50;
  color: #2e7d32;
  background-color: #e8f5e9;
}

.accept-btn:hover {
  background-color: #ffcdd2;
  border-color: #c62828;
}

.cancel-btn {
  border-color: #f44336;
  color: #c62828;
  background-color: #ffebee;
}

.cancel-btn:hover {
  background-color: #ffcdd2;
  border-color: #c62828;
}

.details-btn {
  border-color: #1976d2;
  color: #1565c0;
  background-color: #e3f2fd;
}

.details-btn:hover {
  background-color: #bbdefb;
  border-color: #1565c0;
}

/* Item Information */
.item-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
  padding: 15px 0;
  border-top: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
}

.info-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 12px;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
}

.info-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

/* Item Description */
.item-description {
  margin: 15px 0;
  color: #666;
  font-size: 14px;
  line-height: 1.5;
}

/* Item Tags */
.item-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 12px 0;
}

.tag {
  display: inline-block;
  background-color: #e3f2fd;
  color: #1976d2;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

/* Item Footer */
.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #e0e0e0;
  font-size: 12px;
}

.added-by {
  color: #999;
}

.priority {
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 4px;
}

.priority-high {
  background-color: #ffebee;
  color: #c62828;
}

.priority-medium {
  background-color: #fff3e0;
  color: #e65100;
}

.priority-low {
  background-color: #e8f5e9;
  color: #2e7d32;
}

/* Responsive */
@media (max-width: 1024px) {
  .panel-content {
    padding: 20px;
  }

  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }
}

@media (max-width: 768px) {
  .top-nav {
    flex-wrap: wrap;
    gap: 15px;
    padding: 12px 15px;
  }

  .nav-left,
  .nav-center,
  .nav-right {
    flex: 1 1 100%;
    justify-content: center;
  }

  .app-title {
    font-size: 20px;
  }

  .connection-status {
    font-size: 12px;
    padding: 6px 12px;
  }

  .user-info {
    text-align: center;
  }

  .logout-btn {
    padding: 8px 16px;
    font-size: 12px;
  }

  .item-header-row {
    flex-direction: column;
  }

  .item-actions {
    justify-content: flex-start;
  }

  .action-btn {
    padding: 6px 12px;
    font-size: 12px;
  }

  .item-info {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .panel-content {
    padding: 15px;
  }

  .app-title {
    font-size: 18px;
  }

  .user-name {
    font-size: 14px;
  }

  .action-items-list {
    gap: 15px;
  }

  .action-item-card {
    padding: 15px;
  }

  .item-title {
    font-size: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}

/* Administrative Errands Section */
.administrative-errands-section {
  background-color: white;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.administrative-errands-section h3 {
  margin: 0 0 20px 0;
  font-size: 20px;
  color: #333;
  font-weight: 600;
}

.errands-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.errand-card {
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 15px;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

.errand-card:hover {
  box-shadow: 0 4px 12px rgba(220, 20, 60, 0.15);
  border-color: #DC143C;
  background-color: white;
}

.errand-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
  gap: 10px;
}

.errand-title-section {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.errand-title {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.errand-id {
  font-size: 12px;
  font-weight: 600;
  color: #999;
  background-color: #f0f0f0;
  padding: 2px 8px;
  border-radius: 3px;
}

.errand-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.errand-info .info-row {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.errand-info .info-label {
  font-size: 12px;
  font-weight: 600;
  color: #999;
  text-transform: uppercase;
}

.errand-info .info-value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

.errand-progress-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #666;
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: #e0e0e0;
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #DC143C, #FF6B6B);
  border-radius: 3px;
  transition: width 0.3s ease;
}

/* Dark Mode Styles for Administrative Errands */
:root.dark-mode .administrative-errands-section {
  background-color: black;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

:root.dark-mode .administrative-errands-section h3 {
  color: var(--text-primary);
}

:root.dark-mode .errand-card {
  background-color: black;
  border-color: #222;
}

:root.dark-mode .errand-card:hover {
  background-color: black;
  box-shadow: 0 4px 12px rgba(220, 20, 60, 0.25);
}

:root.dark-mode .errand-title {
  color: var(--text-primary);
}

:root.dark-mode .errand-id {
  background-color: black;
  color: #999;
}

:root.dark-mode .errand-info {
  border-bottom-color: #444;
}

:root.dark-mode .errand-info .info-label {
  color: var(--text-secondary);
}

:root.dark-mode .errand-info .info-value {
  color: var(--text-primary);
}

:root.dark-mode .progress-label {
  color: var(--text-secondary);
}

:root.dark-mode .progress-bar {
  background-color: black;
}

:root.dark-mode .action-btn {
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  border-color: var(--border-color);
}

:root.dark-mode .accept-btn {
  /* border-color: #4CAF50;
  color: #90ee90; */
  background-color: black;
}

:root.dark-mode .cancel-btn {
  /* border-color: #f44336;
  color: #ff6b6b; */
  background-color: black;
}

:root.dark-mode .details-btn {
  /* border-color: #1976d2;
  color: #64B5F6; */
  background-color: black;
}

/* Dark mode: hide gradients and use black background for all stat cards */
:root.dark-mode .stat-card {
  background-image: none !important;
  background-color: #000000 !important;
}

:root.dark-mode .priority {
  color: #FFFF00;
  background-color: black;
}

:root.dark-mode .priority-high {
  background-color: black;
}

:root.dark-mode .priority-medium {
  background-color: black;
}

:root.dark-mode .priority-low {
  background-color: black;
}

:root.dark-mode * {
}

@media (max-width: 768px) {
  .errand-header {
    flex-direction: column;
  }

  .errand-details-btn {
    width: 100%;
  }

  .errand-info {
    grid-template-columns: 1fr;
  }
}
</style>
