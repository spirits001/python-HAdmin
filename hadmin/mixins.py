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
    # 创建的序列化器类
    create_class = None
    # 过滤器的类
    filter_class = None
    # 列表的序列化器类
    list_class = None
    # 读取的序列化器类
    read_class = None
    # 修改序列化器类
    update_class = None
    # 扩展自定义信息
    extra = None
    # 默认选择项数量
    choices_limit = 30
    # inline模式默认数量限制
    inlines_limit = 10

    @staticmethod
    def _build_label(tmp, value):
        """
        清理label
        """
        if tmp['label'].replace(" ", "_").lower() == tmp['field_name']:
            try:
                tmp['label'] = value.root.Meta.model._meta.get_field(tmp['field_name']).verbose_name
            except:
                pass
        return tmp

    def _build_list(self, class_method):
        list_data = list()
        if class_method:
            list_serializer = class_method()
            try:
                custom = list_serializer.Meta.custom
            except:
                custom = dict()
            for key in list_serializer.fields.fields:
                value = list_serializer.fields.fields[key]
                tmp = {
                    'label': value.label,
                    'field_name': value.field_name,
                    'type': value.__class__.__name__,  # 字段类型
                    'required': value.required,  # 是否必填
                    'rules': [],  # 验证器
                    'method': '',  # 渲染方式，如果没有指定，就采用type来自动匹配
                    'max_length': 0,  # 最大长度
                    'precision': None,  # 小数长度
                }
                # 原始字段类型
                try:
                    tmp['field'] = value.root.Meta.model._meta.get_field(value.field_name).__class__.__name__
                except:
                    tmp['field'] = None
                # 放入小数长度
                if tmp['type'] == 'DecimalField':
                    tmp['precision'] = value.decimal_places
                if tmp['type'] == 'IntegerField':
                    tmp['precision'] = 0
                # 放入最大长度
                try:
                    tmp['max_length'] = value.max_length
                except:
                    pass
                # 添加rules
                if value.required:
                    rule = {
                        'required': True,
                        'message': value.error_messages['required']
                    }
                    tmp['rules'].append(rule)
                # 清洗一下label
                tmp = self._build_label(tmp, value)
                # 覆盖自定义数据到配置字典
                if value.field_name in custom:
                    tmp.update(custom[value.field_name])
                list_data.append(tmp)
        return list_data

    def _build_create(self, create, custom, value):
        """
        创建配置函数
        """
        # 如果这个字段不是只读模式
        if not value.read_only and not value.__class__.__name__ == 'HiddenField':
            tmp = {
                'label': value.label,  # 字段名称
                'help_text': value.help_text,  # 辅助说明，默认读取模型的，如果序列化器设定了，就是序列化器的了
                'field_name': value.field_name,  # 字段名
                'required': value.required,  # 是否必填
                'type': value.__class__.__name__,  # 字段类型
                'rules': [],  # 验证器
                'choices': [],  # 选择项
                'method': '',  # 渲染方式，如果没有指定，就采用type来自动匹配
                'max_length': 0,  # 最大长度
                'precision': None,  # 小数长度
            }
            # 原始字段类型
            try:
                tmp['field'] = value.root.Meta.model._meta.get_field(value.field_name).__class__.__name__
            except:
                tmp['field'] = None
            # 放入小数长度
            if tmp['type'] == 'DecimalField':
                tmp['precision'] = value.decimal_places
            if tmp['type'] == 'IntegerField':
                tmp['precision'] = 0
            # 放入最大长度
            try:
                tmp['max_length'] = value.max_length
            except:
                pass
            # 清洗一下label
            tmp = self._build_label(tmp, value)
            # 添加rules
            if value.required:
                rule = {
                    'required': True,
                    'message': value.error_messages['required']
                }
                tmp['rules'].append(rule)
            # 把choices的内容放到数据里,这里要判断选择项数量，太多了可不行
            if tmp['type'] in ['PrimaryKeyRelatedField', 'ManyRelatedField', 'ChoiceField']:
                if tmp['type'] == 'ChoiceField' or (tmp['type'] == 'ManyRelatedField' and value.child_relation.queryset.count() < self.choices_limit) or (
                        tmp['type'] == 'PrimaryKeyRelatedField' and value.queryset.count() < self.choices_limit):
                    for v in value.choices.items():
                        tmp['choices'].append({
                            'value': v[0],
                            'label': v[1]
                        })
            # 合并序列化器里的custom定义的内容
            if value.field_name in custom:
                if 'search' in custom[value.field_name]:
                    tmp['choices'] = []
                tmp.update(custom[value.field_name])
            create['detail'].append(tmp)

    def list(self, request, *args, **kwargs):
        # 初始化过滤器的数据模型
        filter_data = {
            'base': [],
            'adv': [],
            'height': 100,
            'fields': {}
        }
        # 如果存在过滤器类
        if self.filter_class:
            # 开始循环过滤器类中的每一条过滤规则
            for key in self.filter_class.base_filters:
                # 读取到过滤器中每一条中的extra字段
                base_extra = self.filter_class.base_filters[key].extra
                # 读取label字段，正常我们都是把数据写在了这个字段里
                extra = self.filter_class.base_filters[key].label if self.filter_class.base_filters[key].label else {}
                # 构造一条数据模型
                temp = {
                    'label': base_extra['help_text'],  # 名称
                    'method': extra['method'] if 'method' in extra else 'input',  # 表单方式
                    'default': extra['default'] if 'default' in extra else '',  # 默认值
                    'url': extra['url'] if 'url' in extra else '',  # 获取options的路径
                    'limit': extra['limit'] if 'limit' in extra else 1,  # 最多选择几个
                    'span': extra['span'] if 'span' in extra else 6,  # 占用几个栅格，默认为6
                    'key': key,  # 字段名称
                }
                # 如果有url字段，那么表现形式必然是select
                if 'url' in extra:
                    temp['method'] = 'select'
                # 如果有options字段
                if 'options' in extra:
                    # 防止击穿method方法造成问题
                    if 'method' not in extra:
                        temp['method'] = 'select'
                    # 对options进行赋值，优先复制options字段里内容，如果是个列表，就直接赋值，如果不是，那边说明是个函数名称，那就执行一下这个函数
                    temp['options'] = extra['options'] if isinstance(extra['options'], list) else extra['options'](self)
                # 过滤器分为base和其他，用于提供给前端进行区分区域，如果没有设定，就都放到base里去
                filter_data[extra['level'] if 'level' in extra else 'base'].append(temp)
            span = 0
            # 以下是计算一下整个过滤器大概是多高，其实没什么太大作用
            for item in filter_data['base']:
                span += item['span'] if 'span' in item else 6
                filter_data['fields'][item['key']] = item['default']
            for item in filter_data['adv']:
                filter_data['fields'][item['key']] = item['default']
            height = (span // 24 + int(bool(span % 24))) * 50
            if height > filter_data['height']:
                filter_data['height'] = height
        # 修改类的初始化数据结构
        update = {
            'fields': dict(),
            'inlines': dict(),
            'detail': list(),
            'tabs': list()
        }
        # 判断是否存在修改类
        if self.update_class:
            # 执行一下这个写入序列化器类
            update_serializer = self.update_class()
            # 获取一下Meta里的custom
            try:
                custom = update_serializer.Meta.custom
            except:
                custom = dict()
            try:
                update['tabs'] = update_serializer.Meta.tabs
            except:
                pass
            try:
                inlines = update_serializer.Meta.inlines
            except:
                inlines = dict()
            # 写入的初始化字段数据可以一次性获得
            update['fields'] = update_serializer.root.data
            # 开始循环包含的字段
            meta = dict()
            for m in update_serializer.Meta.model._meta.fields:
                if not isinstance(m.default, type):
                    meta[m.attname] = bool(m.default) if m.__class__.__name__ == 'BoolField' else m.default
            for key in update_serializer.fields.fields:
                value = update_serializer.fields.fields[key]
                if value.__class__.__name__ == 'HiddenField' and value.field_name in create['fields']:
                    del update['fields'][value.field_name]
                if value.field_name in update['fields'] and value.field_name in meta:
                    update['fields'][value.field_name] = meta[value.field_name]
                self._build_create(update, custom, value)
            for inline_key, inline_value in inlines.items():
                inline_create = {
                    'fields': dict(),
                    'detail': list(),
                    'inlines': dict()
                }
                inline_serializer = inline_value['class']()
                try:
                    inline_custom = inline_serializer.Meta.custom
                except:
                    inline_custom = dict()
                try:
                    inline_create['tabs'] = inline_serializer.Meta.tabs
                except:
                    inline_create['tabs'] = list()
                inline_create['fields'] = inline_serializer.root.data
                field = inline_value['field'] if 'field' in inline_value else inline_key
                del inline_create['fields'][field]
                for field_key in inline_serializer.fields.fields:
                    field_value = inline_serializer.fields.fields[field_key]
                    if field_value.field_name == field:
                        continue
                    if field_value.__class__.__name__ == 'HiddenField' and field_value.field_name in inline_create['fields']:
                        del inline_create['fields'][field_value.field_name]
                    self._build_create(inline_create, inline_custom, field_value)
                update['inlines'][inline_key] = {
                    'label': inline_value['label'] if 'label' in inline_value else inline_serializer.Meta.model._meta.verbose_name,
                    'create': inline_create,
                    'limit': inline_value['limit'] if 'limit' in inline_value else self.inlines_limit,
                    'api': inline_value['api'] if 'api' in inline_value else '',
                    'field': field
                }
                update['fields'][inline_key] = []
        # 写入类的初始化数据结构
        create = {
            'fields': dict(),
            'inlines': dict(),
            'detail': list(),
            'tabs': list()
        }
        # 判断是否存在写入类
        if self.create_class:
            # 执行一下这个写入序列化器类
            create_serializer = self.create_class()
            # 获取一下Meta里的custom
            try:
                custom = create_serializer.Meta.custom
            except:
                custom = dict()
            try:
                create['tabs'] = create_serializer.Meta.tabs
            except:
                pass
            try:
                inlines = create_serializer.Meta.inlines
            except:
                inlines = dict()
            # 写入的初始化字段数据可以一次性获得
            create['fields'] = create_serializer.root.data
            # 开始循环包含的字段
            meta = dict()
            for m in create_serializer.Meta.model._meta.fields:
                if not isinstance(m.default, type):
                    meta[m.attname] = bool(m.default) if m.__class__.__name__ == 'BoolField' else m.default
            for key in create_serializer.fields.fields:
                value = create_serializer.fields.fields[key]
                if value.__class__.__name__ == 'HiddenField' and value.field_name in create['fields']:
                    del create['fields'][value.field_name]
                if value.field_name in create['fields'] and value.field_name in meta:
                    create['fields'][value.field_name] = meta[value.field_name]
                self._build_create(create, custom, value)
            for inline_key, inline_value in inlines.items():
                inline_create = {
                    'fields': dict(),
                    'detail': list(),
                    'inlines': dict()
                }
                inline_serializer = inline_value['class']()
                try:
                    inline_custom = inline_serializer.Meta.custom
                except:
                    inline_custom = dict()
                try:
                    inline_create['tabs'] = inline_serializer.Meta.tabs
                except:
                    inline_create['tabs'] = list()
                inline_create['fields'] = inline_serializer.root.data
                field = inline_value['field'] if 'field' in inline_value else inline_key
                del inline_create['fields'][field]
                for field_key in inline_serializer.fields.fields:
                    field_value = inline_serializer.fields.fields[field_key]
                    if field_value.field_name == field:
                        continue
                    if field_value.__class__.__name__ == 'HiddenField' and field_value.field_name in inline_create['fields']:
                        del inline_create['fields'][field_value.field_name]
                    self._build_create(inline_create, inline_custom, field_value)
                create['inlines'][inline_key] = {
                    'label': inline_value['label'] if 'label' in inline_value else inline_serializer.Meta.model._meta.verbose_name,
                    'create': inline_create,
                    'limit': inline_value['limit'] if 'limit' in inline_value else self.inlines_limit,
                    'api': inline_value['api'] if 'api' in inline_value else '',
                    'field': field
                }
                create['fields'][inline_key] = []
        res = {
            "filter": filter_data,
            "create": create,
            "update": update,
            "list": self._build_list(self.list_class),  # 列表字段生成器，业务逻辑和创建的差不多了
            "read": self._build_list(self.read_class),  # 读取格式数据，业务逻辑和创建的差不多了
            "extra": self.extra
        }
        return Response(res)
