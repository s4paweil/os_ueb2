# OS-PF2
Der Clojure Code ist kommentiert und geht auf die einzelnen Funktionen ein.
Das Projekt ist als Leiningen-Projekt angelegt und kann auch entsprechend gestartet werden.

Als Parameter müssen die folgenden Werte geordnet angegeben werden:
- seed : Gibt den Seed an, um die Pseudorandomisierung zu vereinheitlichen.
- num-accounts : Gibt die Anzahl der zu erstellenden Accounts an.
- min-start-balance: Minimaler Startwert für Konten
- max-start-balance: Maximaler Startwert für Konten
- min-transfers-amount: Minimaler Betrag bei Überweisungen
- max-transfers-amount: Maximaler Betrag bei Überweisungen
- num-clients : Gibt die Anzahl der Clients/ Thread an.
- num-transfers : Anzahl der Transfere, die von den Clients durchgeführt werden soll.


Ein Beispielaufruf könnte zum Beispiel wie folgt aussehen:

    lein run -m bankkonto.core/main seed 10 500 1000 50 250 5 100 