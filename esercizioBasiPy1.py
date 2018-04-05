'''
Modified on Apr 28, 2018

In questo programma si assume che lo studente NON sappia usare le funzioni di Flask per leggere i dati del request.
Questo programma  FUNZIONA solo con un giocatore alla volta!
@author: posenato
'''

from _random import Random
from flask import Flask

app = Flask("Gioco")
# Alcune variabili dell'applicazione per rappresentare lo stato e le costanti del gioco.
app.rnd = Random()
app.rnd.seed()
app.sequence = [0, 0, 0]
app.seqMaxIndex = 2
app.index = 0
app.moves = 0
app.maxAllowedMoves = 10

# Le seguenti variabili (in realtà costanti stringa) sono per scrivere pezzi di codice HTML in modo semplice
# Sono variabili di MODULO!
head = """<!DOCTYPE html>
<html>
<head>
	<title>Piccolo gioco</title>
	<style type="text/css">
		form, input {
			padding: 2px;
			width: auto;
			text-align: center;
		}
		input {
			font-size: x-large;
			padding: 5px;
		}
	</style>
</head>
<body>
"""

form = """
<form action="/pushed0" method="get">
	<input type="submit" value="0">
</form>
<form action="/pushed1" method="get">
	<input type="submit" value="1">
</form>
"""

tail = """
<form style="text-align: right" action="/" method="get">
	<input type="submit" value="Mi sono rotto, ricomincia!">
</form>
"""


def makeRandomSequence():
	'''Genera una sequenza casuale di 3 bit e la memorizza nell'attributo app.sequence.'''
	'''... da completare da parte dello studente...'''
	for i in range(0,2):
		'''app.rnd.seed()'''
		if (app.rnd.random()>=0.5):
			app.sequence[i] = True
		elif (app.rnd.random()<0.5):
			app.sequence[i] = False

def availableMoves():
	'''Ritorna il numero di mosse ancora possibili'''
	return app.maxAllowedMoves - app.moves


@app.route('/')
def homePage():
	'''Inizializza il gioco e ritorna il codice HTML per la home page.'''
	makeRandomSequence()
	app.index = 0
	app.moves = 0
	return head + """
	<h1>Piccolo gioco di fortuna</h1>
	<p>Il giocatore deve indovinare una sequenza casuale di Vero o False di lunghezza 3.</p>
	<p>Ogni volta che il giocatore indovina un mossa, il gioco va avanti. Ogni volta che il giocatore sbaglia una mossa, il gioco ricomincia.</p>
	<p>Il giocatore vince se indovina una sequenza entro 10 mosse.</p>
	""" + form + tail


@app.route('/pushed0')
def falseButton():
	return manageButton(False)


@app.route('/pushed1')
def trueButton():
	return manageButton(True)


def manageButton(rightValue):
	'''Realizza la logica del gioco. Ritorna il codice HTML della pagina di risposta in base allo stato del gioco e alla mossa fatta e passata in input'''
	if availableMoves() <= 0:
		answer = "<p>Hai terminato le mosse possibili.</p><h3>Hai perso!</h3>"
		return head + answer + tail
	'''... da completare da parte dello studente....'''
	if app.index==2:
		answer = "<p>Complimenti</p><h3>Hai vinto!</h3>"
		return head + answer + tail
	if app.sequence[app.index]==rightValue:
		app.index+=1
		answer = "<p>Hai indovinato n" + str(app.index) + " numero/i</p>"
		return head + form + answer + tail
	if app.sequence[app.index]!=rightValue:
		app.moves+=1
		makeRandomSequence()
		app.index = 0
		answer = "<p>Hai sbagliato, ti rimangono n"+ str(availableMoves()) + " mosse/a</p>"
		return head + form + answer + tail
	


if __name__ == '__main__':
	app.run(debug=True)
