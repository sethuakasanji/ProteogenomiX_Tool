import streamlit as st
import pandas as pd
from typing import Optional, Dict, Tuple
import tempfile
import os
from pathlib import Path
import zipfile
import io

class FileHandler:
    """Handles file upload, validation, and processing"""
    
    def __init__(self):
        self.allowed_extensions = {
            "fasta": [".fasta", ".fa", ".fas"],
            "csv": [".csv"],
            "text": [".txt"],
            "mzml": [".mzml"]
        }
        self.max_file_size = 100 * 1024 * 1024  # 100MB limit
    
    def validate_file(self, file, expected_type: str) -> Tuple[bool, str]:
        """Validate uploaded file"""
        if file is None:
            return False, "No file uploaded"
        
        # Check file size
        if hasattr(file, 'size') and file.size > self.max_file_size:
            return False, f"File too large. Maximum size: {self.max_file_size/(1024*1024):.0f}MB"
        
        # Check file extension
        file_extension = Path(file.name).suffix.lower()
        if expected_type in self.allowed_extensions:
            if file_extension not in self.allowed_extensions[expected_type]:
                return False, f"Invalid file type. Expected: {', '.join(self.allowed_extensions[expected_type])}"
        
        return True, "File is valid"
    
    def read_fasta_file(self, file) -> Optional[str]:
        """Read and validate FASTA file content"""
        try:
            # Read file content
            if hasattr(file, 'read'):
                content = file.read()
                if isinstance(content, bytes):
                    content = content.decode('utf-8')
            else:
                content = str(file)
            
            # Basic FASTA validation
            if not content.strip():
                st.error("File is empty")
                return None
            
            if not content.startswith('>'):
                st.error("Invalid FASTA format. File should start with '>'")
                return None
            
            # Count sequences
            sequence_count = content.count('>')
            if sequence_count == 0:
                st.error("No sequences found in FASTA file")
                return None
            
            st.success(f"✅ Valid FASTA file with {sequence_count} sequences")
            return content
            
        except Exception as e:
            st.error(f"Error reading FASTA file: {str(e)}")
            return None
    
    def read_csv_file(self, file) -> Optional[pd.DataFrame]:
        """Read and validate CSV file"""
        try:
            df = pd.read_csv(file)
            
            if df.empty:
                st.error("CSV file is empty")
                return None
            
            st.success(f"✅ Valid CSV file with {len(df)} rows and {len(df.columns)} columns")
            return df
            
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
            return None
    
    def create_sample_fasta(self, file_type: str) -> str:
        """Create sample FASTA content for demonstration"""
        if file_type == "proteomics":
            return """
>sp|P04637|P53_HUMAN Cellular tumor antigen p53 OS=Homo sapiens GN=TP53 PE=1 SV=4
MEEPQSDPSVEPPLSQETFSDLWKLLPENNVLSPLPSQAMDDLMLSPDDIEQWFTEDPGP
DEAPRMPEAAPPVAPAPAAPTPAAPAPAPSWPLSSSVPSQKTYQGSYGFRLGFLHSGTAK
SVTCTYSPALNKMFCQLAKTCPVQLWVDSTPPPGTRVRAMAIYKQSQHMTEVVRRCPHHH
ERCSDSDGLAPPQHLIRVEGNLRVEYLDDRNTFRHSVVVPYEPPEVGSDCTTIHYNYMCN
SSRLRRQRRFIQHKSNPPPPKKKGQRRLFRHSVVVPYEPKEVGSDCTTIHYNYMCNSSCM
SSRLRRQRRFIQHKSNPPPPKKKGQRRLFRNPPPSYSRAAGFKSRLYFLQSRTAKKNNGG
PLLSYSSGSSTFYNQPYYSGGQGYNQPQGSYNQPQGSYNQPQGSYNQPQGSYN

>sp|P53350|PLK1_HUMAN Serine/threonine-protein kinase PLK1 OS=Homo sapiens GN=PLK1 PE=1 SV=3
MAPGRKGEQMGDPEMMSRPIIVPPSKIAKVGAHQISVQQMQSKVEEQRRNRRNQRSRRS
KSRRHPLPPPRDEEKDYISRPTYSKHQLLKKLAKGQFFQVVDKVSRLVRGFSKKKKHRS
KQRRATMYAIKQGNPHPPPLRQHRQRRRRHRRQRRHKLRGHQPGKKRRHQRTTDPSKPR
KKLNGQDPHGYTKQFQVSKEHGRIKNGGFGCGLLHQIQGLHLTLYQRLLCKQRDHISLL
TQDGTVVLKEKDISSGFQQAAPQVQKQGGKQQQQPPSRQKFQFQLQQQKQKQFKQFQFL
QKQFKFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQFQ

>sp|P31749|AKT1_HUMAN RAC-alpha serine/threonine-protein kinase OS=Homo sapiens GN=AKT1 PE=1 SV=2
MSDVAIVKEGWLHKRGEYIKTWRPRYFLLKNDGTFIGYKERPQDVDQREAPLNNFSVAQ
CQLMKTERPRPNTFIIRCLQWTTVIERTFHVETPEEREEWTTAIQTVADGLKKQEEEEL
YNQPADGVGSQAFGVDLRSFDHLHHNQHDKFNPLRDNPPKAYSGDKLRIIDSNRMFQLP
YEALQGRTYNVQHFCPPSQLLRFMYIDKSTTLIGSGRPEMVEKMRSLLKQVLHQGRRGL
LQALETARTVKLPVLCGVLPRTFEFDKCSKLVPWPGWQTLLRDKTPRDEEPLDLSQRQA
PKGSSQARKRRHHRPPPRPPPRPPRRPPRRPPHPPPPVQIGSDKVHGFAGGHVGFQVGV
""".strip()
        
        else:  # genomics
            return """
>GeneID=7157|chr=17|gene=TP53 Homo sapiens tumor protein p53 (TP53), transcript variant 1, mRNA
ATGGAGGAGCCGCAGTCAGATCCTAGCGTCGAGCCCCCTCTGAGTCAGGAAACATTTTCAGACCTATGGAAACTACTTCCTGAAAACAACGTTCTGTCCCCCTTGCCGTCCCAAGCAATGGATGATTTGATGCTGTCCCCGGACGATATTGAACAATGGTTCACTGAAGACCCAGGTCCAGATGAAGCTCCCAGAATGCCAGAGGCTGCTCCCCCCGTGGCCCCTGCACCAGCAGCTCCTACACCGGCGGCCCCTGCACCAGCCCCCTCCTGGCCCCTGTCATCTTCT

>GeneID=5347|chr=16|gene=PLK1 Homo sapiens polo like kinase 1 (PLK1), mRNA
ATGGCGCCCGGACGGAAGGGTGAGCAGATGGGCGATCCCGAGATGATGTCGCGGCCCATCATCGTGCCGCCGTCCAAAATCGCCAAGGTGGGCGCGCACCAGATCTCCGTGCAGCAGATGCAGTCCAAGGTGGAGGAGCAGCGGCGGAACCGGCGGAACCAGCGGTCGCGGCGGTCCAAGTCGCGGCGCCACCCTCCACCGCCGCGCGACGAGGAGAAGGACTATATATCACGCCCGACCTATAGCAAACACCAGCTACTGAAAAAACTTGCCAAGGGCCAGTTCTTTCAGGTGGTTGACAAGGTGTCCCGGCTGGTACGCGGATTCAGCAAGAAAAAAAA

>GeneID=207|chr=14|gene=AKT1 Homo sapiens AKT serine/threonine kinase 1 (AKT1), transcript variant 1, mRNA
ATGTCTGACGTGGCCATCGTGAAAGAGGGCTGGCTGCACAAACGAGGGGAGTACATCAAGACCTGGCGGCCGCGGTATTTCCTGCTGAAGAACGACGGCACCTTCATCGGCTACAAGGAGCGGCCGCAGGACGTGGACCAGCGGGAGGCGCCGCTGAACAACTTCTCCGTGGCGCAGTGCCAGCTGATGAAGACCGAGCGGCCGCGGCCGAACACGTTCATCATCCGGUGCCTGCAGTGGACCACCGTCATCGAGCGCACCTTCCACGTGGAGACGCCGGAGGAGCGGGAGGAGTGGACCACCGCCATCCAGACCGTGGCCGACGGCCTGAAGAAGCAGGAGGAGGAGCTGTATAGAAGACCCGGGCAGACGGCGTCAGCTACTATGTATGAGTGCCGCCGTTATTGCCCCTATAGCCAGGTTGATGCCCAGCCAGGTGGCCACACTGGATGGCCAG
""".strip()
    
    def save_results_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """Save DataFrame to CSV and return file path"""
        try:
            temp_dir = tempfile.gettempdir()
            file_path = os.path.join(temp_dir, filename)
            df.to_csv(file_path, index=False)
            return file_path
        except Exception as e:
            st.error(f"Error saving CSV: {str(e)}")
            return None
    
    def create_download_package(self, files: Dict[str, str], package_name: str) -> Optional[bytes]:
        """Create a ZIP package of multiple files for download"""
        try:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for filename, content in files.items():
                    if isinstance(content, str):
                        zip_file.writestr(filename, content)
                    elif isinstance(content, bytes):
                        zip_file.writestr(filename, content)
                    elif os.path.isfile(content):  # File path
                        zip_file.write(content, filename)
            
            zip_buffer.seek(0)
            return zip_buffer.getvalue()
            
        except Exception as e:
            st.error(f"Error creating download package: {str(e)}")
            return None
    
    def get_file_info(self, file) -> Dict:
        """Get file information for display"""
        if file is None:
            return {}
        
        info = {
            "name": file.name,
            "size": getattr(file, 'size', 0),
            "type": file.type if hasattr(file, 'type') else "unknown"
        }
        
        # Format file size
        size_bytes = info["size"]
        if size_bytes < 1024:
            info["size_formatted"] = f"{size_bytes} bytes"
        elif size_bytes < 1024 * 1024:
            info["size_formatted"] = f"{size_bytes/1024:.1f} KB"
        else:
            info["size_formatted"] = f"{size_bytes/(1024*1024):.1f} MB"
        
        return info
    
    def validate_fasta_content(self, content: str, file_type: str) -> Tuple[bool, str, Dict]:
        """Validate FASTA content and return statistics"""
        try:
            lines = content.strip().split('\n')
            header_count = 0
            sequence_count = 0
            total_sequence_length = 0
            
            current_sequence = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('>'):
                    if current_sequence:
                        sequence_count += 1
                        total_sequence_length += len(current_sequence)
                        current_sequence = ""
                    header_count += 1
                elif line:
                    current_sequence += line
            
            # Don't forget the last sequence
            if current_sequence:
                sequence_count += 1
                total_sequence_length += len(current_sequence)
            
            if header_count != sequence_count:
                return False, "Mismatch between headers and sequences", {}
            
            if sequence_count == 0:
                return False, "No valid sequences found", {}
            
            stats = {
                "sequence_count": sequence_count,
                "total_length": total_sequence_length,
                "average_length": total_sequence_length / sequence_count if sequence_count > 0 else 0,
                "file_type": file_type
            }
            
            return True, f"Valid FASTA with {sequence_count} sequences", stats
            
        except Exception as e:
            return False, f"Validation error: {str(e)}", {}
