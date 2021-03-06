#!/usr/bin/env python3
'''Núcleo del solucionador de ecuaciones de pyENL'''

import scipy.optimize as opt
from numpy import *
from CoolProp.CoolProp import PropsSI as prop
ln = log
log = log10
import warnings
#from time import time as pyENL_time

#Definición de la función a resolver
#pyENL designa acá el vector de posibles soluciones que se está probando
def pyENL_sistema(pyENL, pyENL_variables, pyENL_eqns):
    cantidad_eqns = len(pyENL_variables)
    #Asignación de variables
    for cont, var in enumerate(pyENL_variables):
        exec(var.name + '= pyENL[' + str(cont) + ']')
    salidapyENL = empty((cantidad_eqns))
    #Funciones para hallar raíces
    for cont, eqn in enumerate(pyENL_eqns):
        salidapyENL[cont] = eval(eqn)
    return salidapyENL


def solver(pyENL_eqns, pyENL_variables, pyENL_iteraciones, pyENL_tol):
    '''
    Acá llegan como parámetros la lista de funciones a hallar raíces como string
    La segunda entrada consiste en los objetos pyENL_variables en lista.
    '''

    warnings.simplefilter('error')
    #for vp in pyENL_variables: print(vp.name)

    #Verificación de que se tiene el mismo número de ecuaciones y de variables:
    if len(pyENL_eqns) != len(pyENL_variables):
        print('No se tiene el mismo número de ecuaciones y de variables')
        print('Hay', str(len(pyENL_eqns)), 'ecuaciones y', \
        str(len(pyENL_variables)), 'variables')
        exit(0)

    #Valores iniciales iguales a cero
    #TODO
    #Lograr dividir las ecuaciones en bloques!!!
    #Reto---------------------------------------------------------------------------
    #Introducir rangos en los que se espera se encuentre una variable y probar con
    #valores aleatorios para pyENL_guesses dentro de esos intervalos hasta dar con la
    #respuesta, siempre que el timeout no se supere.--------------------------------
    #La idea es que las claves del diccionario sean las variables en string y que
    #los valores sean listas con los valores máximos y mínimos de la misma para la
    #búsqueda de valores iniciales

    pyENL_cantidad = len(pyENL_variables)
    pyENL_guesses = zeros(pyENL_cantidad)
    #Actualización de los valores de suposiciones iniciales basados en los
    #atributos de los objetos de entrada de las variables.
    for contd, vard in enumerate(pyENL_variables):
        pyENL_guesses[contd] = vard.guess
    pyENL_ones = ones(pyENL_cantidad)
    try:
        pyENL_sol = opt.fsolve(pyENL_sistema, pyENL_guesses, \
        args=(pyENL_variables, pyENL_eqns), full_output=False,\
         maxfev = pyENL_iteraciones, xtol=pyENL_tol)
    except Exception as pyENL_e:
        print('ERROR:',str(pyENL_e))
        exit(0)


    for cont in range(0,len(pyENL_variables)):
        print(pyENL_variables[cont].name, '=', pyENL_sol[cont])
    print('Residuos:')
    print(pyENL_sistema(pyENL_sol, pyENL_variables, pyENL_eqns))
