/**
 * @file mainwindow.cpp
 * @author Emmanuel Chavarria Solis (leuname592@hotmail.com)
 * @brief Funciones de la clase mainwindow la que se incarga de ingresar los usuarios
 * @version 0.1
 * @date 2023-06-25
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "mainwindow.h"
#include "./ui_mainwindow.h"
#include "includes.hpp"
#include "back_functions.hpp"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    // Seteo de la interfaz grafica de la ventana principal
    ui->setupUi(this);
    ui->lineEditPassword->setEchoMode(QLineEdit::Password);
    ui->lineEditUsuario->setPlaceholderText("Usuario");
    ui->lineEditPassword->setPlaceholderText("Contraseña");
    ui->ingresar->setCursor(Qt::PointingHandCursor);
    ui->registrar->setCursor(Qt::PointingHandCursor);

    QString currentPath = QDir::currentPath();
    int w =ui->logo_main->width();
    int h =ui->logo_main->height();
    QPixmap pix(currentPath+"/images/logo.png");
    ui->logo_main->setPixmap(pix.scaled(w,h,Qt::KeepAspectRatio));

}

MainWindow::~MainWindow()
{
    delete ui;
}


// Al hacer click en el boton registrar se crea una instancia de la clase registrar
void MainWindow::on_registrar_clicked()
{
    ru = new registrar(this);
    ru->showMaximized();
    this->hide();
}

void first_login_db(QString usuario, QString edad, QString texto){
    QString dirPath = "userDB";
    QString filePath = dirPath + "/" + usuario + ".txt";
    QString line;
    int year = present_year()-1;
    int temp_edad = edad.toInt();
    year -= temp_edad;
    QFile file(filePath);
    if (!file.exists()) {
        if (file.open(QIODevice::WriteOnly)) {
            QTextStream out(&file);
            for(int i=1; i<=temp_edad+1;i++){
                line = QString("matrix_%1").arg(i)+","+QString("%1").arg(year)+","+texto; // Crear una linea con el formato de la base de datos para inicializar los botones
                out << line << "\n";
                year++;
            }
            file.close();
        }
    }
}

// Al hacer click en el boton ingresar se verifica que el usuario y la contraseña coincidan con los de la base de datos
void MainWindow::on_ingresar_clicked()
{
    QString dirPath = "userDB";
    QString filePath = dirPath + "/db_users.txt";
    QString usuario = ui->lineEditUsuario->text();
    QString password = ui->lineEditPassword->text();
    QString userpath = dirPath + "/" + usuario + ".txt";
    std::size_t pass1 = std::hash<std::string>{}(password.toStdString());


    QFile file(filePath);
    if (file.exists()) {
        if (file.open(QIODevice::ReadOnly)) {
            QTextStream in(&file);
            while (!in.atEnd()) {
                QString line = in.readLine(); // Leer cada linea del archivo

                QStringList values = line.split(","); // Delimitar cada valor por una coma 

                if (values.size() >= 1) {
                    QString hist_usuarios = values[2]; // Capturar el usuario y la contraseña
                    QString hist_passwords = values[3];
                    QString hist_edades = values[1];
                    if (hist_usuarios == usuario && hist_passwords == QString::fromStdString(std::to_string(pass1))){
                        // En caso de coincidencia ingresar a la aplicación
                        first_login_db(hist_usuarios, hist_edades, "Vivido");
                        sa = new sphereApp(userpath,hist_edades);
                        sa->showMaximized();
                        this->hide();
                    }
                    else{
                        // En caso de no coincidencia mostrar un mensaje de error
                        ui->warningMain->setText("Usuario o contraseña incorrecto");
                    }
                }
            }
            // Cerrar bas de datos
            file.close();
        }
    }
}

