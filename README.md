# finalboss

Voor de eindopdracht van programmeren


# Handleiding

## Aanmaken van CA's

Verschillende cellulaire automaten kunnen gemaakt worden met behulp van de basisklasse `CellularAutomata`. Een CA kan als volgt gemaakt worden:

`myCA = CellularAutomata(shape, rules)`
 
waar shape de vorm van de CA is, wat weergegeven word als een lijst met het aantal cellen in elke dimensie, en rules de functie is die, gegeven een cell, de index van deze cell en de rest van het rooster, de geüpdate staat van deze cell geeft. 

### Voorbeeld 1

We maken hier een 3-dimensionale CA met in elke dimensie 10 cellen, die als regel heeft dat als een cell de waarde 1 heeft, hij 0 wordt en andersom.

We definiëren eerst de functie voor onze regel, en vullen die in wanneer we de CA maken. 
```python
def invert(cell, index, grid):
    if cell == 0:
        return 1
    else:
        return 0

myCA = CellularAutomata([10,10,10], invert)
```
### 1- en 2-dimensionale CA's

Ook kunnen we eenvoudig 1- en 2-dimensionale CA's maken met de  `Cellular1D` en `Cellular2D` klassen. Deze bevatten al ingebouwde functies voor visualisatie, wat handig kan zijn.

Een 1-dimensionale CA met 10 cellen kan als volgt worden aangemaakt:
```python
#we gebruiken dezelfde functie invert als bij het eerste voorbeeld
myCA_1D = Cellular1D(10, invert)
```
Merk op dat hier alleen een getal gegeven wordt voor de grootte, en geen lijst. 

Een 2-dimensionale CA met 10 cellen in de breedte en 5 in de hoogte kan als volgt worden gemaakt:
```python
myCA_2D = Cellular2D(10, 5, invert)
```
Ook hier wordt de breedte en hoogte los gegeven, en niet in een lijst. 

## Het invullen van cellen

Wanneer een CA wordt aangemaakt, begint hij met 0 in elke cell. Er zijn verschillende manieren om waardes aan cellen toe te kennen. 

De meest algemene, die voor elke CA werkt, is `setcells`. Deze functie neemt een lijst met index-tuples en een bepaalde waarde, en kent voor elke index-tuple de bijbehorende cell de gegeven waarde toe. 

```python
#op plaatsen (5,5,5), (0,0,0) & (1,2,3) wordt de waarde van de cell 1. 
myCA.setcells([(5,5,5), (0,0,0), (1,2,3)], 1)
```

Ook bestaat er een functie die alle waarden terugzet naar 0, `setzeros`. Deze werkt ook voor elke CA.
```python
myCA.setzeros()
```
Daarnaast bestaat er ook de functie `random`, die ook voor elke CA werkt, en die alle cellen random 0 of 1 maakt. 
```python
myCA.random()
```
Verder is er ook een functie speciaal voor `Cellular1D`, namelijk `start_middle`, die de cell in het midden naar 1 verandert. 
```python
myCA_1D.start_middle()
```

## Updaten van CA

Het updaten van CA's kan eenvoudig gedaan worden met de `update` functie. Deze functie roept voor iedere cell de rules-functie op, en geeft de cell de output als waarde. 

```python
myCA.update()
```

## Het maken van regels

