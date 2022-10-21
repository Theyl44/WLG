var login = prompt('Entrez votre pseudo :');
var websocket;

// Initialise le Web Socket
createWebSocket();

function createWebSocket() {
    websocket= new WebSocket("ws://localhost:12345/");
}

// Envoie au serveur le message
function sendMessage() {
    let content = document.getElementById("msg").value;//recupere le message de l'input
    document.getElementById("msg").value = "";//on vide l'élément
    websocket.send("["+login+"] "+content);//on envoie le msg au serveur + login de la personne
}

// Réception du message envoyé par le serveur + Affichage
websocket.onmessage = function (event) {
    let tchat = document.getElementById("messages");//on recupere le textarea
    tchat.setAttribute( "disabled", false);
    tchat.append(event.data+"\n");
    tchat.setAttribute("disabled", true);
};

// Notification de connexion
websocket.onopen = function () {
    websocket.send(login+" a rejoint le canal de discussion");
}

// Notification de déconnexion (jamais appelée)
websocket.onclose = function () {
    console.log('FERMETURE');
    websocket.send(login+" a quitté le canal de discussion");
}