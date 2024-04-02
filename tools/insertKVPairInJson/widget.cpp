#include "widget.h"
#include "ui_widget.h"
#include <QDebug>
#include "funcs.h"
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
    if (json.m_obj.isEmpty())
    {
        ui->txtEditWarning->setText("输入非法，请检查输入！");
    }
    ui->txtEditJsonSrcDisplay->setPlainText(QJsonDocument(json.m_obj).toJson(QJsonDocument::Indented));
    json.insertKVPairInJsonEveryDepth(json.m_obj);
    // json.randomInsertKVPairInJsonRandomDepth(json.m_obj);
    ui->txtEditJsonRes->setPlainText(QJsonDocument(json.m_obj).toJson(QJsonDocument::Indented));
}
