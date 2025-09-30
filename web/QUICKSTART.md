# Quick Start Guide - Variant Alert Web Interface

This guide will help you get started with the Variant Alert web interface in minutes.

## Prerequisites

- Python 3.6 or higher
- Poetry (recommended) or pip

## Installation

### Option 1: Using Poetry (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/xukrutdonut/variant_alert.git
cd variant_alert
```

2. Install dependencies:
```bash
poetry install
```

3. Start the web interface:
```bash
poetry run variant-alert-web
```

### Option 2: Using Docker

1. Clone the repository:
```bash
git clone https://github.com/xukrutdonut/variant_alert.git
cd variant_alert
```

2. Build and start the container:
```bash
docker-compose -f docker-compose.web.yml up
```

## Using the Web Interface

1. **Open your browser** and navigate to `http://localhost:8080` (or `http://localhost:5000` if using Docker)

2. **Upload VCF files**:
   - Click "Choose File" for Source VCF (reference/older version)
   - Click "Choose File" for Target VCF (newer version to compare)

3. **Select comparison type**:
   - **Compare Variants**: Identify variants with pathogenicity changes
     - Choose output format: TSV (fast) or VCF (slower, ~10 minutes)
   - **Compare Genes**: Track gene-disease association changes
   - **Clinvarome**: Generate list of all pathogenic genes

4. **Click "Start Comparison"** and wait for processing

5. **Download results** when ready

## Example Workflow

### Comparing Two ClinVar Versions

```
1. Download two ClinVar VCF files:
   - clinvar_20240101.vcf.gz (source/older)
   - clinvar_20240201.vcf.gz (target/newer)

2. Upload both files in the web interface

3. Select "Compare Variants" with TSV output

4. Click "Start Comparison"

5. Download the resulting TSV file with variant changes
```

## Tips

- **File Size**: Large VCF files (>100MB) may take several minutes to process
- **VCF Output**: VCF format output takes significantly longer than TSV (~10 minutes vs. seconds)
- **Recommended Input**: Use VCF files from [ClinVCF](https://github.com/SeqOne/clinvcf) for complete data

## Troubleshooting

### Port Already in Use
If port 8080 is already in use, you can change it:

```bash
export PORT=9000
poetry run variant-alert-web
```

### Memory Issues
Processing large VCF files requires adequate RAM. Ensure you have at least 2GB available.

### Docker Issues
If the Docker container fails to start:

```bash
# Check container logs
docker-compose -f docker-compose.web.yml logs

# Rebuild container
docker-compose -f docker-compose.web.yml build --no-cache
```

## API Usage

The web interface also provides a REST API:

### Health Check
```bash
curl http://localhost:8080/health
```

### Submit Comparison (using curl)
```bash
curl -X POST http://localhost:8080/api/compare \
  -F "source_vcf=@/path/to/source.vcf" \
  -F "target_vcf=@/path/to/target.vcf" \
  -F "comparison_type=compare-variant" \
  -F "output_format=tsv"
```

## Getting Help

- **Documentation**: See [README.md](README.md) for detailed documentation
- **Issues**: Report issues on [GitHub](https://github.com/xukrutdonut/variant_alert/issues)
- **CLI Version**: Use `poetry run variant-alert --help` for command-line usage

## Next Steps

- Read the full [Web Interface Documentation](README.md)
- Learn about [comparison types and output formats](../README.md#glossary)
- Explore the [Genome Alert! framework](https://github.com/SeqOne/GenomeAlert_app)
