#!/usr/bin/env python3
# Unit tests for the Credentials class

import unittest
from unittest.mock import patch
import datetime
import jwt
from src.surquest.utils.appstoreconnect.credentials import Credentials

# Test class for Credentials
class TestCredentials(unittest.TestCase):

    # Set up the test environment
    def setUp(self):
        self.issuer_id = "test_issuer_id"
        self.key_id = "test_key_id"
        self.private_key = "test_private_key"
        # Create a Credentials object with test data
        self.credentials = Credentials(self.issuer_id, self.key_id, self.private_key)

    # Test token generation with default expiration
    def test_generate_token_default_expiration(self):
        # Patch datetime to control the current time
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.timedelta.return_value = datetime.timedelta(minutes=45)
            mock_datetime.timestamp.return_value = 1672588800.0 # timestamp for 2023-01-01 12:00:00 UTC
            
            # Expected payload for the JWT
            expected_payload = {
                "iss": self.issuer_id,
                "iat": 1672588800,
                "exp": 1672588800 + (45 * 60),
                "aud": "appstoreconnect-v1"
            }
            # Expected headers for the JWT
            expected_headers = {
                "alg": "ES256",
                "kid": self.key_id,
                "typ": "JWT"
            }

            # Patch jwt.encode to control the encoding result
            with patch('jwt.encode') as mock_jwt_encode:
                mock_jwt_encode.return_value = b"encoded_token"
                # Generate the token
                token = self.credentials.generate_token()
                # Assert that jwt.encode was called with the expected arguments
                mock_jwt_encode.assert_called_once_with(
                    expected_payload,
                    self.private_key,
                    algorithm="ES256",
                    headers=expected_headers
                )
                # Assert that the generated token matches the expected token
                self.assertEqual(token, "encoded_token")

    # Test token generation with custom expiration
    def test_generate_token_custom_expiration(self):
        # g  datetime to control the current time
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.timedelta.return_value = datetime.timedelta(minutes=30)
            mock_datetime.timestamp.return_value = 1672588800.0

            # Expected payload for the JWT with custom expiration
            expected_payload = {
                "iss": self.issuer_id,
                "iat": 1672588800,
                "exp": 1672588800 + (30 * 60),
                "aud": "appstoreconnect-v1"
            }
            # Expected headers for the JWT
            expected_headers = {
                "alg": "ES256",
                "kid": self.key_id,
                "typ": "JWT"
            }
            
            # Patch jwt.encode to control the encoding result
            with patch('jwt.encode') as mock_jwt_encode:
                mock_jwt_encode.return_value = b"encoded_token_30"
                # Generate the token with custom expiration
                token = self.credentials.generate_token(expiration_minutes=30)
                # Assert that jwt.encode was called with the expected arguments
                mock_jwt_encode.assert_called_once_with(
                    expected_payload,
                    self.private_key,
                    algorithm="ES256",
                    headers=expected_headers
                )
                # Assert that the generated token matches the expected token
                self.assertEqual(token, "encoded_token_30")

    # Test token generation with expiration exceeding 45 minutes
    def test_generate_token_expiration_exceeds_45_minutes(self):
        # Assert that a ValueError is raised
        with self.assertRaises(ValueError) as cm:
            # Attempt to generate a token with expiration exceeding 45 minutes
            self.credentials.generate_token(expiration_minutes=46)
        # Assert that the exception message is correct
        self.assertEqual(str(cm.exception), "Token expiration cannot exceed 45 minutes")

    # Test that the generated token is a string
    def test_generate_token_returns_string(self):
        # Patch datetime to control the current time
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.utcnow.return_value = datetime.datetime(2023, 1, 1, 12, 0, 0)
            mock_datetime.timedelta.return_value = datetime.timedelta(minutes=45)
            mock_datetime.timestamp.return_value = 1672588800.0

            # Patch jwt.encode to control the encoding result
            with patch('jwt.encode') as mock_jwt_encode:
                mock_jwt_encode.return_value = "encoded_token_string"
                # Generate the token
                token = self.credentials.generate_token()
                # Assert that the generated token is a string
                self.assertIsInstance(token, str)
                # Assert that the generated token matches the expected string
                self.assertEqual(token, "encoded_token_string")
