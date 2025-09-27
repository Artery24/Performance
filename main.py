#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import logging
import argparse
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

def normalize_path(path_str: str) -> Path:
    raw = path_str.strip().strip('"').strip("'")
    expanded = os.path.expandvars(raw)
    expanded = expanded.replace("/", os.sep).replace("\\", os.sep)
    return Path(expanded).resolve()

def main():
    __version__ = "1.0.1"
    parser = argparse.ArgumentParser(
        description="Delete all files in Adobe CameraRaw Cache2 directory.")
    parser.add_argument(
        '-p', '--path', type=str,
        help="Path to Cache2 folder (default uses %LOCALAPPDATA%\\Adobe\\CameraRaw\\Cache2)")
    parser.add_argument(
        '-y', '--yes', action='store_true',
        help="Skip confirmation prompt and proceed with deletion.")
    parser.add_argument(
        '--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    console = Console()

    # Determine directory of this script (for log file).
    if getattr(sys, 'frozen', False):
        script_dir = Path(sys.executable).parent
    else:
        script_dir = Path(__file__).resolve().parent

    # Setup logging to file (overwrite mode).
    log_path = script_dir / "delete_cache.log"
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[logging.FileHandler(log_path, mode='w', encoding='utf-8')]
    )
    logger = logging.getLogger()

    # Warning panel
    warning_text = (
        "[yellow]This operation will permanently DELETE ALL files in the Adobe CameraRaw Cache2 folder.[/yellow]\n"
        "The files will NOT be moved to the Recycle Bin."
    )
    console.print(Panel(warning_text, title="Cache2 Deletion Warning", style="bold red"))

    # Determine target Cache2 directory
    if args.path:
        target_path = normalize_path(args.path)
    else:
        local_appdata = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
        default_path = Path(local_appdata) / "Adobe" / "CameraRaw" / "Cache2"
        target_path = default_path.resolve()

    console.print(f"[bold]Target Cache2 directory:[/bold] {target_path}")

    if not target_path.exists() or not target_path.is_dir():
        console.print(f"[red]Error:[/red] The directory {target_path} does not exist or is not accessible.")
        sys.exit(1)
    if "CameraRaw" not in str(target_path) or "Cache2" not in str(target_path):
        console.print("[red]Error:[/red] The specified path is not the expected Adobe CameraRaw Cache2 folder.")
        sys.exit(1)

    if not args.yes:
        prompt = f"Are you sure you want to DELETE ALL files in:\n  {target_path}\nProceed?"
        if not Confirm.ask(prompt):
            console.print("[green]Operation cancelled by user.[/green]")
            logger.info("Operation cancelled by user.")
            sys.exit(0)

    all_files = [p for p in target_path.rglob('*') if p.is_file()]
    all_dirs = [p for p in target_path.rglob('*') if p.is_dir()]
    all_dirs.sort(key=lambda p: len(str(p)), reverse=True)

    total_files = len(all_files)
    if total_files == 0:
        console.print("[yellow]No files to delete in the target directory.[/yellow]")
        logger.info("No files to delete in the target directory.")
    else:
        console.print(f"[cyan]Deleting {total_files} files...[/cyan]")
        with Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task("Deleting files...", total=total_files)
            for file_path in all_files:
                try:
                    if not file_path.resolve().is_relative_to(target_path):
                        logger.warning(f"Skipping file outside target: {file_path}")
                        continue
                    file_path.unlink()
                    logger.info(f"Deleted file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete file {file_path}: {e}")
                progress.update(task, advance=1, description=f"Deleting {file_path.name}")

        for dir_path in all_dirs:
            try:
                if not dir_path.resolve().is_relative_to(target_path):
                    logger.warning(f"Skipping directory outside target: {dir_path}")
                    continue
                dir_path.rmdir()
                logger.info(f"Deleted directory: {dir_path}")
            except Exception as e:
                logger.error(f"Failed to delete directory {dir_path}: {e}")

        console.print("[green]Deletion process completed.[/green]\n")
        logger.info("Deletion process completed.")

    # Summary
    table = Table(title="Summary")
    table.add_column("Item", style="cyan", no_wrap=True)
    table.add_column("Detail", style="magenta")
    table.add_row("Target Directory", str(target_path))
    table.add_row("Files Deleted", str(total_files))
    table.add_row("Log File", str(log_path))
    console.print(table)

if __name__ == "__main__":

    main()
