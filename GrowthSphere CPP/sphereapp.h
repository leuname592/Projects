/**
 * @file sphereapp.h
 * @author Emmanuel Chavarria Solis (leuname592@hotmail.com)
 * @brief 
 * @version 0.1
 * @date 2023-06-25
 * 
 * @copyright MIT
 * 
 */
#ifndef SPHEREAPP_H
#define SPHEREAPP_H

#include <QWidget>
#include <QPushButton>
#include <QFile>
#include "includes.hpp"

/**
 * @brief Esta clase es la encargada de mostrar la ventana de la aplicación
 * @brief Se declara dentro del namespace ui
 */
namespace Ui {
class sphereApp;
}

/**
 * @brief Esta clase es la encargada de mostrar la ventana de la aplicación
 * 
 */
class sphereApp : public QWidget
{
    Q_OBJECT

public:
    explicit sphereApp(QString path,QString year_ext,QWidget *parent = nullptr);
    ~sphereApp();

private slots:
    /**
     * @brief Este método ajusta el tiempo por medio de un slider
     * 
     * @param value Valor de 0 a 100 en el slider
     */
    void on_cronoSlider_valueChanged(int value);

    /**
     * @brief Este método es el encargado de iniciar el cronometro
     * 
     */
    void on_set_goal_clicked();

    /**
     * @brief Este método es el encargado de ejecutar metodos cuando se da click en el tabWidget
     * 
     * @param index Index del tabWidget
     */
    void on_tabWidget_tabBarClicked(int index);

    /**
     * @brief Este método elimina los datos de la base de datos seleccionados 
     * 
     */
    void on_eliminar_clicked();

    /**
     * @brief Este método es el encargado de guardar y mostrar los datos de la base de datos en la tabla menntor
     * 
     */
    void on_guardar_mentor_clicked();

    /**
     * @brief Este método es el encargado de guardar los datos de la base de datos y mostrarlos en la tabla mes
     * 
     */
    void on_guardar_mes_clicked();

    /**
     * @brief Este método es el encargado de mostrar los datos de la base de datos en la tabla mentor en los botones respectivos
     * 
     */
    void on_leer_mes_clicked();

    /**
     * @brief Se setea un pop up para el mes de Noviembre
     * 
     */
    void on_Noviembre_clicked();

    /**
     * @brief Se setea un pop up para el mes de Enero
     * 
     */
    void on_Enero_clicked();

    /**
     * @brief Se setea un pop up para el mes de Febrero
     *
     */
    void on_Febrero_clicked();

    /**
     * @brief Se setea un pop up para el mes de Marzo
     *
     */
    void on_Marzo_clicked();

    /**
     * @brief Se setea un pop up para el mes de Abril
     *
     */
    void on_Abril_clicked();

    /**
     * @brief Se setea un pop up para el mes de Mayo
     *
     */
    void on_Mayo_clicked();

    /**
     * @brief Se setea un pop up para el mes de Junio
     *
     */
    void on_Junio_clicked();

    /**
     * @brief Se setea un pop up para el mes de Julio
     *
     */
    void on_Julio_clicked();

    /**
     * @brief Se setea un pop up para el mes de Agosto
     *
     */
    void on_Agosto_clicked();

    /**
     * @brief Se setea un pop up para el mes de Septiembre
     *
     */
    void on_Septiembre_clicked();

    /**
     * @brief Se setea un pop up para el mes de Octubre
     *
     */
    void on_Octubre_clicked();

    /**
     * @brief Se setea un pop up para el mes de Diciembre
     *
     */
    void on_Diciembre_clicked();

    /**
     * @brief Este método es el encargado de mostrar los datos de la base de datos en la tabla wiki en los botones respectivos despues de eliminar un dato seleccionado
     * 
     */
    void on_eliminar_mentor_clicked();

    /**
     * @brief Este método es el encargado de mostrar los datos de la base de datos en la tabla wiki en los botones respectivos
     * 
     */
    void on_colocar_clicked();

    void on_colocar_2_clicked();

    /**
     * @brief Este método es el encargado de guardar los datos de la base de datos y mostrarlos en la tabla wiki
     * 
     */
    void on_guardar_wiki_clicked();

    void on_buscar_wiki_clicked();

    void on_eliminar_wiki_clicked();

private:
    QString path;
    QString year_ext;
    Ui::sphereApp *ui;
    QSqlDatabase database;

protected:
    void showEvent(QShowEvent *event) override
    {
        QWidget::showEvent(event);

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
                        button->setStyleSheet("QPushButton {font: 12pt \"Segoe UI\";border: none;background-color: rgb(16, 104, 60);color: white;border-radius: 10px;}QPushButton:hover {background-color: rgb(81, 81, 81);border-color: rgb(81, 81, 81);}");
                    }
                }
                file.close();
            } else {
                qDebug() << "Failed to open file for reading";
            }
        }

    }
};

#endif // SPHEREAPP_H
