import json
from unittest import TestCase, mock

import src.etl.event_processor as sqs
from src.etl.event_processor import TriggerEvent, CapturedData
from src.etl.s3 import S3


@mock.patch('src.etl.s3.boto3.client')
class TestCaptureData(TestCase):

    def setUp(self):
        self.record = {
            's3': {
                'bucket': {'name': 'some-s3-name'},
                'object': {'key': 'data/blah.json'}
            }
        }
        self.region = 'us-south-1'

    def test_this_test_class_works(self, _):
        self.assertTrue(True, "works")

    @mock.patch.object(S3, 'get_file')
    def test_captured_body(self, m_method, _):
        fake_data = {'content': 'this is the body', 'metadata': {}}
        m_method.return_value = json.dumps(fake_data)
        message = CapturedData(self.record, self.region).extract_attributes()
        self.assertEqual(fake_data['content'], message.content)

    @mock.patch.object(S3, 'get_file')
    def test_attribute_url(self, m_method, _):
        the_value = "the url"
        fake_data = {'content': 'this is the body', 'metadata': {'URL': {sqs.STRING_VALUE: the_value}}}
        m_method.return_value = json.dumps(fake_data)
        message = CapturedData(self.record, self.region).extract_attributes()
        self.assertEqual(the_value, message.url)


@mock.patch('src.etl.s3.boto3.client')
class TestTriggerEvent(TestCase):

    def setUp(self):
        self.region = 'us-south-10'
        self.event_1 = {
            'Records': [
                {
                  "eventVersion": "2.0",
                  "eventSource": "aws:s3",
                  "awsRegion": "us-west-2",
                  "eventTime": "1970-01-01T00:00:00.000Z",
                  "eventName": "ObjectCreated:Put",
                  "userIdentity": {
                    "principalId": "EXAMPLE"
                  },
                  "requestParameters": {
                    "sourceIPAddress": "127.0.0.1"
                  },
                  "responseElements": {
                    "x-amz-request-id": "EXAMPLE123456789",
                    "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                  },
                  "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                      "name": "example-bucket",
                      "ownerIdentity": {
                        "principalId": "EXAMPLE"
                      },
                      "arn": "arn:aws:s3:::example-bucket"
                    },
                    "object": {
                      "key": "test/key",
                      "size": 1024,
                      "eTag": "0123456789abcdef0123456789abcdef",
                      "sequencer": "0A1B2C3D4E5F678901"
                    }
                  }
                }
            ]
        }
        self.event_2 = {
            'Records': [
                {
                    "eventVersion": "2.0",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-west-2",
                    "eventTime": "1970-01-01T00:00:00.000Z",
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {
                        "principalId": "EXAMPLE"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "127.0.0.1"
                    },
                    "responseElements": {
                        "x-amz-request-id": "EXAMPLE123456789",
                        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "testConfigRule",
                        "bucket": {
                            "name": "example-bucket",
                            "ownerIdentity": {
                                "principalId": "EXAMPLE"
                            },
                            "arn": "arn:aws:s3:::example-bucket"
                         },
                        "object": {
                            "key": "test/key1",
                            "size": 1024,
                            "eTag": "0123456789abcdef0123456789abcdef",
                            "sequencer": "0A1B2C3D4E5F678901"
                        }
                    }
                },
                {
                    "eventVersion": "2.0",
                    "eventSource": "aws:s3",
                    "awsRegion": "us-west-2",
                    "eventTime": "1970-01-01T00:00:00.000Z",
                    "eventName": "ObjectCreated:Put",
                    "userIdentity": {
                        "principalId": "EXAMPLE"
                    },
                    "requestParameters": {
                        "sourceIPAddress": "127.0.0.1"
                    },
                    "responseElements": {
                        "x-amz-request-id": "EXAMPLE123456789",
                        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
                    },
                    "s3": {
                        "s3SchemaVersion": "1.0",
                        "configurationId": "testConfigRule",
                        "bucket": {
                            "name": "example-bucket",
                            "ownerIdentity": {
                                "principalId": "EXAMPLE"
                            },
                            "arn": "arn:aws:s3:::example-bucket"
                        },
                        "object": {
                            "key": "test/key2",
                            "size": 1024,
                            "eTag": "0123456789zyxwt0123456789zyxwt",
                            "sequencer": "0A1B2C3D4E5F678901"
                        }
                    }
                }
            ]
        }

    @mock.patch.object(S3, 'get_file')
    def test_single_record(self, m_method, _):
        fake_data = {
            'content': 'some content',
            'metadata': {
                'URL': {sqs.STRING_VALUE: 'the URL'},
            }
        }
        m_method.return_value = json.dumps(fake_data)

        te = TriggerEvent(self.region)
        te.extract(self.event_1)
        self.assertEqual(1, len(te.data))
        datum = te.data[0]
        self.assertEqual('some content', datum.content)
        self.assertEqual("the URL", datum.url)

    @mock.patch.object(S3, 'get_file')
    def test_two_records(self, m_method, _):
        fake_data_1 = {
            'content': 'some content 1',
            'metadata': {
                'URL': {sqs.STRING_VALUE: 'the URL 1'}
            }
        }
        fake_data_2 = {
            'content': 'some content 2',
            'metadata': {
                'URL': {sqs.STRING_VALUE: 'the URL 2'}
            }
        }
        m_method.side_effect = [json.dumps(fake_data_1), json.dumps(fake_data_2)]

        te = TriggerEvent(self.region)
        te.extract(self.event_2)
        self.assertEqual(2, len(te.data))
        datum_1 = te.data[0]
        self.assertEqual('some content 1', datum_1.content)
        self.assertEqual("the URL 1", datum_1.url)
        datum_2 = te.data[1]
        self.assertEqual('some content 2', datum_2.content)
        self.assertEqual("the URL 2", datum_2.url)
