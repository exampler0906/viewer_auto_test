#include "comparejson.h"

bool compareJson::isCompatible(const QJsonObject &json1, const QJsonObject &json2)
{
    int len1 = json1.size();
    int len2 = json2.size();
    if (len1 <= len2)
    {
        for (auto it = json1.begin(); it != json1.end(); it ++)
        {
            QString key = it.key();
            if (!json2.contains(key) || json1[key] != json2[key])
            {
                return false;
            }
        }
    }
    else
    {
        for (auto it = json2.begin(); it != json2.end(); it ++)
        {
            QString key = it.key();
            if (!json1.contains(key) || json1[key] != json2[key])
            {
                return false;
            }
        }
    }
    return true;
}
