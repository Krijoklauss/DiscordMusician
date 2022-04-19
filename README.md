# DiscordMusician
 Ein einfacher MusikBot für Discord, programmiert in Python.

 - Intention
    Ich wollte mit dem kleinen Projekt hier bloß einen MusikBot für unseren Private DC erstellen,
    Habe das ganze etwas weiterverfolgt und einen Funktionstüchtigen Bot für mehrer Server gebastelt
 
 - Funktionen
    Der Bot kann Musik gleichzeitig auf verschiedenen Servern abspielen,
    dafür muss er nur von einem User mit Admin Rechten eingeladen werden.

    Commands
        prefix
        nick
        bind
        play
        pause
        stop
        resume
        queue
        seek
        clear
        cleaner
        help

- Kommende Updates ( High priority )
   Als nächstes werden erst einmal Grundlegende Funktionen angepasst und optimiert,
   Dazu zählen z.B. besser Formatierte Nachrichten mit denen der Bot antwortet!
   Aktuell sind das nur einfach Messages die abgeschickt werden, welche in Zukunft
   durch "EmbedMessages" ersetzt werden

- Requested Features ( Low priority )
   Aktuell arbeite ich an schnell implementierten playlists sowohl von YouTube als auch Spotify
   Desweiteren Arbeit ich an der seek function welche zum vorspulen in Songs verwendet werden soll.
   Die aktuelle Methode war zu langsam und hat oft ewig gedauert, weshalb ich sie vorerst komplett eingestellt habe.

- Config
    Solltest DU diesen Bot auf deinem Discord benutzen wollen kannst du das Hosten
    entweder mir überlassen und den Bot über *LINK FOLGT* einladen oder einfach diese repository klonen
    und 24/7 laufen lassen.
    Um einen eigenen Bot erstellen zu können müsst ihr euch im Browser zu dieser Seite begeben 'https://discord.com/developers/applications'.
    Anschließend eine Application erstellen und dieser einen Bot hinzufügen.
    Der token wird als Globale Variable auf dem jeweiligen System mit dem Name 'MUSIC_BOT' festgelegt
    Wenn das für manche User keine Option ist, könnt ihr alternativ auch die 'main.py' Datei abändern und die Zeile 12 ("token = environ.get('MUSIC_BOT')")
    in folgendes ändern: "token = 'EUER_BOT_TOKEN'"
    Danach den bot mit python starten und er sollte in eurem Discord online gehen (Sofern dieser bereits eingeladen worden ist!)

- Anderes
   Der Bot wird von mir solange weiter mit updates versorgt bis ich entweder keinen Spaß mehr an dem
   Projekt habe oder ich keine Verwendung mehr für den Bot sehe. Sollte es dazu kommen werde ich es bekannt geben 
   und sollte jemand Interesse daran haben diesen weiterzuführen kann sich derjenige gerne bei mir melden =)

   Achja, der Assets folder kann vorerst ignoriert werden!
   Der wird momentan nicht genutzt, könnte in einem späteren update aber noch interessant werden!
   (Custom Queue images, Custom fonts etc!)
   
   Letztes Update ~ 19.04.2022
