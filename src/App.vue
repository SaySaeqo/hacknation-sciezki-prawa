<script setup>
import { ref, onMounted } from 'vue'

// cookie consent: 'accepted' | 'rejected' | undefined
const showCookieBanner = ref(false)

const COOKIE_KEY = 'cookieConsent'

onMounted(() => {
  try {
    const stored = localStorage.getItem(COOKIE_KEY)
    if (!stored) {
      // first visit -> show banner
      showCookieBanner.value = true
    }
  } catch (e) {
    // if localStorage unavailable, still show banner
    showCookieBanner.value = true
  }
})

const acceptCookies = () => {
  try { localStorage.setItem(COOKIE_KEY, 'accepted') } catch (e) {}
  showCookieBanner.value = false
}

const rejectCookies = () => {
  try { localStorage.setItem(COOKIE_KEY, 'rejected') } catch (e) {}
  // Redirect user away from site when they reject cookies
  // Use a neutral external page; change if you prefer a different URL
  window.location.href = 'https://www.google.com'
}
</script>

<template>
  <router-view />

  <div v-if="showCookieBanner" class="cookie-banner" role="dialog" aria-live="polite">
    <div class="cookie-content">
      <div class="cookie-text">
        Ta strona używa plików cookies w celu poprawy działania serwisu. Akceptując zgadzasz się na użycie
        cookies.
      </div>
      <div class="cookie-actions">
        <button class="cookie-accept" @click="acceptCookies">Akceptuj</button>
        <button class="cookie-reject" @click="rejectCookies">Odrzuć</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cookie-banner {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 18px;
  display: flex;
  justify-content: center;
  pointer-events: none;
  z-index: 2000;
}
.cookie-content {
  pointer-events: auto;
  max-width: 980px;
  width: calc(100% - 32px);
  background: rgba(255,255,255,0.96);
  color: #111;
  border-radius: 8px;
  padding: 14px 16px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.15);
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}
.cookie-text { flex: 1; font-size: 14px }
.cookie-actions { display: flex; gap: 8px }
.cookie-accept {
  background-color: #1976d2;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.cookie-accept:hover { background-color: #1565c0 }
.cookie-reject {
  background-color: transparent;
  color: #c62828;
  border: 2px solid #c62828;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.cookie-reject:hover { background-color: rgba(198,40,40,0.06) }

/* Dark mode adjustments for banner (if dark mode active globally) */
:root.dark-mode .cookie-content {
  background: rgba(255,255,255,0.03);
  color: #e6e6e6;
}

</style>
