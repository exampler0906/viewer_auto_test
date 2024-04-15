#include "comparejson.h"

bool compareJson::isCompatible(QJsonObject json1, QJsonObject json2)
{
    if (json1.size() > json2.size())
    {
        swap(json1, json2);
    }
    else;
    for (auto it = json1.begin(); it != json1.end(); it ++)
    {
        QString key = it.key();
        if (json1[key].isObject() && json2[key].isObject())
        {
            return isCompatible(json1[key].toObject(), json2[key].toObject());
        }
        else if (!json1[key].isObject() && !json2[key].isObject())
        {
            if (json1[key] != json2[key])
            {
                return false;
            }
            else;
        }
        else
        {
            return false;
        }
    }
    return true;
}
