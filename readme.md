# Parthenopeddit API

Le API del progetto parthenopedditrappresentano la backend del social inter-universitario della Parthenope di Napoli.

## Come utilizzarle

Queste istruzioni mostreranno come ottenere una copia del progetto sulla macchina locale per lo sviluppo e testing.

### Prerequisiti

L'unico prerequisito essenziale è il software Docker: https://www.docker.com/  
In caso si voglia modificare i file sorgente, è consigliato un IDE per Python (es. PyCharm: https://www.jetbrains.com/pycharm/)

### Installazione

Installare il software docker.  
Verificare che l'installazione abbia avuto esito positivo utilizzando il comando:

```
docker --version
```

Clonare o scaricare una copia del repository di github: https://github.com/GruppoProgettoTMM201920-Parthenopeddit/RESTPlusAPI.git  
Sempre sul terminale, recarsi sulla directory della root del progetto, e utilizzare il comando:

```
docker-compose up -d --build
```

Attendere qualche secondo, dipende dalla velocità della vostra macchina, e poi visitate con il vostro browser l'indirizzo http://localhost:8000

Le API di Parthenopeddit sono pronte per l'utilizzo.

