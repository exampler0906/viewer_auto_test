#include "widget.h"
#include "ui_widget.h"
#include <QDebug>
#include "insertkvpairinjson.h"

Widget::Widget(QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Widget)
{
    ui->setupUi(this);
}

Widget::~Widget()
{
    delete ui;
}


void Widget::on_btnOK_clicked()
{
    insertKVPairInJson json(ui->txtEditJsonSrc->toPlainText());
    if (json.getJsonObj().isEmpty())
    {
        ui->txtEditWarning->setText("输入非法，请检查输入！");
    }
    ui->txtEditJsonSrcDisplay->setPlainText(QJsonDocument(json.getJsonObj()).toJson(QJsonDocument::Indented));
    json.insertKVPairInJsonEveryDepth();
    // json.randomInsertKVPairInJsonRandomDepth();
    ui->txtEditJsonRes->setPlainText(QJsonDocument(json.getJsonObj()).toJson(QJsonDocument::Indented));
}
