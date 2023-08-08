# print(type(list_data))

# for i in list_data:
# print(type(i))
# print(i.keys())
# print(i['columns'])
# print("records:", i['records'])
# x = i['records']
# print(type(x))
# for j in i['records']:
# print(type(j))
# print(j.keys())
# print(j['table'])
# print(j['values'])

from push import db_colect

print(db_colect.set_app())
print(db_colect.create_links())
