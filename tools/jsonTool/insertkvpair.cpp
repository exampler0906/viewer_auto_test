#include "insertkvpair.h"

insertKVPair::insertKVPair(QString srcStr)
{
    randGenerator = QRandomGenerator::system();
    // srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:'\",.<>/?";
    srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
    this->m_obj = QJsonDocument::fromJson(srcStr.toUtf8()).object();
}

QString insertKVPair::getRandomStr(int length)
{
    QString res = "";
    for (int i = 0; i < length; i ++)
    {
        res += this->srcChar[this->randGenerator->bounded(this->srcChar.size())];
    }
    return res;
}

QJsonValue insertKVPair::getRandomJsonValueNum()
{
    int num = int(this->randGenerator->generate());
    if (this->randGenerator->bounded(2) == 0)   // 整数
    {
        return QJsonValue(num);
    }
    else                                        // 浮点数
    {
        QString strNum = "";
        while (num)
        {
            strNum += (num % 10 + '0');
            num /= 10;
        }
        std::reverse(strNum.begin(), strNum.end());
        strNum = strNum.insert(this->randGenerator->bounded(strNum.size()), '.');
        return QJsonValue(strNum.toDouble());
    }
}

QJsonArray insertKVPair::getRandomJsonArray(int length)
{
    QJsonArray res;
    for (int i = 0; i < length; i ++)
    {
        res.append(this->getRandomJsonValue());
    }
    return res;
}

QJsonObject insertKVPair::getRandomJsonObject(int length)
{
    QJsonObject res;
    for (int i = 0; i < length; i ++)
    {
        QString jsonKey = this->getRandomStr(5);
        QJsonValue jsonValue = this->getRandomJsonValue();
        res.insert(jsonKey, jsonValue);
    }
    return res;
}

QJsonValue insertKVPair::getRandomJsonValue()
{
    int category = this->randGenerator->bounded(6);
    if (category == 0)      // 数字(整数或浮点数)
    {
        return this->getRandomJsonValueNum();
    }
    else if (category == 1) // 字符串(在双引号中)
    {
        return QJsonValue(this->getRandomStr(5));
    }
    else if (category == 2) // 逻辑值(true或false)
    {
        return QJsonValue(this->randGenerator->bounded(2) == 0);
    }
    else if (category == 3) // null
    {
        return QJsonValue::Null;
    }
    else if (category == 4) // 数组QJsonArray
    {
        // return QJsonValue(this->getRandomJsonArray(1));   // 随机生成
        QJsonArray res;
        res.append(QJsonValue("test"));
        res.append(QJsonValue(123));
        res.append(QJsonValue(123.321));
        res.append(QJsonValue(true));
        res.append(QJsonValue::Null);
        return res;
    }
    else if (category == 5) // 对象QJsonObject
    {
        // return QJsonValue(this->getRandomJsonObject(1));  // 随机生成
        QJsonObject res;
        res.insert("test", QJsonValue("test"));
        res.insert("123", QJsonValue(123));
        res.insert("123.321", QJsonValue(123.321));
        res.insert("true", QJsonValue(true));
        res.insert("null", QJsonValue::Null);
        return res;
    }
    else
    {
        return QJsonValue::Null;
    }
}

void insertKVPair::insertKVPairInEveryDepth()
{
    insertKVPairInEveryDepthHelper(this->m_obj);
}

void insertKVPair::insertKVPairInEveryDepthHelper(QJsonObject &obj)
{
    QVector<QString> childObjectsKeys;
    for (QString key : obj.keys())
    {
        if (obj[key].isObject())
        {
            childObjectsKeys.append(key);
        }
        else;
    }
    if (!childObjectsKeys.isEmpty())
    {
        QString selectedKey = childObjectsKeys.at(this->randGenerator->bounded(childObjectsKeys.size()));
        QJsonObject childObj = obj[selectedKey].toObject();
        this->insertKVPairInEveryDepthHelper(childObj);
        obj.insert(selectedKey, childObj);
    }
    else;
    QString jsonKey = this->getRandomStr(5);
    QJsonValue jsonValue = this->getRandomJsonValue();
    obj.insert(jsonKey, jsonValue);
}

void insertKVPair::randomInsertKVPairInRandomDepth(double stopProbability)
{
    randomInsertKVPairInRandomDepthHelper(this->m_obj, stopProbability);
}

void insertKVPair::randomInsertKVPairInRandomDepthHelper(QJsonObject &obj, double stopProbability)
{
    if (this->randGenerator->bounded(100) < int(stopProbability * 100))
    {
        QString jsonKey = this->getRandomStr(5);
        QJsonValue jsonValue = this->getRandomJsonValue();
        obj.insert(jsonKey, jsonValue);
    }
    else
    {
        QVector<QString> childObjectsKeys;
        for (QString key : obj.keys())
        {
            if (obj[key].isObject())
            {
                childObjectsKeys.append(key);
            }
            else;
        }
        if (!childObjectsKeys.isEmpty())
        {
            QString selectedKey = childObjectsKeys.at(this->randGenerator->bounded(childObjectsKeys.size()));
            QJsonObject childObj = obj[selectedKey].toObject();
            this->randomInsertKVPairInRandomDepthHelper(childObj, stopProbability);
            obj.insert(selectedKey, childObj);
        }
        else;
        QString jsonKey = this->getRandomStr(5);
        QJsonValue jsonValue = this->getRandomJsonValue();
        obj.insert(jsonKey, jsonValue);
    }
}
