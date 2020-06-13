# Parthenopeddit API

Le API del progetto parthenopedditrappresentano la backend del social inter-universitario della Parthenope di Napoli.

## Come utilizzarle

Queste istruzioni mostreranno come ottenere una copia del progetto sulla macchina locale per lo sviluppo e testing.

### Prerequisiti

L'unico prerequisito essenziale è il software [Docker](https://www.docker.com/)  
In caso si voglia modificare i file sorgente, è consigliato un IDE per Python (es. [PyCharm](https://www.jetbrains.com/pycharm/) )

### Installazione

* Installare il software docker.  
* Verificare che l'installazione abbia avuto esito positivo utilizzando il comando:

```
docker --version
```

* Clonare o scaricare una copia del [Repository di GitHub](https://github.com/GruppoProgettoTMM201920-Parthenopeddit/RESTPlusAPI.git)  
* Sempre sul terminale, recarsi sulla directory della root del progetto, e utilizzare il comando:

```
docker-compose up -d --build
```

* Attendere qualche secondo, dipende dalla velocità della vostra macchina, e poi visitate con il vostro browser l'indirizzo http://localhost:8000

* Ultimo, ma non meno importante, step è quello di impostare le variabili d'ambiente delle password dei servizi. 
Recarsi sui file **.env.prod**, e **.env.mysql** e sostituire tutte le occorrenze di *<web-secret-key>* e *<db-secret-key>* rispettivamente con le password del servizio web, e del database  

Le API di Parthenopeddit sono ora pronte* per l'utilizzo.

\* per il lancio in ambiente di sviluppo bisogna attivare il login tramite le [API UniParthenope](https://api.uniparthenope.it/), in quanto di default è solo simulato. Questo è presto fatto, basterà modificare il file .env.prod e cambiare il flag di **BYPASS_LOGIN** da 'false' a 'true'

#### *Altri comandi*

Cancellare i container:
```
docker-compose down
```

Cancellare i container *e i dati*:
```
docker-compose down -v
```

Popolare il database con dati preimpostati *(a scopo di test)*
```
docker-compose exec web flask populatedb
```

## Scritto con

* [Python](https://www.python.org/) - Linguaggio di programmazione
* [Flask](https://flask.palletsprojects.com/) - Il micro-framework WEB
* [Flask-RESTPlus](https://flask-restplus.readthedocs.io/) - Supporto a Flask per lo sviluppo di API Rest
* [SQLAlchemy](https://www.sqlalchemy.org/) e [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) - Toolkit per ORM SQL + integrazione con Flask
* [PyMySQL](https://pypi.org/project/PyMySQL/) - Interfaccia al database
* [Whoosh](https://pypi.org/project/Whoosh/) e [Flask-Whooshee](https://pypi.org/project/flask-whooshee/) - Ricerca testuale indicizzata
* [Gunicorn](https://pypi.org/project/gunicorn/) - HTTP Server
