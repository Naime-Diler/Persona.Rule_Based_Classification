# **Potenzielle Kundenwertsberechnung mittels regelbasierter Klassifizierung!**

## **Das Geschäftsproblem**

Unser Unternehmen beabsichtigt, basierend auf bestimmten Merkmalen seiner Kunden levelbasierte neue Kundenprofile zu erstellen. Anhand dieser Profile sollen Segmente definiert werden, um eine 
Schätzung darüber abzugeben, wie viel potenzielle Kunden aus diesen Segmenten durchschnittlich zum Unternehmen beitragen könnten.

## **Daten-Story**

Die Datei "Persona.csv" enthält Informationen über die Preise von Produkten, die von einem multinationalen Unternehmen verkauft wurden, sowie demografische Daten der Benutzer, die diese Produkte
erworben haben. Die Datensätze stammen aus den Transaktionsaufzeichnungen und dies bedeutet, dass die Tabelle nicht dedupliziert ist. Mit anderen Worten kann ein Benutzer mit bestimmten demografischen 
Merkmalen mehrere Einkäufe getätigt haben.

## **Variablen (Features)**

**PRICE:** Betrag, den der Kunde ausgegeben hat,

**SOURCE:** Gerätetyp, mit dem der Kunde verbunden ist (iOS/Android),

**SEX:** Geschlecht des Kunden,

**COUNTRY:** Herkunftsland des Kunden,

**AGE:** Alter des Kunden.
