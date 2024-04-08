#ifndef COMPAREJSON_H
#define COMPAREJSON_H

#include <QString>
#include <QJsonObject>
#include <QList>
#include <QJsonDocument>

class compareJson
{
public:
    compareJson(QString srcStr1, QString srcStr2);

    inline QJsonObject getJsonObj1()
    {
        return this->m_obj1;
    }

    inline QJsonObject getJsonObj2()
    {
        return this->m_obj2;
    }

    /**
     * @brief 比较两json
     *
     * @return int
     * 0: 两json相等
     * 1: json1是json2的子集
     * 2: json2是json1的子集
     * 3: json1中存在json2中没有的键值对
     * 4: json2中存在json1中没有的键值对
     */
    int compare();

private:
    QList<QPair<QString, QJsonValue>> flattenJsonObject(const QJsonObject &obj);

    QJsonObject m_obj1, m_obj2;
    QList<QPair<QString, QJsonValue>> m_flattenedJson1, m_flattenedJson2;
};

#endif // COMPAREJSON_H
