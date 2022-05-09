"""
1. Deeper filter by JSON and JSONB columns like
mount_event.directory->>'city_name' ilike '%Almat%'

2. Self Alchemy Session managing Provider

3. From row with one to many like:
select
test.id as test_id, test.name as test_name,
test2.id as test2_id, test2.test_id as test2_test_id
from test
join test2 on test.id = test2.test_id
result:
test_id=1, test_name='some_name', test2_id=1, test2_test_id=1,
test_id=1, test_name='some_name', test2_id=2, test2_test_id=1,
test_id=1, test_name='some_name', test2_id=3, test2_test_id=1,
test_id=1, test_name='some_name', test2_id=4, test2_test_id=1,

and object result should be like:
class Test2:
    id: int
    test_id: int


class Test:
    id: int
    name: str
    test2_list: List[Test2]


result = Test(id=1, name='some_name', test2_list=[
    Test2(id=1, test_id=1),
    Test2(id=2, test_id=1),
    Test2(id=3, test_id=1),
    Test2(id=4, test_id=1)
])

"""
