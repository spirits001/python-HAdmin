from rest_framework.mixins import *


class CreateModelMixin(CreateModelMixin):
    pass


class ListModelMixin(ListModelMixin):
    pass


class RetrieveModelMixin(RetrieveModelMixin):
    pass


class UpdateModelMixin(UpdateModelMixin):
    pass


class DestroyModelMixin(DestroyModelMixin):
    pass


class PageConfigMixin(ListModelMixin):
    """
    界面配置视图
    """
    create_class = None
    filter_class = None
    list_class = None
    read_class = None

    def list(self, request, *args, **kwargs):
        # 过滤器配置
        filter_data = {
            'base': [],
            'adv': [],
            'height': 100,
            'fields': {}
        }

        if self.filter_class:
            for key in self.filter_class.base_filters:
                base_extra = self.filter_class.base_filters[key].extra
                extra = self.filter_class.base_filters[key].label if self.filter_class.base_filters[key].label else {}
                temp = {
                    'label': base_extra['help_text'],
                    'method': extra['method'] if 'method' in extra else 'input',
                    'default': extra['default'] if 'default' in extra else '',
                    'url': extra['url'] if 'url' in extra else '',
                    'limit': extra['limit'] if 'limit' in extra else 1,
                    'span': extra['span'] if 'span' in extra else 6,
                    'key': key,
                }
                if 'url' in extra:
                    temp['method'] = 'select'
                if 'options' in extra:
                    if 'method' not in extra:
                        temp['method'] = 'select'
                    temp['options'] = extra['options'] if isinstance(extra['options'], list) else extra['options'](self)
                filter_data[extra['level'] if 'level' in extra else 'base'].append(temp)
            span = 0
            for item in filter_data['base']:
                span += item['span'] if 'span' in item else 6
                filter_data['fields'][item['key']] = item['default']
            for item in filter_data['adv']:
                filter_data['fields'][item['key']] = item['default']
            height = (span // 24 + int(bool(span % 24))) * 50
            if height > filter_data['height']:
                filter_data['height'] = height
        # 写入字段生成器
        create = {
            'fields': dict(),
            'detail': list()
        }
        if self.create_class:
            create_serializer = self.create_class()
            create['fields'] = create_serializer.root.data
            for key in create_serializer.fields.fields:
                value = create_serializer.fields.fields[key]
                if not value.read_only:
                    tmp = {
                        'label': value.label,
                        'help_text': value.help_text,
                        'field_name': value.field_name,
                        'required': value.required,
                        'type': str(value.__class__.__name__)
                    }
                    tmp.update(value.style)
                    try:
                        if 'url' not in tmp and value.choices:
                            choices = list()
                            for v in value.choices.items():
                                choices.append({
                                    'id': str(v[0]),
                                    'title': str(v[1])
                                })
                            tmp['choices'] = choices
                    except:
                        pass
                    create['detail'].append(tmp)
        # 列表字段生成器
        list_data = list()
        if self.list_class:
            list_serializer = self.list_class()
            custom = dict()
            try:
                custom = list_serializer.Meta.custom
            except:
                pass
            for key in list_serializer.fields.fields:
                value = list_serializer.fields.fields[key]
                tmp = {
                    'label': value.label,
                    'field_name': value.field_name,
                    'type': str(value.__class__.__name__)
                }
                if value.field_name in custom:
                    tmp.update(custom[value.field_name])
                if tmp['label'].replace(" ", "_").lower() == tmp['field_name']:
                    model = value.root.Meta.model.__dict__
                    if tmp['field_name'] in model:
                        tmp['label'] = model[tmp['field_name']].field.verbose_name
                list_data.append(tmp)
        # 读取格式数据
        read_data = list()
        if self.read_class:
            read_serializer = self.read_class()
            custom = dict()
            try:
                custom = read_serializer.Meta.custom
            except:
                pass
            for key in read_serializer.fields.fields:
                value = read_serializer.fields.fields[key]
                tmp = {
                    'label': value.label,
                    'field_name': value.field_name,
                    'type': str(value.__class__.__name__)
                }
                if value.field_name in custom:
                    tmp.update(custom[value.field_name])
                if tmp['label'].replace(" ", "_").lower() == tmp['field_name']:
                    model = value.root.Meta.model.__dict__
                    if tmp['field_name'] in model:
                        tmp['label'] = model[tmp['field_name']].field.verbose_name
                read_data.append(tmp)
        res = {
            "filter": filter_data,
            "create": create,
            "list": list_data,
            "read": read_data
        }
        return Response(res)
