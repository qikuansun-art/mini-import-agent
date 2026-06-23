STANDARD_FIELDS = [
    {
        "field": "item_no",
        "display_name": "编号",
        "aliases": ["编号", "清单编号", "构件编号", "元件编号", "板件编号", "item_no"],
        "required": True,
    },
    {
        "field": "name",
        "display_name": "名称",
        "aliases": ["名称", "商品名称", "产品名称", "元件名称", "板件名称", "品名"],
        "required": False,
    },
    {
        "field": "length",
        "display_name": "长",
        "aliases": ["长", "长度", "L", "length"],
        "required": True,
    },
    {
        "field": "width",
        "display_name": "宽",
        "aliases": ["宽", "宽度", "W", "width"],
        "required": True,
    },
    {
        "field": "thickness",
        "display_name": "厚",
        "aliases": ["厚", "厚度", "T", "thickness"],
        "required": False,
    },
    {
        "field": "material",
        "display_name": "材质",
        "aliases": ["材质", "石材", "材料", "material"],
        "required": False,
    },
    {
        "field": "quantity",
        "display_name": "数量",
        "aliases": ["数量", "件数", "个数", "qty", "quantity"],
        "required": True,
    },
    {
        "field": "process",
        "display_name": "工艺",
        "aliases": ["工艺", "加工工艺", "切割工艺", "process"],
        "required": False,
    },
    {
        "field": "remark",
        "display_name": "备注",
        "aliases": ["备注", "说明", "remark"],
        "required": False,
    },
]
