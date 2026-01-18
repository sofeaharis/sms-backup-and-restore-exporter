"""Tests for mms_media_extractor module."""
from pathlib import Path

import pytest

from src.mms_media_extractor import (
    get_datetime_from_epoch_milliseconds,
    handle_duplicate_name,
    safe_filename,
)


class TestGetDatetimeFromEpochMilliseconds:
    """Tests for get_datetime_from_epoch_milliseconds function."""

    def test_get_datetime_from_epoch_milliseconds(self):
        """Test converting epoch milliseconds to datetime string."""
        # Jan 1, 2021 00:00:00 UTC = 1609459200000 milliseconds
        # Note: function uses local timezone, so result depends on system timezone
        result = get_datetime_from_epoch_milliseconds("1609459200000")
        # Should be in format YYYYMMDD-HHMMSS (format: %Y%m%d-%H%M%S)
        # 8 digits for date, dash, 6 digits for time = 15 characters total
        assert len(result) == 15
        assert result[8] == "-"  # Date-time separator (after YYYYMMDD)
        assert result[:8].isdigit()  # Date part (YYYYMMDD)
        assert result[9:].isdigit()  # Time part (HHMMSS)

    def test_get_datetime_from_epoch_milliseconds_specific_time(self):
        """Test converting specific epoch milliseconds."""
        # Dec 25, 2020 12:30:45 UTC
        epoch_ms = "1608899445000"
        result = get_datetime_from_epoch_milliseconds(epoch_ms)
        # Should be in format YYYYMMDD-HHMMSS
        assert len(result) == 15  # YYYYMMDD-HHMMSS
        assert result.startswith("2020")


class TestSafeFilename:
    """Tests for safe_filename function."""

    def test_safe_filename_short(self, temp_dir):
        """Test filename that is already safe."""
        filename = "test.jpg"
        result = safe_filename(str(temp_dir), filename)
        assert result == filename

    def test_safe_filename_long(self, temp_dir):
        """Test filename that needs to be shortened."""
        # Create a very long filename
        long_base = "a" * 300
        filename = f"{long_base}.jpg"
        result = safe_filename(str(temp_dir), filename)
        # Result should be shorter than original
        assert len(result) < len(filename)
        assert result.endswith(".jpg")

    def test_safe_filename_with_hash(self, temp_dir):
        """Test that long filenames get MD5 hash."""
        long_base = "a" * 300
        filename = f"{long_base}.jpg"
        result = safe_filename(str(temp_dir), filename)
        # Should contain hash and shortened base
        assert ".jpg" in result
        # Should have a hash somewhere (8 characters from MD5)
        assert len(result.split("_")) >= 2  # Should have separator

    def test_safe_filename_extension_preserved(self, temp_dir):
        """Test that file extension is always preserved."""
        long_base = "a" * 300
        for ext in [".jpg", ".png", ".pdf", ".mp4"]:
            filename = f"{long_base}{ext}"
            result = safe_filename(str(temp_dir), filename)
            assert result.endswith(ext)


class TestHandleDuplicateName:
    """Tests for handle_duplicate_name function."""

    def test_handle_duplicate_name_no_conflict(self, temp_dir):
        """Test handling filename when no duplicate exists."""
        filename = "test.jpg"
        result = handle_duplicate_name(str(temp_dir), filename)
        expected_path = temp_dir / filename
        assert Path(result) == expected_path

    def test_handle_duplicate_name_with_conflict(self, temp_dir):
        """Test handling filename when duplicate exists."""
        filename = "test.jpg"
        # Create existing file
        existing_file = temp_dir / filename
        existing_file.touch()
        
        result = handle_duplicate_name(str(temp_dir), filename)
        expected_path = temp_dir / "test-1.jpg"
        assert Path(result) == expected_path

    def test_handle_duplicate_name_multiple_conflicts(self, temp_dir):
        """Test handling filename with multiple duplicates."""
        filename = "test.jpg"
        # Create multiple existing files
        (temp_dir / "test.jpg").touch()
        (temp_dir / "test-1.jpg").touch()
        (temp_dir / "test-2.jpg").touch()
        
        result = handle_duplicate_name(str(temp_dir), filename)
        expected_path = temp_dir / "test-3.jpg"
        assert Path(result) == expected_path

    def test_handle_duplicate_name_preserves_extension(self, temp_dir):
        """Test that extension is preserved when handling duplicates."""
        filename = "document.pdf"
        (temp_dir / "document.pdf").touch()
        
        result = handle_duplicate_name(str(temp_dir), filename)
        assert result.endswith(".pdf")
        assert "document" in result
