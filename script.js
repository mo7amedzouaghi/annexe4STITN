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
    waitingForTech: false,
    waitingForCategory: false,
    waitingForElement: false
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

function updatePlaceholder(text) {
    userInput.placeholder = text;
}

function showWelcomeMessage() {
    addMessage("Bienvenue dans le Chatbot Tech Web ! 🤖", false);
    addMessage("Sélectionnez une technologie :", false);
    showTechOptions();
    state.waitingForTech = true;
    state.waitingForCategory = false;
    state.waitingForElement = false;
    updatePlaceholder("Saisissez le numéro de la technologie...");
}

function showTechOptions() {
    const techList = Object.keys(techData);
    const optionsDiv = document.createElement('div');
    optionsDiv.classList.add('options-container');
    
    techList.forEach((tech, index) => {
        const button = document.createElement('button');
        button.classList.add('tech-option');
        button.textContent = `${index + 1}. ${tech}`;
        button.onclick = () => {
            addMessage(`${index + 1}`, true);
            selectTech(index);
        };
        optionsDiv.appendChild(button);
    });
    
    chatContainer.appendChild(optionsDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function selectTech(index) {
    const techList = Object.keys(techData);
    if (index < 0 || index >= techList.length) {
        addMessage("❌ Numéro invalide. Veuillez choisir un numéro entre 1 et " + techList.length, false);
        return;
    }
    
    const tech = techList[index];
    state.currentTech = tech;
    state.currentCategory = null;
    
    addMessage(`Vous avez sélectionné ${tech}. Choisissez une catégorie :`, false);
    showTechCategories();
    state.waitingForTech = false;
    state.waitingForCategory = true;
    state.waitingForElement = false;
    updatePlaceholder("Saisissez le numéro de la catégorie (0 pour retour)...");
}

function showTechCategories() {
    const categories = Object.keys(techData[state.currentTech]);
    const optionsDiv = document.createElement('div');
    optionsDiv.classList.add('options-container');
    
    // Bouton retour
    const backButton = document.createElement('button');
    backButton.classList.add('tech-option', 'back-option');
    backButton.textContent = '0. ⬅️ Retour';
    backButton.onclick = () => {
        addMessage("0", true);
        state.currentTech = null;
        state.currentCategory = null;
        chatContainer.innerHTML = '';
        showWelcomeMessage();
    };
    optionsDiv.appendChild(backButton);
    
    // Options catégories
    categories.forEach((category, index) => {
        const button = document.createElement('button');
        button.classList.add('tech-option');
        button.textContent = `${index + 1}. ${category}`;
        button.onclick = () => {
            addMessage(`${index + 1}`, true);
            selectCategory(index + 1);
        };
        optionsDiv.appendChild(button);
    });
    
    chatContainer.appendChild(optionsDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function selectCategory(index) {
    const categories = Object.keys(techData[state.currentTech]);
    
    if (index === 0) {
        // Retour au menu principal
        addMessage("0", true);
        state.currentTech = null;
        state.currentCategory = null;
        chatContainer.innerHTML = '';
        showWelcomeMessage();
        return;
    }
    
    if (index < 1 || index > categories.length) {
        addMessage("❌ Numéro invalide. Veuillez choisir un numéro entre 0 et " + categories.length, false);
        return;
    }
    
    const category = categories[index - 1];
    state.currentCategory = category;
    
    addMessage(`Catégorie "${category}" en ${state.currentTech}`, false);
    
    const items = techData[state.currentTech][category];
    const optionsDiv = document.createElement('div');
    optionsDiv.classList.add('options-container');
    
    // Bouton retour
    const backButton = document.createElement('button');
    backButton.classList.add('tech-option', 'back-option');
    backButton.textContent = '0. ⬅️ Retour';
    backButton.onclick = () => {
        addMessage("0", true);
        state.currentCategory = null;
        chatContainer.innerHTML = '';
        addMessage("Bienvenue dans le Chatbot Tech Web ! 🤖", false);
        addMessage(`Vous avez sélectionné ${state.currentTech}. Choisissez une catégorie :`, false);
        showTechCategories();
        state.waitingForCategory = true;
        state.waitingForElement = false;
        updatePlaceholder("Saisissez le numéro de la catégorie (0 pour retour)...");
    };
    optionsDiv.appendChild(backButton);
    
    // Options éléments
    items.forEach((item, idx) => {
        const key = Object.keys(item)[0];
        const name = item[key] || item.nom || item.attribut || item.événement;
        const button = document.createElement('button');
        button.classList.add('tech-option');
        button.textContent = `${idx + 1}. ${name}`;
        button.onclick = () => {
            addMessage(`${idx + 1}`, true);
            showDefinition(idx + 1);
        };
        optionsDiv.appendChild(button);
    });
    
    chatContainer.appendChild(optionsDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    addMessage("Sélectionnez un élément pour voir sa définition détaillée avec exemple.", false);
    
    state.waitingForCategory = false;
    state.waitingForElement = true;
    updatePlaceholder("Saisissez le numéro de l'élément (0 pour retour)...");
}

function showDefinition(itemIndex) {
    const items = techData[state.currentTech][state.currentCategory];
    
    if (itemIndex === 0) {
        // Retour aux catégories
        addMessage("0", true);
        state.currentCategory = null;
        chatContainer.innerHTML = '';
        addMessage("Bienvenue dans le Chatbot Tech Web ! 🤖", false);
        addMessage(`Vous avez sélectionné ${state.currentTech}. Choisissez une catégorie :`, false);
        showTechCategories();
        state.waitingForCategory = true;
        state.waitingForElement = false;
        updatePlaceholder("Saisissez le numéro de la catégorie (0 pour retour)...");
        return;
    }
    
    if (itemIndex < 1 || itemIndex > items.length) {
        addMessage("❌ Numéro invalide. Veuillez choisir un numéro entre 0 et " + items.length, false);
        return;
    }
    
    const item = items[itemIndex - 1];
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
    
    // Bouton retour
    const optionsDiv = document.createElement('div');
    optionsDiv.classList.add('options-container');
    
    const backButton = document.createElement('button');
    backButton.classList.add('tech-option', 'back-option');
    backButton.textContent = '0. ⬅️ Retour à la liste';
    backButton.onclick = () => {
        addMessage("0", true);
        const prevCategory = state.currentCategory;
        state.currentCategory = null;
        chatContainer.innerHTML = '';
        addMessage("Bienvenue dans le Chatbot Tech Web ! 🤖", false);
        addMessage(`Vous avez sélectionné ${state.currentTech}. Choisissez une catégorie :`, false);
        
        // Re-sélectionner la catégorie précédente
        const categories = Object.keys(techData[state.currentTech]);
        const categoryIndex = categories.indexOf(prevCategory) + 1;
        state.currentCategory = prevCategory;
        selectCategory(categoryIndex);
    };
    optionsDiv.appendChild(backButton);
    
    chatContainer.appendChild(optionsDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    updatePlaceholder("Saisissez 0 pour retour...");
}

function processUserInput(input) {
    if (!input.trim()) return;
    
    const userNumber = parseInt(input.trim());
    
    if (isNaN(userNumber)) {
        addMessage(input, true);
        addMessage("❌ Veuillez saisir un numéro valide.", false);
        userInput.value = '';
        return;
    }
    
    if (state.waitingForTech) {
        if (userNumber < 1 || userNumber > Object.keys(techData).length) {
            addMessage(input, true);
            addMessage("❌ Numéro invalide. Veuillez choisir un numéro valide.", false);
        } else {
            addMessage(input, true);
            selectTech(userNumber - 1);
        }
    } else if (state.waitingForCategory) {
        selectCategory(userNumber);
    } else if (state.waitingForElement) {
        showDefinition(userNumber);
    }
    
    userInput.value = '';
}

function resetChat() {
    state.currentTech = null;
    state.currentCategory = null;
    state.waitingForTech = false;
    state.waitingForCategory = false;
    state.waitingForElement = false;
    chatContainer.innerHTML = '';
    showWelcomeMessage();
}

// Événements
sendButton.addEventListener('click', () => processUserInput(userInput.value));
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') processUserInput(userInput.value);
});
restartButton.addEventListener('click', resetChat);
