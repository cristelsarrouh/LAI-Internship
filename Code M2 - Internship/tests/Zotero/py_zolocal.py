from pprint import pprint
from pyzolocal.sqls import gets as g

x = g.get_attachments()[:3]
print(x)
# pprint(g.get_items_info()[:3])
