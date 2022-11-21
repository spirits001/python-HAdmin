# HAdmin后端对DRF封装
我想实现一个这样的理想国：

比xadmin漂亮；比xadmin强大；前后端分离；基于Django和DRF；智能化配置。

以上几点，是我们对HAdmin的设想，设想这样的后端能够相对自动化输出接口，让前端能够根据配置文件认识输出的标准数据结构，从而进行渲染。

于是，初步版本的HAdmin上线了。

### 特别说明

这个模块只是帮助构建给前端的配置信息，让前端方便进行对应渲染，并不是给前端输送代码！

这个请大家一定要理解清楚，这里仅仅是帮助规范了配置信息结构而已。

# 快速开始

## 安装
```python
pip install hadmin
```
## 使用方式
```python
from rest_framework import viewsets
from hadmin import mixins

class CustomConfigViewSet(mixins.PageConfigMixin, viewsets.GenericViewSet):
    list_class = CustomListSerializer
    filter_class = CustomFilter
    create_class = CustomCreateSerializer
    read_class = CustomReadSerializer
    extra = {}
```
其实，就是用HAdmin下的mixins替代rest_framework下的mixins

并且，增加了一个PageConfigMixin方法，这个方法包含了四种配置文件的输出方式，分别是：

list_class 列表的配置信息

filter_class 筛选器的配置信息

create_class 创建数据表单的配置信息

read_class 读取最终数据的配置信息

extra 是额外扩展的数据，可以是字典或者列表等任意可以转换成json的值，会原样递送到前端，用于前端渲染特殊情况下使用，非必填，根据需要使用

每个对应的都是序列化器的的类，序列化器建议每个方法用不同类，这样可以自由定义。

每个序列化器类的元数据可以增加一个custom字典，以便进行解析。

输出到前端的数据样例：
```json
{
    "filter": {
        "base": [
            {
                "label": "手机号", 
                "method": "input", 
                "default": "", 
                "url": "", 
                "limit": 1, 
                "span": 6, 
                "key": "mobile"
            }, 
            {
                "label": "姓名", 
                "method": "input", 
                "default": "", 
                "url": "", 
                "limit": 1, 
                "span": 6, 
                "key": "name"
            }, 
            {
                "label": "姓名", 
                "method": "input", 
                "default": "", 
                "url": "", 
                "limit": 1, 
                "span": 6, 
                "key": "desc"
            }, 
            {
                "label": "新房客源", 
                "method": "select", 
                "default": "", 
                "url": "", 
                "limit": 1, 
                "span": 6, 
                "key": "new", 
                "options": [
                    {
                        "id": "-1000", 
                        "title": "不限"
                    }, 
                    {
                        "id": "true", 
                        "title": "是"
                    }, 
                    {
                        "id": "false", 
                        "title": "否"
                    }, 
                    {
                        "id": "isnull", 
                        "title": "未填写"
                    }
                ]
            }, 
            {
                "label": "二手房客源", 
                "method": "select", 
                "default": "", 
                "url": "", 
                "limit": 1, 
                "span": 6, 
                "key": "old", 
                "options": [
                    {
                        "id": "-1000", 
                        "title": "不限"
                    }, 
                    {
                        "id": "true", 
                        "title": "是"
                    }, 
                    {
                        "id": "false", 
                        "title": "否"
                    }, 
                    {
                        "id": "isnull", 
                        "title": "未填写"
                    }
                ]
            }, 
            {
                "label": "租房客源", 
                "method": "select", 
                "default": "", 
                "url": "", 
                "limit": 1, 
                "span": 6, 
                "key": "rent", 
                "options": [
                    {
                        "id": "-1000", 
                        "title": "不限"
                    }, 
                    {
                        "id": "true", 
                        "title": "是"
                    }, 
                    {
                        "id": "false", 
                        "title": "否"
                    }, 
                    {
                        "id": "isnull", 
                        "title": "未填写"
                    }
                ]
            }
        ], 
        "adv": [ ], 
        "height": 100, 
        "fields": {
            "mobile": "", 
            "name": "", 
            "desc": "", 
            "new": "", 
            "old": "", 
            "rent": ""
        }
    }, 
    "create": {
        "fields": {
            "master": null, 
            "region": null, 
            "admins": [ ], 
            "mobile": "", 
            "name": "", 
            "new": false, 
            "old": false, 
            "rent": false, 
            "desc": ""
        }, 
        "detail": [
            {
                "label": "主理人", 
                "help_text": null, 
                "field_name": "master", 
                "required": true, 
                "type": "PrimaryKeyRelatedField", 
                "choices": [
                    {
                        "id": "1", 
                        "title": "hofeng"
                    }, 
                    {
                        "id": "13", 
                        "title": "18961330033"
                    }, 
                    {
                        "id": "83", 
                        "title": "shanghai001"
                    }, 
                    {
                        "id": "84", 
                        "title": "shanghai002"
                    }, 
                    {
                        "id": "85", 
                        "title": "shanghai003"
                    }, 
                    {
                        "id": "86", 
                        "title": "suqian001"
                    }
                ]
            }, 
            {
                "label": "地区", 
                "help_text": null, 
                "field_name": "region", 
                "required": true, 
                "type": "PrimaryKeyRelatedField", 
                "choices": [
                    {
                        "id": "1", 
                        "title": "上海【310000】"
                    }, 
                    {
                        "id": "21", 
                        "title": "宿迁【321300】"
                    }, 
                    {
                        "id": "34", 
                        "title": "盐城【320900】"
                    }
                ]
            }, 
            {
                "label": "协作人", 
                "help_text": null, 
                "field_name": "admins", 
                "required": true, 
                "type": "ManyRelatedField", 
                "choices": [
                    {
                        "id": "1", 
                        "title": "hofeng"
                    }, 
                    {
                        "id": "13", 
                        "title": "18961330033"
                    }, 
                    {
                        "id": "83", 
                        "title": "shanghai001"
                    }, 
                    {
                        "id": "84", 
                        "title": "shanghai002"
                    }, 
                    {
                        "id": "85", 
                        "title": "shanghai003"
                    }, 
                    {
                        "id": "86", 
                        "title": "suqian001"
                    }
                ]
            }, 
            {
                "label": "手机号", 
                "help_text": "客源手机号", 
                "field_name": "mobile", 
                "required": true, 
                "type": "CharField"
            }, 
            {
                "label": "姓名", 
                "help_text": null, 
                "field_name": "name", 
                "required": false, 
                "type": "CharField"
            }, 
            {
                "label": "新房客源", 
                "help_text": null, 
                "field_name": "new", 
                "required": false, 
                "type": "BooleanField"
            }, 
            {
                "label": "二手房客源", 
                "help_text": null, 
                "field_name": "old", 
                "required": false, 
                "type": "BooleanField"
            }, 
            {
                "label": "租房客源", 
                "help_text": null, 
                "field_name": "rent", 
                "required": false, 
                "type": "BooleanField"
            }, 
            {
                "label": "简要说明", 
                "help_text": null, 
                "field_name": "desc", 
                "required": false, 
                "type": "CharField", 
                "base_template": "textarea.html"
            }
        ]
    }, 
    "list": [
        {
            "label": "ID", 
            "field_name": "id", 
            "type": "IntegerField", 
            "width": "80"
        }, 
        {
            "label": "手机号", 
            "field_name": "mobile", 
            "type": "CharField"
        }, 
        {
            "label": "姓名", 
            "field_name": "name", 
            "type": "CharField"
        }, 
        {
            "label": "主理人", 
            "field_name": "master", 
            "type": "StringRelatedField"
        }, 
        {
            "label": "新房客源", 
            "field_name": "new", 
            "type": "BooleanField"
        }, 
        {
            "label": "二手房客源", 
            "field_name": "old", 
            "type": "BooleanField"
        }, 
        {
            "label": "租房客源", 
            "field_name": "rent", 
            "type": "BooleanField"
        }, 
        {
            "label": "添加时间", 
            "field_name": "add_time", 
            "type": "DateTimeField"
        }
    ], 
    "read": [
        {
            "label": "主理人", 
            "field_name": "master", 
            "type": "StringRelatedField"
        }, 
        {
            "label": "地区", 
            "field_name": "region", 
            "type": "StringRelatedField"
        }, 
        {
            "label": "协作人", 
            "field_name": "admins", 
            "type": "ManyRelatedField"
        }, 
        {
            "label": "添加时间", 
            "field_name": "add_time", 
            "type": "DateTimeField"
        }, 
        {
            "label": "手机号", 
            "field_name": "mobile", 
            "type": "CharField"
        }, 
        {
            "label": "姓名", 
            "field_name": "name", 
            "type": "CharField"
        }, 
        {
            "label": "新房客源", 
            "field_name": "new", 
            "type": "BooleanField"
        }, 
        {
            "label": "二手房客源", 
            "field_name": "old", 
            "type": "BooleanField"
        }, 
        {
            "label": "租房客源", 
            "field_name": "rent", 
            "type": "BooleanField"
        }, 
        {
            "label": "简要说明", 
            "field_name": "desc", 
            "type": "CharField"
        }
    ]
}
```

下面是具体的使用方法

### list_class
```python
class CustomListSerializer(serializers.ModelSerializer):
    master = serializers.StringRelatedField()
    add_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Custom
        fields = ["id", "mobile", "name", "master", "new", "old", "rent", "add_time"]
        custom = {
            "id": {'width': '80'}
        }
```
这是一个典型的列表读取的序列化器，元数据中规定的输出字段，新增的custom字典表明某个字段的特别约定。

字典的健名用字段名表示定义某个字段；

value值是一个字典，健名自己定义，反馈到前端后，前端方便进行解析。

建议保留width，label这类字段，总之，这里定义什么，前端就会收到什么，然后前端进行渲染。

输出到前端后，对应参数健名为：list

### filter_class
作为筛选器，要定义每个筛选项，这是没办法避免的，例如：
```python
class CustomFilter(django_filters.rest_framework.FilterSet):
    mobile = django_filters.CharFilter(method='keyword_filter', help_text="手机号")
    name = django_filters.CharFilter(method='keyword_filter', help_text="姓名")
    desc = django_filters.CharFilter(method='keyword_filter', help_text="说明")
    new = django_filters.BooleanFilter(method='common_filter', help_text="新房客源", label={'options': get_easy_bool()})
    old = django_filters.BooleanFilter(method='common_filter', help_text="二手房客源", label={'options': get_easy_bool()})
    rent = django_filters.BooleanFilter(method='common_filter', help_text="租房客源", label={'options': get_easy_bool()})
```
以上就是对筛选器的定义，对项的定义，放在label进行定义，选择类的给options值，help_text是显示出来的名称

输出到前端后，对应参数健名为：filter

### create_class
创建类的输出，是为了前端自动构造提交表单而定，序列化器写法没有特别，和list一样，可以在元数据中增加一个custom字典，对应把每个字段的特别要求输送到前端。

和其他不同的是，create的Meta下可以额外增加一个tabs，结构为：

```python
tabs = [{
            'label': '基本信息',
            'fields': ['mobile', 'name', 'region', 'desc']
        }, {
            'label': '权限配置',
            'fields': ['master', 'admins', 'new', 'old', 'rent']
        }]
```

这样设定，前端就可以得到这个tabs，可以用于添加表单分步执行。

输出到前端后，对应参数健名为：create

### read_class
读取详细内容的序列化器，要注意的是最好不要构建外键对象，而是要用serializers.StringRelatedField()方法把外键进行文本化，这样才能在前端正常显示。

输出到前端后，对应参数健名为：read

### extra
这个用于额外给前端一个扩展的数据字段，可以设定一切能够转为json的数据，用于自己定义与前端的协议

输入到前端后，对应参数健名为：extra