#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''Add a user
        '''
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''Find user by <args>
        '''
        for i in kwargs.keys():
            if i not in dir(User):
                raise InvalidRequestError

        found = self._session.query(User).filter_by(**kwargs).first()
        if not found:
            raise NoResultFound

        return found

    def update_user(self, user_id: int, **kwargs) -> None:
        '''update User
        '''
        found = self.find_user_by(id=user_id)

        for key, value in kwargs.items():
            if not hasattr(found, key):
                raise ValueError
            setattr(found, key, value)

        self._session.commit()
        return None
