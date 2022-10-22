var websocket;

// Initialize the webSocket
createWebSocket();

function createWebSocket() {
    websocket= new WebSocket("ws://localhost:9000/");
}

function addWordToList(word){
    let temporaryTableList = document.getElementById("temporary_list");
        let newNumber = temporaryTableList.childElementCount + 1;
        let element = "<tr><td>"+newNumber+"</td><td>"+word+"</td></tr>";
        temporaryTableList.insertAdjacentHTML("beforeend", element);
}


//add a word to the temporary list
function addWord(){
    let wordToAdd = document.getElementById("wordToAdd").value;
    if(wordToAdd !== ""){
        addWordToList(wordToAdd);
    }
}


// read file and check the extension
function readFile(){
    let temporaryList = document.getElementById("temporary_list");
    temporaryList.innerHTML = "";
    var file = new FileReader();
    let nameFile = this.files[0].name;
    let extension = /(\.txt)$/i;
    if (!extension.exec(nameFile))
	{
		console.log('Format de fichier non valide');
	}else{
        file.onload = () => {
            let listSplit = file.result.split(/\r\n|\n/);
            for(let i=0; i<listSplit.length -1;i++){
                addWordToList(listSplit[i]);
            }
        }
    }

    file.readAsText(this.files[0]);
}

document.getElementById('upload_file').addEventListener('change', readFile);



function generate(){
    let temporaryList = document.getElementById("temporary_list");

    if(temporaryList.childElementCount > 0){
        let childrens = temporaryList.children;
        let concatToSend = "generate:";
        for(let i=0; i< childrens.length; i++){
            let element = childrens[i].lastElementChild.textContent;
            concatToSend += element+";";
        }
        websocket.send(concatToSend);
    }
}


// Réception du message envoyé par le serveur + Affichage
websocket.onmessage = function (event) {
    let generateList = document.getElementById("generate_list");
    generateList.innerHTML = "";
    let receiveData = event.data.split(";");
    for(let i=0; i<receiveData.length;i++){
        let addHtml = "<tr><td>"+(i+1)+"</td><td>"+receiveData[i]+"</td></tr>";
        generateList.insertAdjacentHTML("beforeend", addHtml);
    }
};

// Notification de connexion
websocket.onopen = function () {
    console.log("Connection to the server successfully established");
}

// Notification de déconnexion (jamais appelée)
websocket.onclose = function () {
    websocket.send(login+" a quitté le canal de discussion");
}