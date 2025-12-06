<template>
    <div class="login-container">
        <!-- Header -->
        <header class="login-header">
            <div class="logo-section">
                <div class="logo">
                    <!-- <span class="eagle-icon">🦅</span> -->
                    <span class="logo-text">Login Page</span>
                </div>
            </div>
            <div class="language-selector">
                <button class="language-btn">
                    🌐 Język polski ▼
                </button>
            </div>
        </header>

        <!-- Main Content -->
        <div class="main-content">
            <!-- Left Panel - Login Options -->
            <div class="login-panel">
                <h1 class="login-title">Zaloguj się do usługi</h1>
                <p class="login-subtitle">Ostatnio wybrany sposób logowania</p>

                <!-- Login Options -->
                <div class="login-options">
                    <!-- Profil zaufany -->
                    <button class="login-option" @click="selectLoginMethod('profil')">
                        <div class="option-icon profile-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z" />
                            </svg>
                        </div>
                        <div class="option-content">
                            <h3 class="option-title">Profil zaufany</h3>
                            <p class="option-description">Użyj loginu i hasła lub bankowości elektronicznej.</p>
                        </div>
                        <span class="option-arrow">›</span>
                    </button>

                    <!-- Remaining login methods label -->
                    <p class="remaining-methods-label">Pozostałe sposoby logowania</p>

                    <!-- Aplikacja mObywatel -->
                    <button class="login-option" @click="selectLoginMethod('mobywatel')">
                        <div class="option-icon app-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z" />
                            </svg>
                        </div>
                        <div class="option-content">
                            <h3 class="option-title">
                                Aplikacja mObywatel
                                <span class="recommended-badge">Polecany</span>
                            </h3>
                            <p class="option-description">Skanuj kod QR za pomocą aplikacji mObywatel.</p>
                        </div>
                        <span class="option-arrow">›</span>
                    </button>

                    <!-- Bankowość elektroniczna -->
                    <button class="login-option" @click="selectLoginMethod('bank')">
                        <div class="option-icon bank-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M4 10v7h3v-7H4zm6 0v7h3v-7h-3zM2 22h19v-3H2v3zm14-12v7h3v-7h-3zm-4.5-9L2 6v2h19V6l-9.5-5z" />
                            </svg>
                        </div>
                        <div class="option-content">
                            <h3 class="option-title">Bankowość elektroniczna</h3>
                            <p class="option-description">Zaloguj się za pomocą swojego banku.</p>
                        </div>
                        <span class="option-arrow">›</span>
                    </button>

                    <!-- E-dowód -->
                    <button class="login-option" @click="selectLoginMethod('edowod')">
                        <div class="option-icon id-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M20 4H4c-1.11 0-1.99.89-1.99 2L2 18c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V6c0-1.11-.89-2-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z" />
                            </svg>
                        </div>
                        <div class="option-content">
                            <h3 class="option-title">E-dowód</h3>
                            <p class="option-description">Użyj dowodu osobistego z warstwą elektroniczną i smartfona lub
                                czytnika NFC.</p>
                        </div>
                        <span class="option-arrow">›</span>
                    </button>

                    <!-- Use eID -->
                    <button class="login-option" @click="selectLoginMethod('eid')">
                        <div class="option-icon eid-icon">
                            <svg viewBox="0 0 24 24" fill="currentColor">
                                <path
                                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
                            </svg>
                        </div>
                        <div class="option-content">
                            <h3 class="option-title">Use eID</h3>
                            <p class="option-description">Use your National eID to access online services.</p>
                        </div>
                        <span class="option-arrow">›</span>
                    </button>
                </div>

                <!-- Additional Info Link -->
                <a href="#" class="info-link">
                    <span class="info-icon">ℹ</span>
                    Dowiedz się więcej o sposobach logowania
                </a>
            </div>

            <!-- Right Panel - mObywatel Promo -->
            <div class="promo-panel">
                <div class="promo-content">
                    <div class="promo-logo">
                        <span class="eagle-badge">🦅</span>
                        <span class="mobywatel-text">mObywatel</span>
                    </div>
                    <div class="promo-image">
                        <div class="phone-mockup">
                            📱
                        </div>
                    </div>
                    <h2 class="promo-title">Zamień kody SMS na powiadomienia w aplikacji mObywatel</h2>
                    <p class="promo-description">
                        Potwierdzi logowanie do profilu zaufanego, zmiany na koncie i podpisywanie dokumentów jednym
                        przyciskiem w telefonie - wygodnie i bezpiecznie.
                    </p>
                    <button class="promo-button">Dowiedz się więcej</button>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="login-footer">
            <a href="#">Polityka cookies</a>
            <a href="#">Klauzula informacyjna</a>
            <a href="#">Deklaracja dostępności</a>
            <a href="#">Kontakt</a>
        </footer>
    </div>
</template>

<script setup>
import router from '@/router';

const selectLoginMethod = (method) => {
    console.log('Selected login method:', method)
    router.push('/user-panel');
}
</script>

<style scoped>
* {
    box-sizing: border-box;
}

.login-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background-color: #f5f5f5;
}

/* Header */
.login-header {
    background-color: white;
    border-bottom: 1px solid #e0e0e0;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo-section {
    display: flex;
    align-items: center;
}

.logo {
    display: flex;
    align-items: center;
    gap: 8px;
}

.eagle-icon {
    font-size: 24px;
}

.logo-text {
    font-size: 24px;
    font-weight: 700;
    color: #333;
}

.language-selector {
    display: flex;
}

.language-btn {
    padding: 8px 16px;
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    color: #0052B4;
    font-weight: 500;
    transition: all 0.3s ease;
}

.language-btn:hover {
    background-color: #f5f5f5;
}

/* Main Content */
.main-content {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    max-width: 1400px;
    width: 100%;
    margin: 0 auto;
}

/* Login Panel */
.login-panel {
    background-color: white;
    padding: 40px 50px;
    overflow-y: auto;
}

.login-title {
    font-size: 32px;
    font-weight: 700;
    color: #333;
    margin: 0 0 10px 0;
}

.login-subtitle {
    font-size: 16px;
    color: #666;
    margin: 0 0 30px 0;
}

.login-options {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.remaining-methods-label {
    font-size: 14px;
    color: #666;
    margin: 20px 0 10px 0;
    font-weight: 500;
}

.login-option {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 20px;
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: left;
    width: 100%;
}

.login-option:hover {
    border-color: #0052B4;
    box-shadow: 0 2px 8px rgba(0, 82, 180, 0.15);
}

.option-icon {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.option-icon svg {
    width: 28px;
    height: 28px;
}

.profile-icon {
    background-color: #E3F2FD;
    color: #0052B4;
}

.app-icon {
    background-color: #E3F2FD;
    color: #0052B4;
}

.bank-icon {
    background-color: #E8EAF6;
    color: #3F51B5;
}

.id-icon {
    background-color: #F3E5F5;
    color: #9C27B0;
}

.eid-icon {
    background-color: #E0F2F1;
    color: #009688;
}

.option-content {
    flex: 1;
}

.option-title {
    font-size: 16px;
    font-weight: 600;
    color: #333;
    margin: 0 0 5px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.recommended-badge {
    background-color: #0052B4;
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 11px;
    font-weight: 600;
}

.option-description {
    font-size: 14px;
    color: #666;
    margin: 0;
    line-height: 1.4;
}

.option-arrow {
    font-size: 28px;
    color: #999;
    flex-shrink: 0;
}

.info-link {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-top: 30px;
    color: #0052B4;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
}

.info-link:hover {
    text-decoration: underline;
}

.info-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    border: 2px solid #0052B4;
    border-radius: 50%;
    font-size: 12px;
    font-weight: 700;
}

/* Promo Panel */
.promo-panel {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    padding: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.promo-panel::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 50%;
}

.promo-content {
    position: relative;
    z-index: 1;
    text-align: center;
    color: white;
    max-width: 500px;
}

.promo-logo {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background-color: #DC143C;
    padding: 8px 16px;
    border-radius: 8px;
    margin-bottom: 30px;
}

.eagle-badge {
    font-size: 20px;
}

.mobywatel-text {
    font-size: 18px;
    font-weight: 700;
}

.promo-image {
    margin: 30px 0;
}

.phone-mockup {
    font-size: 120px;
    opacity: 0.9;
}

.promo-title {
    font-size: 28px;
    font-weight: 700;
    margin: 0 0 20px 0;
    line-height: 1.3;
}

.promo-description {
    font-size: 16px;
    line-height: 1.6;
    margin: 0 0 30px 0;
    opacity: 0.9;
}

.promo-button {
    padding: 12px 32px;
    background-color: white;
    color: #0052B4;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.promo-button:hover {
    background-color: #f5f5f5;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Footer */
.login-footer {
    background-color: white;
    border-top: 1px solid #e0e0e0;
    padding: 20px 30px;
    display: flex;
    gap: 30px;
    flex-wrap: wrap;
    justify-content: center;
}

.login-footer a {
    color: #666;
    text-decoration: none;
    font-size: 14px;
}

.login-footer a:hover {
    color: #0052B4;
    text-decoration: underline;
}

/* Responsive */
@media (max-width: 1024px) {
    .main-content {
        grid-template-columns: 1fr;
    }

    .promo-panel {
        display: none;
    }

    .login-panel {
        padding: 30px 20px;
    }
}

@media (max-width: 768px) {
    .login-header {
        padding: 12px 20px;
    }

    .login-title {
        font-size: 24px;
    }

    .login-option {
        padding: 15px;
    }

    .option-icon {
        width: 40px;
        height: 40px;
    }

    .option-icon svg {
        width: 24px;
        height: 24px;
    }

    .login-footer {
        flex-direction: column;
        align-items: center;
        gap: 15px;
    }
}
</style>
