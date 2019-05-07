# coding: utf-8
import copy
import math
import random
import sys

# Este valor será reemplazado por sys.argv[1].
TARGET = 2016

# El número de cromosomas contenidos en una población.
POPULATION_SIZE = 50

# Ya que un cromosoma correcto esta compuesto por pares de números y
# operadores, su mejor escogencia es un numero impar de genes.
CHROMOSOME_SIZE = 11

# Lista de valores posibles que un gen puede asumir.
GENES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '+' , '-' , '*' , '/']

# Define la probabilidad usada para aplicar al operador de cruce de un cromosoma.
CROSSOVER_PROBABILITY = 0.7

# Define la probabilidad usada para aplicar al operador de mutación de un cromosoma.
MUTATION_PROBABILITY = 0.7

# Que tanto un mensaje es nostrado en pantalla para mostrar el progreso del trabajo.
SHOW_EVOLUTION = 50

# Un número grande puede ser representado usando un cromosoma el cual es
# una secuencia de numero, operador, numero, operador y asi sucesivamente.
MAX = 8**(math.ceil(CHROMOSOME_SIZE / 1))

# Un número pequeño puede ser representado usando un cromosoma el cual es
# una secuencia de numero, operador, numero, operador y asi sucesivamente.
MIN = -MAX / 8

# La propagación de la función gausiana usada dentro de la función de 
# aptitud esta basada en la normalización de la distancia maxima entre
# dos posibles soluciones y el numero de cromosomas contenidos en una
# población.
GAUSSIAN_SPREAD = (MAX - MIN) / math.sqrt(POPULATION_SIZE)

def randperm(seq):
	'''
	Retorna una version desordenada de la secuencia dada.
	A diferencia del método shuffle del módulo random, las modificaciones
	no son hechas en el sitio.

	'''
	indices = range(len(seq))
	random.shuffle(indices)
	return [seq[i] for i in indices]

def purge_chromosome(chromosome):
	'''
	Corrige el cromosoma dado de errores sintácticos.
	Una secuencia correcta esta compuesta por un numero un operador 
	un numero y asi sucesivamente.

	'''
	correct_chromosome = []
	next_num = True
	for item in chromosome:
		if next_num and item in ['0', '1', '2', '3', '4']:
			correct_chromosome.append(item)
			next_num = False
		elif not next_num and item in ['+', '-', '*', '/']:
			correct_chromosome.append(item)
			next_num = True
	if next_num and correct_chromosome:
		correct_chromosome.pop()

	return correct_chromosome

def my_eval(command):
	'''
	Evalua el comando dado de izquierda a derecha no teniendo encuenta la
	precedencia entre operadores aritméticos.

	'''
	command = list(command)
	if not command:
		raise SyntaxError

	result = int(command.pop(0))
	while command:
		op = command.pop(0)
		other = int(command.pop(0))
		if op == '+':
			result += other
		if op == '-':
			result -= other
		if op == '*':
			result *= other
		if op == '/':
			result /= other
	return result

def fitness(chromosome):
	'''
	Calcula la función de adaptabilidad de un cromosoma dado.
	@param  chromosome cromosoma a evaluar
	@return el valor de adaptabilidad si todo esta ok, None en otro caso.

	'''
	command = ''.join(purge_chromosome(chromosome))
	try:
		value = my_eval(command)
		if value == TARGET:
			return 1
		else:
			# usa la funcion gausiana para calcular la distancia entre la solucion
			# actual y la objetivo.
			return math.exp(-(TARGET - value)**2/GAUSSIAN_SPREAD)
	except SyntaxError:
		return 0
	except ZeroDivisionError:
		return 0

class Chromosome(object):

	def __init__(self, **kwargs):
		'''
		Crea un nuevo cromosoma especificando su valor y un método usado para
		calcular la función de adaptabilidad. Esta es la lista de keywords aceptadas.

		data 
		chromosome_size

		'''

		if 'data' in kwargs:
			self.data = kwargs['data']
		else:
			data = []
			for _ in xrange(kwargs['chromosome_size']):
				data.append(random.choice(GENES))
			self.data = data

	def __len__(self):
		'''
		Retorna la longitud del cromosoma

		'''
		return len(self.data)

	def __getitem__(self, i):
		'''
		Retorna el i-esimo gen del cromosoma.

		'''
		return self.data[i]

	def __setitem__(self, i, value):
		'''
		Modifica el i-esimo gen del cromosoma.

		'''
		self.data[i] = value

	def __str__(self):
		'''
		Muestra el cromosoma en pantalla

		'''
		return ''.join(self.data)

class Population(object):

	def __init__(self, **kwargs):
		'''
		Crea una nueva población de cromosomas y fija los parámetros que se han
		dado para ser usados durante la evolucion. Esta es una lista de keywords aceptadas.

		data
		chromosome_size
		population_size

		'''
		data = []
		if 'data' in kwargs:
			data = kwargs['data']
		elif 'population_size' in kwargs:
			data = []
			for _ in xrange(kwargs['population_size']):
				data.append(Chromosome(**kwargs))
		self.data = data
		self.index = -1

	def roulette_wheel_selection(self, n):
		'''
		Selecciona uno o mas cromosomas de la población mediante el algoritmo de
		la ruleta de seleccion proporcional.
		@param n el numero de cromosomas a extraer.
		@return  un arreglo de cromosomas seleccionados.

		'''
		scores = map(fitness, self.data)
		total_score = sum(scores)

		selection = []
		for _ in xrange(n):
			probability = random.uniform(0, total_score)
			i = 0
			while probability > scores[i]:
				probability -= scores[i]
				i += 1
			selection.append(copy.deepcopy(self.data[i]))

		return selection

	def crossover1(self, i, j, probability):
		'''
		Aplica el operador de cruce entre el i-esimo y j-esimo cromosoma continue
		la probabilidad dada.  Se escoge un solo punto de corte.
		@return un arreglo conteniendo el nuevo cromosoma.

		'''
		if random.random() <= probability:
			point = random.randint(0, len(self.data[i]) - 1)
			datai = self.data[i][:point] + self.data[j][point:]
			dataj = self.data[j][:point] + self.data[i][point:]
			return [Chromosome(data=datai), Chromosome(data=dataj)]
		else:
			return []

	def mutate1(self, i, probability):
		'''
		Muta un gen del i-esimo cromosoma con la probabilidad dada.

		'''
		data = self.data[i].data[:]
		if random.random() <= probability:
			point = random.randint(0, len(self.data[i]) - 1)
			data[point] = random.choice(GENES)
		return Chromosome(data=data)

	def __iadd__(self, other):
		'''
		Adiciona uno o mas cromosomas a la poblacion.

		'''
		if isinstance(other, Chromosome):
			self.data.append(other)
		elif isinstance(other, list):
			self.data += other
		return self

	def __len__(self):
		'''
		Retorna el numero de cromosomas contenidos en la población.

		'''
		return len(self.data)

	def __str__(self):
		'''
		Muestra la población en pantalla, un cromosoma por linea.

		'''
		return '\n'.join(map(str, self.data))

	def __iter__(self):
		'''
		Hace al objeto iterable.

		'''
		return self

	def next(self):
		'''
		Método invocado mientras se itera sobre la población de cromosomas.

		'''
		if self.index == len(self.data) - 1:
			raise StopIteration
		self.index = self.index + 1
		return self.data[self.index]


def main(argv):
##	if len(sys.argv) != 2:
##		print 'Usage: %s ' % sys.argv[0]
##		return 1

##	global TARGET
##	TARGET = float(sys.argv[1])
	

	pop = Population(population_size=POPULATION_SIZE, 
		chromosome_size=CHROMOSOME_SIZE)

	generation = 0
	while True:
		# evaluacion
		if generation != 0 and not generation % SHOW_EVOLUTION:
			print 'Generacion #%d' % generation
		for chromosome in pop:
			score = fitness(chromosome)

			if score == 1:
				print 'Acierto(#%d):' % generation,
				print ''.join(purge_chromosome(chromosome))
				return

		# seleccion
		pop_1 = Population(data=pop.roulette_wheel_selection(POPULATION_SIZE))

		# crossover
		pop_2 = Population()
		while len(pop_2) != POPULATION_SIZE:
			i = random.randint(0, POPULATION_SIZE - 1)
			j = random.randint(0, POPULATION_SIZE - 1)
			pop_2 += pop_1.crossover1(i, j, CROSSOVER_PROBABILITY)

		# mutacion
		pop = Population()
		for i in xrange(len(pop_2)):
			pop += pop_2.mutate1(i, MUTATION_PROBABILITY)

		generation += 1


main(TARGET)
