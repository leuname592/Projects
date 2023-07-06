/**
 * @file back_functions.hpp
 * @author Emmanuel Chavarria Solis (leuname592@hotmail.com)
 * @brief 
 * @version 0.1
 * @date 2023-07-04
 * 
 * @copyright MIT
 * 
 */
#include "includes.hpp"

/**
 * @brief Esta funcion usa un regex para validar si el formato de entrada es el deseado
 * 
 * @param entrada string a comparar
 * @param patron Patron contra el que se va a comparar
 * @return true 
 * @return false 
 */
bool validarEntrada(std::string entrada, std::string patron);

/**
 * @brief Esta función devuelve el año actual
 * 
 * @return int año actual
 */
int present_year();

/**
 * @brief Escribe data en un archivo, se usa como base de datos
 * 
 * @param archivo ruta a la base de datos en este caso se uso un archivo .txt
 * @param data La data a ser escrita en la base de datos
 */
void write_data(QString archivo, vector<QString> data);

/**
 * @brief Crear un objeto de tipo base de datos para los meses
 * 
 * @param path Path a la base de datos
 */
void create_month_db(QString path);

/**
 * @brief Esta funcion se encarga de copiar la base de datos excepto la linea en la que se encuentra el usuario, tiene como funcionalidad eliminar datos
 * 
 * @param archivo Ruta a la base de datos
 * @param lastSelectedRow Linea que se va a eliminar
 */
void write_data_delete(const QString& archivo, int lastSelectedRow);

/**
 * @brief Crear un objeto de tipo base de datos para las tareas
 * 
 * @param path Path a la base de datos para las tareas
 */
void create_task_db(QString path);

/**
 * @brief Funcion para leer una columna de texto de una base de datos y actualizar los meses en la pagina wiki 
 * 
 * @param path a la base de datos
 * @return QStringList 
 */
QStringList read_text_column(const QString& path);

/**
 * @brief Crear un objeto wiki de tipo base de datos
 * 
 * @param path Path a la base de datos del wiki
 */
void create_wiki_db(QString path);
