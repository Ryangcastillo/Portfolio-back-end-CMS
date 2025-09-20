#!/usr/bin/env python3
"""
System cleanup orchestrator for the error management system.
Handles various cleanup operations including logs, temp files, and file reorganization.
"""

import os
import sys
import json
import logging
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import shutil
import gzip
import glob

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Configure logging first
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("cleanup_system")

# Database components (optional - graceful degradation if not available)
try:
    from backend.models.error import SystemCleanupLog
    from backend.database import get_db_session
    ENABLE_DB_LOGGING = True
except ImportError as e:
    logger.warning(f"Database components not available: {e}. Running in standalone mode.")
    ENABLE_DB_LOGGING = False


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("cleanup_system")


class SystemCleanup:
    """Main system cleanup coordinator."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.project_root = project_root
        self.config = self._load_config(config_path)
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load cleanup configuration."""
        
        default_config = {
            "cleanup_rules": {
                "logs": {
                    "retention_days": 30,
                    "archive_threshold_mb": 100,
                    "compress_older_than_days": 7
                },
                "temp_files": {
                    "retention_hours": 24,
                    "excluded_patterns": ["*.lock", "*.pid", "node_modules"]
                },
                "error_artifacts": {
                    "retention_days": 7,
                    "max_file_size_mb": 100
                },
                "reports": {
                    "archive_older_than_days": 30,
                    "keep_latest": 5
                }
            },
            "reorganization": {
                "refactoring_reports": "reports/archive/refactoring/",
                "system_logs": "logs/",
                "documentation": "docs/",
                "scripts": "scripts/",
                "cleanup_logs": "logs/cleanup/"
            }
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = json.load(f)
                # Merge configs (user config overrides defaults)
                return {**default_config, **user_config}
        
        return default_config
    
    async def run_all_cleanup(self) -> Dict[str, Any]:
        """Run all cleanup operations."""
        
        logger.info("Starting comprehensive system cleanup")
        
        results = {
            "started_at": datetime.utcnow().isoformat(),
            "operations": {}
        }
        
        # Run cleanup operations
        cleanup_operations = [
            ("logs", self._cleanup_logs),
            ("temp_files", self._cleanup_temp_files),
            ("error_artifacts", self._cleanup_error_artifacts),
            ("refactoring_reports", self._cleanup_refactoring_reports),
            ("reorganize_files", self._reorganize_files)
        ]
        
        for operation_name, operation_func in cleanup_operations:
            try:
                logger.info(f"Running {operation_name} cleanup")
                result = await operation_func()
                results["operations"][operation_name] = result
                
                # Log cleanup operation to database
                if ENABLE_DB_LOGGING:
                    await self._log_cleanup_operation(operation_name, result)
                
            except Exception as e:
                error_result = {
                    "success": False,
                    "error": str(e),
                    "files_processed": 0,
                    "files_affected": 0,
                    "bytes_processed": 0
                }
                results["operations"][operation_name] = error_result
                logger.error(f"Failed to run {operation_name} cleanup: {e}")
        
        results["completed_at"] = datetime.utcnow().isoformat()
        logger.info("System cleanup completed")
        
        return results
    
    async def run_specific_cleanup(self, cleanup_type: str) -> Dict[str, Any]:
        """Run a specific cleanup operation."""
        
        operations = {
            "logs": self._cleanup_logs,
            "temp_files": self._cleanup_temp_files,
            "error_artifacts": self._cleanup_error_artifacts,
            "refactoring_reports": self._cleanup_refactoring_reports,
            "reorganize_files": self._reorganize_files
        }
        
        if cleanup_type not in operations:
            raise ValueError(f"Unknown cleanup type: {cleanup_type}")
        
        logger.info(f"Running {cleanup_type} cleanup")
        result = await operations[cleanup_type]()
        if ENABLE_DB_LOGGING:
            await self._log_cleanup_operation(cleanup_type, result)
        
        return result
    
    async def _cleanup_logs(self) -> Dict[str, Any]:
        """Clean up old log files."""
        
        config = self.config["cleanup_rules"]["logs"]
        retention_days = config["retention_days"]
        compress_days = config["compress_older_than_days"]
        
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        compress_date = datetime.now() - timedelta(days=compress_days)
        
        files_processed = 0
        files_affected = 0
        bytes_processed = 0
        
        # Find log files
        log_patterns = [
            self.project_root / "logs" / "*.log",
            self.project_root / "backend" / "*.log",
            self.project_root / "*.log"
        ]
        
        for pattern in log_patterns:
            for log_file in glob.glob(str(pattern)):
                log_path = Path(log_file)
                if not log_path.exists():
                    continue
                
                files_processed += 1
                file_mtime = datetime.fromtimestamp(log_path.stat().st_mtime)
                file_size = log_path.stat().st_size
                
                # Delete old files
                if file_mtime < cutoff_date:
                    log_path.unlink()
                    files_affected += 1
                    bytes_processed += file_size
                    logger.info(f"Deleted old log file: {log_path}")
                
                # Compress files older than compress_days
                elif file_mtime < compress_date and not log_file.endswith('.gz'):
                    compressed_path = Path(str(log_path) + '.gz')
                    with open(log_path, 'rb') as f_in:
                        with gzip.open(compressed_path, 'wb') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                    
                    log_path.unlink()
                    files_affected += 1
                    bytes_processed += file_size
                    logger.info(f"Compressed log file: {log_path} -> {compressed_path}")
        
        return {
            "success": True,
            "operation": "archive_and_delete",
            "files_processed": files_processed,
            "files_affected": files_affected,
            "bytes_processed": bytes_processed,
            "retention_days": retention_days
        }
    
    async def _cleanup_temp_files(self) -> Dict[str, Any]:
        """Clean up temporary files."""
        
        config = self.config["cleanup_rules"]["temp_files"]
        retention_hours = config["retention_hours"]
        excluded_patterns = config["excluded_patterns"]
        
        cutoff_time = datetime.now() - timedelta(hours=retention_hours)
        
        files_processed = 0
        files_affected = 0
        bytes_processed = 0
        
        # Cleanup directories
        temp_dirs = [
            "/tmp",
            self.project_root / "tmp",
            self.project_root / ".next" / "cache",
            self.project_root / "node_modules" / ".cache"
        ]
        
        for temp_dir in temp_dirs:
            temp_path = Path(temp_dir)
            if not temp_path.exists():
                continue
            
            for file_path in temp_path.rglob("*"):
                if not file_path.is_file():
                    continue
                
                # Skip excluded patterns
                if any(file_path.match(pattern) for pattern in excluded_patterns):
                    continue
                
                files_processed += 1
                file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                if file_mtime < cutoff_time:
                    try:
                        file_size = file_path.stat().st_size
                        file_path.unlink()
                        files_affected += 1
                        bytes_processed += file_size
                        logger.debug(f"Deleted temp file: {file_path}")
                    except (OSError, PermissionError) as e:
                        logger.warning(f"Could not delete {file_path}: {e}")
        
        return {
            "success": True,
            "operation": "delete",
            "files_processed": files_processed,
            "files_affected": files_affected,
            "bytes_processed": bytes_processed,
            "retention_hours": retention_hours
        }
    
    async def _cleanup_error_artifacts(self) -> Dict[str, Any]:
        """Clean up error-related artifacts."""
        
        config = self.config["cleanup_rules"]["error_artifacts"]
        retention_days = config["retention_days"]
        max_size_mb = config["max_file_size_mb"]
        
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        max_size_bytes = max_size_mb * 1024 * 1024
        
        files_processed = 0
        files_affected = 0
        bytes_processed = 0
        
        # Find error artifact patterns
        error_patterns = [
            self.project_root / "*.dump",
            self.project_root / "core.*",
            self.project_root / "*.stacktrace",
            self.project_root / "error_*.txt",
            self.project_root / "crash_*.log"
        ]
        
        for pattern in error_patterns:
            for error_file in glob.glob(str(pattern)):
                error_path = Path(error_file)
                if not error_path.exists():
                    continue
                
                files_processed += 1
                file_mtime = datetime.fromtimestamp(error_path.stat().st_mtime)
                file_size = error_path.stat().st_size
                
                # Delete old or large files
                if file_mtime < cutoff_date or file_size > max_size_bytes:
                    try:
                        error_path.unlink()
                        files_affected += 1
                        bytes_processed += file_size
                        logger.info(f"Deleted error artifact: {error_path}")
                    except (OSError, PermissionError) as e:
                        logger.warning(f"Could not delete {error_path}: {e}")
        
        return {
            "success": True,
            "operation": "delete",
            "files_processed": files_processed,
            "files_affected": files_affected,
            "bytes_processed": bytes_processed,
            "retention_days": retention_days
        }
    
    async def _cleanup_refactoring_reports(self) -> Dict[str, Any]:
        """Clean up and archive refactoring report files."""
        
        files_processed = 0
        files_affected = 0
        bytes_processed = 0
        
        # Create archive directory
        archive_dir = self.project_root / "reports" / "archive" / "refactoring"
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Find refactoring report files
        refactoring_files = [
            "REFACTORING_SUMMARY.md",
            "COMPREHENSIVE_SYSTEM_REFACTORING_REPORT.md",
            "PYTHON39_REFACTORING_REPORT.md", 
            "REFACTORING_COMPLETE_REPORT.md",
            "SYSTEM_STATUS_REPORT.md"
        ]
        
        for filename in refactoring_files:
            file_path = self.project_root / filename
            if file_path.exists():
                files_processed += 1
                file_size = file_path.stat().st_size
                
                # Create timestamped archive name
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_name = f"{timestamp}_{filename}"
                archive_path = archive_dir / archive_name
                
                # Move file to archive
                shutil.move(str(file_path), str(archive_path))
                files_affected += 1
                bytes_processed += file_size
                logger.info(f"Archived refactoring report: {filename} -> {archive_name}")
        
        return {
            "success": True,
            "operation": "archive",
            "files_processed": files_processed,
            "files_affected": files_affected,
            "bytes_processed": bytes_processed,
            "archive_location": str(archive_dir)
        }
    
    async def _reorganize_files(self) -> Dict[str, Any]:
        """Reorganize files into logical directory structure."""
        
        files_processed = 0
        files_affected = 0
        bytes_processed = 0
        
        reorganization_rules = self.config["reorganization"]
        
        # Ensure target directories exist
        for target_dir in reorganization_rules.values():
            target_path = self.project_root / target_dir
            target_path.mkdir(parents=True, exist_ok=True)
        
        # Reorganization operations
        operations = [
            # Move any remaining scattered documentation
            {
                "source_patterns": ["*.md"],
                "source_dir": self.project_root,
                "target_dir": "docs/misc/",
                "exclude": ["README.md", "TASKS.md"]  # Keep these at root
            },
            # Organize any loose scripts
            {
                "source_patterns": ["*.py", "*.sh"],
                "source_dir": self.project_root,
                "target_dir": "scripts/misc/",
                "exclude": []
            }
        ]
        
        for operation in operations:
            source_dir = Path(operation["source_dir"])
            target_dir = self.project_root / operation["target_dir"]
            target_dir.mkdir(parents=True, exist_ok=True)
            
            for pattern in operation["source_patterns"]:
                for file_path in source_dir.glob(pattern):
                    if not file_path.is_file():
                        continue
                    
                    # Skip excluded files
                    if file_path.name in operation["exclude"]:
                        continue
                    
                    # Skip if already in organized directories
                    if any(part.startswith('.') for part in file_path.parts):
                        continue
                    if any(part in ['backend', 'frontend', 'app', 'docs', 'scripts'] for part in file_path.parts[:-1]):
                        continue
                    
                    files_processed += 1
                    
                    try:
                        file_size = file_path.stat().st_size
                        target_path = target_dir / file_path.name
                        
                        # Avoid overwriting existing files
                        if target_path.exists():
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            target_path = target_dir / f"{timestamp}_{file_path.name}"
                        
                        shutil.move(str(file_path), str(target_path))
                        files_affected += 1
                        bytes_processed += file_size
                        logger.info(f"Moved file: {file_path} -> {target_path}")
                        
                    except (OSError, PermissionError) as e:
                        logger.warning(f"Could not move {file_path}: {e}")
        
        return {
            "success": True,
            "operation": "reorganize",
            "files_processed": files_processed,
            "files_affected": files_affected,
            "bytes_processed": bytes_processed
        }
    
    async def _log_cleanup_operation(self, operation_type: str, result: Dict[str, Any]):
        """Log cleanup operation to database."""
        
        if not ENABLE_DB_LOGGING:
            logger.info(f"Database logging disabled. Operation {operation_type} result: {result}")
            return
        
        try:
            with get_db_session() as db:
                cleanup_log = SystemCleanupLog(
                    cleanup_type=operation_type,
                    operation=result.get("operation", "unknown"),
                    files_processed=result.get("files_processed", 0),
                    files_affected=result.get("files_affected", 0),
                    bytes_processed=result.get("bytes_processed", 0),
                    success=result.get("success", False),
                    error_message=result.get("error"),
                    completed_at=datetime.utcnow(),
                    details=result
                )
                
                if cleanup_log.completed_at and cleanup_log.started_at:
                    duration = (cleanup_log.completed_at - cleanup_log.started_at).total_seconds()
                    cleanup_log.duration_seconds = int(duration)
                
                db.add(cleanup_log)
                db.commit()
                
        except Exception as e:
            logger.error(f"Failed to log cleanup operation {operation_type}: {e}")


# Standalone functions for API usage
async def run_all_cleanup() -> Dict[str, Any]:
    """Run all cleanup operations."""
    cleanup = SystemCleanup()
    return await cleanup.run_all_cleanup()


async def run_specific_cleanup(cleanup_type: str) -> Dict[str, Any]:
    """Run a specific cleanup operation."""
    cleanup = SystemCleanup()
    return await cleanup.run_specific_cleanup(cleanup_type)


if __name__ == "__main__":
    """Command-line interface for cleanup system."""
    import argparse
    
    parser = argparse.ArgumentParser(description="System cleanup utility")
    parser.add_argument(
        "--type", 
        choices=["logs", "temp_files", "error_artifacts", "refactoring_reports", "reorganize_files"],
        help="Specific cleanup type to run"
    )
    parser.add_argument("--config", help="Path to cleanup configuration file")
    
    args = parser.parse_args()
    
    cleanup = SystemCleanup(config_path=args.config)
    
    async def main():
        if args.type:
            result = await cleanup.run_specific_cleanup(args.type)
        else:
            result = await cleanup.run_all_cleanup()
        
        print(json.dumps(result, indent=2))
    
    asyncio.run(main())