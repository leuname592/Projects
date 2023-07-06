/**
 * @file class.hpp
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
 * @brief Esta clase se usa para manejar los datos de la ventana wiki
 * 
 */
class wiki{
    private:
        QString concept;
        QString definition;
    public:
        wiki();
        wiki(QString concept, QString definition);
        void setConcept(QString concept);
        void setDefinition(QString definition);
        QString getConcept();
        QString getDefinition();
};

/**
 * @brief Esta clase se usa para manejar los datos de la ventana de metas mensuales
 * 
 */
class MetaMensual{
    private:
        QString mes;
        int year;
        QString meta;
    public:
        MetaMensual();
        MetaMensual(QString mes, int year, QString meta);
        void setMes(QString mes);
        void setYear(int year);
        void setMeta(QString meta);
        QString getMes();
        int getYear();
        QString getMeta();
};

/**
 * @brief Esta clase se usa para manejar los datos de la ventana de mentores
 * 
 */
class Mentores{
    private:
        QString nombre;
        QString contacto;
    public:
        Mentores();
        Mentores(QString nombre, QString contacto);
        void setNombre(QString nombre);
        void setContacto(QString contacto);
        QString getNombre();
        QString getContacto();
};


/**
 * @brief Esta clase se usa para manejar los datos de la ventana de tareas
 * 
 */
class Tareas{
    private:
        QString tarea;
    public:
        Tareas();
        Tareas(QString tarea);
        void setTarea(QString tarea);
        QString getTarea();
};

/**
 * @brief Esta clase se usa para manejar los datos de la ventana de matriz de años
 * 
 */
class Matriz{
    private:
        int year_inicio;
        int year_fin;
        QString meta;
    public:
        Matriz();
        Matriz(int year_inicio, int year_fin, QString meta);
        void setYear_inicio(int year_inicio);
        void setYear_fin(int year_fin);
        void setMeta(QString meta);
        int getYear_inicio();
        int getYear_fin();
        QString getMeta();

};
