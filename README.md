# Italian-LitBank

Italian-LitBank rappresenta un corpus completamente italiano generato a partire da testi, opere e collezioni di opere di narrativa, selezionati per tale obiettivo. Le tre attività principali che hanno portato alla sua creazione sono: Selezione delle opere di narrativa, Creazione dei dataset annotati, Analisi dei dataset e creazione di Italian-LitBank.

## Selezione delle opere di narrativa

Sono state selezionate dal sito Project Gutenberg esclusivamente 87 opere e collezioni di opere di finzione appartenenti tra il XVIII e il XX secolo. I motivi sono:
1.	Evitare di selezionare testi scritti in “italiano antico”.
2.	I testi di finzione hanno un alto numero di dialoghi, monologhi e entità.

### Modifica dei testi

In seguito alla selezione vi è la modifica del contenuto dei testi. Con modifica del contenuto di un testo si fa riferimento a tale procedura:
1.	Rimozione delle pagine di copertina.
2.	Rimozione del frontespizio e dell’occhiello.
3.	Rimozione degli indici.
4.	Riduzione delle parole del testo a circa 2000.
5.	Aggiunta di spazi bianchi e ritorni a capo tra i vari segni d’interpunzione.

## Creazione dei dataset annotati

A partire dai file di testo inizia l’annotazione vera e propria per la realizzazione di due dataset (denominati ItaSet), effettuata da due autori, di cui uno è il sottoscritto.

### Annotazione delle entità

L’annotazione delle entità è avvenuta sfruttando doccano, utilizzando la stessa metodologia di LitBank. Quindi, oltre all’esclusione del tipo WEA, i tipi possibili di entità sono: PER, FAC, LOC, GPE, VEH e ORG. Inoltre le entità di ItaSet presentano una nested structure.
doccano genera un file di estensione JSONL, che contiene diverse informazioni per ogni riga presenti secondo l’ordine specificato di seguito:
1.	id: valore numerico relativo al testo annotato.
2.	text: il contenuto del testo annotato.
3.	label: le annotazioni del testo.
4.	Comments: i commenti inseriti nel testo annotato.

### Controllo e Rifinitura annotazioni

I file JSONL sono stati ricontrollati e rifiniti: ids (identificativo di ogni testo), texts (contenuto di ogni testo), annotations (annotazioni di ogni testo), labels of type (annotazioni con tipi specifici di entità), comments (commenti inseriti nei testi). Questo controllo iniziale è stato susseguito dalla ricerca di annotazioni errate, per cui sono state controllate:
-	Correttezza delle annotazioni:
inizio_annotazione <= fine_annotazione
-	Ordine delle annotazioni:
inizio_annotazione1 < inizio_annotazione2
-	Spazi bianchi.
-	Parole incomplete.
-	Tipo delle annotazioni.

Sono state aggiunte altre annotazioni per entità previamente non annotate a causa di sviste o errori.
I file JSONL modificati sono stati infine utilizzati per la creazione dei file di annotazioni aventi estensione ANN. Il formato che si ottiene a partire da file di testo e file di annotazioni prende il nome di brat standoff format.

## Analisi dei dataset e creazione di Italian-LitBank

Completata la creazione dei due dataset, l'ultima fase è costituita dall’analisi delle differenze principali che sussistono tra i dataset stessi e dalla loro fusione, cioè la creazione del dataset finale denominato Italian-LitBank.

### Analisi

L’analisi dei dataset si svolge in due momenti:
-	Il primo momento coincide con il punto in cui i due dataset sono stati creati.
-	Il secondo momento rappresenta il punto in cui vi è stata la rimozione di articoli determinativi, articoli indeterminativi e alcune stringhe all’inizio delle annotazioni.

Sono stati calcolati numero di annotazioni uguali e numero di annotazioni differenti che esistono tra i due dataset. Le annotazioni differenti sono state salvate in due file separati, uno relativo al primo dataset e uno relativo al secondo dataset, in modo tale da essere controllate manualmente e selezionate per la creazione del dataset finale.

### Creazione

I file di differenza sono stati chiamati entrambi “differences” e contengono le annotazioni presenti in un dataset e assenti nell’altro per ogni testo. É stato creato un altro file chiamato “final_differences” in cui sono state memorizzate manualmente tutte le annotazioni selezionate da entrambi i file “differences” che saranno presenti nel dataset finale. Infine, sono state inserite tali annotazioni nel primo dataset, rimuovendo anche eventuali annotazioni risultate non idonee o inadatte, per via del fatto che la maggior parte delle annotazioni erano presenti in entrambi i dataset.