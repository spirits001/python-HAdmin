def build_search(url: str, page_size: int = 300, data_key: str = "results", search_key: str = "title", value: str = "id", label: str = "title"):
    # 生成搜索配置
    return {
        "search": {
            "url": url,
            "form": {
                "pageSize": page_size
            },
            "data_key": data_key,
            "search_key": search_key,
            "filed_names": {
                "value": value,
                "label": label
            }
        },
    }


def get_easy_bool():
    # 生成布尔值配置
    return [
        {"id": "-1000", "title": "不限"},
        {"id": "true", "title": "是"},
        {"id": "false", "title": "否"},
        {"id": "isnull", "title": "未填写"},
    ]


def get_settings_choices(data):
    # 生成配置选项
    tmp = [{"id": "-1000", "title": "不限"}]
    for item in data:
        tmp.append({"id": str(item[0]), "title": str(item[1])})
    tmp.append({"id": "isnull", "title": "未填写"})
    return tmp


def build_filter_by_model(data, key: str = "title"):
    tmp = [{"id": "-1000", key: "不限"}]
    for item in data:
        tmp.append({"id": str(item.id), key: item.__str__()})
    tmp.append({"id": "isnull", key: "未填写"})
    return tmp
