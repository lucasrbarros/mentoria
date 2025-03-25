// Aplicamos o tema imediatamente para evitar flash de tema incorreto
(function() {
    // Obtém o tema das preferências do usuário
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Aplica o tema ao documento imediatamente
    document.documentElement.setAttribute('data-theme', savedTheme);
})();

// Função para alternar o tema
function toggleTheme() {
    // Verifica o tema atual
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Alterna para o tema oposto
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    // Armazena a preferência do usuário
    localStorage.setItem('theme', newTheme);
    
    // Aplica o tema ao documento
    document.documentElement.setAttribute('data-theme', newTheme);
    
    // Atualiza o estado do switch
    const themeSwitch = document.getElementById('themeSwitch');
    if (themeSwitch) {
        themeSwitch.checked = newTheme === 'dark';
    }
    
    // Atualiza o ícone
    updateThemeIcon(newTheme);
}

// Função para atualizar o ícone de acordo com o tema
function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('themeIcon');
    if (themeIcon) {
        if (theme === 'dark') {
            themeIcon.classList.remove('bi-sun');
            themeIcon.classList.add('bi-moon');
        } else {
            themeIcon.classList.remove('bi-moon');
            themeIcon.classList.add('bi-sun');
        }
    }
}

// Função para aplicar o tema salvo
function applyTheme() {
    // Obtém o tema das preferências do usuário
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Aplica o tema ao documento
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    // Atualiza o estado do switch
    const themeSwitch = document.getElementById('themeSwitch');
    if (themeSwitch) {
        themeSwitch.checked = savedTheme === 'dark';
    }
    
    // Atualiza o ícone
    updateThemeIcon(savedTheme);
}

// Aplicar o tema quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    applyTheme();
    
    // Adiciona evento de clique ao botão de alternar tema
    const themeSwitch = document.getElementById('themeSwitch');
    if (themeSwitch) {
        themeSwitch.addEventListener('change', toggleTheme);
    }
}); 