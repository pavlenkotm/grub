"""
File operations utility module
"""

import os
import shutil
import json
from typing import Any, List, Optional
from pathlib import Path

from .logger import get_logger


class FileOperations:
    """Utility class for file operations"""

    def __init__(self):
        """Initialize file operations"""
        self.logger = get_logger()

    def read_file(self, filepath: str, encoding: str = 'utf-8') -> str:
        """Read file contents

        Args:
            filepath: Path to file
            encoding: File encoding

        Returns:
            File contents as string
        """
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
            self.logger.debug(f"Read file: {filepath}")
            return content
        except Exception as e:
            self.logger.error(f"Failed to read file {filepath}: {e}")
            raise

    def write_file(self, filepath: str, content: str, encoding: str = 'utf-8') -> None:
        """Write content to file

        Args:
            filepath: Path to file
            content: Content to write
            encoding: File encoding
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding=encoding) as f:
                f.write(content)
            self.logger.debug(f"Wrote file: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to write file {filepath}: {e}")
            raise

    def read_json(self, filepath: str) -> Any:
        """Read JSON file

        Args:
            filepath: Path to JSON file

        Returns:
            Parsed JSON data
        """
        content = self.read_file(filepath)
        return json.loads(content)

    def write_json(self, filepath: str, data: Any, indent: int = 2) -> None:
        """Write data to JSON file

        Args:
            filepath: Path to JSON file
            data: Data to write
            indent: JSON indentation
        """
        content = json.dumps(data, indent=indent)
        self.write_file(filepath, content)

    def copy_file(self, src: str, dst: str) -> None:
        """Copy file from source to destination

        Args:
            src: Source file path
            dst: Destination file path
        """
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            self.logger.info(f"Copied file: {src} -> {dst}")
        except Exception as e:
            self.logger.error(f"Failed to copy file: {e}")
            raise

    def move_file(self, src: str, dst: str) -> None:
        """Move file from source to destination

        Args:
            src: Source file path
            dst: Destination file path
        """
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            self.logger.info(f"Moved file: {src} -> {dst}")
        except Exception as e:
            self.logger.error(f"Failed to move file: {e}")
            raise

    def delete_file(self, filepath: str) -> None:
        """Delete file

        Args:
            filepath: Path to file
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                self.logger.info(f"Deleted file: {filepath}")
            else:
                self.logger.warning(f"File not found: {filepath}")
        except Exception as e:
            self.logger.error(f"Failed to delete file: {e}")
            raise

    def file_exists(self, filepath: str) -> bool:
        """Check if file exists

        Args:
            filepath: Path to file

        Returns:
            True if file exists
        """
        return os.path.isfile(filepath)

    def dir_exists(self, dirpath: str) -> bool:
        """Check if directory exists

        Args:
            dirpath: Path to directory

        Returns:
            True if directory exists
        """
        return os.path.isdir(dirpath)

    def create_directory(self, dirpath: str) -> None:
        """Create directory

        Args:
            dirpath: Path to directory
        """
        try:
            os.makedirs(dirpath, exist_ok=True)
            self.logger.info(f"Created directory: {dirpath}")
        except Exception as e:
            self.logger.error(f"Failed to create directory: {e}")
            raise

    def list_files(self, directory: str, pattern: Optional[str] = None) -> List[str]:
        """List files in directory

        Args:
            directory: Directory path
            pattern: Optional glob pattern

        Returns:
            List of file paths
        """
        path = Path(directory)
        if pattern:
            files = [str(f) for f in path.glob(pattern) if f.is_file()]
        else:
            files = [str(f) for f in path.iterdir() if f.is_file()]

        self.logger.debug(f"Listed {len(files)} files in {directory}")
        return files

    def get_file_size(self, filepath: str) -> int:
        """Get file size in bytes

        Args:
            filepath: Path to file

        Returns:
            File size in bytes
        """
        return os.path.getsize(filepath)

    def get_file_extension(self, filepath: str) -> str:
        """Get file extension

        Args:
            filepath: Path to file

        Returns:
            File extension (with dot)
        """
        return os.path.splitext(filepath)[1]
