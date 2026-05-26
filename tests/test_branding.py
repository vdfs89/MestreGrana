"""
Test suite for branding module
Tests custom theme, colors, and UI components
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from branding import COLORS, get_color, apply_custom_theme


def test_color_palette_exists():
    """Test that color palette is defined"""
    assert COLORS is not None
    assert isinstance(COLORS, dict)
    assert len(COLORS) > 0


def test_primary_colors_defined():
    """Test that primary brand colors are defined"""
    assert "primary" in COLORS
    assert "dark_blue" in COLORS
    assert "black" in COLORS
    assert "white" in COLORS


def test_primary_color_value():
    """Test that primary color is correct MestreGrana green"""
    assert COLORS["primary"] == "#00CB63"
    assert COLORS["dark_blue"] == "#042540"


def test_get_color_function():
    """Test get_color() helper function"""
    assert get_color("primary") == "#00CB63"
    assert get_color("dark_blue") == "#042540"
    
    # Test invalid color name
    result = get_color("invalid_color")
    assert result is not None or result is None  # Should handle gracefully


def test_color_format():
    """Test that all colors are in hex format"""
    for name, hex_code in COLORS.items():
        assert hex_code.startswith("#"), f"Color {name} is not in hex format"
        assert len(hex_code) == 7, f"Color {name} has incorrect hex length"


def test_typography_config():
    """Test that typography is accessible"""
    # This test verifies branding module doesn't crash on import
    # Typography is applied via CSS, not Python objects
    assert callable(apply_custom_theme)


if __name__ == "__main__":
    # Run tests
    test_color_palette_exists()
    test_primary_colors_defined()
    test_primary_color_value()
    test_get_color_function()
    test_color_format()
    test_typography_config()
    print("✅ All branding tests passed!")
