#!/usr/bin/env python3
"""
Mantra Programming Language CLI
"""

import sys
import os
import argparse
from . import MantraRunner

def main():
    parser = argparse.ArgumentParser(
        description='Mantra Programming Language - Sanskrit-inspired coding',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  mantra hello.man           # Run a Mantra file
  mantra --repl             # Start interactive REPL  
  mantra --version          # Show version
  
Visit https://github.com/mantra-lang/mantra for documentation.
        '''
    )
    
    parser.add_argument('file', nargs='?', help='Mantra source file (.man)')
    parser.add_argument('--version', action='version', version='Mantra 0.1.0')
    parser.add_argument('--repl', '-r', action='store_true', help='Start interactive REPL')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    runner = MantraRunner()
    
    if args.repl or not args.file:
        runner.repl()
    else:
        if not args.file.endswith('.man'):
            print("Error: Mantra files must have .man extension")
            print("Example: mantra hello.man")
            sys.exit(1)
        
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found")
            sys.exit(1)
        
        result = runner.run_file(args.file)
        if result is None and args.debug:
            sys.exit(1)

if __name__ == "__main__":
    main()