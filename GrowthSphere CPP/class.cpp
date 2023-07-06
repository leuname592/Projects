#include "class.hpp"
#include "includes.hpp"


// Se defnen los metodos de las clases usadas en el backend
wiki::wiki(){
    concept = "";
    definition = "";
}
wiki::wiki(QString concept, QString definition){
    this->concept = concept;
    this->definition = definition;
}
void wiki::setConcept(QString concept){
    this->concept = concept;
}
void wiki::setDefinition(QString definition){
    this->definition = definition;
}
QString wiki::getConcept(){
    return concept;
}
QString wiki::getDefinition(){
    return definition;
}

MetaMensual::MetaMensual(){
    mes = "";
    year = 0;
    meta = "";
}
MetaMensual::MetaMensual(QString mes, int year, QString meta){
    this->mes = mes;
    this->year = year;
    this->meta = meta;
}

void MetaMensual::setMes(QString mes){
    this->mes = mes;
}

void MetaMensual::setYear(int year){
    this->year = year;
}

void MetaMensual::setMeta(QString meta){
    this->meta = meta;
}

QString MetaMensual::getMes(){
    return mes;
}

int MetaMensual::getYear(){
    return year;
}

QString MetaMensual::getMeta(){
    return meta;
}

Mentores::Mentores(){
    nombre = "";
    contacto = "";
}

Mentores::Mentores(QString nombre, QString contacto){
    this->nombre = nombre;
    this->contacto = contacto;
}

void Mentores::setNombre(QString nombre){
    this->nombre = nombre;
}

void Mentores::setContacto(QString contacto){
    this->contacto = contacto;
}

QString Mentores::getNombre(){
    return nombre;
}

QString Mentores::getContacto(){
    return contacto;
}


Tareas::Tareas(){
    tarea="";
}

Tareas::Tareas(QString tarea){
    this->tarea = tarea;
}

void Tareas::setTarea(QString tarea){
    this->tarea = tarea;
}

QString Tareas::getTarea(){
    return tarea;
}

Matriz::Matriz(){
    year_inicio = 0;
    year_fin = 0;
    meta = "";
}

Matriz::Matriz(int year_inicio, int year_fin, QString meta){
    this->year_inicio = year_inicio;
    this->year_fin = year_fin;
    this->meta = meta;
}

void Matriz::setYear_inicio(int year_inicio){
    this->year_inicio = year_inicio;
}

void Matriz::setYear_fin(int year_fin){
    this->year_fin = year_fin;
}

void Matriz::setMeta(QString meta){
    this->meta = meta;
}

int Matriz::getYear_inicio(){
    return year_inicio;
}

int Matriz::getYear_fin(){
    return year_fin;
}

QString Matriz::getMeta(){
    return meta;
}