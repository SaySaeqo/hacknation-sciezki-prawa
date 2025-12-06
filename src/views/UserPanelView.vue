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
          <div v-for="stat in itemStats" :key="stat.stage" class="stat-card" :style="{ backgroundImage: stat.gradient }">
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
                {{ item.priority === 'high' ? '⚠ Wysoki priorytet' : item.priority === 'medium' ? '→ Średni priorytet' : '✓ Niski priorytet' }}
              </span>
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

const logout = () => {
  console.log('User logged out')
  alert('Wylogowano pomyślnie')
  // In real app, clear session and redirect to login
  window.location.href = '/login'
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
  background-color: white;
  border-bottom: 2px solid #DC143C;
  padding: 15px 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-left {
  flex: 0 0 auto;
}

.app-title {
  margin: 0;
  font-size: 24px;
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

/* Panel Content */
.panel-content {
  flex: 1;
  padding: 30px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
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
</style>
