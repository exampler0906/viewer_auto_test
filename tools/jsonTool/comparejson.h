#ifndef COMPAREJSON_H
#define COMPAREJSON_H

#include <QString>
#include <QJsonObject>
#include <QJsonDocument>


class compareJson
{
public:
    static bool isCompatible(const QJsonObject &json1, const QJsonObject &json2);
};

#endif // COMPAREJSON_H
