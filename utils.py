import re
import httpx
async def is_valid_link(url: str) -> bool:
    # Simple regex pattern for a basic URL validation
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Check if the URL matches the regex
    if re.match(regex, url) is None:
        return False

    # Attempt to make an HTTP request to the URL
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            # Check if the status code is OK (200)
            return response.status_code == 200
    except Exception as e:
        return False
