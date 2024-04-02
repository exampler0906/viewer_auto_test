#ifndef INSERTKVPAIRINJSON_H
#define INSERTKVPAIRINJSON_H

#include <QString>
#include <QRandomGenerator>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QVector>
#include <QStringList>


class insertKVPairInJson
{
public:
    inline insertKVPairInJson()
    {}
    inline insertKVPairInJson(QString srcStr)
    {
        this->m_obj = QJsonDocument::fromJson(srcStr.toUtf8()).object();
    }

    /**
     * @brief 在QJsonObject的所有层级下，插入一个合法的键值对
     */
    void insertKVPairInJsonEveryDepth(QJsonObject &obj);
    /**
     * @brief 在QJsonObject的随机层级下，插入一个合法的键值对
     *
     * @param stopProbability 停止概率，当小于该概率时，直接在当前层级下插入，否则继续遍历
     */
    void randomInsertKVPairInJsonRandomDepth(QJsonObject &obj, double stopProbability = 0.6);

    QJsonObject m_obj;

private:
    /**
     * @brief 在srcChar中随机挑选若干字符，得到一个随机的QString
     *
     * @param length 随机QString的长度
     * @return QString
     */
    QString getRandomStr(int length);

    /**
     * @brief 得到一个类型为数字的QJsonValue
     *
     * @return QJsonValue
     */
    QJsonValue getRandomJsonValueNum();

    /**
     * @brief 得到一个随机的QJsonArray
     *
     * @param length QJsonArray长度
     * @return QJsonArray
     */
    QJsonArray getRandomJsonArray(int length);

    /**
     * @brief 得到一个随机的QJsonObject
     *
     * @param length QJsonObject内的对象个数
     * @return QJsonObject
     */
    QJsonObject getRandomJsonObject(int length);

    /**
     * @brief 得到一个随机的QJsonValue
     *
     * @return QJsonValue
     */
    QJsonValue getRandomJsonValue();

    QRandomGenerator *randGenerator = QRandomGenerator::system();
    // const QString srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()_+-=[]{}|;:'\",.<>/?";
    const QString srcChar = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
};

#endif // INSERTKVPAIRINJSON_H
