from google.cloud import datastore

datastore_client = datastore.Client()


def insert(data):
    try:
        print(f"data:{data}")
        kind = "friends_list"  # table name
        task_key = datastore_client.key(kind, data['name'])  # for table DOB name is the primary key
        task = datastore.Entity(task_key)
        task["mobile"] = data['mobile']
        task["dob"] = data['dob']
        datastore_client.put(task)
    except Exception as err:
        print("Exception has occured:" + str(err))


def refactor():
    kind = "friends_list"
    query = datastore_client.query(kind=kind)
    return list(query.fetch())
# insert("Jothi", "015144614367", "May 16th, 1983")
