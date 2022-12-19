# Kontextbewusstes Fallbasiertes Schließen am Beispiel der Immobilienbewertung

## Beschreibung

Dieses Programm wurde im Rahmen der Masterarbeit "Kontextbewusstes Fallbasiertes Schließen am Beispiel der Immobilienbewertung" entwickelt. Ziel der Arbeit ist es, den Einfluss des Kontexts der Anfragesituation auf das Fallbasierte Schließen zu untersuchen. Das vorliegende Programm stellt ein fallbasiertes System aus dem Aufgaben bersich der Immobilienbewertung dar. Im System sind unterschieldliche Methoden implemntiert, um Kontext in das Retrieval und die Lösungsadaption fallbasierter Systeme zu integrieren. 

Das Programm besteht aus den zwei Komponenten "Web-Scrapping" und "Fallbasiertes System", die unabhängig voneinander ausführbar sind. Die Komponente "Web-Scrapping" wird dazu eingesetzt, Informationen über Inserate zum verkaufstehender Immobilienobjekte der Website: "www.immowelt.de" zu sammeln. Diese Informationen können durch das eigentliche fallbasierte System verwendet werden. Die Komponente "Fallbasiertes System" stellt dieses fallbasiere System dar. In den folgenden Abschnitten werden zunächst die zur Asuführung des Programms benötigten Anforderungen aufgezählt und im Anschluss die Ausführung der beiden Komponenten einzeln vorgestellt.

## Anforderungen

Zur Ausführung des Programms wird die Python-Version 3.6.8 oder höher benötigt. Darüberhinaus werden folgende Python-Module eingesetzt:

- beautifulsoup4==4.9.3
- joblib==1.1.0
- keras==2.6.0
- numpy==1.18.5
- pandas==1.1.5
- tensorflow==2.6.2 
- urllib3==1.26.9
- sklearn

## Web-Scrapping

Die Komponenten "Web-Scrapping" kann mit der Datei: "Scrapping.py" ausgeführt werden. Das Starten von "Scrapping.py" startet direkt den Prozess des Web-Scrappings. In der Konsole werden Informationen über den Verlauf dieses Prozesses ausgegeben. Um den Web-Scrapping-Prozess zu beenden muss die Ausführung der Datei "Scrapping.py" manuell gestoppt werden. 

Dei gescrappten-Daten werden in automatisch erzeugten CSV-Dateien im Ordner "data/haus" gespeichert. Nach jedem in der Konsole ausgegebenen Lauf wird eine solche CSV-Datei angelegt.

## Fallbasiertes System

Das fallbasierte System kann durch die Date "Main.py" gestartet werden. Durch ändern der in "Main.py" definierten Konstanten kann die gewünschte Retrieval- und Adaptionsmethode ausgewählt werden. Wurden durch die "Web-Scrapping"-Komponente neue Daten erfasst, erkennt die "Fallbasiertes System"-Komponenten dieses und integriert die neuen Fälle automtisch in die Fallbasis