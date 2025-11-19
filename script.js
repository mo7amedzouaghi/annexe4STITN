// Charger les données depuis les fichiers JSON
let techData = {};

// Charger tous les fichiers JSON
Promise.all([
    fetch('html5.json').then(response => response.json()),
    fetch('css3.json').then(response => response.json()),
    fetch('javascript.json').then(response => response.json()),
    fetch('php.json').then(response => response.json()),
    fetch('sql.json').then(response => response.json())
])
.then(([html5Data, css3Data, jsData, phpData, sqlData]) => {
    // Assembler toutes les données
    techData = {
        'HTML5': html5Data,
        'CSS3': css3Data,
        'JavaScript': jsData,
        'PHP': phpData,
        'SQL': sqlData
    };
    // Initialiser le chat une fois les données chargées
    showWelcomeMessage();
})
.catch(error => {
    console.error('Erreur lors du chargement des données:', error);
    addMessage("Désolé, une erreur est survenue lors du chargement des données.", false);
});

// État du chatbot
const state = {
    currentTech: null,
    currentCategory: null,
    waitingForDefinition: false,
    searchTerm: ""
};

// Éléments DOM
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const restartButton = document.getElementById('restartButton');

// Fonctions utilitaires
function addMessage(text, isUser = false, isCode = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');
    
    if (isCode) {
        const codeDiv = document.createElement('div');
        codeDiv.classList.add('code-block');
        codeDiv.textContent = text;
        messageDiv.appendChild(codeDiv);
    } else {
        messageDiv.textContent = text;
    }
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showWelcomeMessage() {
    addMessage("Bienvenue dans le Chatbot Tech Web ! 🤖", false);
    addMessage("Sélectionnez une technologie pour voir ses catégories :", false);
    showTechOptions();
}

function showTechOptions() {
    const optionsDiv = document.createElement('div');
    optionsDiv.classList.add('options-container');
    
    Object.keys(techData).forEach(tech => {
        const button = document.createElement('button');
        button.classList.add('tech-option');
        button.textContent = tech;
        button.onclick = () => selectTech(tech);
        optionsDiv.appendChild(button);
    });
    
    chatContainer.appendChild(optionsDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function selectTech(tech) {
    state.currentTech = tech;
    state.currentCategory = null;
    addMessage(tech, true);
    
    addMessage(`Vous avez sélectionné ${tech}. Choisissez une catégorie pour voir la liste des éléments :`, false);
    showTechCategories();
}

function showTechCategories() {
    const categories = Object.keys(techData[state.currentTech]);
    const optionsDiv = document.createElement('div');
    optionsDiv.classList.add('options-container');
    
    categories.forEach(category => {
        const button = document.createElement('button');
        button.classList.add('tech-option');
        button.textContent = category;
        button.onclick = () => selectCategory(category);
        optionsDiv.appendChild(button);
    });
    
    chatContainer.appendChild(optionsDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function selectCategory(category) {
    state.currentCategory = category;
    addMessage(category, true);
    
    const items = techData[state.currentTech][category];
    let message = `Voici les éléments de la catégorie "${category}" en ${state.currentTech}:\n\n`;
    
    items.forEach((item, index) => {
        const key = Object.keys(item)[0];
        const name = item[key] || item.nom || item.attribut || item.événement;
        message += `${index + 1}. ${name}\n`;
    });
    
    addMessage(message, false);
    addMessage("Entrez le numéro d'un élément pour voir sa définition détaillée avec exemple d'utilisation.", false);
    addMessage("Tapez 'retour' pour choisir une autre catégorie ou 'menu' pour revenir au choix de technologie.", false);
}

function showDefinition(itemIndex) {
    const items = techData[state.currentTech][state.currentCategory];
    if (itemIndex < 0 || itemIndex >= items.length) {
        addMessage("Numéro invalide. Veuillez choisir un numéro dans la liste.", false);
        return;
    }
    
    const item = items[itemIndex];
    let definition = "";
    
    // Construire la réponse en fonction de la structure de l'élément
    for (const key in item) {
        if (key === "attributs" && Array.isArray(item[key])) {
            definition += `Attributs: ${item[key].join(", ")}\n`;
        } else if (key === "syntaxe") {
            definition += `Syntaxe:\n${item[key]}\n`;
        } else if (key !== "définition" && key !== "exemple") {
            definition += `${key.charAt(0).toUpperCase() + key.slice(1)}: ${item[key]}\n`;
        }
    }
    
    // Toujours afficher la définition
    if (item.définition) {
        definition += `\nDéfinition: ${item.définition}`;
    }
    
    addMessage(`📚 Détails de l'élément sélectionné:`, false);
    addMessage(definition, false, true);
    
    // Afficher l'exemple s'il existe
    if (item.exemple) {
        addMessage("💡 Exemple d'utilisation:", false);
        addMessage(item.exemple, false, true);
    }
    
    addMessage("Tapez 'retour' pour choisir une autre catégorie, ou 'menu' pour revenir au choix de technologie.", false);
}

function processUserInput(input) {
    if (!input.trim()) return;
    
    addMessage(input, true);
    
    if (state.waitingForDefinition) {
        searchElement(input);
        state.waitingForDefinition = false;
    } else if (input.toLowerCase() === 'menu') {
        resetChat();
    } else if (input.toLowerCase() === 'retour' && state.currentTech) {
        if (state.currentCategory) {
            state.currentCategory = null;
            showTechCategories();
        } else {
            resetChat();
        }
    } else if (state.currentTech && state.currentCategory) {
        const itemIndex = parseInt(input) - 1;
        if (!isNaN(itemIndex)) {
            showDefinition(itemIndex);
        } else {
            addMessage("Veuillez entrer un numéro valide ou 'retour'/'menu'.", false);
        }
    } else {
        resetChat();
    }
    
    userInput.value = '';
}

function searchElement(term) {
    term = term.toLowerCase();
    let found = false;
    
    for (const category in techData[state.currentTech]) {
        const items = techData[state.currentTech][category];
        
        for (const item of items) {
            for (const key in item) {
                if (key === "exemple") continue; // Ne pas chercher dans les exemples
                
                const value = String(item[key]).toLowerCase();
                
                if (value.includes(term)) {
                    addMessage(`✅ Résultat trouvé dans la catégorie "${category}":`, false);
                    
                    let definition = "";
                    for (const k in item) {
                        if (k === "attributs" && Array.isArray(item[k])) {
                            definition += `Attributs: ${item[k].join(", ")}\n`;
                        } else if (k === "syntaxe") {
                            definition += `Syntaxe:\n${item[k]}\n`;
                        } else if (k !== "définition" && k !== "exemple") {
                            definition += `${k.charAt(0).toUpperCase() + k.slice(1)}: ${item[k]}\n`;
                        }
                    }
                    
                    if (item.définition) {
                        definition += `\nDéfinition: ${item.définition}`;
                    }
                    
                    addMessage(definition, false, true);
                    
                    // Afficher l'exemple s'il existe
                    if (item.exemple) {
                        addMessage("💡 Exemple d'utilisation:", false);
                        addMessage(item.exemple, false, true);
                    }
                    
                    found = true;
                    break;
                }
            }
            if (found) break;
        }
        if (found) break;
    }
    
    if (!found) {
        addMessage(`❌ Désolé, je n'ai pas trouvé d'élément correspondant à "${term}".`, false);
    }
    
    addMessage("Tapez 'menu' pour revenir au choix de technologie.", false);
}

function resetChat() {
    state.currentTech = null;
    state.currentCategory = null;
    state.waitingForDefinition = false;
    state.searchTerm = "";
    chatContainer.innerHTML = '';
    showWelcomeMessage();
}

// Événements
sendButton.addEventListener('click', () => processUserInput(userInput.value));
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') processUserInput(userInput.value);
});
restartButton.addEventListener('click', resetChat);