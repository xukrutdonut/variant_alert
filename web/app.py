#!/usr/bin/env python
# coding=utf-8
"""
Web interface for Variant Alert!
Provides a user-friendly web UI for comparing ClinVar VCF files.
"""

import os
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_file, url_for
from werkzeug.utils import secure_filename

from parsers.vcf.clinvar import ClinvarVCFComparator
from logger.logger import get_logger

app = Flask(__name__)
logger = get_logger(__name__)

# Configuration
BASE_DIR = Path(__file__).parent
UPLOAD_FOLDER = BASE_DIR / 'uploads'
OUTPUT_FOLDER = BASE_DIR / 'outputs'
ALLOWED_EXTENSIONS = {'vcf', 'vcf.gz'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['OUTPUT_FOLDER'] = str(OUTPUT_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ensure directories exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/compare', methods=['POST'])
def compare_vcf():
    """
    API endpoint to compare VCF files
    Expects: source_vcf, target_vcf files, and comparison_type
    """
    try:
        # Validate request
        if 'source_vcf' not in request.files or 'target_vcf' not in request.files:
            return jsonify({'error': 'Missing VCF files'}), 400
        
        source_file = request.files['source_vcf']
        target_file = request.files['target_vcf']
        comparison_type = request.form.get('comparison_type', 'compare-variant')
        output_format = request.form.get('output_format', 'tsv')
        
        # Validate files
        if source_file.filename == '' or target_file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        if not (allowed_file(source_file.filename) and allowed_file(target_file.filename)):
            return jsonify({'error': 'Invalid file type. Only .vcf and .vcf.gz allowed'}), 400
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        session_folder = UPLOAD_FOLDER / session_id
        session_folder.mkdir(exist_ok=True)
        
        output_folder = OUTPUT_FOLDER / session_id
        output_folder.mkdir(exist_ok=True)
        
        # Save uploaded files
        source_filename = secure_filename(source_file.filename)
        target_filename = secure_filename(target_file.filename)
        
        source_path = session_folder / source_filename
        target_path = session_folder / target_filename
        
        source_file.save(str(source_path))
        target_file.save(str(target_path))
        
        logger.info(f"Processing comparison for session {session_id}")
        logger.info(f"Source: {source_filename}, Target: {target_filename}, Type: {comparison_type}")
        
        # Perform comparison
        try:
            comparator = ClinvarVCFComparator(str(source_path), str(target_path))
            genome_reference = comparator.compare_references()
            logger.info(f"Genome reference: {genome_reference}")
            
            result_files = []
            
            if comparison_type == 'compare-variant':
                compared_variants, has_lost_variants = comparator.compare_variants()
                comparator.write_variant_comparison(
                    compared_variants, 
                    str(output_folder),
                    output_format
                )
                
                # Find the generated file
                for f in output_folder.iterdir():
                    if f.is_file():
                        result_files.append({
                            'name': f.name,
                            'path': str(f),
                            'url': url_for('download_result', session_id=session_id, filename=f.name)
                        })
                
                if has_lost_variants:
                    logger.warning("New ClinVar version is missing variants from source file")
            
            elif comparison_type == 'compare-gene':
                compared_genes = comparator.compare_genes()
                comparator.write_gene_comparison(compared_genes, str(output_folder))
                
                for f in output_folder.iterdir():
                    if f.is_file():
                        result_files.append({
                            'name': f.name,
                            'path': str(f),
                            'url': url_for('download_result', session_id=session_id, filename=f.name)
                        })
            
            elif comparison_type == 'clinvarome':
                comparator.write_clinvarome(str(output_folder))
                
                for f in output_folder.iterdir():
                    if f.is_file():
                        result_files.append({
                            'name': f.name,
                            'path': str(f),
                            'url': url_for('download_result', session_id=session_id, filename=f.name)
                        })
            
            else:
                return jsonify({'error': 'Invalid comparison type'}), 400
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'genome_reference': genome_reference,
                'result_files': result_files,
                'message': f'Comparison completed successfully'
            })
        
        except Exception as e:
            logger.error(f"Comparison error: {str(e)}", exc_info=True)
            return jsonify({'error': f'Comparison failed: {str(e)}'}), 500
    
    except Exception as e:
        logger.error(f"Request error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<session_id>/<filename>')
def download_result(session_id, filename):
    """Download result file"""
    try:
        # Validate session_id to prevent directory traversal
        if not session_id.replace('-', '').isalnum():
            return jsonify({'error': 'Invalid session ID'}), 400
        
        file_path = OUTPUT_FOLDER / session_id / secure_filename(filename)
        
        if not file_path.exists():
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            str(file_path),
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


def main():
    """Main entry point for the web application"""
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
