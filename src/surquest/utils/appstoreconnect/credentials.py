import jwt
import datetime

class Credentials:
    """Handles the creation and generation of JWT tokens for App Store Connect API."""
    def __init__(self, issuer_id: str, key_id: str, private_key: str):
        """
        Initializes the Credentials object with required information.
        
        :param issuer_id: The issuer ID from App Store Connect.
        :param key_id: The key ID for the API key.
        :param private_key: The private key content.
        """
        self.issuer_id = issuer_id
        self.key_id = key_id
        self.private_key = private_key

    def generate_token(self, expiration_minutes: int = 45) -> str:
        """
        Generates a JWT token for App Store Connect API.
        
        :param expiration_minutes: Token expiration time in minutes (max 45)
        :return: Signed JWT token string
        """
        # App Store Connect tokens have a maximum expiration of 45 minutes.
        if expiration_minutes > 45:
            raise ValueError("Token expiration cannot exceed 45 minutes")

        # Set the token's issue and expiration times.
        now = datetime.datetime.utcnow()

        # Define the token headers.
        headers = {
            "alg": "ES256",
            "kid": self.key_id,
            "typ": "JWT"
        }

        # Define the token payload.
        payload = {
            "iss": self.issuer_id,  # Issuer ID
            "iat": now,
            "exp": now + datetime.timedelta(minutes=20),
            "aud": "appstoreconnect-v1"  # Audience (App Store Connect API)
        }

        # Encode the token using the payload, private key, algorithm, and headers.
        token = jwt.encode(
            payload, 
            self.private_key, 
            algorithm="ES256", 
            headers=headers
        )

        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return token
