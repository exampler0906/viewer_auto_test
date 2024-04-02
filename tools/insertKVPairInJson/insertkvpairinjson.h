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
    insertKVPairInJson(QString srcStr);

    inline QJsonObject getJsonObj()
    {
        return this->m_obj;
    }

    /**
     * @brief 在QJsonObject的所有层级下，插入一个合法的键值对，直接调用insertKVPairInJsonEveryDepthHelper(QJsonObject &obj)
     */
    void insertKVPairInJsonEveryDepth();

    /**
     * @brief 在QJsonObject的随机层级下，插入一个合法的键值对，直接调用randomInsertKVPairInJsonRandomDepthHelper(QJsonObject &obj, double stopProbability = 0.6)
     *
     * @param stopProbability 停止概率，当小于该概率时，直接在当前层级下插入，否则继续遍历
     */
    void randomInsertKVPairInJsonRandomDepth(double stopProbability = 0.6);

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

    /**
     * @brief 在QJsonObject的所有层级下，插入一个合法的键值对，传入的是m_obj
     */
    void insertKVPairInJsonEveryDepthHelper(QJsonObject &obj);

    /**
     * @brief 在QJsonObject的随机层级下，插入一个合法的键值对，传入的是m_obj
     *
     * @param stopProbability 停止概率，当小于该概率时，直接在当前层级下插入，否则继续遍历
     */
    void randomInsertKVPairInJsonRandomDepthHelper(QJsonObject &obj, double stopProbability = 0.6);

    QRandomGenerator *randGenerator;
    QString srcChar;
    QJsonObject m_obj;
};

#endif // INSERTKVPAIRINJSON_H
