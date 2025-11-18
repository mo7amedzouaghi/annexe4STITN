// Charger les données depuis data.json
let techData = {};

fetch('data.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur de chargement des données');
        }
        return response.json();
    })
    .then(data => {
        techData = data;
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
    addMessage("Bienvenue dans le Chatbot Tech Web !", false);
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
        const key = Object.keys(item)[0]; // balise, propriété, fonction, etc.
        const name = item[key] || item.nom || item.attribut || item.évènement;
        message += `${index + 1}. ${name}\n`;
    });
    
    addMessage(message, false);
    addMessage("Entrez le numéro d'un élément pour voir sa définition détaillée.", false);
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
        } else if (key !== "définition") {
            definition += `${key.charAt(0).toUpperCase() + key.slice(1)}: ${item[key]}\n`;
        }
    }
    
    // Toujours afficher la définition en dernier
    if (item.définition) {
        definition += `\nDéfinition: ${item.définition}`;
    }
    
    addMessage(`Détails de l'élément sélectionné:`, false);
    addMessage(definition, false, true);
    addMessage("Tapez 'retour' pour choisir une autre catégorie, ou 'menu' pour revenir au choix de technologie.", false);
}

function processUserInput(input) {
    if (!input.trim()) return;
    
    addMessage(input, true);
    
    if (state.waitingForDefinition) {
        // Recherche d'un élément spécifique
        searchElement(input);
        state.waitingForDefinition = false;
    } else if (input.toLowerCase() === 'menu') {
        // Retour au menu principal
        resetChat();
    } else if (input.toLowerCase() === 'retour' && state.currentTech) {
        if (state.currentCategory) {
            // Retour aux catégories
            state.currentCategory = null;
            showTechCategories();
        } else {
            // Retour aux technologies
            resetChat();
        }
    } else if (state.currentTech && state.currentCategory) {
        // Vérifier si l'utilisateur a entré un numéro
        const itemIndex = parseInt(input) - 1;
        if (!isNaN(itemIndex)) {
            showDefinition(itemIndex);
        } else {
            addMessage("Veuillez entrer un numéro valide ou 'retour'/'menu'.", false);
        }
    } else {
        // Commencer une nouvelle conversation
        resetChat();
    }
    
    userInput.value = '';
}

function searchElement(term) {
    term = term.toLowerCase();
    let found = false;
    
    // Parcourir toutes les catégories de la technologie actuelle
    for (const category in techData[state.currentTech]) {
        const items = techData[state.currentTech][category];
        
        for (const item of items) {
            // Vérifier chaque propriété de l'élément
            for (const key in item) {
                const value = String(item[key]).toLowerCase();
                
                if (value.includes(term)) {
                    // Afficher l'élément trouvé
                    addMessage(`Résultat trouvé dans la catégorie "${category}":`, false);
                    
                    let definition = "";
                    for (const k in item) {
                        if (k === "attributs" && Array.isArray(item[k])) {
                            definition += `Attributs: ${item[k].join(", ")}\n`;
                        } else if (k === "syntaxe") {
                            definition += `Syntaxe:\n${item[k]}\n`;
                        } else if (k !== "définition") {
                            definition += `${k.charAt(0).toUpperCase() + k.slice(1)}: ${item[k]}\n`;
                        }
                    }
                    
                    if (item.définition) {
                        definition += `\nDéfinition: ${item.définition}`;
                    }
                    
                    addMessage(definition, false, true);
                    found = true;
                    break;
                }
            }
            if (found) break;
        }
        if (found) break;
    }
    
    if (!found) {
        addMessage(`Désolé, je n'ai pas trouvé d'élément correspondant à "${term}".`, false);
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

// Initialisation
resetChat();