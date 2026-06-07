"""
Azure Key Vault secret fetching via DefaultAzureCredential.

How DefaultAzureCredential works (in order of precedence):
1. Environment variables (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID) — CI/CD
2. Workload identity (AKS)
3. Managed Identity — what App Service uses in production (no credentials needed)
4. Azure CLI (`az login`) — what you use locally during development
5. ...several more fallbacks

This means the exact same code works locally (uses your az login session)
and in production (uses the App Service managed identity). Zero code changes between environments.

Requirements:
    uv add azure-identity azure-keyvault-secrets
"""

import os
import logging
from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.core.exceptions import ResourceNotFoundError, ClientAuthenticationError

logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def _get_secret_client() -> SecretClient:
    """
    Build and cache a SecretClient for the duration of the process.

    lru_cache ensures we only instantiate DefaultAzureCredential once —
    it does auth token negotiation on first use, caching the result internally.
    """
    vault_uri = os.environ.get("KEY_VAULT_URI")
    if not vault_uri:
        raise EnvironmentError(
            "KEY_VAULT_URI environment variable is not set. "
            "Set it to your Key Vault URI (e.g. https://weatherdjango-kv.vault.azure.net/) "
            "for both local dev and production."
        )

    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_uri, credential=credential)


def get_secret(secret_name: str) -> str:
    """
    Fetch a secret from Azure Key Vault by name.

    Args:
        secret_name: The name of the secret in Key Vault (e.g. "OPENWEATHER-API-KEY")

    Returns:
        The secret value as a string.

    Raises:
        EnvironmentError: KEY_VAULT_URI is not configured.
        ResourceNotFoundError: Secret does not exist in the vault.
        ClientAuthenticationError: Identity has no permission to read this secret.
    """
    try:
        client = _get_secret_client()
        secret = client.get_secret(secret_name)
        logger.debug("Successfully fetched secret: %s", secret_name)
        return secret.value
    except ClientAuthenticationError as e:
        logger.error(
            "Authentication failed when fetching secret '%s'. "
            "Locally: run `az login`. In production: check managed identity role assignment. "
            "Error: %s", secret_name, e
        )
        raise
    except ResourceNotFoundError:
        logger.error("Secret '%s' not found in Key Vault.", secret_name)
        raise


def get_openweather_api_key() -> str:
    """Convenience wrapper — fetches the OpenWeatherMap API key."""
    return get_secret("OPENWEATHER-API-KEY")


def get_django_secret_key() -> str:
    """Convenience wrapper — fetches the Django SECRET_KEY."""
    return get_secret("DJANGO-SECRET-KEY")
