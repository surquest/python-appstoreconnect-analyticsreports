import jwt
from datetime import datetime, timedelta
from typing import Optional

class Credentials:
    """Handles creation and signing of JWT tokens for the App Store Connect API."""

    MAX_EXPIRATION_MINUTES = 20

    def __init__(self, issuer_id: str, key_id: str, private_key: str):
        """
        Initialize the Credentials object.

        Args:
            issuer_id (str): The issuer ID from App Store Connect.
            key_id (str): The key ID for the API key.
            private_key (str): The private key (P8 format) used for signing the token.
        """
        if not issuer_id or not key_id or not private_key:
            raise ValueError("issuer_id, key_id, and private_key are all required.")
        
        self.issuer_id = issuer_id
        self.key_id = key_id
        self.private_key = private_key

    def generate_token(self, expiration_minutes: int = 20) -> str:
        """
        Generate a signed JWT token.

        Args:
            expiration_minutes (int, optional): Token lifetime in minutes (max 20). Defaults to 20.

        Returns:
            str: The signed JWT token string.

        Raises:
            ValueError: If expiration exceeds the allowed maximum.
        """
        if not (0 < expiration_minutes <= self.MAX_EXPIRATION_MINUTES):
            raise ValueError(f"Token expiration must be between 1 and {self.MAX_EXPIRATION_MINUTES} minutes.")

        now = datetime.utcnow()
        exp_time = now + timedelta(minutes=expiration_minutes)

        payload = {
            "iss": self.issuer_id,
            "iat": int(now.timestamp()),
            "exp": int(exp_time.timestamp()),
            "aud": "appstoreconnect-v1"
        }

        headers = {
            "alg": "ES256",
            "kid": self.key_id,
            "typ": "JWT"
        }

        return jwt.encode(
            payload=payload,
            key=self.private_key,
            algorithm="ES256",
            headers=headers
        )
