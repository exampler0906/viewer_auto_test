﻿#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "insertkvpair.h"
#include "comparejson.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    init();
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::init()
{
    ui->lineEditHint->setReadOnly(true);

    ui->txtEditInsertInputDisplay->setReadOnly(true);
    ui->txtEditInsertOutput->setReadOnly(true);

    ui->txtEditCompareInputDisplay1->setReadOnly(true);
    ui->txtEditCompareInputDisplay2->setReadOnly(true);
}

void MainWindow::on_btnInsert_clicked()
{
    ui->lineEditHint->setText("");
    ui->txtEditInsertInputDisplay->setPlainText("");
    ui->txtEditInsertOutput->setPlainText("");
    insertKVPair json(ui->txtEditInsertInput->toPlainText());
    if (json.getJsonObj().isEmpty())
    {
        ui->lineEditHint->setText(QString::fromLocal8Bit("输入非法，请检查输入！"));
        ui->txtEditInsertInputDisplay->setPlainText("");
        ui->txtEditInsertOutput->setPlainText("");
    }
    else
    {
        ui->txtEditInsertInputDisplay->setPlainText(QJsonDocument(json.getJsonObj()).toJson(QJsonDocument::Indented));
        json.insertKVPairInEveryDepth();
        ui->txtEditInsertOutput->setPlainText(QJsonDocument(json.getJsonObj()).toJson(QJsonDocument::Indented));
    }
}

void MainWindow::on_btnCompare_clicked()
{
    ui->lineEditHint->setText("");
    ui->txtEditCompareInputDisplay1->setPlainText("");
    ui->txtEditCompareInputDisplay2->setPlainText("");
    QJsonObject json1, json2;
    json1 = QJsonDocument::fromJson(ui->txtEditCompareInput1->toPlainText().toUtf8()).object();
    json2 = QJsonDocument::fromJson(ui->txtEditCompareInput2->toPlainText().toUtf8()).object();
    if (json1.isEmpty())
    {
        ui->lineEditHint->setText(QString::fromLocal8Bit("json1输入非法，请检查输入！"));
        return;
    }
    else;
    if (json2.isEmpty())
    {
        ui->lineEditHint->setText(QString::fromLocal8Bit("json2输入非法，请检查输入！"));
        return;
    }
    else;
    ui->txtEditCompareInputDisplay1->setPlainText(QJsonDocument(json1).toJson(QJsonDocument::Indented));
    ui->txtEditCompareInputDisplay2->setPlainText(QJsonDocument(json2).toJson(QJsonDocument::Indented));
    if (compareJson::isCompatible(json1, json2) == true)
    {
        ui->lineEditHint->setText(QString::fromLocal8Bit("两json兼容"));
    }
    else
    {
        ui->lineEditHint->setText(QString::fromLocal8Bit("两json不兼容"));
    }
}
