function checkSession(){
    let wordListString = sessionStorage.getItem("words");

    let typo = sessionStorage.getItem("typo");
    if(typo != null && typo !== ""){
        console.log("Typo : "+typo);
        let typoArea = document.getElementById("stored_typo");
        typoArea.value = typo;
        //ajout dans le valid feedback
        validTypo(typo, true, document.getElementById("areaTypoValidation"));
    }

    if(wordListString != null && wordListString !== ""){
        let wordList = JSON.parse(wordListString);
        for(let i=0; i<wordList.length; i++){
            addWordToList(wordList[i]);
        }
    }
}

checkSession();



function addWordToList(word){
    let temporaryTableList = document.getElementById("temporary_list");
    let newNumber = temporaryTableList.childElementCount + 1;
    let element = "<tr><td>"+newNumber+"</td><td>"+word+"</td></tr>";
    temporaryTableList.insertAdjacentHTML("beforeend", element);

    //------V2-------
    let area = document.getElementById("wordList");
    area.value += word+"\n";
}

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


//add a word to the temporary list
function addWord(){
    let wordToAddArea = document.getElementById("wordToAdd");
    let wordToAdd = wordToAddArea.value;
    addWordToSession(wordToAdd);
    if(wordToAdd !== ""){
        addWordToList(wordToAdd);
    }
    wordToAddArea.value = "";

}

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
document.getElementById('upload_file').addEventListener('change', readFile);


// read file and check the extension
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