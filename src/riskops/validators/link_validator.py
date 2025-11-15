"""Link validator for compliance documentation with security hardening.

Security improvements:
- Path traversal protection using Path().resolve()
- HTTP request timeouts and SSL verification
- Rate limiting to prevent DoS
- Proper error handling and logging
"""

import re
import time
from pathlib import Path
from typing import List, Tuple

import requests

from riskops.core.constants import ALLOWED_DIRS, RATE_LIMIT_DELAY, REQUEST_HEADERS, REQUEST_TIMEOUT


class LinkValidator:
    """Validates links in markdown documentation files with security features."""

    def __init__(self, timeout: int = REQUEST_TIMEOUT, rate_limit: float = RATE_LIMIT_DELAY):
        """
        Initialize link validator.

        Args:
            timeout: HTTP request timeout in seconds
            rate_limit: Delay between requests in seconds
        """
        self.timeout = timeout
        self.rate_limit = rate_limit
        self.headers = REQUEST_HEADERS
        # URL pattern for matching HTTP/HTTPS links
        self.url_pattern = (
            r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        )

    def validate_file_path(self, file_path: str) -> Path:
        """
        Validates file path to prevent path traversal attacks.

        Security measures:
        - Resolves to absolute path to prevent ../.. attacks
        - Validates against whitelist of allowed directories
        - Ensures file exists and is readable

        Args:
            file_path: Relative or absolute path to validate

        Returns:
            Validated Path object

        Raises:
            ValueError: If path is invalid or outside allowed directories
            FileNotFoundError: If file does not exist
        """
        try:
            # Get project root (parent of src/)
            project_root = Path(__file__).parent.parent.parent.parent.resolve()

            # Convert to Path and resolve to absolute path (prevents ../ attacks)
            if Path(file_path).is_absolute():
                resolved_path = Path(file_path).resolve()
            else:
                resolved_path = (project_root / file_path).resolve()

            # Security check: Ensure path is within project root
            if project_root not in resolved_path.parents and resolved_path != project_root:
                raise ValueError(
                    f"Security: Path {resolved_path} is outside project root {project_root}"
                )

            # Security check: Validate against allowed directories
            relative_path = resolved_path.relative_to(project_root)
            is_allowed = any(
                str(relative_path).startswith(allowed_dir) for allowed_dir in ALLOWED_DIRS
            )

            if not is_allowed:
                raise ValueError(
                    f"Security: Path {relative_path} is not in allowed directories: {ALLOWED_DIRS}"
                )

            # Check file exists
            if not resolved_path.exists():
                raise FileNotFoundError(f"File not found: {resolved_path}")

            # Check file is readable
            if not resolved_path.is_file():
                raise ValueError(f"Path is not a file: {resolved_path}")

            return resolved_path

        except Exception as e:
            print(f"Error validating path '{file_path}': {e}")
            raise

    def is_valid_link(self, url: str) -> bool:
        """
        Checks if a URL is valid and accessible.

        Security improvements:
        - Timeout to prevent hanging connections
        - SSL certificate verification enabled
        - Custom User-Agent header
        - Comprehensive error handling

        Args:
            url: URL to validate

        Returns:
            True if URL returns HTTP 200, False otherwise
        """
        try:
            # Security: Set timeout, verify SSL, add User-Agent
            response = requests.get(
                url,
                timeout=self.timeout,
                verify=True,  # Verify SSL certificates
                headers=self.headers,
                allow_redirects=True,  # Follow redirects but with timeout
            )
            return response.status_code == 200

        except requests.exceptions.SSLError as e:
            print(f"SSL Error for {url}: {e}")
            return False
        except requests.exceptions.Timeout as e:
            print(f"Timeout for {url}: {e}")
            return False
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error for {url}: {e}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Request Error for {url}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error for {url}: {e}")
            return False

    def extract_links(self, file_path: Path) -> List[str]:
        """
        Extracts all HTTP/HTTPS links from a file.

        Args:
            file_path: Path to file to extract links from

        Returns:
            List of unique URLs found in the file
        """
        links = []

        # Read file with explicit encoding
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            print(f"Warning: Unable to decode {file_path} as UTF-8, trying latin-1")
            with open(file_path, "r", encoding="latin-1") as file:
                lines = file.readlines()

        # Extract links using regex
        for line in lines:
            found_links = re.findall(self.url_pattern, line)
            links.extend(found_links)

        # Return unique links only
        return list(set(links))

    def validate_links(self, file_path: Path, verbose: bool = True) -> Tuple[List[str], List[str]]:
        """
        Validates all links in a file.

        Args:
            file_path: Path to file containing links
            verbose: Whether to print progress messages

        Returns:
            Tuple of (valid_links, invalid_links)
        """
        valid_links = []
        invalid_links = []

        # Extract all links
        links = self.extract_links(file_path)

        if verbose:
            print(f"\nFound {len(links)} unique URLs in {file_path.name}")

        # Validate each link
        for link in links:
            if verbose:
                print(f"Checking: {link}")

            # Security: Rate limiting to prevent DoS
            time.sleep(self.rate_limit)

            if self.is_valid_link(link):
                valid_links.append(link)
                if verbose:
                    print("   Valid")
            else:
                invalid_links.append(link)
                if verbose:
                    print("   Invalid")

        return valid_links, invalid_links


def validate_documentation_links(file_path: str, verbose: bool = True) -> bool:
    """
    Convenience function to validate links in a documentation file.

    Args:
        file_path: Path to documentation file
        verbose: Whether to print detailed output

    Returns:
        True if all links are valid, False otherwise

    Example:
        >>> validate_documentation_links("docs/compliance/iso27002-iomt-mapping.md")
        True
    """
    validator = LinkValidator()

    try:
        # Validate file path
        validated_path = validator.validate_file_path(file_path)

        if verbose:
            print("=" * 60)
            print("RiskOps Link Validator")
            print("=" * 60)
            print(f"Validating: {validated_path}")

        # Validate links
        valid_links, invalid_links = validator.validate_links(validated_path, verbose=verbose)

        # Display results
        if verbose:
            print("\n" + "=" * 60)
            print("RESULTS")
            print("=" * 60)
            print(f"Valid links: {len(valid_links)}")
            for link in valid_links:
                print(f"   {link}")

            print(f"\nInvalid links: {len(invalid_links)}")
            for link in invalid_links:
                print(f"   {link}")

        # Return True if all links valid
        return len(invalid_links) == 0

    except (ValueError, FileNotFoundError) as e:
        if verbose:
            print(f"\nError: {e}")
        return False
