import re
import pandas as pd
from typing import Tuple, Dict, List, Optional
import streamlit as st

class DataValidator:
    """Validates biological data inputs and formats"""
    
    def __init__(self):
        # Amino acid codes
        self.amino_acids = set('ACDEFGHIKLMNPQRSTVWY')
        self.nucleotides = set('ATCGN')
        
        # Common contaminants or problematic sequences
        self.contaminants = [
            'KERATIN',
            'TRYPSIN',
            'CHYMOTRYPSIN',
            'PEPSIN',
            'ALBUMIN'
        ]
    
    def validate_fasta_format(self, content: str) -> Tuple[bool, str, Dict]:
        """
        Validate FASTA format and content
        Returns: (is_valid, message, statistics)
        """
        try:
            if not content or not content.strip():
                return False, "Empty file content", {}
            
            lines = content.strip().split('\n')
            if not lines[0].startswith('>'):
                return False, "File must start with FASTA header (>)", {}
            
            sequences = []
            headers = []
            current_sequence = ""
            current_header = ""
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('>'):
                    # Save previous sequence if exists
                    if current_sequence and current_header:
                        sequences.append(current_sequence)
                        headers.append(current_header)
                    
                    # Start new sequence
                    current_header = line[1:]  # Remove '>'
                    current_sequence = ""
                    
                    if not current_header:
                        return False, f"Empty header at line {i+1}", {}
                        
                else:
                    # Sequence line
                    if not current_header:
                        return False, f"Sequence data before header at line {i+1}", {}
                    
                    # Remove whitespace and convert to uppercase
                    sequence_line = re.sub(r'\s+', '', line.upper())
                    current_sequence += sequence_line
            
            # Don't forget the last sequence
            if current_sequence and current_header:
                sequences.append(current_sequence)
                headers.append(current_header)
            
            if not sequences:
                return False, "No valid sequences found", {}
            
            # Validate sequences
            validation_result = self._validate_sequences(sequences, headers)
            if not validation_result[0]:
                return validation_result
            
            # Generate statistics
            stats = self._generate_fasta_stats(sequences, headers)
            
            return True, f"Valid FASTA with {len(sequences)} sequences", stats
            
        except Exception as e:
            return False, f"Validation error: {str(e)}", {}
    
    def _validate_sequences(self, sequences: List[str], headers: List[str]) -> Tuple[bool, str]:
        """Validate individual sequences"""
        for i, (seq, header) in enumerate(zip(sequences, headers)):
            if not seq:
                return False, f"Empty sequence for header: {header[:50]}..."
            
            if len(seq) < 10:
                st.warning(f"Very short sequence ({len(seq)} characters) for: {header[:50]}...")
            
            # Check for valid characters
            invalid_chars = set(seq) - self.amino_acids - self.nucleotides - {'X', 'U', 'B', 'Z', 'J', 'O'}
            if invalid_chars:
                return False, f"Invalid characters in sequence {i+1}: {', '.join(sorted(invalid_chars))}"
            
            # Check for excessive ambiguous characters
            ambiguous_chars = set(seq) & {'X', 'N', 'B', 'Z', 'J', 'O'}
            if len(ambiguous_chars) > len(seq) * 0.3:
                st.warning(f"High percentage of ambiguous characters in sequence {i+1}")
        
        return True, "All sequences valid"
    
    def _generate_fasta_stats(self, sequences: List[str], headers: List[str]) -> Dict:
        """Generate statistics for FASTA data"""
        lengths = [len(seq) for seq in sequences]
        
        stats = {
            'sequence_count': len(sequences),
            'total_length': sum(lengths),
            'min_length': min(lengths),
            'max_length': max(lengths),
            'avg_length': sum(lengths) / len(lengths),
            'median_length': sorted(lengths)[len(lengths)//2],
            'short_sequences': len([l for l in lengths if l < 50]),
            'long_sequences': len([l for l in lengths if l > 1000])
        }
        
        # Detect sequence type (protein vs nucleotide)
        protein_chars = 0
        nucleotide_chars = 0
        
        for seq in sequences[:5]:  # Check first 5 sequences
            protein_chars += len(set(seq) & self.amino_acids)
            nucleotide_chars += len(set(seq) & self.nucleotides)
        
        if protein_chars > nucleotide_chars:
            stats['sequence_type'] = 'protein'
        else:
            stats['sequence_type'] = 'nucleotide'
        
        return stats
    
    def validate_csv_data(self, df: pd.DataFrame, expected_columns: List[str] = None) -> Tuple[bool, str, Dict]:
        """Validate CSV data format and content"""
        try:
            if df.empty:
                return False, "CSV file is empty", {}
            
            # Check for required columns
            if expected_columns:
                missing_cols = set(expected_columns) - set(df.columns)
                if missing_cols:
                    return False, f"Missing required columns: {', '.join(missing_cols)}", {}
            
            # Check for completely empty rows
            empty_rows = df.isnull().all(axis=1).sum()
            if empty_rows > 0:
                st.warning(f"Found {empty_rows} completely empty rows")
            
            # Generate statistics
            stats = {
                'row_count': len(df),
                'column_count': len(df.columns),
                'empty_rows': empty_rows,
                'columns': list(df.columns),
                'data_types': df.dtypes.to_dict()
            }
            
            return True, f"Valid CSV with {len(df)} rows and {len(df.columns)} columns", stats
            
        except Exception as e:
            return False, f"CSV validation error: {str(e)}", {}
    
    def detect_sequence_type(self, sequence: str) -> str:
        """Detect if sequence is protein or nucleotide"""
        sequence = sequence.upper()
        
        # Count character types
        protein_specific = len(set(sequence) & (self.amino_acids - self.nucleotides))
        nucleotide_specific = len(set(sequence) & self.nucleotides)
        
        if protein_specific > 0:
            return 'protein'
        elif nucleotide_specific > 0 and len(set(sequence) & self.nucleotides) >= 3:
            return 'nucleotide'
        else:
            return 'unknown'
    
    def check_sequence_quality(self, sequence: str) -> Dict:
        """Analyze sequence quality metrics"""
        sequence = sequence.upper()
        
        quality = {
            'length': len(sequence),
            'gc_content': 0,
            'ambiguous_percentage': 0,
            'repetitive_percentage': 0,
            'complexity_score': 0
        }
        
        if not sequence:
            return quality
        
        # GC content (for nucleotides)
        if self.detect_sequence_type(sequence) == 'nucleotide':
            gc_count = sequence.count('G') + sequence.count('C')
            quality['gc_content'] = gc_count / len(sequence) * 100
        
        # Ambiguous characters
        ambiguous = sequence.count('X') + sequence.count('N')
        quality['ambiguous_percentage'] = ambiguous / len(sequence) * 100
        
        # Simple repetitiveness check
        unique_chars = len(set(sequence))
        quality['complexity_score'] = unique_chars / len(sequence) * 100
        
        # Repetitive sequences (simple check for runs)
        max_run = 0
        current_run = 1
        for i in range(1, len(sequence)):
            if sequence[i] == sequence[i-1]:
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 1
        
        quality['repetitive_percentage'] = max_run / len(sequence) * 100
        
        return quality
    
    def validate_biomarker_criteria(self, df: pd.DataFrame) -> Tuple[bool, str, Dict]:
        """Validate that biomarker analysis criteria can be applied"""
        required_cols = ['Sequence']
        
        # Check for required columns
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return False, f"Missing required columns for biomarker analysis: {', '.join(missing_cols)}", {}
        
        # Check sequence data quality
        valid_sequences = 0
        total_sequences = len(df)
        
        for _, row in df.iterrows():
            sequence = str(row['Sequence'])
            if sequence and sequence != 'nan' and len(sequence) > 10:
                valid_sequences += 1
        
        validity_percentage = valid_sequences / total_sequences * 100 if total_sequences > 0 else 0
        
        if validity_percentage < 50:
            return False, f"Too many invalid sequences ({validity_percentage:.1f}% valid)", {}
        
        stats = {
            'total_sequences': total_sequences,
            'valid_sequences': valid_sequences,
            'validity_percentage': validity_percentage
        }
        
        return True, f"Data suitable for biomarker analysis ({validity_percentage:.1f}% valid sequences)", stats
    
    def check_for_contaminants(self, headers: List[str]) -> List[str]:
        """Check for common contaminant proteins in headers"""
        contaminants_found = []
        
        for header in headers:
            header_upper = header.upper()
            for contaminant in self.contaminants:
                if contaminant in header_upper:
                    contaminants_found.append(f"{contaminant} in: {header[:50]}...")
        
        return contaminants_found
    
    def validate_integration_compatibility(self, df1: pd.DataFrame, df2: pd.DataFrame) -> Tuple[bool, str, Dict]:
        """Check if two datasets can be integrated"""
        compatibility = {
            'sequence_overlap': 0,
            'id_overlap': 0,
            'common_columns': [],
            'integration_method': 'none'
        }
        
        # Check for sequence-based integration
        if 'Sequence' in df1.columns and 'Sequence' in df2.columns:
            common_sequences = set(df1['Sequence']) & set(df2['Sequence'])
            compatibility['sequence_overlap'] = len(common_sequences)
            if len(common_sequences) > 0:
                compatibility['integration_method'] = 'sequence'
        
        # Check for ID-based integration
        id_cols_1 = [col for col in df1.columns if 'id' in col.lower() or 'protein' in col.lower() or 'gene' in col.lower()]
        id_cols_2 = [col for col in df2.columns if 'id' in col.lower() or 'protein' in col.lower() or 'gene' in col.lower()]
        
        if id_cols_1 and id_cols_2:
            # Try to find ID overlap
            for col1 in id_cols_1:
                for col2 in id_cols_2:
                    # Extract numeric IDs
                    ids1 = df1[col1].astype(str).str.extract(r'(\d+)').dropna()
                    ids2 = df2[col2].astype(str).str.extract(r'(\d+)').dropna()
                    if not ids1.empty and not ids2.empty:
                        common_ids = set(ids1[0]) & set(ids2[0])
                        if len(common_ids) > compatibility['id_overlap']:
                            compatibility['id_overlap'] = len(common_ids)
                            if compatibility['integration_method'] == 'none':
                                compatibility['integration_method'] = 'id'
        
        # Common columns
        compatibility['common_columns'] = list(set(df1.columns) & set(df2.columns))
        
        # Determine if integration is possible
        can_integrate = (
            compatibility['sequence_overlap'] > 0 or 
            compatibility['id_overlap'] > 0 or
            len(compatibility['common_columns']) > 1
        )
        
        if can_integrate:
            message = f"Integration possible via {compatibility['integration_method']} matching"
        else:
            message = "No suitable integration method found"
        
        return can_integrate, message, compatibility

class QualityAssessment:
    """Assess data quality for biomarker analysis"""
    
    def __init__(self):
        self.validator = DataValidator()
    
    def assess_dataset_quality(self, df: pd.DataFrame, data_type: str = 'proteomics') -> Dict:
        """Comprehensive quality assessment of a dataset"""
        assessment = {
            'overall_score': 0,
            'issues': [],
            'recommendations': [],
            'quality_metrics': {}
        }
        
        # Basic metrics
        total_entries = len(df)
        assessment['quality_metrics']['total_entries'] = total_entries
        
        if total_entries == 0:
            assessment['issues'].append("Dataset is empty")
            return assessment
        
        # Sequence quality
        if 'Sequence' in df.columns:
            valid_sequences = 0
            sequence_lengths = []
            
            for _, row in df.iterrows():
                seq = str(row['Sequence'])
                if seq and seq != 'nan' and len(seq) > 10:
                    valid_sequences += 1
                    sequence_lengths.append(len(seq))
                    
                    # Check sequence quality
                    quality = self.validator.check_sequence_quality(seq)
                    if quality['ambiguous_percentage'] > 30:
                        assessment['issues'].append(f"High ambiguous content in sequence")
            
            assessment['quality_metrics']['valid_sequences'] = valid_sequences
            assessment['quality_metrics']['sequence_validity'] = valid_sequences / total_entries * 100
            
            if sequence_lengths:
                assessment['quality_metrics']['avg_sequence_length'] = sum(sequence_lengths) / len(sequence_lengths)
                assessment['quality_metrics']['min_sequence_length'] = min(sequence_lengths)
                assessment['quality_metrics']['max_sequence_length'] = max(sequence_lengths)
        
        # Completeness check
        null_percentages = df.isnull().sum() / len(df) * 100
        high_null_cols = null_percentages[null_percentages > 50].index.tolist()
        
        if high_null_cols:
            assessment['issues'].append(f"High missing data in columns: {', '.join(high_null_cols)}")
        
        # Data consistency
        if 'Protein' in df.columns or 'Gene' in df.columns:
            id_col = 'Protein' if 'Protein' in df.columns else 'Gene'
            duplicate_ids = df[id_col].duplicated().sum()
            if duplicate_ids > 0:
                assessment['issues'].append(f"{duplicate_ids} duplicate entries found")
        
        # Calculate overall score
        score = 100
        score -= len(assessment['issues']) * 10  # Deduct 10 points per issue
        
        if 'sequence_validity' in assessment['quality_metrics']:
            if assessment['quality_metrics']['sequence_validity'] < 80:
                score -= 20
        
        assessment['overall_score'] = max(0, score)
        
        # Generate recommendations
        if assessment['overall_score'] < 70:
            assessment['recommendations'].append("Consider data cleaning before analysis")
        
        if 'sequence_validity' in assessment['quality_metrics'] and assessment['quality_metrics']['sequence_validity'] < 90:
            assessment['recommendations'].append("Remove or fix invalid sequences")
        
        if high_null_cols:
            assessment['recommendations'].append("Address missing data in key columns")
        
        return assessment
