/**
 * @file mainwindow.h
 * @author Emmanuel Chavarria Solis (leuname592@hotmail.com)
 * @brief Esta clase es la encargada de mostrar la ventana principal de la aplicación
 * @version 0.1
 * @date 2023-06-25
 * 
 * @copyright MIT
 * 
 */
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "registrar.h"
#include "sphereapp.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

/**
 * @brief Esta clase es la encargada de mostrar la ventana principal de la aplicación
 * 
 */
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    /**
     * @brief Este método es el encargado de mostrar la ventana de registro
     * 
     */
    void on_registrar_clicked();

    /**
     * @brief Este método es el encargado de mostrar la ventana de la aplicación en caso de haber coincidencia de usuario y contraseña
     * 
     */
    void on_ingresar_clicked();

private:
    Ui::MainWindow *ui;
    /**
     * @brief Este atributo es el encargado de mostrar la ventana de registro
     * 
     */
    registrar *ru;

    /**
     * @brief Este atributo es el encargado de mostrar la ventana de la aplicación en caso de haber coincidencia de usuario y contraseña
     * 
     */
    sphereApp *sa;
};
#endif // MAINWINDOW_H
