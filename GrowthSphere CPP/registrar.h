/**
 * @file registrar.h
 * @author Emmanuel Chavarria Solis (leuname592@hotmail.com)
 * @brief Esta clase es la encargada de mostrar la ventana de registro
 * @version 0.1
 * @date 2023-06-25
 * 
 * @copyright MIT
 * 
 */
#ifndef REGISTRAR_H
#define REGISTRAR_H

#include <QWidget>

/**
 * @brief Esta clase es la encargada de mostrar la ventana de registro
 * @brief Se declara dentro del namespace ui
 */
namespace Ui {
class registrar;
}

/**
 * @brief Esta clase es la encargada de mostrar la ventana de registro
 * 
 */
class registrar : public QWidget
{
    Q_OBJECT

public:
    explicit registrar(QWidget *parent = nullptr);
    ~registrar();

private slots:
    /**
     * @brief Este método es el encargado de registrar un usuario en la base de datos y nos devuelve a la pagina principal
     * 
     */
    void on_registrarUsuario_clicked();

private:
    Ui::registrar *ui;
};

#endif // REGISTRAR_H
