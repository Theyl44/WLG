<p align="center"><img style="width:200px;" src="img/icon_name.png" /></p>

------

<h2>Présentation</h2>

<p>
Il est souvent utile de créer des dictionnaires de mots lorsqu’on souhaite bruteforce un mot de passe ou vérifier les différentes url disponibles sur un site.La liste d’origine peut contenir (mot, prénom, nom, numéro, adresse, date_naissance,etc). L’objectif est d’automatiser la chose pour gagner du temps et créer des listes qui correspondent à des cas particuliers. 
Exemple : Dans le cas d’un pentest de l’isen ouest, nous souhaitons générer une liste de mot de passe (isen2018, isen2022, 1s3n2018, 1s3n2022, …)
</p>


video de présentation du projet

<h3>Ligne de commande</h3>
<p>
    On peut se servir de ce programme en ligne de comme 
</p>

    exemple de code

<h3>Script Shell</h3>
<p>
    Le programme est récupérable via Docker sous le nom <strong>saltas44/wlg_light:latest</strong>.
    
    Pour se faire :
        docker pull saltas44/wlg_light:latest
    Puis pour lancer ce container :
        docker run -d -p 8080:80 wlg_light
        
    Vous pouvez ainsi accéder au site via http://localhost:8080 sur votre machine.
</p>
<h5>Shell</h5>
<p>
    Il est aussi possible d'utiliser les scripts shell adaptés pour wlg_light disponible dans le dossier shell.
    
    Voici la liste des scripts disponibles :
        - get_docker.sh
            --> Equivalent au docker pull du projet
        - run_docker.sh
            --> Equivalent a faire un docker run
        - stop_docker.sh
            --> Stop le docker du wlg_light grâce à son ID de container
    
    Exemple : ./get_docker.sh
              ./run_docker.sh
              ./stop_docker.sh
    Accéder ensuite au site via http://localhost:8080 sur votre machine.
</p>
