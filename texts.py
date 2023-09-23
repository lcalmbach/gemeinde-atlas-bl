intro = """Diese App zeigt dir verschiedene Informationen zu den Gemeinden im Kanton Basel-Landschaft ([Datenquelle](https://data.bl.ch/explore/dataset/10650)).

Zuerst wählst du eine Kennzahl aus, und danach klickst du auf eine Gemeinde.
Neben der Karte siehst du anschliessend:
- eine Balkengrafik mit den Werten der Kennzahl aller Gemeinden, wobei die Gemeinde, die du ausgewählt hast rot markiert ist.
- Alle Werte für die Gemeinde als Tabelle.
- Einen Link auf die Webseite der Gemeinde.
Alle durch Anklicken aktivierten Gemeinden werden in der Balkengrafik rot eingefärbt. Durch erneutes Anklicken kannst du die Gemeinde wieder deaktivieren.

Unter der Karte erscheint ein Radar-Chart, das die aktivierten Gemeinden anhand verschiedener Kennzahlen vergleicht.
"""

radar_chart = """Ein Radar-Chart kann eine hilfreiche Methode sein, um mehrere Merkmale von Gemeinden auf einen Blick darzustellen und zu vergleichen. In diesem Radar-Chart werden verschiedene Kennzahlen wie der Anteil der 0-14-Jährigen an der Bevölkerung, der Steuerfuss und der Bodenpreis betrachtet.

Um die Vergleichbarkeit der unterschiedlichen Merkmale zu gewährleisten, wurden alle Werte auf eine Skala von 0 bis 5 normalisiert. Dabei repräsentiert der Wert 0 das jeweilige Minimum und der Wert 5 das Maximum innerhalb des betrachteten Datensatzes für jedes Merkmal. Diese Normalisierung erlaubt es, eine balancierte Sicht auf die Stärken und Schwächen jeder Gemeinde zu bekommen, ohne dass ein einzelnes Merkmal das Gesamtbild verzerrt.

Bitte beachte, dass die Werte im Diagramm relativ zu den beobachteten Minima und Maxima in diesem speziellen Datensatz sind. Sie sollten daher nicht ohne Kontext oder ohne Kenntnis der ursprünglichen Skalen interpretiert werden. In der untenstehenden Tabelle sind die Minima und Maxima für jede Achse gelistet. Eine 0 auf der Achse des Radar-Charts entspricht dem Minimum Wert für den entsprechenden Parameter, eine 5 entspricht dem Maximum Wert aller Gemeinden.
"""
