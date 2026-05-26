"""Utility functions for data formatting."""

from datetime import datetime
import locale


def format_currency(value, currency="R$", decimal_places=2):
    """Format value as currency.
    
    Args:
        value: float - Value to format
        currency: str - Currency symbol (default 'R$')
        decimal_places: int - Decimal places (default 2)
    
    Returns:
        str - Formatted currency string
    """
    if value is None:
        return f"{currency} 0,00"
    
    format_str = f"{{:,.{decimal_places}f}}"
    formatted = format_str.format(abs(value))
    # Replace US formatting with BR formatting
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    
    if value < 0:
        return f"-{currency} {formatted}"
    return f"{currency} {formatted}"


def format_percentage(value, decimal_places=2):
    """Format value as percentage.
    
    Args:
        value: float - Value (0-1 or 0-100)
        decimal_places: int - Decimal places
    
    Returns:
        str - Formatted percentage string
    """
    if value is None:
        return "0,00%"
    
    # Assume 0-1 range, multiply by 100
    if value <= 1:
        value *= 100
    
    format_str = f"{{:.{decimal_places}f}}"
    formatted = format_str.format(value)
    formatted = formatted.replace(".", ",")
    
    return f"{formatted}%"


def format_date(date_obj, format="%d/%m/%Y"):
    """Format date object.
    
    Args:
        date_obj: datetime or str - Date to format
        format: str - Format string (default '%d/%m/%Y')
    
    Returns:
        str - Formatted date string
    """
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.fromisoformat(date_obj)
        except:
            return date_obj
    
    if date_obj is None:
        return "-"
    
    return date_obj.strftime(format)


def format_datetime(dt_obj, format="%d/%m/%Y %H:%M:%S"):
    """Format datetime object.
    
    Args:
        dt_obj: datetime or str - Datetime to format
        format: str - Format string
    
    Returns:
        str - Formatted datetime string
    """
    if isinstance(dt_obj, str):
        try:
            dt_obj = datetime.fromisoformat(dt_obj)
        except:
            return dt_obj
    
    if dt_obj is None:
        return "-"
    
    return dt_obj.strftime(format)


def truncate_text(text, max_length=100, suffix="..."):
    """Truncate text to max length.
    
    Args:
        text: str - Text to truncate
        max_length: int - Maximum length
        suffix: str - Suffix to add if truncated
    
    Returns:
        str - Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def highlight_number(value, threshold=0, positive_color="green", negative_color="red"):
    """Return color based on value vs threshold.
    
    Args:
        value: float - Value to check
        threshold: float - Threshold
        positive_color: str - Color name for positive (default 'green')
        negative_color: str - Color name for negative (default 'red')
    
    Returns:
        str - Color name
    """
    if value >= threshold:
        return positive_color
    return negative_color
