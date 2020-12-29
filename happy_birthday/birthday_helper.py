from google.cloud import datastore

datastore_client = datastore.Client()


def insert(name, mobile, dob):
    try:
        kind = "DOB"  # table name
        task_key = datastore_client.key(kind, name)
        task = datastore.Entity(key=task_key)
        task["mobile"] = mobile
        task["dob"] = dob
        datastore_client.put(task)
    except Exception as err:
        print("Exception has occured:" + str(err))


insert("jonasa", "015144614367", "May 16th, 1983")
