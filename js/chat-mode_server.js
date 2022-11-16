/**
 * Check the current session & search for typo and words save in session storage
 */
function checkSession(){
    let wordListString = sessionStorage.getItem("words");
    let typo = sessionStorage.getItem("typo");
    let checkTransformation = sessionStorage.getItem("transformate");
    if(typo != null && typo !== ""){
        console.log("Typo : "+typo);
        let typoArea = document.getElementById("stored_typo");
        typoArea.value = typo;
        //ajout dans le valid feedback
        validTypo(typo, true, document.getElementById("areaTypoValidation"));
    }
    if(checkTransformation != null){
        if(checkTransformation === "false"){
            document.getElementById("validTransfo").checked = false;
        }else if(checkTransformation === "true"){
            document.getElementById("validTransfo").checked = true;
        }
    }

    if(wordListString != null && wordListString !== ""){
        if(document.getElementById("validTransfo").checked === true){
            //add in the hidden element
            //get the current table
            let list = document.getElementById("temporary_list");
            if(list.childElementCount > 0) {
                let childrens = list.children;
                for (let i = 0; i < childrens.length; i++) {
                    let miniChilds = childrens[i];
                    if(miniChilds.childElementCount > 0){
                        let element = miniChilds.lastElementChild.textContent;
                        console.log("element : "+element);
                        addWordToHiddenList(element);
                    }
                }
            }
        }else{
            //clean acutal temporary list
            let area = document.getElementById("wordList");
            area.value = "";

            let tempo = document.getElementById("temporary_list");
            tempo.innerHTML = "";

            let wordList = JSON.parse(wordListString);
            for(let i=0; i<wordList.length; i++){
                addWordToList(wordList[i]);
            }
        }
    }


}
checkSession();

/**
 * add a word to the temporary-list, before the generation
 * @param word
 */
function addWordToList(word){
    let temporaryTableList = document.getElementById("temporary_list");
    let newNumber = temporaryTableList.childElementCount + 1;
    let element = "<tr><td>"+newNumber+"</td><td>"+word+"</td></tr>";
    temporaryTableList.insertAdjacentHTML("beforeend", element);

    //------V2-------
    addWordToHiddenList(word);
}

function addWordToHiddenList(word){
    let area = document.getElementById("wordList");
    area.value += word+"\n";
}


/**
 * Like addWordToList, it add a word in the list contains in the session storage
 * @param word
 */
function addWordToSession(word){
    if(sessionStorage.getItem("words") == null){
        sessionStorage.setItem("words", JSON.stringify(""));
        let array_word = [];
        array_word.push(word);
        sessionStorage.setItem("words", JSON.stringify(array_word));
    }else{
        let wordListSession = JSON.parse(sessionStorage.getItem("words"));
        console.log(typeof wordListSession);
        wordListSession.push(word);
        sessionStorage.setItem("words", JSON.stringify(wordListSession));
    }
}


/**
 * Function activated when clicking on Add a word or while reading words contains in a file
 */
function addWord(){
    let wordToAddArea = document.getElementById("wordToAdd");
    let wordToAdd = wordToAddArea.value;
    addWordToSession(wordToAdd);
    if(wordToAdd !== ""){
        addWordToList(wordToAdd);
    }
    wordToAddArea.value = "";

}

/**
 * function activated when you want to valid your typo for generation
 */
function addTypo(){
    //clean typo
    let form = document.getElementById("formTypo");
    form.classList.remove("was-validated");
    form.classList.add("needs-validation");

    let typo = document.getElementById("typo");
    let typoUse = typo.value;
    let regexp = /^[#\*@]{1,}$/;
    if(typoUse !== "" && typoUse.match(regexp)){
        console.log("Typo isn't empty");
        let typoArea = document.getElementById("stored_typo");
        typoArea.value = typoUse;
        //add typo to sessionStorage and print it to the user on the web page
        sessionStorage.setItem("typo", typoUse);
        validTypo(typoUse, true, typo);
    }else{
        console.log("Wrong Typo");
        validTypo(typoUse, false, typo);
    }
    typo.value = "";
}

/**
 * Check if the typo is valid, respect the typo used in the server
 * @param typoWord
 * @param isValid
 * @param inputTypo
 */
function validTypo(typoWord, isValid, inputTypo) {
    let divTypo = document.getElementById("validationTypo");
    let form = document.getElementById("formTypo");
    if (isValid) {
        form.classList.add("was-validated");
        form.classList.remove("needs-validation");
        divTypo.classList.remove("invalid-feedback");
        divTypo.classList.add("valid-feedback");
        inputTypo.classList.remove("is-invalid");
        inputTypo.classList.add("is-valid");
        typoWord += " is a valid expression";
    } else {
        inputTypo.classList.remove("is-valid");
        inputTypo.classList.add("is-invalid");
        divTypo.classList.remove("valid-feedback");
        divTypo.classList.add("invalid-feedback");
        typoWord += " is not a valid expression";
    }
    divTypo.innerText = typoWord;
}

/**
 * check if a file is put in the area upload_file
 */
document.getElementById('upload_file').addEventListener('change', readFile);

/**
 * read a file contains in upload-file input and check the extension
 */
function readFile(){
    let temporaryList = document.getElementById("temporary_list");
    let area = document.getElementById("wordList");
    temporaryList.innerHTML = "";
    area.innerHTML = "";

    //clean session Storage
    if(sessionStorage.getItem("words") != null){
        let tab = [];
        sessionStorage.setItem("words", JSON.stringify(tab));
    }

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
                addWordToSession(listSplit[i]);
                addWordToList(listSplit[i]);
            }
        }
    }
    file.readAsText(this.files[0]);
}

document.getElementById('validTransfo').addEventListener('change', addTransformation);

function isEmpty(element){
    let empty = false;
    if(element.value === "" || element.value === "\n"){
        empty = true;
        console.log("Is empty");
    }
    return empty;
}


function addTransformation(){
    let valueTransfo = document.getElementById("validTransfo").checked;
    if(valueTransfo){
        sessionStorage.setItem("transformate", "true");
        //avant de submit, on ajoute la liste des mots a transformer
        let formTransfo = document.getElementById('formTransformation');
        let element = document.getElementById("wordList");
        //check if element is empty or not
        if(!isEmpty(element)){
            formTransfo.insertAdjacentElement('beforeend', element);
            formTransfo.submit();
        }
    }else{
        console.log("Transformation removed");
        sessionStorage.setItem("transformate", "false");
        //modifier le table et la remettre d'origine comme le formulaire hidden
        checkSession();
    }
}

function generation(){
    //clear session storage
    if(sessionStorage.getItem("words") != null){
        let tab = [];
        sessionStorage.setItem("words", JSON.stringify(tab));
    }
}