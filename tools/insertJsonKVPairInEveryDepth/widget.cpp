#include "widget.h"
#include "ui_widget.h"
#include <QDebug>
#include "funcs.h"

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
    QString srcStr = ui->txtEditJsonSrc->toPlainText();
    // qDebug() << srcStr;
    QJsonObject srcJson = qStr2qJson(srcStr);
    if (srcJson.isEmpty())
    {
        ui->txtEditWarning->setText("输入非法，请检查输入！");
        return;
    }
    // qDebug() << srcJson;
    ui->txtEditJsonSrcDisplay->setPlainText(qJson2qStr(srcJson));
    // randomInsertJsonKVPairInRandomDepth(srcJson);
    insertJsonKVPairInEveryDepth(srcJson);
    QString resStr = qJson2qStr(srcJson);
    ui->txtEditJsonRes->setPlainText(resStr);
}
