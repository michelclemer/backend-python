# pylint: disable=E1101

from typing import List
from src.domain.models import Users
from src.infra.config import DBConnectionHandler
from src.infra.entities import Users as UsersModel


class UserRepository:
    """Class to manage User Repository"""

    @classmethod
    def insert_user(self, name: str, password: str) -> Users:
        """insert data in user entity
        :param - name: person name
                - password: user password

        return tuple with new user inserted

        """
        with DBConnectionHandler() as db_connect:
            try:
                new_user = UsersModel(name=name, password=password)
                db_connect.session.add(new_user)
                db_connect.session.commit()

                return Users(
                    id=new_user.id, name=new_user.name, password=new_user.password
                )
            except:
                db_connect.session.rollback()
                raise
            finally:
                db_connect.session.close()
        return None

    @classmethod
    def select_user(cls, user_id: int = None, name: str = None) -> List[Users]:
        """
        Select data in user entity by id and/or name
        :param - user_id: Id od the registy
               - name: User name
        :return - List with Users selected
        """

        try:
            query_data = None
            if user_id and not name:
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(UsersModel)
                        .filter_by(id=user_id)
                        .one()
                    )
                    query_data = [data]
            elif not user_id and name:
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(UsersModel)
                        .filter_by(name=name)
                        .one()
                    )
                    query_data = [data]

            elif user_id and name:
                with DBConnectionHandler() as db_connection:
                    data = (
                        db_connection.session.query(UsersModel)
                        .filter_by(id=user_id, name=name)
                        .one()
                    )
                    query_data = [data]
            return query_data
        except:
            db_connection.session.reollback()
            raise
        finally:
            db_connection.session.close()
        return None
