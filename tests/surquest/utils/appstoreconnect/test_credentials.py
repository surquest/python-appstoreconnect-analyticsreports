#!/usr/bin/env python3
# Unit tests for the Credentials class

import unittest
from surquest.utils.appstoreconnect.credentials import Credentials
import jwt
from unittest.mock import patch
from pathlib import Path
import datetime


class TestCredentials(unittest.TestCase):
    def setUp(self):
        self.issuer_id = "TEST_ISSUER_ID"
        self.key_id = "TEST_KEY_ID"
        # Sample ES256 private key (test-only)
        self.key_path = Path.cwd() / "credentials" / "key.p8"
        self.private_key = self.key_path.read_text()
        self.credentials = Credentials(
            issuer_id=self.issuer_id,
            key_id=self.key_id,
            private_key=self.private_key
        )

    def test_generate_token_valid(self):
        token = self.credentials.generate_token()
        decoded = jwt.decode(
            token,
            options={"verify_signature": False},  # We only check payload structure here
            algorithms=["ES256"]
        )

        assert decoded["iss"] == self.issuer_id
        assert decoded["aud"] == "appstoreconnect-v1"
        assert "iat" in decoded
        assert "exp" in decoded
        assert decoded["exp"] > decoded["iat"]

    def test_generate_token_expiration_limit(self):
        try:
            self.credentials.generate_token(expiration_minutes=60)
            assert False, "Expected ValueError for expiration > 20 minutes"
        except ValueError as e:
            assert "oken expiration must be between 1 and 20 minutes." in str(e)

    def test_default_expiration_is_20_minutes(self):
        token = self.credentials.generate_token()
        decoded = jwt.decode(
            token,
            options={"verify_signature": False},
            algorithms=["ES256"]
        )
        iat = decoded["iat"]
        exp = decoded["exp"]
        assert exp - iat == 20 * 60, \
            f"Difference between expected and actual expiration is {exp - iat} seconds"