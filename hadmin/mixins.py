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
    # 扩展自定义信息
    extra = None

    @staticmethod
    def _build_label(tmp, value):
        if tmp['label'].replace(" ", "_").lower() == tmp['field_name']:
            try:
                tmp['label'] = value.root.Meta.model._meta.get_field(tmp['field_name']).verbose_name
            except:
                pass
        return tmp

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
        # 写入类的初始化数据结构
        create = {
            'fields': dict(),
            'detail': list()
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
                create['tabs'] = list()
            # 写入的初始化字段数据可以一次性获得
            create['fields'] = create_serializer.root.data
            # 开始循环包含的字段
            for key in create_serializer.fields.fields:
                value = create_serializer.fields.fields[key]
                # 如果这个字段不是只读模式
                if not value.read_only:
                    tmp = {
                        'label': value.label,  # 字段名称
                        'help_text': value.help_text,  # 辅助说明，默认读取模型的，如果序列化器设定了，就是序列化器的了
                        'field_name': value.field_name,  # 字段名
                        'required': value.required,  # 是否必填
                        'type': str(value.__class__.__name__),  # 字段类型
                        'rules': [],  # 验证器
                        'choices': [],  # 选择项
                        'choices_apis': [],  # 选择项远程搜索api接口和关键字段等相关约定,包括创建许可和规则
                        'method': '',  # 渲染方式，如果没有指定，就采用type来自动匹配
                    }
                    # 清洗一下label
                    tmp = self._build_label(tmp, value)
                    # 添加rules
                    if value.required:
                        rule = {
                            'required': True,
                            'message': value.error_messages['required']
                        }
                        tmp['rules'].append(rule)
                    # 把choices的内容放到数据里
                    try:
                        for v in value.choices.items():
                            tmp['choices'].append({
                                'value': v[0],
                                'label': v[1]
                            })
                    except:
                        pass
                    # 合并序列化器里的custom定义的内容
                    if value.field_name in custom:
                        tmp.update(custom[value.field_name])
                    create['detail'].append(tmp)
        # 列表字段生成器，业务逻辑和创建的差不多了
        list_data = list()
        if self.list_class:
            list_serializer = self.list_class()
            try:
                custom = list_serializer.Meta.custom
            except:
                custom = dict()
            for key in list_serializer.fields.fields:
                value = list_serializer.fields.fields[key]
                tmp = {
                    'label': value.label,
                    'field_name': value.field_name,
                    'type': str(value.__class__.__name__)
                }
                # 清洗一下label
                tmp = self._build_label(tmp, value)
                # 覆盖自定义数据到配置字典
                if value.field_name in custom:
                    tmp.update(custom[value.field_name])
                list_data.append(tmp)
        # 读取格式数据，业务逻辑和创建的差不多了
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
                # 清洗一下label
                tmp = self._build_label(tmp, value)
                # 覆盖自定义数据到配置字典
                if value.field_name in custom:
                    tmp.update(custom[value.field_name])
                read_data.append(tmp)
        res = {
            "filter": filter_data,
            "create": create,
            "list": list_data,
            "read": read_data,
            "extra": self.extra
        }
        return Response(res)
