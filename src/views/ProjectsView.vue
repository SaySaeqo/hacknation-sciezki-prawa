<template>
  <div class="projects-container">
    <!-- Navigation Bar -->
    <nav class="navbar">
      <button 
        v-for="tab in tabs" 
        :key="tab"
        @click="activeTab = tab"
        :class="['nav-btn', { active: activeTab === tab }]"
      >
        {{ tab }}
      </button>
    </nav>

    <!-- Image Gallery Section -->
    <section class="image-gallery">
      <div 
        v-for="image in imageGallery" 
        :key="image.id"
        @click="activeTab = image.tab"
        class="image-card"
        :title="image.title"
      >
        <div class="image-placeholder">
          <img :src="image.src" :alt="image.title" class="gallery-image">
        </div>
        <p class="image-label">{{ image.title }}</p>
      </div>
    </section>

    <!-- Search Section -->
    <section class="search-section">
      <div class="search-bar-wrapper">
        <input 
          v-model="searchQuery" 
          type="text" 
          placeholder="Szukaj projektów..."
          class="search-input"
        >
        <button @click="showAdvancedSearch = !showAdvancedSearch" class="advanced-search-btn">
          {{ showAdvancedSearch ? '▼' : '▶' }} Zaawansowane wyszukiwanie
        </button>
      </div>

      <!-- Advanced Search (Hidden by default) -->
      <div v-if="showAdvancedSearch" class="advanced-search">
        <div class="search-field">
          <label for="search-title">Tytuł:</label>
          <input v-model="advancedSearch.title" id="search-title" type="text" placeholder="Szukaj po tytule">
        </div>
        <div class="search-field">
          <label for="search-tags">Tagi:</label>
          <input v-model="advancedSearch.tags" id="search-tags" type="text" placeholder="Szukaj po tagach (oddzielone przecinkami)">
        </div>
        <div class="search-field">
          <label for="search-initiative">Inicjatywa:</label>
          <input v-model="advancedSearch.initiative" id="search-initiative" type="text" placeholder="Szukaj po inicjatywie">
        </div>
        <button @click="clearAdvancedSearch" class="clear-btn">Wyczyść filtry</button>
      </div>
    </section>

    <!-- Items List -->
    <section class="items-section">
      <div v-if="filteredItems.length === 0" class="no-results">
        Brak projektów spełniających kryteria wyszukiwania
      </div>
      <div v-else class="items-list">
        <div 
          v-for="item in filteredItems" 
          :key="item.id" 
          class="item-card"
          @click="navigateToItem(item.id)"
        >
          <div class="item-header">
            <h3 class="item-title">{{ item.title }}</h3>
            <span class="item-number">{{ item.number }}</span>
          </div>

          <p class="item-description">{{ item.description }}</p>

          <div class="item-meta">
            <span class="item-date">📅 {{ formatDate(item.date) }}</span>
            <span class="item-initiative">👤 {{ item.initiative }}</span>
          </div>

          <!-- Progress bar for "Bieżące" tab -->
          <div v-if="activeTab === 'Bieżące'" class="progress-wrapper">
            <div class="progress-label">
              <span>Postęp</span>
              <span>{{ item.progress }}%</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: item.progress + '%' }"></div>
            </div>
          </div>

          <div class="item-tags">
            <span v-for="tag in item.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>

          <div class="item-footer">
            <span class="item-added-by">Dodane przez: {{ item.addedBy }}</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ore from '@/assets/ore.webp'
import wagon from '@/assets/wagon.webp'
import outsideOre from '@/assets/outside_ore.webp'
import router from '@/router'

// Tabs
const tabs = ref(['Projekty', 'Bieżące', 'Zatwierdzone'])
const activeTab = ref('Projekty')

// Image Gallery
const imageGallery = ref([
  {
    id: 1,
    title: 'Projekty',
    tab: 'Projekty',
    src: ore
  },
  {
    id: 2,
    title: 'Bieżące',
    tab: 'Bieżące',
    src: wagon
  },
  {
    id: 3,
    title: 'Zatwierdzone',
    tab: 'Zatwierdzone',
    src: outsideOre
  }
])

// Search
const searchQuery = ref('')
const showAdvancedSearch = ref(false)
const advancedSearch = ref({
  title: '',
  tags: '',
  initiative: ''
})

// Sample Data
const allItems = ref([
  {
    id: 1,
    title: 'Ustawa o zmianie ustawy o ochronie danych osobowych',
    number: 'UD-2024-001',
    initiative: 'Rada Ministrów',
    tags: ['#ochrona-danych', '#privacy', '#RODO'],
    date: '2024-12-01',
    description: 'Projekt wprowadza zmiany w zakresie przetwarzania danych osobowych w administracji publicznej.',
    addedBy: 'Anna Nowak (Urzędnik)',
    progress: 45,
    tab: 'Projekty'
  },
  {
    id: 2,
    title: 'Ustawa o wspieraniu małych i średnich przedsiębiorstw',
    number: 'UD-2024-007',
    initiative: 'Grupa posłów (180 podpisów)',
    tags: ['#gospodarka', '#MSP', '#podatki', '#przedsiębiorczość'],
    date: '2024-12-05',
    description: 'Wprowadzenie ulg podatkowych i uproszczeń administracyjnych dla firm zatrudniających do 50 osób.',
    addedBy: 'Marek Wiśniewski (Urzędnik)',
    progress: 30,
    tab: 'Projekty'
  },
  {
    id: 3,
    title: 'Ustawa o odnawialnych źródłach energii',
    number: 'UD-2024-002',
    initiative: 'Grupa posłów (150 podpisów)',
    tags: ['#energia', '#OZE', '#klimat'],
    date: '2024-11-20',
    description: 'Reforma systemu wsparcia dla energii odnawialnej.',
    addedBy: 'Piotr Kowalski (Urzędnik)',
    progress: 65,
    tab: 'Bieżące'
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
    progress: 80,
    tab: 'Bieżące'
  },
  {
    id: 5,
    title: 'Ustawa o ochronie środowiska',
    number: 'UD-2024-004',
    initiative: 'Grupa posłów (200 podpisów)',
    tags: ['#środowisko', '#ekologia', '#zielona-energia'],
    date: '2024-10-30',
    description: 'Wzmocnienie ochrony przyrody i zasobów naturalnych.',
    addedBy: 'Jan Nowak (Urzędnik)',
    progress: 100,
    tab: 'Zatwierdzone'
  },
  {
    id: 6,
    title: 'Ustawa o promocji turystyki',
    number: 'UD-2024-005',
    initiative: 'Ministerstwo Turystyki',
    tags: ['#turystyka', '#gospodarka', '#promocja'],
    date: '2024-10-20',
    description: 'Program wspierający rozwój turystyki wewnętrznej i zagranicznej.',
    addedBy: 'Anna Kowalska (Urzędnik)',
    progress: 100,
    tab: 'Zatwierdzone'
  }
])

// Filter items based on active tab and search
const filteredItems = computed(() => {
  let items = allItems.value.filter(item => item.tab === activeTab.value)

  // Apply basic search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    items = items.filter(item =>
      item.title.toLowerCase().includes(query) ||
      item.number.toLowerCase().includes(query)
    )
  }

  // Apply advanced search
  if (advancedSearch.value.title) {
    items = items.filter(item =>
      item.title.toLowerCase().includes(advancedSearch.value.title.toLowerCase())
    )
  }

  if (advancedSearch.value.tags) {
    const searchTags = advancedSearch.value.tags.split(',').map(t => t.trim().toLowerCase())
    items = items.filter(item =>
      searchTags.some(searchTag =>
        item.tags.some(tag => tag.toLowerCase().includes(searchTag))
      )
    )
  }

  if (advancedSearch.value.initiative) {
    items = items.filter(item =>
      item.initiative.toLowerCase().includes(advancedSearch.value.initiative.toLowerCase())
    )
  }

  return items
})

// Helper functions
const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' }
  return new Date(dateString).toLocaleDateString('pl-PL', options)
}

const clearAdvancedSearch = () => {
  advancedSearch.value = {
    title: '',
    tags: '',
    initiative: ''
  }
}

const navigateToItem = (itemId) => {
  // Navigate to item detail view
  // This will work once you set up the router
  router.push("/item/" + itemId)
}
</script>

<style scoped>
.projects-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* Navigation Bar */
.navbar {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  background-color: white;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-btn {
  padding: 10px 20px;
  border: 2px solid #e0e0e0;
  background-color: white;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  color: #333;
}

.nav-btn:hover {
  border-color: #DC143C;
  color: #DC143C;
}

.nav-btn.active {
  background-color: #DC143C;
  color: white;
  border-color: #DC143C;
}

/* Image Gallery */
.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.image-card {
  cursor: pointer;
  text-align: center;
  transition: transform 0.3s ease;
}

.image-card:hover {
  transform: scale(1.05);
}

.image-placeholder {
  width: 200px;
  height: 200px;
  margin: 0 auto;
  border-radius: 8px;
  overflow: hidden;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.gallery-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-label {
  margin-top: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

/* Search Section */
.search-section {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-bar-wrapper {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #DC143C;
}

.advanced-search-btn {
  padding: 12px 16px;
  background-color: #f0f0f0;
  border: 2px solid #e0e0e0;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  transition: all 0.3s ease;
}

.advanced-search-btn:hover {
  background-color: #e8e8e8;
  border-color: #DC143C;
}

/* Advanced Search */
.advanced-search {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
}

.search-field {
  display: flex;
  flex-direction: column;
}

.search-field label {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.search-field input {
  padding: 10px 12px;
  border: 2px solid #e0e0e0;
  border-radius: 4px;
  font-size: 14px;
  transition: border-color 0.3s ease;
}

.search-field input:focus {
  outline: none;
  border-color: #DC143C;
}

.clear-btn {
  padding: 10px 16px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.3s ease;
  align-self: flex-end;
}

.clear-btn:hover {
  background-color: #d32f2f;
}

/* Items Section */
.items-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.no-results {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-size: 16px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.item-card {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  background-color: #fafafa;
  transition: all 0.3s ease;
  text-decoration: none;
  cursor: pointer;
}

.item-card * {
  user-select: text;
  pointer-events: auto;
}

.item-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #DC143C;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 10px;
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
  margin-left: 10px;
}

.item-description {
  color: #666;
  font-size: 14px;
  margin: 10px 0;
  line-height: 1.5;
}

.item-meta {
  display: flex;
  gap: 20px;
  margin: 12px 0;
  font-size: 13px;
  color: #777;
}

.item-date,
.item-initiative {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

/* Progress Bar */
.progress-wrapper {
  margin: 15px 0;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #666;
  margin-bottom: 5px;
  font-weight: 500;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #DC143C, #FF6B6B);
  border-radius: 4px;
  transition: width 0.3s ease;
}

/* Tags */
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

.item-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #e0e0e0;
  font-size: 12px;
  color: #999;
}

/* Responsive */
@media (max-width: 768px) {
  .projects-container {
    padding: 10px;
  }

  .navbar {
    flex-wrap: wrap;
  }

  .image-gallery {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
  }

  .image-placeholder {
    width: 100%;
    height: 150px;
  }

  .search-bar-wrapper {
    flex-direction: column;
  }

  .item-header {
    flex-direction: column;
  }

  .item-number {
    margin-left: 0;
    margin-top: 10px;
  }

  .item-meta {
    flex-direction: column;
    gap: 8px;
  }

  .advanced-search {
    grid-template-columns: 1fr;
  }
}
</style>
