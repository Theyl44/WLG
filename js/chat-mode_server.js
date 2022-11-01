function addWordToList(word){
    let temporaryTableList = document.getElementById("temporary_list");
    let newNumber = temporaryTableList.childElementCount + 1;
    let element = "<tr><td>"+newNumber+"</td><td>"+word+"</td></tr>";
    temporaryTableList.insertAdjacentHTML("beforeend", element);

    //------V2-------
    // let area = document.getElementById("wordList");
    // area.value += word+"\n";
}


//add a word to the temporary list
function addWord(){
    let wordToAdd = document.getElementById("wordToAdd").value;
    if(wordToAdd !== ""){
        addWordToList(wordToAdd);
    }
}

function addTypo(){
    let typoUse = document.getElementById("typo").value;
    let regexp = /[#**@]/;
    if(typoUse !== "" && regexp.test(typoUse)){
        console.log("Typo isn't empty");
        let concatToSend = "typo:";
        concatToSend += typoUse;
        websocket.send(concatToSend);
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
            for(let i=0; i<listSplit.length;i++){
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
            if(i < childrens.length -1){
                concatToSend += element+";";
            }else{
                concatToSend += element;
            }
        }
        websocket.send(concatToSend);
    }
}


function getFile(){
    websocket.send("resultGeneration");
    let btn_dl = document.getElementById("btn_dl");
    btn_dl.setAttribute("disabled", "true");
}