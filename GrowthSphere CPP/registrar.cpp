/**
 * @file registrar.cpp
 * @author Emmanuel Chavarria Solis (leuname592@hotmail.com)
 * @brief Se definen los métodos de la clase registrar
 * @version 0.1
 * @date 2023-06-25
 * 
 * @copyright MIT
 * 
 */
#include "registrar.h"
#include "ui_registrar.h"
#include "back_functions.hpp"
#include "includes.hpp"

registrar::registrar(QWidget *parent) :
    QWidget(parent, Qt::Window),
    ui(new Ui::registrar)
{
    // Seteo de la interfaz grafica de la ventana de registro
    ui->setupUi(this);
    ui->registrarUsuario->setCursor(Qt::PointingHandCursor);
    ui->lineEditPasswordR->setEchoMode(QLineEdit::Password);
    ui->lineEditNombre->setPlaceholderText("Nombre Apellido");
    ui->lineEditEdad->setPlaceholderText("5-85");
    ui->lineEditUsuarioR->setPlaceholderText("UsuarioUnico123");
    ui->lineEditPasswordR->setPlaceholderText("Contraseña");
    ui->lineEditEmail->setPlaceholderText("email@domain.com");
}

registrar::~registrar()
{
    delete ui;
}


// Al hacer click en el boton registrar se verifica que los datos ingresados sean correctos y se crea el usuario
void registrar::on_registrarUsuario_clicked()
{
    QString dirPath = "userDB";
    QString filePath = dirPath + "/db_users.txt";
    QString nombre = ui->lineEditNombre->text();
    QString edad = ui->lineEditEdad->text();
    QString usuario = ui->lineEditUsuarioR->text();
    QString password = ui->lineEditPasswordR->text();
    QString email = ui->lineEditEmail->text();

    std::size_t pass1 = std::hash<std::string>{}(password.toStdString());

    // Se crea una linea con los datos ingresados
    QString line = nombre+","+edad+","+usuario+","+QString::fromStdString(std::to_string(pass1))+","+email;


    // Se verifica que los datos ingresados sean correctos
    if (!validarEntrada(edad.toStdString(),"([0-9]+)")){
        ui->warning->setText("Edad con formato inválido");
        return;
    }
    if (stoi(edad.toStdString())>79 || stoi(edad.toStdString())<5){
        ui->warning->setText("Digite una edad en el rango 5-80");
        return;
    }
    if (!validarEntrada(email.toStdString(),"([a-zA-Z0-9_.]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+)")){
        ui->warning->setText("El correo no es correcto");
        return;
    }

    // Se crea una carpeta de base de datos si esta no existe
    QDir dir;
    if (!dir.exists(dirPath)) {
        if (dir.mkpath(dirPath)) {
        } else {
            ui->warning->setText("Fallo al crear el usuario");
        }
    }

    // Se verifica que el usuario sea unico
    QFile file(filePath);
    if (file.exists()) {
        if (file.open(QIODevice::ReadOnly)) {
            QTextStream in(&file);
            while (!in.atEnd()) {
                QString line = in.readLine(); // Cada linea siendo leida

                QStringList values = line.split(","); // Partir en el delimitador ","

                if (values.size() >= 1) {
                    QString hist_usuarios = values[2]; // Capturar que el usuario sea unico
                    if (hist_usuarios == usuario){
                        ui->warning->setText("Usuario ya existe, intente con otro");
                        return;
                    }
                }
            }
            file.close();
        } else {
            qDebug() << "Failed to open file for reading";
        }
    }

    // En caso de un usuario unico se crea el usuario en la base de datos y nos devolvemos a la pagina principal
    if (file.open(QIODevice::Append)) {
        qDebug() << "File created successfully";
        QTextStream out(&file);
        out << line << "\n";
        file.close();
        this->close();
        this->parentWidget()->show();
    } else {
        ui->warning->setText("Fallo al crear el usuario");
    }
}
