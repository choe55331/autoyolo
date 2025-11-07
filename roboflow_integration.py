#!/usr/bin/env python3
"""
Roboflow Integration Module
Download and prepare rune datasets from Roboflow
"""

import argparse
import os
from pathlib import Path
from roboflow import Roboflow


class RoboflowDatasetManager:
    """Manage Roboflow datasets for rune detection"""

    def __init__(self, api_key):
        """
        Initialize Roboflow client

        Args:
            api_key: Roboflow API key
        """
        self.api_key = api_key
        self.rf = Roboflow(api_key=api_key)
        print("Roboflow client initialized")

    def download_dataset(self, workspace, project, version, format='yolov8', location='./data'):
        """
        Download dataset from Roboflow

        Args:
            workspace: Roboflow workspace name
            project: Project name
            version: Dataset version number
            format: Export format (default: yolov8, compatible with YOLO12)
            location: Download location (default: ./data)

        Returns:
            Path to downloaded dataset
        """
        print(f"\nDownloading dataset from Roboflow...")
        print(f"  Workspace: {workspace}")
        print(f"  Project: {project}")
        print(f"  Version: {version}")
        print(f"  Format: {format}")

        try:
            # Get project
            project_obj = self.rf.workspace(workspace).project(project)

            # Get specific version
            dataset = project_obj.version(version)

            # Download dataset
            dataset_path = dataset.download(format, location=location)

            print(f"\nDataset downloaded successfully!")
            print(f"Location: {dataset_path}")

            return dataset_path

        except Exception as e:
            print(f"\nError downloading dataset: {e}")
            print("\nTroubleshooting:")
            print("1. Verify your API key is correct")
            print("2. Check workspace, project, and version names")
            print("3. Ensure you have access to the project")
            return None

    def list_projects(self, workspace):
        """
        List all projects in a workspace

        Args:
            workspace: Workspace name
        """
        try:
            workspace_obj = self.rf.workspace(workspace)
            projects = workspace_obj.projects()

            print(f"\nProjects in workspace '{workspace}':")
            for project in projects:
                print(f"  - {project.name}")

        except Exception as e:
            print(f"Error listing projects: {e}")

    def get_dataset_info(self, workspace, project, version):
        """
        Get information about a specific dataset

        Args:
            workspace: Workspace name
            project: Project name
            version: Version number
        """
        try:
            project_obj = self.rf.workspace(workspace).project(project)
            dataset = project_obj.version(version)

            print(f"\nDataset Information:")
            print(f"  Workspace: {workspace}")
            print(f"  Project: {project}")
            print(f"  Version: {version}")

            # Try to get additional info if available
            if hasattr(dataset, 'id'):
                print(f"  Dataset ID: {dataset.id}")

        except Exception as e:
            print(f"Error getting dataset info: {e}")


def main():
    parser = argparse.ArgumentParser(description='Roboflow Dataset Manager')
    parser.add_argument('--api-key', type=str, required=True, help='Roboflow API key')

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Download command
    download_parser = subparsers.add_parser('download', help='Download dataset')
    download_parser.add_argument('--workspace', type=str, required=True, help='Workspace name')
    download_parser.add_argument('--project', type=str, required=True, help='Project name')
    download_parser.add_argument('--version', type=int, required=True, help='Dataset version')
    download_parser.add_argument('--format', type=str, default='yolov8', help='Export format (default: yolov8)')
    download_parser.add_argument('--location', type=str, default='./data', help='Download location')

    # List projects command
    list_parser = subparsers.add_parser('list', help='List projects in workspace')
    list_parser.add_argument('--workspace', type=str, required=True, help='Workspace name')

    # Info command
    info_parser = subparsers.add_parser('info', help='Get dataset information')
    info_parser.add_argument('--workspace', type=str, required=True, help='Workspace name')
    info_parser.add_argument('--project', type=str, required=True, help='Project name')
    info_parser.add_argument('--version', type=int, required=True, help='Dataset version')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize manager
    manager = RoboflowDatasetManager(args.api_key)

    # Execute command
    if args.command == 'download':
        manager.download_dataset(
            workspace=args.workspace,
            project=args.project,
            version=args.version,
            format=args.format,
            location=args.location
        )
    elif args.command == 'list':
        manager.list_projects(args.workspace)
    elif args.command == 'info':
        manager.get_dataset_info(
            workspace=args.workspace,
            project=args.project,
            version=args.version
        )


if __name__ == '__main__':
    main()
