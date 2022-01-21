# pylint: disable=E1101

from collections import namedtuple
from src.infra.config import DBConnectionHandler
from src.infra.entities import Users


class UserRepository:
    """Class to manage User Repository"""

    @classmethod
    def insert_user(self, name: str, password: str) -> Users:
        """insert data in user entity
        :param - name: person name
                - password: user password

        return tuple with new user inserted

        """
        InsertData = namedtuple("Users", "id name, password")
        with DBConnectionHandler() as db_connect:
            try:
                new_user = Users(name=name, password=password)
                db_connect.session.add(new_user)
                db_connect.session.commit()

                return InsertData(
                    id=new_user.id, name=new_user.name, password=new_user.password
                )
            except:
                db_connect.session.rollback()
                raise
            finally:
                db_connect.session.close()
        return None
