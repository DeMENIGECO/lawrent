# Lawrent

<img width="479" height="243" alt="image" src="https://github.com/user-attachments/assets/6f5dc041-b4a6-408a-bb3b-94d77007d525" />




Lawrent è una piccola shell desktop Linux contenuta in **una singola finestra GTK4 massimizzata**. Le applicazioni native sono widget GTK composti da un window manager interno, quindi l'apertura di un'applicazione non crea un'altra finestra di primo livello.

## Architettura e integrazione

GTK4 è il toolkit della shell perché fornisce la singola finestra di primo livello, il routing dell'input, l'accessibilità, lo stile CSS e i widget nativi. Web utilizza WebKitGTK quando installato. Il terminale utilizza un vero e proprio sottoprocesso che esegue `$SHELL`; File legge la directory home reale; Note e Impostazioni sono applicazioni native GTK.

Le applicazioni Linux esterne sono una funzionalità separata. Su X11, un futuro backend può utilizzare XEmbed/XReparentWindow o un bridge del compositore X11 per collegare una finestra nativa. Su Wayland, i client arbitrari non possono essere riassegnati come figli da un'altra applicazione: Wedexktop lo rileva e non dichiara di integrarli. Un backend di produzione dovrebbe utilizzare protocolli gestiti dal compositore o un compositore nidificato dedicato, ove disponibile. D-Bus e il rilevamento di `.desktop` vengono utilizzati per i metadati e l'avvio delle applicazioni, non come API di embedding simulate.

Livelli di funzionalità:

1. Applicazione nativa Lawrent: incorporata direttamente nel window manager interno.

2. Applicazione esterna compatibile: avviata e incorporata da un backend della piattaforma, attualmente riservato a X11.

3. Applicazione non incorporabile: segnalata come non supportata anziché aprire una finestra aggiuntiva incontrollata.

## Funzionalità nell'MVP

- Una finestra GTK massimizzata e decorata.

- Finestre interne con controlli per focus, z-order, chiusura, minimizzazione e massimizzazione.

- Quattro aree di lavoro virtuali e tasti di scelta rapida da `Super+1` a `Super+4`.

- Shell scura verde con barra superiore, orologio, dock e launcher delle applicazioni.

- Processo terminale reale, elenco reale del filesystem, browser WebKit quando disponibile, note e impostazioni.

- Rilevamento della voce `.desktop` in `wedexktop/core/app_manager.py`.

## Installazione su Linux

GTK e PyGObject sono pacchetti di sistema nella maggior parte delle distribuzioni. Su Debian/Ubuntu:

```bash
./install.sh
./run.sh
```

Lo script installa anche `python3-pip` e `python3-venv`, crea `.venv` con accesso ai pacchetti GTK di sistema e installa Wedexktop in modalità editabile. Questo evita l'errore `No module named pip` e i blocchi degli ambienti Python gestiti dal sistema. I pacchetti richiesti sono GTK4, PyGObject e, facoltativamente, WebKitGTK 6.0. L'applicazione grafica non può essere eseguita nativamente su Windows perché la sua piattaforma di destinazione è Linux/GTK; `python -m compileall -q lawrent` controlla comunque il codice sorgente di Python su qualsiasi piattaforma.

## Scorciatoie

`Super+Spazio` apre il launcher. `Super+W` chiude la finestra interna attiva e `Super+M` la riduce a icona. Da `Super+1` a `Super+4` si cambia area di lavoro. I pulsanti nella barra del titolo consentono di chiudere, ridurre a icona e ingrandire la finestra.
