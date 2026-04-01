"""Tests for smart_crop.translator module."""
import pytest
from smart_crop.translator import Translator


class TestTranslator:
    """Test cases for Translator class."""

    def test_init(self):
        """Test Translator initialization."""
        translator = Translator()
        assert translator is not None

    def test_translate_text(self):
        """Test text translation."""
        translator = Translator()
        text = 'Hello, how are you?'
        target_lang = 'hi'
        result = translator.translate_text(text, target_lang)
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    def test_detect_language(self):
        """Test language detection."""
        translator = Translator()
        text = 'Hello, how are you?'
        lang = translator.detect_language(text)
        assert lang is not None
        assert isinstance(lang, str)

    def test_get_supported_languages(self):
        """Test getting supported languages."""
        translator = Translator()
        languages = translator.get_supported_languages()
        assert languages is not None
        assert isinstance(languages, (list, dict))
