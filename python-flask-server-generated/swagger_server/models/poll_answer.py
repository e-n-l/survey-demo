# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class PollAnswer(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, poll_id: int=None, answer_id: int=None, answer: str=None):  # noqa: E501
        """PollAnswer - a model defined in Swagger

        :param poll_id: The poll_id of this PollAnswer.  # noqa: E501
        :type poll_id: int
        :param answer_id: The answer_id of this PollAnswer.  # noqa: E501
        :type answer_id: int
        :param answer: The answer of this PollAnswer.  # noqa: E501
        :type answer: str
        """
        self.swagger_types = {
            'poll_id': int,
            'answer_id': int,
            'answer': str
        }

        self.attribute_map = {
            'poll_id': 'poll_id',
            'answer_id': 'answer_id',
            'answer': 'answer'
        }
        self._poll_id = poll_id
        self._answer_id = answer_id
        self._answer = answer

    @classmethod
    def from_dict(cls, dikt) -> 'PollAnswer':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PollAnswer of this PollAnswer.  # noqa: E501
        :rtype: PollAnswer
        """
        return util.deserialize_model(dikt, cls)

    @property
    def poll_id(self) -> int:
        """Gets the poll_id of this PollAnswer.


        :return: The poll_id of this PollAnswer.
        :rtype: int
        """
        return self._poll_id

    @poll_id.setter
    def poll_id(self, poll_id: int):
        """Sets the poll_id of this PollAnswer.


        :param poll_id: The poll_id of this PollAnswer.
        :type poll_id: int
        """
        if poll_id is None:
            raise ValueError("Invalid value for `poll_id`, must not be `None`")  # noqa: E501

        self._poll_id = poll_id

    @property
    def answer_id(self) -> int:
        """Gets the answer_id of this PollAnswer.


        :return: The answer_id of this PollAnswer.
        :rtype: int
        """
        return self._answer_id

    @answer_id.setter
    def answer_id(self, answer_id: int):
        """Sets the answer_id of this PollAnswer.


        :param answer_id: The answer_id of this PollAnswer.
        :type answer_id: int
        """

        self._answer_id = answer_id

    @property
    def answer(self) -> str:
        """Gets the answer of this PollAnswer.


        :return: The answer of this PollAnswer.
        :rtype: str
        """
        return self._answer

    @answer.setter
    def answer(self, answer: str):
        """Sets the answer of this PollAnswer.


        :param answer: The answer of this PollAnswer.
        :type answer: str
        """

        self._answer = answer
