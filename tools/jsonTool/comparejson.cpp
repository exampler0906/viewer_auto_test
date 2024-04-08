#include "comparejson.h"

compareJson::compareJson(QString srcStr1, QString srcStr2)
{
    this->m_obj1 = QJsonDocument::fromJson(srcStr1.toUtf8()).object();
    this->m_obj2 = QJsonDocument::fromJson(srcStr2.toUtf8()).object();
    this->m_flattenedJson1 = this->flattenJsonObject(this->m_obj1);
    this->m_flattenedJson2 = this->flattenJsonObject(this->m_obj2);
}

int compareJson::compare()
{
    int len1 = this->m_flattenedJson1.size();
    int len2 = this->m_flattenedJson2.size();
    if (len1 == len2)
    {
        for (int i = 0; i < len1; i ++)
        {
            if (this->m_flattenedJson1[i].first != this->m_flattenedJson2[i].first ||
                this->m_flattenedJson1[i].second != this->m_flattenedJson2[i].second)
            {
                return 3;
            }
        }
    }
    else if (len1 > len2)
    {
        for (int i = 0, j = 0; i < len2; i ++)
        {
            if (j >= len1)
            {
                return 4;
            }
            if (this->m_flattenedJson1[j].first == this->m_flattenedJson2[i].first &&
                this->m_flattenedJson1[j].second == this->m_flattenedJson2[i].second)
            {
                j ++;
            }
            else
            {
                while (j < len1 &&
                       (this->m_flattenedJson1[j].first != this->m_flattenedJson2[i].first ||
                        this->m_flattenedJson1[j].second != this->m_flattenedJson2[i].second))
                {
                    j ++;
                }
            }
        }
        return 2;
    }
    else if (len1 < len2)
    {
        for (int i = 0, j = 0; i < len1; i ++)
        {
            if (j >= len2)
            {
                return 3;
            }
            if (this->m_flattenedJson1[i].first == this->m_flattenedJson2[j].first &&
                this->m_flattenedJson1[i].second == this->m_flattenedJson2[j].second)
            {
                j ++;
            }
            else
            {
                while (j < len2 &&
                       (this->m_flattenedJson1[i].first != this->m_flattenedJson2[j].first ||
                        this->m_flattenedJson1[i].second != this->m_flattenedJson2[j].second))
                {
                    j ++;
                }
            }
        }
        return 1;
    }
    else;
    return 0;
}

QList<QPair<QString, QJsonValue>> compareJson::flattenJsonObject(const QJsonObject &obj)
{
    QList<QPair<QString, QJsonValue>> res;
    for (auto it = obj.begin(); it != obj.end(); it ++)
    {
        res.append({it.key(), it.value()});
        if (it.value().isObject())
        {
            res += flattenJsonObject(it.value().toObject());
        }
    }
    return res;
}
