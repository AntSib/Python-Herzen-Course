from pymongo import MongoClient

class MongoDBConnectManager(object):
    def __init__(self, host="mongodb://localhost:27017/", username="admin", password="admin"):
        """
        Create a new instance of the MongoDBConnectManager class.

        :param host: The url of the MongoDB server
        :param username: The username to use for authentication
        :param password: The password to use for authentication
        :return: a MongoDBConnectManager instance
        """
        self.host = host
        self.username = username
        self.password = password
        self.connection = None

    def __enter__(self):
        """
        Start a new connection to the MongoDB server.

        :return: the MongoDBConnectManager instance
        """
        self.connection = MongoClient(
            self.host,
            username=self.username, password=self.password,
            authMechanism="SCRAM-SHA-1"
            )
        
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()


def main():
    mongo = MongoDBConnectManager(host="mongodb://localhost:27017/", username="AntSibAdmin", password="AntSibDBPassword")

    with mongo as mongo_client:
        users = mongo_client.connection['mynewdb']['user']

        # users_lst = [
        #     {'name': 'Ada Lovelace', 'age': 205},
        #     {'name': 'Guide van Rossum', 'age': 67},
        #     {'name': 'James Gosling', 'age': 69}
        # ]
        
        # users.insert_one({'name': 'Ivan', 'age': 205})
        # users.insert_many(users_lst)
        # users.delete_many({})

        print(f"All users:")
        found_users = users.find()

        for user in found_users:
            print(user)
        
        print(f"User by age 205")
        found_users = users.find({'age': 205})

        for user in found_users:
            print(user)


if __name__ == "__main__":
    main()

# Подключение к локальной базе данных MongoDB
# client = MongoClient('mongodb://localhost:27017/')

# # Выбор базы данных
# db = client['mydatabase']

# # Работа с коллекцией (таблицей в MongoDB)
# collection = db['mycollection']

# # Пример вставки документа
# collection.insert_one({"name": "John", "age": 30})

# # Пример чтения документа
# document = collection.find_one({"name": "John"})
# print(document)
