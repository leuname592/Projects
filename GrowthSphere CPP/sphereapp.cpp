/**
 * @file sphereapp.cpp
 * @author Emmanuel Chavarria Solis (leuname592@hotmail.com)
 * @brief Se especifican los métodos de la clase sphereApp
 * @version 0.1
 * @date 2023-06-25
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "sphereapp.h"
#include "ui_sphereapp.h"
#include "back_functions.hpp"
#include "includes.hpp"
#include "class.hpp"

sphereApp::sphereApp(QString path,QString year_ext,QWidget *parent) :
    year_ext(year_ext),
    path(path),
    QWidget(parent),
    ui(new Ui::sphereApp)
{
    // Inicializar la interfaz grafica con valores deseados
    ui->setupUi(this);
    ui->set_goal->setCursor(Qt::PointingHandCursor);
    ui->startCrono->setCursor(Qt::PointingHandCursor);
    ui->resetCrono->setCursor(Qt::PointingHandCursor);
    ui->guardar_mes->setCursor(Qt::PointingHandCursor);
    ui->leer_mes->setCursor(Qt::PointingHandCursor);
    ui->colocar->setCursor(Qt::PointingHandCursor);
    ui->guardar_mentor->setCursor(Qt::PointingHandCursor);
    ui->eliminar_mentor->setCursor(Qt::PointingHandCursor);
    ui->guardar_wiki->setCursor(Qt::PointingHandCursor);
    ui->buscar_wiki->setCursor(Qt::PointingHandCursor);
    ui->Enero->setCursor(Qt::PointingHandCursor);
    ui->Febrero->setCursor(Qt::PointingHandCursor);
    ui->Marzo->setCursor(Qt::PointingHandCursor);
    ui->Abril->setCursor(Qt::PointingHandCursor);
    ui->Mayo->setCursor(Qt::PointingHandCursor);
    ui->Junio->setCursor(Qt::PointingHandCursor);
    ui->Julio->setCursor(Qt::PointingHandCursor);
    ui->Agosto->setCursor(Qt::PointingHandCursor);
    ui->Septiembre->setCursor(Qt::PointingHandCursor);
    ui->Octubre->setCursor(Qt::PointingHandCursor);
    ui->Noviembre->setCursor(Qt::PointingHandCursor);
    ui->Diciembre->setCursor(Qt::PointingHandCursor);
    ui->colocar_2->setCursor(Qt::PointingHandCursor);
    ui->eliminar_wiki->setCursor(Qt::PointingHandCursor);

    QString currentPath = QDir::currentPath();
    int w =ui->logo_matrix->width();
    int h =ui->logo_matrix->height();
    QPixmap pix(currentPath+"/images/logo.png");
    ui->logo_matrix->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));
    ui->logo_anual->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));
    ui->logo_mensual->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));
    ui->logo_wiki->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));
    ui->logo_task->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));
    ui->logo_cron->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));
    ui->logo_mentor->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));
    ui->logo_time->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));


    ui->cronoSlider->setMinimum(0);
    ui->cronoSlider->setMaximum(60);

    w =ui->suntzu->width();
    h =ui->suntzu->height();
    QPixmap pix_suntzu(currentPath+"/images/suntzu.png");
    ui->suntzu->setPixmap(pix_suntzu.scaled(w,h,Qt::KeepAspectRatio));

    w =ui->bird->width();
    h =ui->bird->height();
    QPixmap pix_bird(currentPath+"/images/bird.png");
    ui->bird->setPixmap(pix_bird.scaled(w,h,Qt::KeepAspectRatio));

    ui->tablaMentores->horizontalHeader()->setStretchLastSection(true);
    ui->tablaWiki->horizontalHeader()->setStretchLastSection(true);

    QStringList options = { "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre" };
    ui->meses->addItems(options);

    QStringList headerLabels;
    headerLabels << "Nombre" << "Información de Contacto";
    ui->tablaMentores->setHorizontalHeaderLabels(headerLabels);

    ui->tablaTareas->setHorizontalHeaderLabels(QStringList("Tareas"));
    ui->tablaTareas->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);

    ui->tablaWiki->setHorizontalHeaderLabels(QStringList({"Concepto","Meta","Definicion"}));

    QDateTime targetDateTime;
    targetDateTime.setDate(QDate(present_year()-year_ext.toInt()+80, 12, 31));
    targetDateTime.setTime(QTime(23, 59, 59));

    // Qtimer para llevar el conteo del tiempo
    QTimer* countdownTimer = new QTimer(this);
    countdownTimer->setInterval(1000);
    connect(countdownTimer, &QTimer::timeout, this, [=]() {
        QDateTime currentDateTime = QDateTime::currentDateTime();
        qint64 remainingTime = currentDateTime.msecsTo(targetDateTime);

        QDateTime targetHour = QDateTime::currentDateTime();
        targetHour.setTime(QTime(23, 59, 59));
        qint64 remainingHour = currentDateTime.msecsTo(targetHour);
        qint64 hours_left = remainingHour / 1000 / 60 / 60;
        if (remainingTime <= 0) {
            countdownTimer->stop();
        } else {
            // Calcular segundos, minutos, horas
            qint64 seconds = remainingTime / 1000;
            qint64 minutes = seconds / 60;
            qint64 hours = minutes / 60;

            // Formatear timer
            QString formattedTime = QString("%1:%2:%3")
                                        .arg(hours_left, 2, 10, QLatin1Char('0'))
                                        .arg(minutes % 60, 2, 10, QLatin1Char('0'))
                                        .arg(seconds % 60, 2, 10, QLatin1Char('0'));

            QDateTime remainingDateTime = QDateTime::fromMSecsSinceEpoch(remainingTime);
            // Formatear meses
            int remainingMonths = remainingDateTime.date().month();
            QString formattedMonths = QString("%1 meses").arg(remainingMonths-1);

            //Formatear años
            int remainingYears = remainingDateTime.date().year() - QDate::currentDate().year()+(present_year()-1970)-1;
            QString formattedYears = QString("%1 años").arg(remainingYears);

            // Update el label con el tiempo
            ui->timeLabel->setText(formattedTime);
            ui->yearLabel->setText(formattedYears);
            ui->monthLabel->setText(formattedMonths);
        }
    });

    // Empezar el timer
    countdownTimer->start();


    QPushButton* startCrono = ui->startCrono;
    QPushButton* resetCrono = ui->resetCrono;
    QLabel* cronoLabel = ui->cronoLabel;
    QSlider* cronoSlider = ui->cronoSlider;
    QTimer* countdownCrono = new QTimer;

    QObject::connect(startCrono, &QPushButton::clicked, [startCrono, resetCrono, cronoLabel, cronoSlider, countdownCrono]() {
        startCrono->setEnabled(false);
        resetCrono->setEnabled(true);

        cronoSlider->setMinimum(0);
        cronoSlider->setMaximum(60);

        int countdownDuration = cronoSlider->value();
        if (countdownDuration==0){
            countdownDuration=1;
        }

        QTime startTime = QTime::currentTime();
        QTime endTime = startTime.addSecs(countdownDuration * 60);

        countdownCrono->setInterval(1000);

        QObject::connect(countdownCrono, &QTimer::timeout, [startCrono, resetCrono, startTime, endTime, cronoLabel, countdownCrono]() {
            QTime currentTime = QTime::currentTime();
            int remainingTime = currentTime.secsTo(endTime);

            if (remainingTime <= 0) {
                countdownCrono->stop();
                cronoLabel->setText("00:00");
                startCrono->setEnabled(true);
                resetCrono->setEnabled(false);
            } else {
                QTime time(0, remainingTime / 60, remainingTime % 60);
                cronoLabel->setText(time.toString("mm:ss"));
            }
        });

        countdownCrono->start(); // Empieza el cronometro
    });

    QObject::connect(resetCrono, &QPushButton::clicked, [resetCrono, startCrono, countdownCrono]() {
        countdownCrono->stop();
        resetCrono->setEnabled(false);
        startCrono->setEnabled(true);
    });


    // Conectar con la base de datos
    create_month_db(path);
    create_task_db(path);
    create_wiki_db(path);
}

sphereApp::~sphereApp()
{
    delete ui;
}

void sphereApp::on_cronoSlider_valueChanged(int value)
{
    ui->cronoLabel->setText( QString("%1:00").arg(value));
}


void sphereApp::on_set_goal_clicked()
{
    Matriz Matriz;
    int year_inicio = ui->dateEdit_inicio->date().year();
    Matriz.setYear_inicio(ui->dateEdit_inicio->date().year());
    Matriz.setYear_fin(ui->dateEdit_final->date().year());
    if (year_inicio>Matriz.getYear_fin()){
        ui->warningAnual->setText("Problema al ingresar años");
        return;
    }
    else{
        ui->warningAnual->setText("");
    }
    if (Matriz.getYear_fin()>(present_year()-year_ext.toInt()+80)-2){
        ui->warningAnual->setText("Problema al ingresar años");
        return;
    }
    else{
        ui->warningAnual->setText("");
    }
    if (year_inicio<(present_year()-year_ext.toInt()-1)){
        ui->warningAnual->setText("Problema al ingresar años");
        return;
    }
    else{
        ui->warningAnual->setText("");
    }

    Matriz.setMeta(ui->textEdit->toPlainText());
    QString line;
    qDebug()<<path;
    QFile file(path);
    if (file.open(QIODevice::Append)) {
        QTextStream out(&file);
        for(int i = year_inicio-(present_year()-year_ext.toInt())+2;i<=Matriz.getYear_fin()-(present_year()-year_ext.toInt())+2;i++){
            line = QString("matrix_%1").arg(i)+","+QString("%1").arg(Matriz.getYear_inicio())+","+Matriz.getMeta(); // Se inician los valores de los botones en la matriz de  botones
            try{
            out << line << "\n";
            }
            catch(const std::exception& e){
                qDebug() << e.what();
                return;
            }
            Matriz.setYear_inicio(Matriz.getYear_inicio()+1);
        }

    }
    file.close();
}


void sphereApp::on_tabWidget_tabBarClicked(int index)
{
    QFile file(path);
    if (file.exists()) {
        if (file.open(QIODevice::ReadOnly)) {
            QTextStream in(&file);
            while (!in.atEnd()) {
                QString line = in.readLine(); // Cada linea siendo leida

                QStringList values = line.split(","); // Partir en el delimitador ","
                QString boton = values[0];
                QString year = values[1];
                QString texto = values[2];

                if (values.size() >= 1) {
                    QString buttonName = boton;
                    QPushButton* button = findChild<QPushButton*>(buttonName);
                    button->setText(QString("%1\n").arg(year)+texto);
                    // Se coloca el stylesheet de los botones
                    button->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(16, 104, 60);color: white;border-radius: 10px;}QPushButton:hover {background-color: rgb(81, 81, 81);border-color: rgb(81, 81, 81);}");
                }
            }
            file.close();
        } else {
            qDebug() << "Failed to open file for reading";
        }
    }


    QString archivo;
    QString mentor_path = path;
    if(path.indexOf("mentores.txt") == std::string::npos){
        archivo = mentor_path.replace(".txt","_mentores.txt");
    } else {
        archivo = mentor_path;
    }
    qDebug()<<archivo;
    ui->tablaMentores->setRowCount(0);

    QFile file_mentor(archivo);
    if (file_mentor.exists()) {
        if (file_mentor.open(QIODevice::ReadOnly)) {
            QTextStream in(&file_mentor);
            while (!in.atEnd()) {
                QString line = in.readLine(); // Cada linea siendo leida
                QStringList values = line.split(","); // Partir en el delimitador ","
                if (values.size() >= 1) {

                    // Agregar una fila
                    int row = ui->tablaMentores->rowCount();
                    ui->tablaMentores->setRowCount(row + 1);
                    ui->tablaMentores->setItem(row, 0, new QTableWidgetItem(values[0]));
                    ui->tablaMentores->setItem(row, 1, new QTableWidgetItem(values[1]));


                    // Actualizar la tabla
                    ui->tablaMentores->update();
                }
            }
            file_mentor.close();
        }
    }

    QString eliminar_task_path = path;
    if(eliminar_task_path.indexOf("_task.db") == std::string::npos){
        archivo = eliminar_task_path.replace(".txt","_task.db");
    } else {
        archivo = eliminar_task_path;
    }
    QSqlDatabase database = QSqlDatabase::database("task_connection");
    database.setDatabaseName(archivo);

    database.open();
    QSqlQuery query(database);
    query.prepare("SELECT * FROM tableTask");
    ui->tablaTareas->setRowCount(0);
    if (query.exec()) {
        while (query.next()) {
            // Obtener valores de la busqueda
            QString task = query.value("task").toString();
            int row = ui->tablaTareas->rowCount();
            ui->tablaTareas->setRowCount(row + 1);
            ui->tablaTareas->setItem(row, 0, new QTableWidgetItem(task));
            ui->tablaTareas->update();
        }
    } else {
        qDebug() << "Failed to execute query:";
    }
    database.close();


    QString wiki_path = path;
    if(wiki_path.indexOf("_wiki.db") == std::string::npos){
        archivo = wiki_path.replace(".txt","_wiki.db");
    } else {
        archivo = wiki_path;
    }
    QSqlDatabase databaseWiki = QSqlDatabase::database();
    databaseWiki.setDatabaseName(archivo);

    databaseWiki.open();
    QSqlQuery queryWiki(databaseWiki);
    queryWiki.prepare("SELECT * FROM wiki");
    ui->tablaWiki->setRowCount(0);
    if (queryWiki.exec()) {
        while (queryWiki.next()) {
            // Obtener valores de la busqueda
            QString concepto_r = queryWiki.value("concepto").toString();
            QString mes_r = queryWiki.value("mes").toString();
            QString definicion_r = queryWiki.value("definicion").toString();
            int row = ui->tablaWiki->rowCount();
            ui->tablaWiki->setRowCount(row + 1);
            ui->tablaWiki->setItem(row, 0, new QTableWidgetItem(concepto_r));
            ui->tablaWiki->setItem(row, 1, new QTableWidgetItem(mes_r));
            ui->tablaWiki->setItem(row, 2, new QTableWidgetItem(definicion_r));
            ui->tablaWiki->update();
        }
    } else {
        qDebug() << "Failed to execute query:";
    }
    // Close the database connection
    databaseWiki.close();

    ui->meses_text->clear();
    QStringList wiki_month = read_text_column(path);
    ui->meses_text->addItems(wiki_month);

}


void sphereApp::on_guardar_mentor_clicked()
{
    Mentores Mentores;
    Mentores.setNombre(ui->nombre_mentor->text());
    Mentores.setContacto(ui->contacto_info->text());
    vector<QString> data;
    QString archivo;
    QString mentor_path = path;
    if(path.indexOf("mentores.txt") == std::string::npos){
        archivo = mentor_path.replace(".txt","_mentores.txt");
    } else {
        archivo = mentor_path;
    }
    data.push_back(Mentores.getNombre());
    data.push_back(Mentores.getContacto());
    write_data(archivo, data);

    ui->tablaMentores->setRowCount(0);
    QFile file(archivo);
    if (file.exists()) {
        if (file.open(QIODevice::ReadOnly)) {
            QTextStream in(&file);
            while (!in.atEnd()) {
                QString line = in.readLine(); // Cada linea siendo leida
                QStringList values = line.split(","); // Partir en el delimitador ","
                if (values.size() >= 1) {

                    int row = ui->tablaMentores->rowCount();
                    ui->tablaMentores->setRowCount(row + 1);
                    ui->tablaMentores->setItem(row, 0, new QTableWidgetItem(values[0]));
                    ui->tablaMentores->setItem(row, 1, new QTableWidgetItem(values[1]));


                    // Actualizar la tabla
                    ui->tablaMentores->update();
                }
            }
            file.close();
        }
    }
}


void sphereApp::on_eliminar_clicked()
{
    int rowIndex = ui->tablaMentores->currentRow();
    qDebug() << "Selected Row Index: " << rowIndex;
}

void sphereApp::on_guardar_mes_clicked()
{
    MetaMensual MetaMensual;
    MetaMensual.setMeta(ui->textMonth->toPlainText());
    MetaMensual.setMes(ui->meses->currentText());
    MetaMensual.setYear(ui->year_mes->date().year());

    if (MetaMensual.getYear()>(present_year()-year_ext.toInt()+80)-2){
        ui->warningMensual->setText("Problema en el rango anual");
        return;
    }
    else{
        ui->warningMensual->setText("");
    }
    if (MetaMensual.getYear()<(present_year()-year_ext.toInt()-1)){
        ui->warningMensual->setText("Problema en el rango anual");
        return;
    }
    else{
        ui->warningMensual->setText("");
    }

    QString archivo;
    QString mentor_path = path;
    if(path.indexOf("_month.db") == std::string::npos){
        archivo = mentor_path.replace(".txt","_month.db");
    } else {
        archivo = mentor_path;
    }
    QSqlDatabase database = QSqlDatabase::database();
    database.setDatabaseName(archivo);

    if (!database.open()) {
        qDebug() << "Failed to open database:";
        return;
    }

    // Crear query para inserción de info
    QSqlQuery query(database);
    query.prepare("DELETE FROM myTable WHERE year = :year AND month = :month");
    query.bindValue(":year", MetaMensual.getYear());
    query.bindValue(":month", MetaMensual.getMes());
    if (!query.exec()) {
        qDebug() << "Failed to execute query:";
    } else {
        qDebug() << "Row inserted successfully!";
    }
    QString insertQuery = "INSERT INTO myTable (year, month, text) VALUES (:year, :month, :text)";
    query.prepare(insertQuery);
    query.bindValue(":year", MetaMensual.getYear());
    query.bindValue(":month", MetaMensual.getMes());
    query.bindValue(":text", MetaMensual.getMeta());

    if (!query.exec()) {
        qDebug() << "Failed to execute query:";
    } else {
        qDebug() << "Row inserted successfully!";
    }

    // Cerrar db
    database.close();
}


void sphereApp::on_leer_mes_clicked()
{
    int year = ui->year_mes->date().year();

    QString archivo;
    QString mentor_path = path;
    if(path.indexOf("_month.db") == std::string::npos){
        archivo = mentor_path.replace(".txt","_month.db");
    } else {
        archivo = mentor_path;
    }
    QSqlDatabase database = QSqlDatabase::database();
    database.setDatabaseName(archivo);

    if (!database.open()) {
        qDebug() << "Failed to open database:";
        return;
    }

    // Create a query to insert a row of information
    QSqlQuery query(database);
    query.prepare("SELECT * FROM myTable WHERE year = :year");
    query.bindValue(":year", year);

    // Se setean los stylesheets de los botones meses 
    ui->Enero->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Enero->setText(QString("Enero"));
    ui->Febrero->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Febrero->setText(QString("Febrero"));
    ui->Marzo->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Marzo->setText(QString("Marzo"));
    ui->Abril->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Abril->setText(QString("Abril"));
    ui->Mayo->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Mayo->setText(QString("Mayo"));
    ui->Junio->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Junio->setText(QString("Junio"));
    ui->Julio->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Julio->setText(QString("Julio"));
    ui->Agosto->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Agosto->setText(QString("Agosto"));
    ui->Septiembre->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Septiembre->setText(QString("Septiembre"));
    ui->Octubre->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Octubre->setText(QString("Octubre"));
    ui->Noviembre->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Noviembre->setText(QString("Noviembre"));
    ui->Diciembre->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(67, 195, 209);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
    ui->Diciembre->setText(QString("Diciembre"));

    if (query.exec()) {
        while (query.next()) {
            // Obtener valores de la busqueda
            QString month = query.value("month").toString();
            QString text = query.value("text").toString();

            QString buttonName = month;
            QPushButton* button = findChild<QPushButton*>(buttonName);
            button->setText(QString(month+": "+text));
            button->setStyleSheet("QPushButton {text-align: left;font: 12pt \"Segoe UI\";border: none;background-color: rgb(255, 138, 134);color: rgb(47, 47, 47);border-radius: 10px;}QPushButton:hover {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}QPushButton:pressed {background-color: rgb(199, 199, 199);border-color: rgb(81, 81, 81);}");
        }
    } else {
        qDebug() << "Failed to execute query:";
    }
    database.close();
}


void sphereApp::on_Noviembre_clicked()
{
    QPushButton* Noviembre = ui->Noviembre;
    QString buttonText = Noviembre->text();
    QMessageBox::information(nullptr, "Meta de Noviembre: ", buttonText);
}


void sphereApp::on_Enero_clicked()
{
    QPushButton* Enero = ui->Enero;
    QString buttonText = Enero->text();
    QMessageBox::information(nullptr, "Meta de Enero: ", buttonText);
}


void sphereApp::on_Febrero_clicked()
{
    QPushButton* Febrero = ui->Febrero;
    QString buttonText = Febrero->text();
    QMessageBox::information(nullptr, "Meta de Febrero: ", buttonText);
}


void sphereApp::on_Marzo_clicked()
{
    QPushButton* Marzo = ui->Marzo;
    QString buttonText = Marzo->text();
    QMessageBox::information(nullptr, "Meta de Marzo: ", buttonText);
}


void sphereApp::on_Abril_clicked()
{
    QPushButton* Abril = ui->Abril;
    QString buttonText = Abril->text();
    QMessageBox::information(nullptr, "Meta de Abril: ", buttonText);
}


void sphereApp::on_Mayo_clicked()
{
    QPushButton* Mayo = ui->Mayo;
    QString buttonText = Mayo->text();
    QMessageBox::information(nullptr, "Meta de Mayo: ", buttonText);
}


void sphereApp::on_Junio_clicked()
{
    QPushButton* Junio = ui->Junio;
    QString buttonText = Junio->text();
    QMessageBox::information(nullptr, "Meta de Junio: ", buttonText);
}


void sphereApp::on_Julio_clicked()
{
    QPushButton* Julio = ui->Julio;
    QString buttonText = Julio->text();
    QMessageBox::information(nullptr, "Meta de Julio: ", buttonText);
}


void sphereApp::on_Agosto_clicked()
{
    QPushButton* Agosto = ui->Agosto;
    QString buttonText = Agosto->text();
    QMessageBox::information(nullptr, "Meta de Agosto: ", buttonText);
}


void sphereApp::on_Septiembre_clicked()
{
    QPushButton* Septiembre = ui->Septiembre;
    QString buttonText = Septiembre->text();
    QMessageBox::information(nullptr, "Meta de Septiembre: ", buttonText);
}


void sphereApp::on_Octubre_clicked()
{
    QPushButton* Octubre = ui->Octubre;
    QString buttonText = Octubre->text();
    QMessageBox::information(nullptr, "Meta de Octubre: ", buttonText);
}


void sphereApp::on_Diciembre_clicked()
{
    QPushButton* Diciembre = ui->Diciembre;
    QString buttonText = Diciembre->text();
    QMessageBox::information(nullptr, "Meta de Diciembre: ", buttonText);
}


void sphereApp::on_eliminar_mentor_clicked()
{
    QString archivo;
    QString mentor_path = path;
    if(path.indexOf("mentores.txt") == std::string::npos){
        archivo = mentor_path.replace(".txt","_mentores.txt");
    } else {
        archivo = mentor_path;
    }
    int lastSelectedRow = ui->tablaMentores->currentRow();
    write_data_delete(archivo, lastSelectedRow);
    ui->tablaMentores->setRowCount(0);
    QFile file(archivo);
    if (file.exists()) {
        if (file.open(QIODevice::ReadOnly)) {
            QTextStream in(&file);
            while (!in.atEnd()) {
                QString line = in.readLine(); // Cada linea siendo leida
                QStringList values = line.split(","); // Partir en el delimitador ","
                if (values.size() >= 1) {

                    int row = ui->tablaMentores->rowCount();
                    ui->tablaMentores->setRowCount(row + 1);
                    ui->tablaMentores->setItem(row, 0, new QTableWidgetItem(values[0]));
                    ui->tablaMentores->setItem(row, 1, new QTableWidgetItem(values[1]));


                    // Actualizar la tabla
                    ui->tablaMentores->update();
                }
            }
            file.close();
        }
    }
}


void sphereApp::on_colocar_clicked()
{
    QString archivo;
    QString task_path = path;
    Tareas Tareas;
    Tareas.setTarea(ui->taskw->text());
    if(task_path.indexOf("_task.db") == std::string::npos){
        archivo = task_path.replace(".txt","_task.db");
    } else {
        archivo = task_path;
    }
    QSqlDatabase database = QSqlDatabase::database("task_connection");
    qDebug()<<archivo;
    database.setDatabaseName(archivo);

    if (!database.open()) {
        qDebug() << "Failed to open database:";
    }
    QSqlQuery query(database);
    QString insertQuery = "INSERT INTO tableTask (task) VALUES (:task)";
    query.prepare(insertQuery);
    query.bindValue(":task", Tareas.getTarea());
    // Se ejecuta el query
    if (!query.exec()) {
        qDebug() << "Failed to execute query:";
    } else {
        qDebug() << "Row inserted successfully!";
    }


    query.prepare("SELECT * FROM tableTask");
    ui->tablaTareas->setRowCount(0);
    if (query.exec()) {
        while (query.next()) {
            // Obtener valores de la busqueda
            QString task = query.value("task").toString();
            int row = ui->tablaTareas->rowCount();
            ui->tablaTareas->setRowCount(row + 1);
            ui->tablaTareas->setItem(row, 0, new QTableWidgetItem(task));
            ui->tablaTareas->update();
        }
    } else {
        qDebug() << "Failed to execute query:";
    }


    // Cerrar db
    database.close();
}


void sphereApp::on_colocar_2_clicked()
{
    QString archivo;
    QString eliminar_task_path = path;
    QString task_text=ui->taskw->text();
    if(eliminar_task_path.indexOf("_task.db") == std::string::npos){
        archivo = eliminar_task_path.replace(".txt","_task.db");
    } else {
        archivo = eliminar_task_path;
    }

    QSqlDatabase database = QSqlDatabase::database("task_connection");
    database.setDatabaseName(archivo);

    if (!database.open()) {
        qDebug() << "Failed to open database:";
    }
    QSqlQuery query(database);
    QString deleteQuery = "DELETE FROM tableTask WHERE task = :value";
    query.prepare(deleteQuery);
    query.bindValue(":value", task_text);
    if (!query.exec()) {
        qDebug() << "Failed to execute query:";
    } else {
        qDebug() << "Row inserted successfully!";
    }

    query.prepare("SELECT * FROM tableTask");
    ui->tablaTareas->setRowCount(0);
    if (query.exec()) {
        while (query.next()) {
            // Obtener valores de la busqueda
            QString task = query.value("task").toString();
            int row = ui->tablaTareas->rowCount();
            ui->tablaTareas->setRowCount(row + 1);
            ui->tablaTareas->setItem(row, 0, new QTableWidgetItem(task));
            ui->tablaTareas->update();
        }
    } else {
        qDebug() << "Failed to execute query:";
    }


    // Close the database connection
    database.close();
}


void sphereApp::on_guardar_wiki_clicked()
{
    wiki Wiki;
    QString concepto = ui->concepto->text();
    QString definicion = ui->definicion->toPlainText();
    QString mes = ui->meses_text->currentText();
    Wiki.setConcept(concepto);
    Wiki.setDefinition(definicion);

    QString archivo;
    QString wiki_path = path;
    if(wiki_path.indexOf("_wiki.db") == std::string::npos){
        archivo = wiki_path.replace(".txt","_wiki.db");
    } else {
        archivo = wiki_path;
    }
    QSqlDatabase database = QSqlDatabase::database();
    database.setDatabaseName(archivo);

    database.open();
    QSqlQuery query(database);
    QString insertQuery = "INSERT INTO wiki (concepto, mes, definicion) VALUES (:concepto, :mes, :definicion)";
    query.prepare(insertQuery);
    query.bindValue(":concepto", Wiki.getConcept());
    query.bindValue(":mes", mes);
    query.bindValue(":definicion", Wiki.getDefinition());
    // Execute the query
    query.exec();

    query.prepare("SELECT * FROM wiki");
    ui->tablaWiki->setRowCount(0);
    if (query.exec()) {
        while (query.next()) {
            // Obtener valores de la busqueda
            QString concepto_r = query.value("concepto").toString();
            QString mes_r = query.value("mes").toString();
            QString definicion_r = query.value("definicion").toString();
            int row = ui->tablaWiki->rowCount();
            ui->tablaWiki->setRowCount(row + 1);
            ui->tablaWiki->setItem(row, 0, new QTableWidgetItem(concepto_r));
            ui->tablaWiki->setItem(row, 1, new QTableWidgetItem(mes_r));
            ui->tablaWiki->setItem(row, 2, new QTableWidgetItem(definicion_r));
            ui->tablaWiki->update();
        }
    } else {
        qDebug() << "Failed to execute query:";
    }

    // Cerrar db
    database.close();

}


void sphereApp::on_buscar_wiki_clicked()
{
    QString buscar_text=ui->buscar_text_wiki->text();

    QString archivo;
    QString wiki_path = path;
    if(wiki_path.indexOf("_wiki.db") == std::string::npos){
        archivo = wiki_path.replace(".txt","_wiki.db");
    } else {
        archivo = wiki_path;
    }
    QSqlDatabase database = QSqlDatabase::database();
    database.setDatabaseName(archivo);

    database.open();
    QSqlQuery query(database);
    QString searchQuery = "SELECT * FROM wiki WHERE definicion LIKE '%' || :searchValue || '%' COLLATE NOCASE";
    query.prepare(searchQuery);
    query.bindValue(":searchValue", buscar_text);
    ui->tablaWiki->setRowCount(0);
    if (query.exec()) {
        while (query.next()) {
            // Obtener valores de la busqueda
            QString concepto_r = query.value("concepto").toString();
            QString mes_r = query.value("mes").toString();
            QString definicion_r = query.value("definicion").toString();
            int row = ui->tablaWiki->rowCount();
            ui->tablaWiki->setRowCount(row + 1);
            ui->tablaWiki->setItem(row, 0, new QTableWidgetItem(concepto_r));
            ui->tablaWiki->setItem(row, 1, new QTableWidgetItem(mes_r));
            ui->tablaWiki->setItem(row, 2, new QTableWidgetItem(definicion_r));
            ui->tablaWiki->update();
        }
    } else {
        qDebug() << "Failed to execute query:";
    }

    // Cerrar db
    database.close();

}


void sphereApp::on_eliminar_wiki_clicked()
{
    QString archivo;
    QString eliminar_path = path;
    QString wiki_text=ui->buscar_text_wiki->text();
    if(eliminar_path.indexOf("_wiki.db") == std::string::npos){
        archivo = eliminar_path.replace(".txt","_wiki.db");
    } else {
        archivo = eliminar_path;
    }
    QSqlDatabase database = QSqlDatabase::database();
    database.setDatabaseName(archivo);

    database.open();
    QSqlQuery query(database);
    QString deleteQuery = "DELETE FROM wiki WHERE concepto = :value";
    query.prepare(deleteQuery);
    query.bindValue(":value", wiki_text);
    query.exec();

    query.prepare("SELECT * FROM wiki");
    ui->tablaWiki->setRowCount(0);
    if (query.exec()) {
        while (query.next()) {
            // Obtener valores de la busqueda
            QString concepto_r = query.value("concepto").toString();
            QString mes_r = query.value("mes").toString();
            QString definicion_r = query.value("definicion").toString();
            int row = ui->tablaWiki->rowCount();
            ui->tablaWiki->setRowCount(row + 1);
            ui->tablaWiki->setItem(row, 0, new QTableWidgetItem(concepto_r));
            ui->tablaWiki->setItem(row, 1, new QTableWidgetItem(mes_r));
            ui->tablaWiki->setItem(row, 2, new QTableWidgetItem(definicion_r));
            ui->tablaWiki->update();
        }
    } else {
        qDebug() << "Failed to execute query:";
    }

    // Cerrar db
    database.close();
}

