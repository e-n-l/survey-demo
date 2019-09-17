# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error_model import ErrorModel  # noqa: E501
from swagger_server.models.poll import Poll  # noqa: E501
from swagger_server.models.poll_answer import PollAnswer  # noqa: E501
from swagger_server.models.polls import Polls  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_create_answer(self):
        """Test case for create_answer

        add a new answer
        """
        query_string = [('answer', 'answer_example')]
        response = self.client.open(
            '/create/{poll_id}/answer'.format(poll_id=56),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_post(self):
        """Test case for create_post

        create a poll
        """
        query_string = [('question', 'question_example')]
        response = self.client.open(
            '/create',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_poll(self):
        """Test case for get_poll

        
        """
        response = self.client.open(
            '/poll/{poll_id}/'.format(poll_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_poll_poll_idpost(self):
        """Test case for poll_poll_idpost

        submit answers to poll questions
        """
        query_string = [('vote', 56)]
        response = self.client.open(
            '/poll/{poll_id}/'.format(poll_id=56),
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_polls_get(self):
        """Test case for polls_get

        display all available polls
        """
        response = self.client.open(
            '/polls',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
