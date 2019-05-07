# proyecto 1 de copiladores
# Ruben Dario Acuna o y juan pablo campos

#librerias
import ply.lex as lex

#-------------------------------------------------------------------------

tokens=(    
    #SIMBOLOS
    'MAS','MENOS','MULTI','DIVI','IGUAL','MODULO',
    'MENOR','MAYOR','PUNTOCOMA','COMA','LPAREN','RPAREN','LCORCHET',
    'RCORCHET','LLLAVE','RLLAVE',
    'MENORIGUAL','MAYORIGUAL','IGUALL','INTIGUAL','AND','OR','PUNTO',
    'DOSPUNTOS',
    #funciones para identificar
    'NUMERO','IDENTIFICADOR','saltoLinea','ENTERO','CIENTIFICO',
    'HEXADECIMAL','comentario','cadena','ID','NUMBIN',
    #reservados
    'CLASS','EXTENDS','VOID','INT','BOOLEAN',
    'STRING','RETURN','IF','ELSE','WHILE',
    'BREAK','CONTINUE','THIS','NEW','LENGTH',
    'TRUE','FALSE','NULL',
    )

#--------------------------------------------------------------------------

# expreciones regulares 
#signos aritmeticos
t_MAS   = r'\+'
t_MENOS  = r'-'
t_MULTI  = r'\*'
t_DIVI = r'\/'
t_IGUAL  = r'='
t_MODULO = r'%'
#singnos comparaciones
t_MENOR   = r'<'
t_MENORIGUAL   = r'<='
t_MAYOR = r'>'
t_MAYORIGUAL = r'>='
t_IGUALL = r'=='
t_INTIGUAL = r'!='
#singnos booleanos
t_AND  = r'&&'
t_OR  = r'\|\|'
#signos de agrupacion
t_LPAREN = r'\('
t_RPAREN  = r'\)'
t_LCORCHET = r'\['
t_RCORCHET = r'\]'
t_LLLAVE   = r'{'
t_RLLAVE  = r'}'
# singnos puntuacion
t_PUNTO = r'.'
t_DOSPUNTOS = r':'
t_PUNTOCOMA = r';'
t_COMA  = r','
t_IDENTIFICADOR = r'[a-zA-Z]\w*'

#---------------------------------------------------------------------------
# analiza si esta reservada

def t_CLASS(t):
    r'class'
    return t

def t_EXTENDS(t):
    r'extends'
    return t

def t_VOID(t):
    r'void'
    return t

def t_INT(t):
    r'int'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_STRING(t):
    r'string'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_BREAK(t):
    r'break'
    return t

def t_CONTINUE(t):
    r'continue'
    return t

def t_THIS(t):
    r'this'
    return t

def t_NEW(t):
    r'new'
    return t

def t_length(t):
    r'length'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'felse'
    return t

def t_NULL(t):
    r'null'
    return t

#------------------------------------------------------------------------
##analiza y busca donde hay una letra con tilde o ñ para remplazarlo por_
def t_ID(t):
    r'[a-zA-z_]([\wñÑáéíóúÁÉÍÓÚ]*[a-zA-z_ñNáéíóúÁÉÍÓÚ]+)?'
    for text in ['ñ','Ñ','á','é','í','ó','ú','Á','É','Í','Ó','Ú']:
            t.value=t.value.replace(text,'_')
    return (t)
    

# Caracteres que se reconocen e ignoran


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
# Error
def t_error(t):
    print("No se reconoce el caracter '%s'" % t.value[0])
    t.lexer.skip(1)
#

# salta las lineas 
def t_saltoLinea(t):
    r'\n+'
    t.lex.lineno += len(t.value)

t_ignore= ' \t' #ingnora espacios y tabulaciones

#reconoce Numeros binario
def t_NUMBIN(t):
    r'\-?\d+[0-1]'
    return t

#reconoce numeros hexadecimal
#(x|X)
def t_HEXADECIMAL(t):
    r'\-?\d+[A-F]+\d+'
    return t


#reconoce numeros cientificos
def t_CIENTIFICO (t):
    r'\-?[0-9]+(\.[0-9]+)?([eE]\-?[0-9]+)'
    return t

#reconoce numeros enteros  
def t_ENTERO (t):
    r'\-?\d+'
    t.value = int (t.value)
    if (t.value > (-21474883648) ) and (t.value < 21474883647):
        return t
    else:
        print "ERROR: Linea '%d'" % t.lineno +" El numero '%d' no es de 32 bits" % t.value

#reconoce los comentarios y los ignora
def t_comentario(t):
    r'\//.*'
    pass
    #t.lexer.lineno += 1

def t_cadena (t):
    r'\"(.|\\|\")*\"'
    return t

# Construye el analizador

analizador=lex.lex()

#--------------------------------------------------------------------------

analizador=lex.lex()
##busca en la carpeta raiz un archivo txt y lo abre y lo lee y guarda en
#memoria lo leido
cadena = open('ej1.txt','r')
archivo = cadena.read()
#archivo = archivo.split()
cadena.close()
for box in archivo:
    analizador.input(archivo)
    
#print archivo
   
cadena.close()
#cierra el archivo

#----------------------------------------------------------------------------
#  Muestra la lista de tokens
while True:
    tok = analizador.token()
    if not tok: break      #fin de la lista
    print (tok)






