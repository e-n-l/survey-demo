# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.poll_answer import PollAnswer  # noqa: F401,E501
from swagger_server.models.user import User  # noqa: F401,E501
from swagger_server import util


class PollVote(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, poll_id: int=None, voter: User=None, answer: PollAnswer=None):  # noqa: E501
        """PollVote - a model defined in Swagger

        :param poll_id: The poll_id of this PollVote.  # noqa: E501
        :type poll_id: int
        :param voter: The voter of this PollVote.  # noqa: E501
        :type voter: User
        :param answer: The answer of this PollVote.  # noqa: E501
        :type answer: PollAnswer
        """
        self.swagger_types = {
            'poll_id': int,
            'voter': User,
            'answer': PollAnswer
        }

        self.attribute_map = {
            'poll_id': 'poll_id',
            'voter': 'voter',
            'answer': 'answer'
        }
        self._poll_id = poll_id
        self._voter = voter
        self._answer = answer

    @classmethod
    def from_dict(cls, dikt) -> 'PollVote':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PollVote of this PollVote.  # noqa: E501
        :rtype: PollVote
        """
        return util.deserialize_model(dikt, cls)

    @property
    def poll_id(self) -> int:
        """Gets the poll_id of this PollVote.


        :return: The poll_id of this PollVote.
        :rtype: int
        """
        return self._poll_id

    @poll_id.setter
    def poll_id(self, poll_id: int):
        """Sets the poll_id of this PollVote.


        :param poll_id: The poll_id of this PollVote.
        :type poll_id: int
        """
        if poll_id is None:
            raise ValueError("Invalid value for `poll_id`, must not be `None`")  # noqa: E501

        self._poll_id = poll_id

    @property
    def voter(self) -> User:
        """Gets the voter of this PollVote.


        :return: The voter of this PollVote.
        :rtype: User
        """
        return self._voter

    @voter.setter
    def voter(self, voter: User):
        """Sets the voter of this PollVote.


        :param voter: The voter of this PollVote.
        :type voter: User
        """
        if voter is None:
            raise ValueError("Invalid value for `voter`, must not be `None`")  # noqa: E501

        self._voter = voter

    @property
    def answer(self) -> PollAnswer:
        """Gets the answer of this PollVote.


        :return: The answer of this PollVote.
        :rtype: PollAnswer
        """
        return self._answer

    @answer.setter
    def answer(self, answer: PollAnswer):
        """Sets the answer of this PollVote.


        :param answer: The answer of this PollVote.
        :type answer: PollAnswer
        """
        if answer is None:
            raise ValueError("Invalid value for `answer`, must not be `None`")  # noqa: E501

        self._answer = answer
