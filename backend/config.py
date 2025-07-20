import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Base configuration class with default settings"""
    
    # Application settings
    APP_NAME: str = "Medical Data Extractor"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    TESTING: bool = False
    
    # API settings
    API_PREFIX: str = "/api"
    API_TITLE: str = APP_NAME
    API_DESCRIPTION: str = "API for extracting structured medical data from documents"
    API_VERSION: str = APP_VERSION
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    RELOAD: bool = DEBUG
    
    # File processing settings
    MAX_FILE_SIZE_MB: int = 10  # Maximum file size in MB
    ALLOWED_FILE_TYPES: Dict[str, str] = {
        "application/pdf": "pdf",
        "image/jpeg": "jpg",
        "image/png": "png",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx"
    }
    UPLOAD_FOLDER: str = str(Path(__file__).parent.parent / "uploads")
    
    # OCR settings
    TESSERACT_CMD: str = "/usr/bin/tesseract"  # Default Linux path
    TESSERACT_CONFIG: str = "--oem 3 --psm 6"  # OCR Engine mode 3 (Default), Page segmentation mode 6
    
    # NLP settings
    SPACY_MODEL: str = "en_core_web_sm"
    
    # Security settings
    CORS_ORIGINS: list = ["*"]  # For development only - restrict in production
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-to-a-random-secret-key")
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @classmethod
    def get_allowed_extensions(cls) -> list:
        """Get list of allowed file extensions"""
        return list(cls.ALLOWED_FILE_TYPES.values())
    
    @classmethod
    def get_max_file_size_bytes(cls) -> int:
        """Get max file size in bytes"""
        return cls.MAX_FILE_SIZE_MB * 1024 * 1024


class DevelopmentConfig(Config):
    """Development specific configuration"""
    DEBUG: bool = True
    RELOAD: bool = True
    LOG_LEVEL: str = "DEBUG"


class TestingConfig(Config):
    """Testing specific configuration"""
    TESTING: bool = True
    LOG_LEVEL: str = "DEBUG"
    MAX_FILE_SIZE_MB: int = 1  # Smaller limit for tests


class ProductionConfig(Config):
    """Production specific configuration"""
    DEBUG: bool = False
    RELOAD: bool = False
    WORKERS: int = 4
    LOG_LEVEL: str = "WARNING"
    CORS_ORIGINS: list = [
        "https://your-production-domain.com",
        "https://www.your-production-domain.com"
    ]


def get_config() -> Config:
    """Get appropriate configuration based on environment"""
    env = os.getenv("APP_ENV", "development").lower()
    
    config_map: Dict[str, Any] = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig
    }
    
    return config_map.get(env, DevelopmentConfig)()


# Initialize the configuration
current_config = get_config()