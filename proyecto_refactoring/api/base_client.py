"""Cliente HTTP robusto con timeout, reintentos y backoff exponencial."""

import logging
import time

import requests

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10
DEFAULT_MAX_RETRIES = 3
BACKOFF_CAP = 4


class APIClient:
    """Base para clientes de APIs REST."""

    def __init__(
        self,
        base_url: str,
        api_key: str = "",
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        debug: bool = False,
        verbose: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.debug = debug
        self.verbose = verbose

    def get_json(self, path: str = "", params: dict | None = None) -> dict | list:
        """Realiza la petición GET con timeout y reintentos con backoff."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                if self.debug:
                    logger.debug("GET %s", url)
                response = requests.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as err:
                last_error = err
                if self.verbose:
                    logger.warning(
                        "Intento %d falló para %s: %s", attempt + 1, url, err
                    )
                time.sleep(min(2**attempt, BACKOFF_CAP))
        raise ConnectionError(
            f"Fallaron {self.max_retries} intentos para {url}"
        ) from last_error
