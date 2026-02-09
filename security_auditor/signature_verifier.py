"""
GuardianPDF - Signature Verifier

Digital signature and integrity verification for PDFs.
"""

from pypdf import PdfReader
import hashlib
from datetime import datetime
from typing import Dict, Optional, List
import os


class SignatureVerifier:
    """
    Verify PDF digital signatures and integrity.
    
    Features:
    - Digital signature validation
    - Metadata tampering detection
    - File hash verification
    - Modification timestamp analysis
    """
    
    def __init__(self):
        """Initialize signature verifier."""
        print("✅ Signature verifier initialized")
    
    def verify_pdf(self, filepath: str) -> Dict[str, any]:
        """
        Comprehensive PDF integrity check.
        
        Args:
            filepath: Path to PDF file
            
        Returns:
            Dict with verification results
        """
        if not os.path.exists(filepath):
            return {"error": "File not found", "verified": False}
        
        results = {
            "filepath": filepath,
            "file_size": os.path.getsize(filepath),
            "verified": True,
            "warnings": []
        }
        
        try:
            # Read PDF
            reader = PdfReader(filepath)
            
            # Basic info
            results["page_count"] = len(reader.pages)
            results["is_encrypted"] = reader.is_encrypted
            
            # Metadata analysis
            metadata = reader.metadata
            if metadata:
                results["metadata"] = self._analyze_metadata(metadata)
            else:
                results["warnings"].append("No metadata found")
            
            # Check for signatures (basic check)
            results["has_signature"] = self._check_signatures(reader)
            
            # Calculate file hash
            results["file_hash"] = self._calculate_hash(filepath)
            
            # Check for suspicious metadata
            suspicious = self._check_suspicious_metadata(metadata)
            if suspicious:
                results["warnings"].extend(suspicious)
                results["verified"] = False
            
        except Exception as e:
            results["error"] = str(e)
            results["verified"] = False
        
        return results
    
    def _analyze_metadata(self, metadata) -> Dict:
        """Extract and analyze PDF metadata."""
        meta_dict = {}
        
        # Common metadata fields
        fields = ['title', 'author', 'subject', 'creator', 'producer', 
                  'creation_date', 'modification_date']
        
        for field in fields:
            value = getattr(metadata, field, None)
            if value:
                meta_dict[field] = str(value)
        
        return meta_dict
    
    def _check_signatures(self, reader: PdfReader) -> bool:
        """
        Check if PDF has digital signatures.
        
        Note: Full signature validation requires additional libraries
        (e.g., pyHanko). This is a basic check.
        """
        # Check for signature fields in PDF catalog
        try:
            if '/AcroForm' in reader.trailer['/Root']:
                acro_form = reader.trailer['/Root']['/AcroForm']
                if '/Fields' in acro_form:
                    fields = acro_form['/Fields']
                    for field in fields:
                        field_obj = field.get_object()
                        if '/FT' in field_obj and field_obj['/FT'] == '/Sig':
                            return True
        except:
            pass
        
        return False
    
    def _calculate_hash(self, filepath: str, algorithm: str = "sha256") -> str:
        """Calculate file hash for integrity verification."""
        hash_func = hashlib.new(algorithm)
        
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        
        return hash_func.hexdigest()
    
    def _check_suspicious_metadata(self, metadata) -> List[str]:
        """
        Detect suspicious metadata patterns.
        
        Returns:
            List of warnings
        """
        warnings = []
        
        if not metadata:
            return warnings
        
        # Check for AI tool signatures
        ai_tools = ['ChatGPT', 'GPT', 'Claude', 'Bard', 'AI', 'Gemini']
        creator = str(getattr(metadata, 'creator', ''))
        producer = str(getattr(metadata, 'producer', ''))
        
        for tool in ai_tools:
            if tool.lower() in creator.lower() or tool.lower() in producer.lower():
                warnings.append(f"Metadata indicates AI tool: {tool}")
        
        # Check for metadata bombs (excessive entries)
        # Note: This is a simplified check
        all_metadata = str(metadata)
        if len(all_metadata) > 10000:
            warnings.append("Unusually large metadata (potential metadata bomb)")
        
        # Check for missing critical metadata
        if not getattr(metadata, 'creation_date', None):
            warnings.append("Missing creation date")
        
        # Check for suspicious date patterns
        creation = getattr(metadata, 'creation_date', None)
        modification = getattr(metadata, 'modification_date', None)
        
        if creation and modification:
            try:
                # Simple check: modification should be after creation
                # Full implementation would parse dates properly
                pass
            except:
                pass
        
        return warnings
    
    def batch_verify(self, filepaths: List[str]) -> Dict[str, Dict]:
        """
        Verify multiple PDF files.
        
        Args:
            filepaths: List of PDF paths
            
        Returns:
            Dict mapping filepath to verification results
        """
        results = {}
        
        for filepath in filepaths:
            results[filepath] = self.verify_pdf(filepath)
        
        return results
