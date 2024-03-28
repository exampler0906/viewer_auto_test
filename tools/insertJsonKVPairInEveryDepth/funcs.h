#ifndef FUNCS_H
#define FUNCS_H

#include <QJsonObject>
#include <QJsonArray>

/**
 * @brief 将QString转换为QJsonObject
 *
 * @param src 源QString
 * @return QJsonObject
 */
QJsonObject qStr2qJson(QString src);

/**
 * @brief 将QJsonObject转换为QString
 *
 * @param src 源QJsonObject
 * @return QString
 */
QString qJson2qStr(QJsonObject src);

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
 * @brief 在QJsonObject的所有层级下，插入一个合法的键值对
 *
 * @param obj 待操作的QJsonObject
 */
void insertJsonKVPairInEveryDepth(QJsonObject &obj);

/**
 * @brief 在QJsonObject的随机层级下，插入一个合法的键值对
 *
 * @param obj 待操作的QJsonObject
 * @param stopProbability 停止概率，当小于该概率时，直接在当前层级下插入，否则继续遍历
 */
void randomInsertJsonKVPairInRandomDepth(QJsonObject &obj, double stopProbability = 0.99);

#endif // FUNCS_H
