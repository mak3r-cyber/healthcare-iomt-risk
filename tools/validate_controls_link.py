#!/usr/bin/env python3
"""Link validator for compliance documentation with security hardening.

Security improvements:
- Path traversal protection using Path().resolve()
- HTTP request timeouts and SSL verification
- Rate limiting to prevent DoS
- Proper error handling and logging

DEPRECATION WARNING:
    This standalone script is deprecated and will be removed in v1.0.
    Please use the riskops CLI instead:

        pip install -e .
        riskops validate links <file_or_directory>

    The new CLI provides the same security features with better error handling
    and integration with the full RiskOps toolkit.
"""
import re
import sys
import time
import warnings
from pathlib import Path
from typing import List, Tuple

import requests

# Deprecation warning
warnings.warn(
    "tools/validate_controls_link.py is deprecated. Use 'riskops validate links' instead. "
    "Install with: pip install -e . && riskops validate links <file>",
    DeprecationWarning,
    stacklevel=2,
)
print("\n" + "=" * 70)
print("⚠️  DEPRECATION WARNING")
print("=" * 70)
print("This script (tools/validate_controls_link.py) is deprecated")
print("\nPlease install and use the riskops CLI instead:")
print("  1. pip install -e .")
print("  2. riskops validate links <file_or_directory>")
print("\nThe CLI provides the same security features with better integration.")
print("=" * 70 + "\n")


# Security: Define allowed directories to prevent path traversal attacks
ALLOWED_DIRS = [
    "docs/compliance",
    "docs/architecture",
    "docs/cces",
    "05-Business-Processes",
]

# Security: HTTP request configuration
REQUEST_TIMEOUT = 10  # seconds
REQUEST_HEADERS = {"User-Agent": "RiskOps-LinkValidator/1.0"}
RATE_LIMIT_DELAY = 0.5  # seconds between requests


def validate_file_path(file_path: str) -> Path:
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
        # Get project root (parent of tools/)
        project_root = Path(__file__).parent.parent.resolve()

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
        is_allowed = any(str(relative_path).startswith(allowed_dir) for allowed_dir in ALLOWED_DIRS)

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


def is_valid_link(url: str) -> bool:
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
            timeout=REQUEST_TIMEOUT,
            verify=True,  # Verify SSL certificates
            headers=REQUEST_HEADERS,
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


def extract_and_validate_links(file_path: Path) -> Tuple[List[str], List[str]]:
    """
    Extracts links from markdown file and validates them.

    Args:
        file_path: Validated Path object to markdown file

    Returns:
        Tuple of (valid_links, invalid_links)
    """
    valid_links = []
    invalid_links = []

    # Read file with explicit encoding
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        print(f"Warning: Unable to decode {file_path} as UTF-8, trying latin-1")
        with open(file_path, "r", encoding="latin-1") as file:
            lines = file.readlines()

    # URL pattern (same as original)
    url_pattern = (
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )

    # Extract and validate links
    print(f"\nScanning {len(lines)} lines for URLs...")

    for line_num, line in enumerate(lines, 1):
        links_in_line = re.findall(url_pattern, line)

        for link in links_in_line:
            # Skip duplicates
            if link in valid_links or link in invalid_links:
                continue

            print(f"Checking: {link}")

            # Security: Rate limiting to prevent DoS
            time.sleep(RATE_LIMIT_DELAY)

            if is_valid_link(link):
                valid_links.append(link)
                print("  ✓ Valid")
            else:
                invalid_links.append(link)
                print("  ✗ Invalid")

    return valid_links, invalid_links


def main():
    """Main function to validate links in compliance documentation."""
    # Default file path
    default_file = "docs/compliance/iso27002-iomt-mapping.md"

    # Allow command-line argument for file path
    file_path_str = sys.argv[1] if len(sys.argv) > 1 else default_file

    print("RiskOps Link Validator v1.0")
    print(f"{'=' * 60}")

    try:
        # Security: Validate file path to prevent path traversal
        validated_path = validate_file_path(file_path_str)
        print(f"Validated file: {validated_path}")

        # Extract and validate links
        valid_links, invalid_links = extract_and_validate_links(validated_path)

        # Display results
        print(f"\n{'=' * 60}")
        print("RESULTS")
        print(f"{'=' * 60}")
        print(f"Valid links: {len(valid_links)}")
        for link in valid_links:
            print(f"  ✓ {link}")

        print(f"\nInvalid links: {len(invalid_links)}")
        for link in invalid_links:
            print(f"  ✗ {link}")

        # Exit with error code if invalid links found
        if invalid_links:
            sys.exit(1)
        else:
            print("\n✓ All links are valid!")
            sys.exit(0)

    except (ValueError, FileNotFoundError) as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
