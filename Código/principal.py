#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
import math
import cmath
import webbrowser
import sqlite3
import numpy as np
from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager
#Ruta de la base de datos
path='Bancos.db'

#Funcion que conecta a la base de datos
def connect_to_database(path):
    try:
        con = sqlite3.connect(path)
        cursor = con.cursor()
        con.commit()
        con.close()
    except Exception as e:
        print(e)
#Inicialización de las corrientes de linea del sistema y variables de los capacitores
global ItotalA
ItotalA = [0+0j]
global ItotalB
ItotalB = [0+0j]
global ItotalC
ItotalC = [0+0j]
fp = 0
contador = 1
global lista
lista = ""
global capschneider1
global capschneider2
global capeaton1
global capeaton2
capschneider1=""
capschneider2=""
capeaton1=""
capeaton2=""
sentido = False
#Lista de capacitores utilizados (Solamente las magnitudes de las potencias reactivas, la información detallada sobre los capacitores se encuentra en la base de datos.)
Schneider240 = [7000, 10000, 17000, 20000, 27000, 30000, 37000, 40000, 50000, 60000]
Schneider480 = [10000, 15000, 22000, 25000, 30000, 37000, 40000, 45000, 50000, 60000, 70000, 80000, 90000, 100000, 110000, 120000, 132000, 142000]
Eaton240 = [15000, 25000, 30000, 40000, 50000, 75000, 100000, 160000]
Eaton480 = [10000, 15000, 25000, 30000, 40000, 50000, 75000, 100000, 150000, 200000]

# Clase para la pantalla de bienvenida
class RunPage(Screen):
    def cambio(self):
        self.manager.current = "fuente"

# Clase para la ventana del menú principal, donde se despliegan los botones para ingresar las cargas, calcular el fp o ir a ver la lista de cargas actuales.
class MainPage(Screen):
    def calculotot(self):
        ItotalLA = 0
        ItotalLB = 0
        ItotalLC = 0
        for i in ItotalA:
            ItotalLA += i
        for i in ItotalB:
            ItotalLB += i
        for i in ItotalC:
            ItotalLC += i
        global Stot
        Stot = (VfaseA*(complex.conjugate(ItotalLA))) + ((VfaseA*(complex(-0.5 ,(-math.sqrt(3)/2))))*(complex.conjugate(ItotalLB))) + ((VfaseA*(complex(-0.5 ,(math.sqrt(3)/2))))*(complex.conjugate(ItotalLC)))
        global cita
        cita = cmath.phase(Stot)
        print("EL cita es:")
        print(cita)
        global fp
        fp = math.cos(cita)
        print(fp)
        self.manager.current = "factorpotencia"

# Pantalla para cargas en delta, que ofrece las tres formas de ingresarlas.
class DeltabMenuPage(Screen):
    pass

# Clase de ingreso de cargas delta mediante la Potencia activa
class DeltabPPage(Screen):
    #Esta función se encarga de calcular las corrientes de línea a partir de la potencia activa, las líneas a las que se conecta y su f.p. Posee manejo de errores y convierte el sentido del f.p. a minúsculas para evitar errores al comparar strings.
    def calcdeltabp(self):
        try:
            #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
            pactiv = float(self.ids["activadeltab"].text)
            fpdp = float(self.ids["fpdeltab"].text)
            cit = math.acos(fpdp)
            print("El cita antes de especificar atraso;")
            print(cit)
            a = self.ids["adelantoatraso"].text
            cosa = a.lower()
            #Si está en adelanto el ángulo es negativo, se debe establecer porque el factor de potencia es el coseno del ángulo, y al ser coseno una función par, se debe hacer este cambio cuando el fp está en adelanto.
            if (cosa == "adelanto"):
                cit = -1*cit
                print("caca, nuevo cita: ")
                print(cit)
            global lista
            global contador
            #Control del ingreso de cargas para mostrarlas en la actualización de lista
            lista += (str(contador) + ". Carga delta balanceada con potencia activa de " + str(pactiv) + " W con un factor de potencia de " + str(fpdp) + " en " + str(cosa) + "\n")
            contador += 1
            magnIfaseA = pactiv/(3*fpdp*abs(VFlineaAB))
            fi = cmath.phase(VFlineaAB) - cit
            im = math.sin(fi)*magnIfaseA
            re = math.cos(fi)*magnIfaseA
            IfaseA = complex(re, im)
            #Se calculan las corrientes y se hace un append a las corrientes totales.
            IlineaA = complex(1.5, -math.sqrt(3)/2)*IfaseA
            ItotalA.append(IlineaA)
            IlineaB = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaA
            ItotalB.append(IlineaB)
            IlineaC = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaB
            ItotalC.append(IlineaC)
            #Se limpian los campos de texto
            self.ids["activadeltab"].text = ''
            self.ids["fpdeltab"].text= ''
            self.ids["adelantoatraso"].text = ''
            self.manager.current = "main"
        except:
            #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
            self.ids["activadeltab"].text = ''
            self.ids["fpdeltab"].text= ''
            self.ids["adelantoatraso"].text = ''
            self.manager.current = "errordeltabp"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error en la página de delta por potencia activa.
class ErrorPagedeltabp(Screen):
    pass

#Clase de ingreso de cargas delta mediante potencia aparente
class DeltabSPage(Screen):
    #Función que realiza los cálculos de la corriente de línea al ingresar una carga delta por medio de su potencia aparente y su f.p.
    def calcdeltabs(self):
        try:
            #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
            s = float(self.ids["aparentedeltab"].text)
            fpdp = float(self.ids["fpdeltab"].text)
            cit = math.acos(fpdp)
            a = self.ids["adelantoatraso"].text
            cosa = a.lower()
            #Si está en adelanto el ángulo es negativo, se debe establecer porque el factor de potencia es el coseno del ángulo, y al ser coseno una función par, se debe hacer este cambio cuando el fp está en adelanto.
            if (cosa == "adelanto"):
                cit = -1*cit
                print(cit)
            magnIfaseA = s/(3*abs(VFlineaAB))
            global lista
            global contador
            #Lista que permite actualizar la lista de cargas ingresadas
            lista += (str(contador) + ". Carga delta balanceada con potencia aparente de " + str(s) + " VA con un factor de potencia de " + str(fpdp) + " en " + str(cosa) + "\n")
            contador += 1
            fi = cmath.phase(VFlineaAB) - cit
            im = math.sin(fi)*magnIfaseA
            re = math.cos(fi)*magnIfaseA
            IfaseA = complex(re, im)
            #Se calculan las corrientes y se hace un append a las corrientes totales.
            IlineaA = complex(1.5, -math.sqrt(3)/2)*IfaseA
            ItotalA.append(IlineaA)
            IlineaB = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaA
            ItotalB.append(IlineaB)
            IlineaC = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaB
            ItotalC.append(IlineaC)
            #Se limpian los campos de texto
            self.ids["aparentedeltab"].text = ''
            self.ids["fpdeltab"].text = ''
            self.ids["adelantoatraso"].text = ''
            self.manager.current = "main"
        except:
            #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
            self.ids["aparentedeltab"].text = ''
            self.ids["fpdeltab"].text = ''
            self.ids["adelantoatraso"].text = ''
            self.manager.current = "errordeltabs"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error en la página de delta por potencia aparente.
class ErrorPagedeltabs(Screen):
    pass

#Clase de ingreso de cargas delta mediante impedancia.
class DeltabZPage(Screen):
    #Función que realiza los cálculos de la corriente de línea al ingresar una carga delta por medio de su impedancia de carga y de línea.
    def calcdeltabz(self):
        try:
            #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
            cargadeltab = complex(self.ids["impdeltab"].text)
            print(cargadeltab)
            impcable = complex(self.ids["implineadeltab"].text)
            global lista
            global contador
            #Lista que permite actualizar la lista de cargas ingresadas
            lista += (str(contador) + ". Carga delta balanceada de impedancia " + str(cargadeltab) + " ohms con una impedancia de linea de " + str(impcable) + " ohms \n")
            contador += 1
            Yconvert = (cargadeltab)/3
            print("Ya convertido a estrella queda asi:")
            print(Yconvert)
            #Se calculan las corrientes y se hace un append a las corrientes totales.
            IlineaAa = VfaseA/(Yconvert+impcable)
            IlineaBb = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaAa
            IlineaCc = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaBb
            ItotalC.append(IlineaCc)
            ItotalA.append(IlineaAa)
            ItotalB.append(IlineaBb)
            print(IlineaAa)
            print(IlineaBb)
            print(IlineaCc)
            #Se limpian los campos de texto
            self.ids["impdeltab"].text = ''
            self.ids["implineadeltab"].text = ''
            self.manager.current = "main"
        except:
            #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
            self.ids["impdeltab"].text = ''
            self.ids["implineadeltab"].text = ''
            self.manager.current = "errordeltabz"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error en la página de delta por impedancias.
class ErrorPagedeltabz(Screen):
    pass

# Pantalla para cargas en estrella, que ofrece las tres formas de ingresarlas.
class YbMenuPage(Screen):
    pass

#Clase de ingreso de cargas estrella mediante su impedancia de línea y de carga.
class YbZPage(Screen):
    #Función que realiza los cálculos de la corriente de línea al ingresar una carga estrella por medio de su impedancia de carga y de línea.
    def calcybz(self):
        #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
        try:
            global lista
            cargayb = complex(self.ids["impyb"].text)
            print(cargayb)
            impcable = complex(self.ids["implineayb"].text)
            global contador
            #Lista que permite actualizar la lista de cargas ingresadas
            lista += (str(contador) + ". Carga estrella balanceada de impedancia " + str(cargayb) + " ohms con una impedancia de linea de " + str(impcable) + " ohms \n")
            contador += 1
            print(cargayb +impcable)
            #Se calculan las corrientes y se hace un append a las corrientes totales.
            IlineaA = (VfaseA)/(cargayb + impcable)
            IlineaB = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaA
            IlineaC = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaB
            print(IlineaA)
            print(IlineaB)
            print(IlineaC)
            ItotalC.append(IlineaC)
            ItotalA.append(IlineaA)
            ItotalB.append(IlineaB)
            #Se limpian los campos de texto
            self.ids["impyb"].text = ''
            self.ids["implineayb"].text = ''
            self.manager.current = "main"
        except:
            #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
            self.ids["impyb"].text = ''
            self.ids["implineayb"].text = ''
            self.manager.current = "errorybz"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error en la página de estrella por impedancias.
class ErrorPageYbz(Screen):
    pass

#Clase de ingreso de cargas estrella mediante potencia activa.
class YbPPage(Screen):
    #Función que realiza los cálculos de la corriente de línea al ingresar una carga estrella por medio de su potencia activa y su f.p.
    def calcybp(self):
        #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
        try:
            p = float(self.ids["activayb"].text)
            fpyb = float(self.ids["fpyb"].text)
            cit = math.acos(fpyb)
            a = self.ids["adelantoatraso"].text
            cosa = a.lower()
            #Si está en adelanto el ángulo es negativo, se debe establecer porque el factor de potencia es el coseno del ángulo, y al ser coseno una función par, se debe hacer este cambio cuando el fp está en adelanto.
            if (cosa == "adelanto"):
                cit = -1*cit
                print("El cita es: ")
                print(cit)
            global lista
            global contador
            #Lista que permite actualizar la lista de cargas ingresadas
            lista += (str(contador) + ". Carga estrella balanceada con potencia activa de " + str(p) + " W con un factor de potencia de " + str(fpyb) + " en " + str(cosa) + "\n")
            contador += 1
            magnIlineaA = p/(3*abs(VfaseA)*fpyb)
            fi = cmath.phase(VfaseA) - cit
            print(fi)
            im = math.sin(fi)*magnIlineaA
            re = math.cos(fi)*magnIlineaA
            #Se calculan las corrientes y se hace un append a las corrientes totales.
            IlineaA = complex(re, im)
            ItotalA.append(IlineaA)
            print(IlineaA)
            IlineaB = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaA
            ItotalB.append(IlineaB)
            IlineaC = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaB
            ItotalC.append(IlineaC)
            #Se limpian los campos de texto
            self.ids["activayb"].text = ''
            self.ids["fpyb"].text= ''
            self.ids["adelantoatraso"].text = ''
            self.manager.current = "main"
        except:
            #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
            self.ids["activayb"].text = ''
            self.ids["fpyb"].text= ''
            self.ids["adelantoatraso"].text = ''
            self.manager.current = "errorybp"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error en la página de estrella por potencia activa y f.p.
class ErrorPageYbp(Screen):
    pass

#Clase de ingreso de cargas estrella mediante potencia aparente.
class YbSPage(Screen):
    #Función que realiza los cálculos de la corriente de línea al ingresar una carga estrella por medio de su potencia aparente y su f.p.
    def calcybs(self):
        #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
        try:
            s = float(self.ids["aparenteyb"].text)
            fpyb = float(self.ids["fpyb"].text)
            cit = math.acos(fpyb)
            a = self.ids["adelantoatraso"].text
            cosa = a.lower()
            global lista
            global contador
            #Lista que permite actualizar la lista de cargas ingresadas
            lista += (str(contador) + ". Carga estrella balanceada con potencia aparente de " + str(s) + " VA con un factor de potencia de " + str(fpyb) + " en " + str(cosa) + "\n")
            contador += 1
            #Si está en adelanto el ángulo es negativo, se debe establecer porque el factor de potencia es el coseno del ángulo, y al ser coseno una función par, se debe hacer este cambio cuando el fp está en adelanto.
            if (cosa == "adelanto"):
                cit = -1*cit
                print("El cita es: ")
                print(cit)
            magnIlineaA = s/(3*abs(VfaseA))
            fi = cmath.phase(VfaseA) - cit
            print(fi)
            im = math.sin(fi)*magnIlineaA
            re = math.cos(fi)*magnIlineaA
            #Se calculan las corrientes y se hace un append a las corrientes totales.
            IlineaA = complex(re, im)
            ItotalA.append(IlineaA)
            print(IlineaA)
            IlineaB = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaA
            ItotalB.append(IlineaB)
            IlineaC = complex(-0.5 ,(-math.sqrt(3)/2))*IlineaB
            ItotalC.append(IlineaC)
            #Se limpian los campos de texto
            self.ids["aparenteyb"].text = ''
            self.ids["fpyb"].text = ''
            self.ids["adelantoatraso"].text = ''
            self.manager.current = "main"
        except:
            #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
            self.ids["aparenteyb"].text = ''
            self.ids["fpyb"].text = ''
            self.ids["adelantoatraso"].text = ''
            self.manager.current = "errorybs"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error en la página de estrella por potencia aparente y f.p.
class ErrorPageYbs(Screen):
    pass

# Pantalla para cargas monofásicas, que ofrece las tres formas de ingresarlas.
class MonoMenuPage(Screen):
    pass

#Clase de ingreso de cargas monofásicas mediante impedancia de línea y de carga.
class MonofasicaZPage(Screen):
    def calcmonofasica(self):
        #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
        try:
            cargamono = complex(self.ids["impmonofasica"].text)
            implinea = complex(self.ids["implinemonofasica"].text)
            linea1 = self.ids["linea1"].text
            linea1 = l1.upper()
            print(linea1)
            linea2 = self.ids["linea2"].text
            linea2 = l1.upper()
            print(linea2)
            global lista
            global contador
            if (linea1 == "A" and linea2 == "B"):
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = VFlineaAB/(cargamono+implinea)
                ItotalA.append(Ilineamono)
                ItotalB.append(-1*(Ilineamono))
                print(VFlineaAB)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con impedancia de " + str(cargamono) + " ohms e impedancia de línea " + str(implinea) + " ohms \n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "B" and linea2 == "C"):
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = VFlineaBC/(cargamono+implinea)
                ItotalB.append(Ilineamono)
                ItotalC.append(-1*Ilineamono)
                print(VFlineaBC)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con impedancia de " + str(cargamono) + " ohms e impedancia de línea " + str(implinea) + " ohms \n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "C" and linea2 == "A"):
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = VFlineaCA/(cargamono+implinea)
                ItotalC.append(Ilineamono)
                ItotalA.append(-1*Ilineamono)
                print(VFlineaCA)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con impedancia de " + str(cargamono) + " ohms e impedancia de línea " + str(implinea) + " ohms \n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "A" and linea2 == "N"):
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = VfaseA/(cargamono+implinea)
                ItotalA.append(Ilineamono)
                print(VfaseA)
                print(Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con impedancia de " + str(cargamono) + " ohms e impedancia de línea " + str(implinea) + " ohms \n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "B" and linea2 == "N"):
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = VfaseB/(cargamono+implinea)
                ItotalA.append(Ilineamono)
                print(VfaseB)
                print(Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con impedancia de " + str(cargamono) + " ohms e impedancia de línea " + str(implinea) + " ohms \n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "C" and linea2 == "N"):
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = VfaseC/(cargamono+implinea)
                ItotalA.append(Ilineamono)
                print(VfaseC)
                print(Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con impedancia de " + str(cargamono) + " ohms e impedancia de línea " + str(implinea) + " ohms \n")
                contador += 1
            else:
                self.manager.current = "errormonoz"
            #Se limpian los campos de texto
            self.ids["impmonofasica"].text = ''
            self.ids["implinemonofasica"].text = ''
            self.ids["linea1"].text = ''
            self.ids["linea2"].text = ''
        except:
            #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
            self.ids["impmonofasica"].text = ''
            self.ids["implinemonofasica"].text = ''
            self.ids["linea1"].text = ''
            self.ids["linea2"].text = ''
            self.manager.current = "errormonoz"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error con el ingreso de los datos en la página de monofásica por impedancias.
class ErrorPagemonoz(Screen):
    pass

#Clase de ingreso de cargas monofásicas mediante potencia activa.
class MonoPPage(Screen):
    #Función que realiza los cálculos de la corriente de línea al ingresar una carga monofásica por medio de su potencia activa y su f.p.
    def calcmonop(self):
        #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
        try:
            pmono = float(self.ids["activamono"].text)
            fpmono = float(self.ids["fpmono"].text)
            l1 = self.ids["linea1"].text
            linea1 = l1.upper()
            print(linea1)
            l2 = self.ids["linea2"].text
            linea2 = l2.upper()
            print(linea2)
            citamono = math.acos(fpmono)
            a = self.ids["adelantoatraso"].text
            cosa = a.lower()
            if ( cosa == "adelanto"):
                #Si está en adelanto el ángulo es negativo, se debe establecer porque el factor de potencia es el coseno del ángulo, y al ser coseno una función par, se debe hacer este cambio cuando el fp está en adelanto.
                citamono = -1*citamono
                print("El cita es: ")
                print(citamono)
            global lista
            global contador
            if (linea1 == "A" and linea2 == "B"):
                magIlineamono = pmono/(fpmono*abs(VFlineaAB))
                fimono = cmath.phase(VFlineaAB)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalA.append(Ilineamono)
                ItotalB.append(-1*(Ilineamono))
                print(VFlineaAB)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia activa de " + str(pmono) + " W con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "B" and linea2 == "C"):
                magIlineamono = pmono/(fpmono*abs(VFlineaBC))
                fimono = cmath.phase(VFlineaBC)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                Ilineamono = complex(remono, immono)
                #Lista que permite actualizar la lista de cargas ingresadas
                ItotalB.append(Ilineamono)
                ItotalC.append(-1*(Ilineamono))
                print(VFlineaBC)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia activa de " + str(pmono) + " W con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "C" and linea2 == "A"):
                magIlineamono = pmono/(fpmono*abs(VFlineaCA))
                fimono = cmath.phase(VFlineaCA)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalC.append(Ilineamono)
                ItotalA.append(-1*(Ilineamono))
                print(VFlineaCA)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia activa de " + str(pmono) + " W con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "A" and linea2 == "N"):
                magIlineamono = pmono/(fpmono*abs(VfaseA))
                fimono = cmath.phase(VfaseA)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                #Lista que permite actualizar la lista de cargas ingresadas
                ItotalA.append(Ilineamono)
                print(VfaseA)
                print(Ilineamono)
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia activa de " + str(pmono) + " W con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "B" and linea2 == "N"):
                magIlineamono = pmono/(fpmono*abs(VfaseB))
                fimono = cmath.phase(VfaseB)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                Ilineamono = complex(remono, immono)
                #Lista que permite actualizar la lista de cargas ingresadas
                ItotalB.append(Ilineamono)
                print(VfaseB)
                print(Ilineamono)
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia activa de " + str(pmono) + " W con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "C" and linea2 == "N"):
                magIlineamono = pmono/(fpmono*abs(VfaseC))
                fimono = cmath.phase(VfaseC)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalC.append(Ilineamono)
                print(VfaseC)
                print(Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia activa de " + str(pmono) + " W con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            else:
                print("Holaas \n")
                self.manager.current = "errormonop"
            #Se limpian los campos de texto
            self.ids["activamono"].text = ''
            self.ids["linea1"].text = ''
            self.ids["linea2"].text = ''
            self.ids["linea2"].text = ''
            self.ids["adelantoatraso"].text = ''
            self.ids["fpmono"].text = ''
        except:
            #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
            self.ids["activamono"].text = ''
            self.ids["linea1"].text = ''
            self.ids["linea2"].text = ''
            self.ids["linea2"].text = ''
            self.ids["adelantoatraso"].text = ''
            self.ids["fpmono"].text = ''
            self.manager.current = "errormonop"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error en la página de estrella por potencia activa y f.p.
class ErrorPagemonop(Screen):
    pass

#Clase de ingreso de cargas monofásicas mediante potencia aparente.
class MonoSPage(Screen):
    #Función que realiza los cálculos de la corriente de línea al ingresar una carga estrella por medio de su potencia aparente y su f.p.
    def calcmonos(self):
        #En este try se realizan los cálculos en caso de haber ingresado los datos correctamente.
        try:
            smono = float(self.ids["aparentemono"].text)
            fpmono = float(self.ids["fpmono"].text)
            l1 = self.ids["linea1"].text
            linea1 = l1.upper()
            print(linea1)
            l2 = self.ids["linea2"].text
            linea2 = l2.upper()
            print(linea2)
            citamono = math.acos(fpmono)
            a = self.ids["adelantoatraso"].text
            cosa = a.lower()
            global lista
            global contador
            #Si está en adelanto el ángulo es negativo, se debe establecer porque el factor de potencia es el coseno del ángulo, y al ser coseno una función par, se debe hacer este cambio cuando el fp está en adelanto.
            if ( cosa == "adelanto"):
                citamono = -1*citamono
                print("el cita es:")
                print(citamono)
            if (linea1 == "A" and linea2 == "B"):
                magIlineamono = smono/(abs(VFlineaAB))
                fimono = cmath.phase(VFlineaAB)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalA.append(Ilineamono)
                ItotalB.append(-1*(Ilineamono))
                print(VFlineaAB)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia aparente de " + str(smono) + " VA con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "B" and linea2 == "C"):
                magIlineamono = smono/(abs(VFlineaBC))
                fimono = cmath.phase(VFlineaBC)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalB.append(Ilineamono)
                ItotalC.append(-1*(Ilineamono))
                print(VFlineaBC)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia aparente de " + str(smono) + " VA con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "C" and linea2 == "A"):
                magIlineamono = smono/abs(VFlineaCA)
                fimono = cmath.phase(VFlineaCA)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalC.append(Ilineamono)
                ItotalA.append(-1*(Ilineamono))
                print(VFlineaCA)
                print(Ilineamono)
                print(-1*Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia aparente de " + str(smono) + " VA con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "A" and linea2 == "N"):
                magIlineamono = smono/(abs(VfaseA))
                fimono = cmath.phase(VfaseA)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalA.append(Ilineamono)
                print(VfaseA)
                print(Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia aparente de " + str(smono) + " VA con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "B" and linea2 == "N"):
                magIlineamono = smono/(abs(VfaseB))
                fimono = cmath.phase(VfaseB)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalB.append(Ilineamono)
                print(VfaseB)
                print(Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia aparente de " + str(smono) + " VA con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            elif (linea1 == "C" and linea2 == "N"):
                magIlineamono = smono/(abs(VfaseC))
                fimono = cmath.phase(VfaseC)-citamono
                remono = math.cos(fimono)*magIlineamono
                immono = math.sin(fimono)*magIlineamono
                #Se calculan las corrientes y se hace un append a las corrientes totales.
                Ilineamono = complex(remono, immono)
                ItotalC.append(Ilineamono)
                print(VfaseC)
                print(Ilineamono)
                #Lista que permite actualizar la lista de cargas ingresadas
                lista += (str(contador) + ". Carga monofásica entre " + str(linea1) + " y " + str(linea2) + " con potencia aparente de " + str(smono) + " VA con un factor de potencia de " + str(fpmono) + " en " + str(cosa) + "\n")
                contador += 1
                self.manager.current = "main"
            else:
                self.manager.current = "errormonos"
            #Se limpian los campos de texto
            self.ids["aparentemono"].text = ''
            self.ids["linea1"].text = ''
            self.ids["linea2"].text = ''
            self.ids["linea2"].text = ''
            self.ids["adelantoatraso"].text = ''
            self.ids["fpmono"].text = ''
        #Este except se ejecuta en caso de que se genere un error. Lo guía a otra ventana y limpia los campos de texto.
        except:
            self.ids["aparentemono"].text = ''
            self.ids["linea1"].text = ''
            self.ids["linea2"].text = ''
            self.ids["linea2"].text = ''
            self.ids["adelantoatraso"].text = ''
            self.ids["fpmono"].text = ''
            self.manager.current = "errormonos"

#Esta es la clase de la página a la que se redirecciona en caso de haber un error en la página de estrella por potencia aparente y f.p.
class ErrorPagemonos(Screen):
    pass

#Clase para la ventana donde se ingresan los datos de la fuente, como el ángulo de fase y la tensión de línea.
class FuentePage(Screen):
    #Si se selecciona el voltaje de 240, se calculan las tensiones de todas las líneas y fases de acuerdo con esta magnitud y la fase ingresada.
    def calcfuente240(self):
        global VFlineaAB
        global VFlineaBC
        global VFlineaCA
        global VfaseA
        global VfaseB
        global VfaseC
        global control1
        control1=240
        #Se intentan realizar los cálculos, si los datos se ingresaron correctamente
        try:
            angulogrados = float(self.ids["FaseVab"].text)
            angulorad = ((math.pi)/180)*angulogrados
            VFlineaAB = cmath.rect(240, angulorad)
            print(VFlineaAB)
            VFlineaBC = complex(-0.5 ,(-math.sqrt(3)/2))*VFlineaAB
            print(VFlineaBC)
            VFlineaCA = complex(-0.5 ,(-math.sqrt(3)/2))*VFlineaBC
            print(VFlineaCA)
            VfaseA = VFlineaAB/(complex(1.5,((math.sqrt(3))/2)))
            print(VfaseA)
            VfaseB = complex(-0.5 ,(-math.sqrt(3)/2))*VfaseA
            print(VfaseB)
            VfaseC = complex(-0.5 ,(-math.sqrt(3)/2))*VfaseB
            print(VfaseC)
            self.ids["FaseVab"].text = ""
            self.manager.current = "main"
        #Este except lleva a la pantalla de error en caso de que se ingresaran datos erróneos en el campo de la fase.
        except:
            self.ids["FaseVab"].text = ""
            self.manager.current = "errorfuente"
    #Si se selecciona el voltaje de 480, se calculan las tensiones de todas las líneas y fases de acuerdo con esta magnitud y la fase ingresada.
    def calcfuente480(self):
        #Se intentan realizar los cálculos, si los datos se ingresaron correctamente
        try:
            global VFlineaAB
            global VFlineaBC
            global VFlineaCA
            global VfaseA
            global VfaseB
            global VfaseC
            global control1
            control1=480
            angulogrados = float(self.ids["FaseVab"].text)
            angulorad = ((math.pi)/180)*angulogrados
            VFlineaAB = cmath.rect(480, angulorad)
            VFlineaBC = complex(-0.5 ,(-math.sqrt(3)/2))*VFlineaAB
            VFlineaCA = complex(-0.5 ,(-math.sqrt(3)/2))*VFlineaBC
            print(VFlineaAB)
            VfaseA = VFlineaAB/(complex(1.5,((math.sqrt(3))/2)))
            VfaseB = complex(-0.5 ,(-math.sqrt(3)/2))*VfaseA
            VfaseC = complex(-0.5 ,(-math.sqrt(3)/2))*VfaseB
            self.ids["FaseVab"].text = ""
            self.manager.current = "main"

        except:
            self.ids["FaseVab"].text = ""
            self.manager.current = "errorfuente"

#Clase de la ventana a la que se redirecciona al usuario en caso de haber un error en la página de la fuente.
class ErrorPagefuente(Screen):
    pass

#Esta clase se relaciona con la página en donde se se calcula el f.p. actual del sistema ingresado.
class FPPage(Screen):
    fptext = StringProperty()
    #Función que realiza el cálculo del f.p. actual. Se define si es en adelanto o atraso según el valor del ángulo relacionado con el f.p.
    def probando(self, ):
        global fp
        global cita
        global sentido
        if cita < -0.000001:
            sentido = True
            print(cita)
            self.fptext = " " + str(fp)
            self.fptext += " en adelanto"
            print(self.fptext)
        elif (-0.000001 <= cita <= 0.000001):
            sentido = False
            print(cita)
            self.fptext = " " + str(fp)
            print(self.fptext)
        elif cita > 0.000001:
            sentido = False
            print(cita)
            self.fptext = " " + str(fp)
            self.fptext += " en atraso"
            print(self.fptext)
        else:
            print("Ocurrio un error en el calculo.")

#Esta es la clase relacionada con la página en la que se calcula la potencia reactiva actual, se ofrecen bancos de capacitores según el f.p. nuevo deseado y se calcula el f.p. real que el sistema tendría con alguno de estos bancos.
class NuevoFPPage(Screen):
        Qtotal = StringProperty()
        Schneider1 = StringProperty()
        Schneider2 = StringProperty()
        Eaton1 = StringProperty()
        Eaton2 = StringProperty()
        fpcortext = StringProperty()
        aresep = StringProperty()
        #Esta función se encarga de realizar el cálculo de la potencia reactiva actual del sistema.
        def calcreactiva(self):
            try:
                global cita
                global Stot
                global Qtot
                global fp
                Qtot = abs(math.sin(cita)*abs(Stot))
                self.Qtotal = str(Qtot)
                print(fp)
                print(abs(Stot))
                print(Qtot)
                Ptot = (abs(Stot))*math.cos(cita)
                if ((Ptot <= 1000000)&(fp < 0.9)):
                    self.aresep = "Para evitar multas por bajo factor de potencia, según la normativa del Aresep, se recomienda corregirlo a 0.9"
                elif ((Ptot > 1000000)&(Ptot <= 5000000)&(fp < 0.95)):
                    self.aresep = "Para evitar multas por bajo factor de potencia, según la normativa del Aresep, se recomienda corregirlo a 0.95"
                elif ((Ptot > 5000000)&(fp < 0.98)):
                    self.aresep = "Para evitar multas por bajo factor de potencia, según la normativa del Aresep, se recomienda corregirlo a 0.98"
                else:
                    self.aresep = "Su factor de potencia actual cumple con la normativa del Aresep"
            except:
                self.manager.current = "errorfpnuevo"
        #La función se encarga de calcular la potencia reactiva que necesita el sistema para tener un factor de potencia de 0.9, además busca los bancos de capacitores que se van a desplegar en la pantalla de corrección.
        def calcnuevareactiva90(self):
            try:
                global Qtot
                global cita
                global Stot
                global VFlineaAB
                global capschneider1
                global capschneider2
                global capeaton1
                global capeaton2
                global sentido
                capschneider1=""
                capschneider2=""
                capeaton1=""
                capeaton2=""
                if (sentido == False):
                    Ptot = (abs(Stot))*math.cos(cita)
                    citanuevo = math.acos(0.9)
                    Qnuevo = Ptot * (math.tan(citanuevo))
                    Qcap = Qtot - Qnuevo
                    print(Qnuevo)
                    print(Qcap)
                    if (((abs(VFlineaAB)) < 242) and ((abs(VFlineaAB)) > 238)):
                        condeaton = False
                        condschneider = False
                        i = 0
                        while ((i < 9)&(condschneider == False)):
                            if ((Schneider240[i] <= Qcap) & (Schneider240[i+1] >= Qcap)):
                                capschneider1 = Schneider240[i]
                                capschneider2 = Schneider240[i+1]
                                condschneider = True
                            i += 1
                        if (condschneider == False):
                            if (Qcap >= Schneider240[9]):
                                self.Schneider1 = "No encontrado"
                                capschneider2 = Schneider240[9]
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            elif (Qcap <= Schneider240[0]):
                                self.Schneider2 = "No encontrado"
                                capschneider1 = Schneider240[0]
                                if(capschneider1 <= Qtot):
                                    self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                                else:
                                    self.Schneider1 = "No encontrado"
                            else:
                                self.Schneider1 = "No encontrado"
                                self.Schneider2 = "No encontrado"
                        else:
                            self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                            if(capschneider2 <= Qtot):
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            else:
                                self.Schneider2 = "No encontrado"

                        j = 0
                        while ((j < 7)&(condeaton == False)):
                            if ((Eaton240[j] <= Qcap) & (Eaton240[j+1] >= Qcap)):
                                capeaton1 = Eaton240[j]
                                capeaton2 = Eaton240[j+1]
                                condeaton = True
                            j += 1
                        if (condeaton == False):
                            if (Qcap >= Eaton240[7]):
                                self.Eaton1 = "No encontrado"
                                capeaton2 = Eaton240[7]
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            elif (Qcap <= Eaton240[0]):
                                self.Eaton2 = "No encontrado"
                                capeaton1 = Eaton240[0]
                                if(capeaton1 <= Qtot):
                                    self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                                else:
                                    self.Eaton1 = "No encontrado"
                            else:
                                self.Eaton1 = "No encontrado"
                                self.Eaton2 = "No encontrado"
                        else:
                            self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                            if(capeaton2 <= Qtot):
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            else:
                                self.Eaton2 = "No encontrado"

                    elif (((abs(VFlineaAB)) < 482) and ((abs(VFlineaAB)) > 478)):
                        condeaton = False
                        condschneider = False
                        i = 0
                        while ((i < 17)&(condschneider == False)):
                            if ((Schneider480[i] <= Qcap) & (Schneider480[i+1] >= Qcap)):
                                capschneider1 = Schneider480[i]
                                capschneider2 = Schneider480[i+1]
                                condschneider = True
                            i += 1
                        if (condschneider == False):
                            if (Qcap >= Schneider480[17]):
                                self.Schneider1 = "No encontrado"
                                capschneider2 = Schneider480[17]
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            elif (Qcap <= Schneider480[0]):
                                self.Schneider2 = "No encontrado"
                                capschneider1 = Schneider480[0]
                                if(capschneider1 <= Qtot):
                                    self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                                else:
                                    self.Schneider1 = "No encontrado"
                        else:
                            self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                            if(capschneider2 <= Qtot):
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            else:
                                self.Schneider2 = "No encontrado"

                        j = 0
                        while ((j < 9)&(condeaton == False)):
                            if ((Eaton480[j] <= Qcap) & (Eaton480[j+1] >= Qcap)):
                                capeaton1 = Eaton480[j]
                                capeaton2 = Eaton480[j+1]
                                condeaton = True
                            j += 1
                        if (condeaton == False):
                            if (Qcap >= Eaton480[9]):
                                self.Eaton1 = "No encontrado"
                                capeaton2 = Eaton480[9]
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            elif (Qcap <= Eaton480[0]):
                                self.Eaton2 = "No encontrado"
                                capeaton1 = Eaton480[0]
                                if(capeaton1 <= Qtot):
                                    self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                                else:
                                    self.Eaton1 = "No encontrado"
                            else:
                                self.Eaton1 = "No encontrado"
                                self.Eaton2 = "No encontrado"
                        else:
                            self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                            if(capeaton2 <= Qtot):
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            else:
                                self.Eaton2 = "No encontrado"
                else:
                    self.Schneider1 = "No encontrado"
                    self.Schneider2 = "No encontrado"
                    self.Eaton1 = "No encontrado"
                    self.Eaton2 = "No encontrado"
                if(self.Schneider1 == "No encontrado"):
                    capschneider1=""
                if(self.Schneider2 == "No encontrado"):
                    capschneider2=""
                if(self.Eaton1 == "No encontrado"):
                    capeaton1=""
                if(self.Eaton2 == "No encontrado"):
                    capeaton2=""
            except:
                self.manager.current = "errorfpnuevo"

        #La función se encarga de calcular la potencia reactiva que necesita el sistema para tener un factor de potencia de 0.95, además busca los bancos de capacitores que se van a desplegar en la pantalla de corrección.
        def calcnuevareactiva95(self):
            try:
                global Qtot
                global cita
                global Stot
                global VFlineaAB
                global capschneider1
                global capschneider2
                global capeaton1
                global capeaton2
                global sentido
                capschneider1=""
                capschneider2=""
                capeaton1=""
                capeaton2=""
                if (sentido == False):
                    Ptot = (abs(Stot))*math.cos(cita)
                    citanuevo = math.acos(0.95)
                    Qnuevo = Ptot * (math.tan(citanuevo))
                    Qcap = Qtot - Qnuevo
                    print(Qnuevo)
                    print(Qcap)
                    if (((abs(VFlineaAB)) < 242) and ((abs(VFlineaAB)) > 238)):
                        condeaton = False
                        condschneider = False
                        i = 0
                        while ((i < 9)&(condschneider == False)):
                            if ((Schneider240[i] <= Qcap) & (Schneider240[i+1] >= Qcap)):
                                capschneider1 = Schneider240[i]
                                capschneider2 = Schneider240[i+1]
                                condschneider = True
                            i += 1
                        if (condschneider == False):
                            if (Qcap >= Schneider240[9]):
                                self.Schneider1 = "No encontrado"
                                capschneider2 = Schneider240[9]
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            elif (Qcap <= Schneider240[0]):
                                self.Schneider2 = "No encontrado"
                                capschneider1 = Schneider240[0]
                                if(capschneider1 <= Qtot):
                                    self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                                else:
                                    self.Schneider1 = "No encontrado"
                            else:
                                self.Schneider1 = "No encontrado"
                                self.Schneider2 = "No encontrado"
                        else:
                            self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                            if(capschneider2 <= Qtot):
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            else:
                                self.Schneider2 = "No encontrado"

                        j = 0
                        while ((j < 7)&(condeaton == False)):
                            if ((Eaton240[j] <= Qcap) & (Eaton240[j+1] >= Qcap)):
                                capeaton1 = Eaton240[j]
                                capeaton2 = Eaton240[j+1]
                                condeaton = True
                            j += 1
                        if (condeaton == False):
                            if (Qcap >= Eaton240[7]):
                                self.Eaton1 = "No encontrado"
                                capeaton2 = Eaton240[7]
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            elif (Qcap <= Eaton240[0]):
                                self.Eaton2 = "No encontrado"
                                capeaton1 = Eaton240[0]
                                if(capeaton1 <= Qtot):
                                    self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                                else:
                                    self.Eaton1 = "No encontrado"
                            else:
                                self.Eaton1 = "No encontrado"
                                self.Eaton2 = "No encontrado"
                        else:
                            self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                            if(capeaton2 <= Qtot):
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            else:
                                self.Eaton2 = "No encontrado"

                    elif (((abs(VFlineaAB)) < 482) and ((abs(VFlineaAB)) > 478)):
                        condeaton = False
                        condschneider = False
                        i = 0
                        while ((i < 17)&(condschneider == False)):
                            if ((Schneider480[i] <= Qcap) & (Schneider480[i+1] >= Qcap)):
                                capschneider1 = Schneider480[i]
                                capschneider2 = Schneider480[i+1]
                                condschneider = True
                            i += 1
                        if (condschneider == False):
                            if (Qcap >= Schneider480[17]):
                                self.Schneider1 = "No encontrado"
                                capschneider2 = Schneider480[17]
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            elif (Qcap <= Schneider480[0]):
                                self.Schneider2 = "No encontrado"
                                capschneider1 = Schneider480[0]
                                if(capschneider1 <= Qtot):
                                    self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                                else:
                                    self.Schneider1 = "No encontrado"
                        else:
                            self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                            if(capschneider2 <= Qtot):
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            else:
                                self.Schneider2 = "No encontrado"

                        j = 0
                        while ((j < 9)&(condeaton == False)):
                            if ((Eaton480[j] <= Qcap) & (Eaton480[j+1] >= Qcap)):
                                capeaton1 = Eaton480[j]
                                capeaton2 = Eaton480[j+1]
                                condeaton = True
                            j += 1
                        if (condeaton == False):
                            if (Qcap >= Eaton480[9]):
                                self.Eaton1 = "No encontrado"
                                capeaton2 = Eaton480[9]
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            elif (Qcap <= Eaton480[0]):
                                self.Eaton2 = "No encontrado"
                                capeaton1 = Eaton480[0]
                                if(capeaton1 <= Qtot):
                                    self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                                else:
                                    self.Eaton1 = "No encontrado"
                            else:
                                self.Eaton1 = "No encontrado"
                                self.Eaton2 = "No encontrado"
                        else:
                            self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                            if(capeaton2 <= Qtot):
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            else:
                                self.Eaton2 = "No encontrado"
                else:
                    self.Schneider1 = "No encontrado"
                    self.Schneider2 = "No encontrado"
                    self.Eaton1 = "No encontrado"
                    self.Eaton2 = "No encontrado"
                if(self.Schneider1 == "No encontrado"):
                    capschneider1=""
                if(self.Schneider2 == "No encontrado"):
                    capschneider2=""
                if(self.Eaton1 == "No encontrado"):
                    capeaton1=""
                if(self.Eaton2 == "No encontrado"):
                    capeaton2=""
            except:
                self.manager.current = "errorfpnuevo"

        #La función se encarga de calcular la potencia reactiva que necesita el sistema para tener un factor de potencia de 0.98, además busca los bancos de capacitores que se van a desplegar en la pantalla de corrección.
        def calcnuevareactiva98(self):
            try:
                global Qtot
                global cita
                global Stot
                global VFlineaAB
                global capschneider1
                global capschneider2
                global capeaton1
                global capeaton2
                global sentido
                capschneider1=""
                capschneider2=""
                capeaton1=""
                capeaton2=""
                if (sentido == False):
                    Ptot = (abs(Stot))*math.cos(cita)
                    citanuevo = math.acos(0.98)
                    Qnuevo = Ptot * (math.tan(citanuevo))
                    Qcap = Qtot - Qnuevo
                    print(Qnuevo)
                    print(Qcap)
                    if (((abs(VFlineaAB)) < 242) and ((abs(VFlineaAB)) > 238)):
                        condeaton = False
                        condschneider = False
                        i = 0
                        while ((i < 9)&(condschneider == False)):
                            if ((Schneider240[i] <= Qcap) & (Schneider240[i+1] >= Qcap)):
                                capschneider1 = Schneider240[i]
                                capschneider2 = Schneider240[i+1]
                                condschneider = True
                            i += 1
                        if (condschneider == False):
                            if (Qcap >= Schneider240[9]):
                                self.Schneider1 = "No encontrado"
                                capschneider2 = Schneider240[9]
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            elif (Qcap <= Schneider240[0]):
                                self.Schneider2 = "No encontrado"
                                capschneider1 = Schneider240[0]
                                if(capschneider1 <= Qtot):
                                    self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                                else:
                                    self.Schneider1 = "No encontrado"
                            else:
                                self.Schneider1 = "No encontrado"
                                self.Schneider2 = "No encontrado"
                        else:
                            self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                            if(capschneider2 <= Qtot):
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            else:
                                self.Schneider2 = "No encontrado"

                        j = 0
                        while ((j < 7)&(condeaton == False)):
                            if ((Eaton240[j] <= Qcap) & (Eaton240[j+1] >= Qcap)):
                                capeaton1 = Eaton240[j]
                                capeaton2 = Eaton240[j+1]
                                condeaton = True
                            j += 1
                        if (condeaton == False):
                            if (Qcap >= Eaton240[7]):
                                self.Eaton1 = "No encontrado"
                                capeaton2 = Eaton240[7]
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            elif (Qcap <= Eaton240[0]):
                                self.Eaton2 = "No encontrado"
                                capeaton1 = Eaton240[0]
                                if(capeaton1 <= Qtot):
                                    self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                                else:
                                    self.Eaton1 = "No encontrado"
                        else:
                            self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                            if(capeaton2 <= Qtot):
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            else:
                                self.Eaton2 = "No encontrado"

                    elif (((abs(VFlineaAB)) < 482) and ((abs(VFlineaAB)) > 478)):
                        condeaton = False
                        condschneider = False
                        i = 0
                        while ((i < 17)&(condschneider == False)):
                            if ((Schneider480[i] <= Qcap) & (Schneider480[i+1] >= Qcap)):
                                capschneider1 = Schneider480[i]
                                capschneider2 = Schneider480[i+1]
                                condschneider = True
                            i += 1
                        if (condschneider == False):
                            if (Qcap >= Schneider480[17]):
                                self.Schneider1 = "No encontrado"
                                capschneider2 = Schneider480[17]
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            elif (Qcap <= Schneider480[0]):
                                self.Schneider2 = "No encontrado"
                                capschneider1 = Schneider480[0]
                                if(capschneider1 <= Qtot):
                                    self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                                else:
                                    self.Schneider1 = "No encontrado"
                        else:
                            self.Schneider1 = "Banco de " + str((capschneider1)/1000) + " kVAr"
                            if(capschneider2 <= Qtot):
                                self.Schneider2 = "Banco de " + str((capschneider2)/1000) + " kVAr"
                            else:
                                self.Schneider2 = "No encontrado"

                        j = 0
                        while ((j < 9)&(condeaton == False)):
                            if ((Eaton480[j] <= Qcap) & (Eaton480[j+1] >= Qcap)):
                                capeaton1 = Eaton480[j]
                                capeaton2 = Eaton480[j+1]
                                condeaton = True
                            j += 1
                        if (condeaton == False):
                            if (Qcap >= Eaton480[9]):
                                self.Eaton1 = "No encontrado"
                                capeaton2 = Eaton480[9]
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            elif (Qcap <= Eaton480[0]):
                                self.Eaton2 = "No encontrado"
                                capeaton1 = Eaton480[0]
                                if(capeaton1 <= Qtot):
                                    self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                                else:
                                    self.Eaton1 = "No encontrado"
                            else:
                                self.Eaton1 = "No encontrado"
                                self.Eaton2 = "No encontrado"
                        else:
                            self.Eaton1 = "Banco de " + str((capeaton1)/1000) + " kVAr"
                            if(capeaton2 <= Qtot):
                                self.Eaton2 = "Banco de " + str((capeaton2)/1000) + " kVAr"
                            else:
                                self.Eaton2 = "No encontrado"
                else:
                    self.Schneider1 = "No encontrado"
                    self.Schneider2 = "No encontrado"
                    self.Eaton1 = "No encontrado"
                    self.Eaton2 = "No encontrado"
                if(self.Schneider1 == "No encontrado"):
                    capschneider1=""
                if(self.Schneider2 == "No encontrado"):
                    capschneider2=""
                if(self.Eaton1 == "No encontrado"):
                    capeaton1=""
                if(self.Eaton2 == "No encontrado"):
                    capeaton2=""
            except:
                self.manager.current = "errorfpnuevo"

        #Si la persona elige la primera opción de los bancos de capacitores de Eaton, esta es la función que calcula y realiza los cambios en las potencias y fp del sistema.
        def seleccioneaton1(self):
            #Manejo de errores: si falta algún dato o no se han igresado cargas, se muestra una pantalla de error.
            try:
                global capeaton1
                global Qtot
                global cita
                global Stot
                Ptot = (abs(Stot))*math.cos(cita)
                Qcor = Qtot - capeaton1
                citacor = math.atan(Qcor/Ptot)
                fpcor = math.cos(citacor)
                self.fpcortext = str(fpcor)
            except:
                self.manager.current = "errorfpnuevo"

        #Si la persona elige la segunda opción de los bancos de capacitores de Eaton, esta es la función que calcula y realiza los cambios en las potencias y fp del sistema.
        def seleccioneaton2(self):
            #Manejo de errores: si falta algún dato o no se han igresado cargas, se muestra una pantalla de error.
            try:
                global capeaton2
                global Qtot
                global cita
                global Stot
                Ptot = (abs(Stot))*math.cos(cita)
                Qcor = Qtot - capeaton2


                citacor = math.atan(Qcor/Ptot)
                fpcor = math.cos(citacor)
                self.fpcortext = str(fpcor)
            except:
                self.manager.current = "errorfpnuevo"

        #Si la persona elige la primera opción de los bancos de capacitores de Shneider, esta es la función que calcula y realiza los cambios en las potencias y fp del sistema.
        def seleccionschneider1(self):
            #Manejo de errores: si falta algún dato o no se han igresado cargas, se muestra una pantalla de error.
            try:
                global capschneider1
                global Qtot
                global cita
                global Stot
                Ptot = (abs(Stot))*math.cos(cita)
                Qcor = Qtot - capschneider1
                citacor = math.atan(Qcor/Ptot)
                fpcor = math.cos(citacor)
                self.fpcortext = str(fpcor)
            except:
                self.manager.current = "errorfpnuevo"

        #Si la persona elige la segunda opción de los bancos de capacitores de Shneider, esta es la función que calcula y realiza los cambios en las potencias y fp del sistema.
        def seleccionschneider2(self):
            #Manejo de errores: si falta algún dato o no se han igresado cargas, se muestra una pantalla de error.
            try:
                global capschneider2
                global Qtot
                global cita
                global Stot
                Ptot = (abs(Stot))*math.cos(cita)
                Qcor = Qtot - capschneider2
                citacor = math.atan(Qcor/Ptot)
                fpcor = math.cos(citacor)
                self.fpcortext = str(fpcor)
            except:
                self.manager.current = "errorfpnuevo"

        #Esta función se ejecuta para utilizar la base de datos en Bancos.db para mostrar los detalles de los bancos de capacitores.
        def create_database(self):
            try:
                connect_to_database(path)
                con = sqlite3.connect(path)
                cursor = con.cursor()
                global capschneider1
                global capschneider2
                global capeaton1
                global capeaton2
                global control1
                a =np.array(VFlineaAB)
                cursor.execute('select * from Bancos WHERE (Var = "{}" or Var ="{}" or Var ="{}" or Var="{}") and Linea="{}"'.format(capschneider1, capschneider2, capeaton1, capeaton2,control1))
                global rows
                rows=cursor.fetchall()
                arrayd= np.array(rows)
                global nombre
                nombre=""
                for i in range(0,arrayd.size/4):
                    nombre =nombre+"                                                                                 Capacitor {} \n".format(i+1) + "Empresa: {}            ".format(rows[i][0])+"Potencia reactiva: {}            ".format(rows[i][1])+"Voltaje de línea: {}            ".format(rows[i][2])+"Catálogo: {}\n".format(rows[i][3])+" \n"
                con.close()
                if (nombre==""):
                    nombre = "No hay capacitores que sean iguales en la base de datos actual"
                self.manager.current = "database"
            except:
                self.manager.current = "errorfpnuevo"

#Esta es la clase relacionada con la página a la cual se redirecciona al usuario en caso de existir un error en la página en la que se corrige el f.p.
class ErrorPagefpnuevo(Screen):
    pass

#Clase relacionada con la página en la cual se muestran la lista de cargas ingresadas.
class ListaPage(Screen):
    listcharges = StringProperty()
    #Esta función actualiza la lista de las cargas ingresadas a partir de la variable 'lista'.
    def actualizacion(self, ):
        global lista
        print(lista)
        self.listcharges = lista

#Esta clase está relacionada con la página en la cual se muestran los detalles de los bancos de capacitores escogidos según el fp deseado.
class DataBaseWid(Screen):
    listcharges = StringProperty()
    #Esta función se encarga de actualizar la lista de capacitores ofrecidos para corregir el fp del sistema ingresado.
    def actualizacion2(self, ):
        global nombre
        self.listcharges = nombre
    #Función encargada de abrir página de distribuidores de Schneider.
    def linkschneider(self):
        webbrowser.open('https://www.schneider-electric.co.cr/es/locator/?locale=CR_es2&header=se&mxdi=500&locator=networking&poco=all&world_country=Costa%20Rica')
    #Función encargada de abrir página de distribuidores de Eaton.
    def linkeaton(self):
        webbrowser.open('https://comunidadeaton.com/distribuidores/')

#Clase que se encarga de llevar el control de todas las Screens creadas.
class ScreenManagement(ScreenManager):
    pass
kv_file = Builder.load_file('auxiliar.kv')

#Esta clase se encarga de hacer la aplicación final.
class Auxiliar(App):
    def build(self):
        return kv_file
if __name__ == '__main__':
    Auxiliar().run()
