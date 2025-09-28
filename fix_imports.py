#!/usr/bin/env python3
"""
Script para corregir las importaciones problemáticas en el proyecto variant_alert
"""

import os
import re

def fix_import_in_file(filepath, old_import, new_import):
    """Corrige una importación específica en un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Corregido import en: {filepath}")
            return True
        else:
            print(f"- No se encontró import problemático en: {filepath}")
            return False
    except Exception as e:
        print(f"✗ Error corrigiendo {filepath}: {e}")
        return False

def main():
    print("=== Corrigiendo importaciones problemáticas ===")
    
    # Buscar y corregir importaciones problemáticas
    files_to_fix = [
        "parsers/vcf/clinvar.py"
    ]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"\nRevisando: {file_path}")
            
            # Corregir import de logger
            fixed = fix_import_in_file(
                file_path,
                "from logger import logger",
                "from logger.logger import get_logger"
            )
            
            if fixed:
                # También necesitamos cambiar la línea que usa logger.get_logger
                fix_import_in_file(
                    file_path,
                    "self.logger = logger.get_logger(__name__)",
                    "self.logger = get_logger(__name__)"
                )
        else:
            print(f"✗ Archivo no encontrado: {file_path}")
    
    print("\n=== Corrección de importaciones completada ===")

if __name__ == "__main__":
    main()
