#include "funcs.h"
#include <QJsonDocument>
#include <QRandomGenerator>
#include <QString>
#include <QVector>
#include <QStringList>
#include <QDebug>

QJsonObject qStr2qJson(QString src)
{
    QJsonDocument temp = QJsonDocument::fromJson(src.toUtf8());
    QJsonObject res = temp.object();
    return res;
}

QString qJson2qStr(QJsonObject src)
{
    QJsonDocument temp(src);
    QString res = temp.toJson(QJsonDocument::Indented);
    return res;
}

QString getRandomStr(int length)
{
    QRandomGenerator *randGenerator = QRandomGenerator::system();
    // const QString srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:'\",.<>/?";
    const QString srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    QString res = "";
    for (int i = 0; i < length; i ++)
        res += srcChar[randGenerator->bounded(srcChar.size())];
    return res;
}

QJsonValue getRandomJsonValueNum()
{
    QRandomGenerator *randGenerator = QRandomGenerator::system();
    int num = int(randGenerator->generate());
    if (randGenerator->bounded(2) == 0) // 整数
    {
        return QJsonValue(num);
    }
    else                                // 浮点数
    {
        QString strNum = "";
        while (num)
        {
            strNum += (num % 10 + '0');
            num /= 10;
        }
        strNum = strNum.insert(randGenerator->bounded(strNum.size()), '.');
        return QJsonValue(strNum.toDouble());
    }
}

QJsonArray getRandomJsonArray(int length)
{
    QJsonArray res;
    for (int i = 0; i < length; i ++)
    {
        res.append(getRandomJsonValue());
    }
    return res;
}

QJsonObject getRandomJsonObject(int length)
{
    QJsonObject res;
    for (int i = 0; i < length; i ++)
    {
        QString jsonKey = getRandomStr(5);
        QJsonValue jsonValue = getRandomJsonValue();
        res.insert(jsonKey, jsonValue);
    }
    return res;
}

QJsonValue getRandomJsonValue()
{
    QRandomGenerator *randGenerator = QRandomGenerator::system();
    int category = randGenerator->bounded(6);
    if (category == 0)      // 数字(整数或浮点数)
        return getRandomJsonValueNum();
    else if (category == 1) // 字符串(在双引号中)
        return QJsonValue(getRandomStr(5));
    else if (category == 2) // 逻辑值(true或false)
        return QJsonValue(randGenerator->bounded(2) == 0);
    else if (category == 3) // null
        return QJsonValue::Null;
    else if (category == 4) // 数组
    {
        // return QJsonValue(getRandomJsonArray(1));   // 随机生成
        QJsonArray res;
        res.append(QJsonValue("test"));
        res.append(QJsonValue(123));
        res.append(QJsonValue(123.321));
        res.append(QJsonValue(true));
        res.append(QJsonValue::Null);
        return res;
    }
    else if (category == 5) // 对象
    {
        // return QJsonValue(getRandomJsonObject(1));  // 随机生成
        QJsonObject res;
        res.insert("test", QJsonValue("test"));
        res.insert("123", QJsonValue(123));
        res.insert("123.321", QJsonValue(123.321));
        res.insert("true", QJsonValue(true));
        res.insert("null", QJsonValue::Null);
        return res;
    }
    else
        return QJsonValue::Null;
}

void insertJsonKVPairInEveryDepth(QJsonObject &obj)
{
    QVector<QString> childObjectsKeys;
    for (QString key : obj.keys())
        if (obj[key].isObject())
            childObjectsKeys.append(key);
    if (!childObjectsKeys.isEmpty())
    {
        QString selectedKey = childObjectsKeys.at(QRandomGenerator::global()->bounded(childObjectsKeys.size()));
        QJsonObject childObj = obj[selectedKey].toObject();
        insertJsonKVPairInEveryDepth(childObj);
        obj.insert(selectedKey, childObj);
    }
    QString jsonKey = getRandomStr(5);
    QJsonValue jsonValue = getRandomJsonValue();
    obj.insert(jsonKey, jsonValue);
}

void randomInsertJsonKVPairInRandomDepth(QJsonObject &obj, double stopProbability)
{
    if (QRandomGenerator::global()->generateDouble() < stopProbability)
    {
        QString jsonKey = getRandomStr(5);
        QJsonValue jsonValue = getRandomJsonValue();
        obj.insert(jsonKey, jsonValue);
    }
    else
    {
        QVector<QString> childObjectsKeys;
        for (QString key : obj.keys())
            if (obj[key].isObject())
                childObjectsKeys.append(key);
        if (!childObjectsKeys.isEmpty())
        {
            QString selectedKey = childObjectsKeys.at(QRandomGenerator::global()->bounded(childObjectsKeys.size()));
            QJsonObject childObj = obj[selectedKey].toObject();
            randomInsertJsonKVPairInRandomDepth(childObj, stopProbability);
            obj.insert(selectedKey, childObj);
        }
        else
        {
            QString jsonKey = getRandomStr(5);
            QJsonValue jsonValue = getRandomJsonValue();
            obj.insert(jsonKey, jsonValue);
        }
    }
}
