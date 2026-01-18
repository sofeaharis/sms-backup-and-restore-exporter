"""Pytest configuration and shared fixtures for tests."""
import os
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_sms_xml_file(temp_dir):
    """Create a sample SMS XML file with MMS content."""
    xml_content = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<smses count="1">
    <mms address="+1234567890" date="1609459200000" readable_date="Jan 1, 2021 12:00:00 AM">
        <parts>
            <part seq="0" ct="text/plain" text="Test message" />
            <part seq="1" ct="image/jpeg" data="/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/2wBDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwA/8A=" name="test.jpg" />
        </parts>
    </mms>
</smses>"""
    xml_file = temp_dir / "sms-test.xml"
    xml_file.write_text(xml_content, encoding='utf-8')
    return xml_file


@pytest.fixture
def sample_calls_xml_file(temp_dir):
    """Create a sample calls XML file."""
    xml_content = """<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
<calls count="2">
    <call number="+1234567890" duration="120" date="1609459200000" type="1" readable_date="Jan 1, 2021 12:00:00 AM" contact_name="John Doe" />
    <call number="+9876543210" duration="45" date="1609545600000" type="2" readable_date="Jan 2, 2021 12:00:00 AM" contact_name="Jane Smith" />
</calls>"""
    xml_file = temp_dir / "calls-test.xml"
    xml_file.write_text(xml_content, encoding='utf-8')
    return xml_file


@pytest.fixture
def sample_vcf_file(temp_dir):
    """Create a sample VCF file."""
    vcf_content = """BEGIN:VCARD
VERSION:3.0
FN:John Doe
N:Doe;John;;;
EMAIL;TYPE=INTERNET:john.doe@example.com
TEL;TYPE=CELL:+1234567890
PHOTO;ENCODING=BASE64;TYPE=JPEG:/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQH/
END:VCARD
BEGIN:VCARD
VERSION:3.0
FN:Jane Smith
N:Smith;Jane;;;
TEL;TYPE=HOME:+9876543210
END:VCARD"""
    vcf_file = temp_dir / "contacts.vcf"
    vcf_file.write_text(vcf_content, encoding='utf-8')
    return vcf_file
