#include "back_functions.hpp"


// Función para validar la entrada de datos
bool validarEntrada(std::string entrada, std::string patron) {
    std::regex regex_patron(patron);
    // En caso de haber coincidencia retorna true, caso opuesto retorna false
    return std::regex_search(entrada, regex_patron);
}


int present_year() {
    // Tiempo actual
    std::time_t currentTime = std::time(nullptr);

    // Calendario
    std::tm* calendarTime = std::localtime(&currentTime);

    // sumando 1900 para obtener el año
    int currentYear = calendarTime->tm_year + 1900;

    return currentYear;
}

void write_data(QString archivo, vector<QString> data){
    QString text;
    text = data[0];
    for(int i=1; i<data.size();i++){
        text.append(","+data[i]); // Se agrega una coma para separar los datos
    }


    QFile file(archivo);
    // Se abre el archivo en modo escritura
    if (file.open(QIODevice::Append)) {
        QTextStream out(&file);
        out << text << "\n";
    }
    file.close();
}

void write_data_delete(const QString& archivo, int lastSelectedRow) {
    QFile file(archivo);

    if (file.open(QIODevice::ReadWrite | QIODevice::Text)) {
        QTextStream stream(&file);
        QStringList lines;

        // Leer todas las líneas del archivo y almacenarlas en una lista
        while (!stream.atEnd()) {
            QString line = stream.readLine();
            lines.append(line);
        }

        // Limpiar el archivo
        file.resize(0);

        // Escribir todas las líneas menos la seleccionada
        for (int i = 0; i < lines.size(); ++i) {
            if (i != lastSelectedRow) {
                stream << lines.at(i) << "\n";
            }
        }
    } else {
        qDebug() << "Failed to open file.";
    }

    file.close();
}

void create_month_db(QString path){
    QString archivo;
    QString mentor_path = path;
    // Se verifica si el path contiene el nombre de la base de datos
    if(mentor_path.indexOf("_month.db") == std::string::npos){
        archivo = mentor_path.replace(".txt","_month.db");
    } else {
        archivo = mentor_path;
    }
    // Se crea la base de datos
    QSqlDatabase database = QSqlDatabase::addDatabase("QSQLITE");
    database.setDatabaseName(archivo);

    if (!database.open()) {
        qDebug() << "Failed to open database:";
    }

    QSqlQuery query(database);

    // Se crea la tabla
    QString createTableQuery = "CREATE TABLE IF NOT EXISTS myTable ("
                               "year INTEGER, "
                               "month TEXT, "
                               "text TEXT"
                               ");";
    if (!query.exec(createTableQuery)) {
        qDebug() << "Failed to execute query:";
    } else {
        qDebug() << "Table created successfully!";
    }
    database.close();
}

void create_task_db(QString path){
    QString archivo;
    QString mentor_path = path;
    if(mentor_path.indexOf("_task.db") == std::string::npos){
        archivo = mentor_path.replace(".txt","_task.db");
    } else {
        archivo = mentor_path;
    }
    QSqlDatabase database = QSqlDatabase::addDatabase("QSQLITE", "task_connection");
    // Se crea la base de datos
    database.setDatabaseName(archivo);

    if (!database.open()) {
        qDebug() << "Failed to open database:";
    }
    
    // Query para ejecutar comandos en la base de datos
    QSqlQuery query(database);

    QString createTableQuery = "CREATE TABLE IF NOT EXISTS tableTask ("
                               "task TEXT "
                               ");";
    if (!query.exec(createTableQuery)) {
        qDebug() << "Failed to execute query:";
    } else {
        qDebug() << "Table created successfully!";
    }
    database.close();
}

QStringList read_text_column(const QString& path) {
    QStringList textList;
    QString archivo;
    QString mentor_path = path;

    if (mentor_path.indexOf("_month.db") == std::string::npos) {
        archivo = mentor_path.replace(".txt", "_month.db");
    } else {
        archivo = mentor_path;
    }

    QSqlDatabase database = QSqlDatabase::database();
    database.setDatabaseName(archivo);

    if (!database.open()) {
        qDebug() << "Failed to open database:";
    }

    QSqlQuery query(database);
    // Se selecciona la columna text de la tabla myTable
    QString selectQuery = "SELECT text FROM myTable";

    if (!query.exec(selectQuery)) {
        qDebug() << "Failed to execute query:";
    } else {
        while (query.next()) {
            QString text = query.value("text").toString();
            textList.append(text); // Se agrega el texto a la lista
        }
    }

    database.close();
    textList.removeDuplicates();
    return textList;
}

void create_wiki_db(QString path){
    QString archivo;
    QString wiki_path = path;
    if(wiki_path.indexOf("_task.db") == std::string::npos){
        archivo = wiki_path.replace(".txt","_wiki.db");
    } else {
        archivo = wiki_path;
    }
    QSqlDatabase database = QSqlDatabase::database();
    database.setDatabaseName(archivo);

    if (!database.open()) {
        qDebug() << "Failed to open database:";
    }

    QSqlQuery query(database);
    // Se crea la tabla
    QString createTableQuery = "CREATE TABLE IF NOT EXISTS wiki ("
                               "concepto TEXT, "
                               "mes TEXT, "
                               "definicion TEXT "
                               ");";
    query.exec(createTableQuery);
    database.close();
}
