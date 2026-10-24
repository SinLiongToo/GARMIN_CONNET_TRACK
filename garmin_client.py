"""Garmin Connect Client and Authentication Manager."""

import os
import getpass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

load_dotenv()

TOKEN_DIR = Path.home() / ".garminconnect"


def prompt_mfa_code() -> str:
    """Prompt the user in the terminal for Garmin 2-Factor Authentication (MFA) code."""
    print("\n[!] Garmin MFA / 2FA is required for your account.")
    code = input("Enter the security code sent to your email or phone: ").strip()
    return code


class GarminClientManager:
    """Manages login, token persistence, and session lifecycle with Garmin Connect."""

    def __init__(self, token_dir: Optional[Path] = None):
        self.token_dir = token_dir or TOKEN_DIR
        self.token_dir.mkdir(parents=True, exist_ok=True)
        self.client: Optional[Garmin] = None

    def get_client(self, email: Optional[str] = None, password: Optional[str] = None) -> Garmin:
        """Authenticate with Garmin Connect using cached tokens or credentials."""
        token_path_str = str(self.token_dir)

        # 1. Try restoring existing session from token store
        try:
            client = Garmin()
            client.login(tokenstore=token_path_str)
            self.client = client
            return client
        except Exception:
            # Token expired or not present, proceed with fresh login
            pass

        # 2. Retrieve credentials if not provided
        email = email or os.getenv("GARMIN_EMAIL")
        password = password or os.getenv("GARMIN_PASSWORD")
        is_cn_env = os.getenv("GARMIN_IS_CN", "false").lower() in ("true", "1", "yes")

        if not email:
            print("\n--- Garmin Connect Login ---")
            email = input("Garmin Email: ").strip()

        if not password:
            password = getpass.getpass("Garmin Password: ").strip()

        if not email or not password:
            raise ValueError("Garmin email and password must not be empty.")

        # 3. Perform login with tokenstore persistence and MFA callback
        try:
            client = Garmin(
                email=email,
                password=password,
                is_cn=is_cn_env,
                prompt_mfa=prompt_mfa_code,
            )
            client.login(tokenstore=token_path_str)
            self.client = client
            return client
        except GarminConnectAuthenticationError as e:
            raise RuntimeError(
                f"Authentication failed: Please verify your Garmin email and password.\n"
                f"If you are using special characters, setting them in a .env file is recommended.\n"
                f"Details: {e}"
            )
        except GarminConnectTooManyRequestsError as e:
            raise RuntimeError(
                f"Garmin IP rate limit (HTTP 429): Garmin is temporarily throttling login requests from this IP.\n"
                f"Please wait 5-10 minutes before trying again, or switch networks/hotspot.\n"
                f"Details: {e}"
            )
        except GarminConnectConnectionError as e:
            raise RuntimeError(f"Connection failed: Could not connect to Garmin servers. ({e})")
        except Exception as e:
            raise RuntimeError(f"Failed to login to Garmin Connect: {e}")
