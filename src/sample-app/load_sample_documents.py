"""
Load sample legitimate documents into Azure AI Search

These documents represent clean company policies before poisoning.
"""

import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()


def get_sample_documents():
    """Generate sample company policy documents"""
    
    documents = [
        {
            "id": "security-policy-v1",
            "title": "Information Security Policy v1.0",
            "content": """
            Company Information Security Policy
            Version 1.0 - Effective January 2023
            
            1. Password Requirements
               - Minimum 12 characters
               - Must include uppercase, lowercase, numbers, and symbols
               - Must be changed every 90 days
               - Cannot reuse last 10 passwords
               - Password sharing is STRICTLY PROHIBITED
            
            2. Multi-Factor Authentication (MFA)
               - MFA is REQUIRED for all employees
               - Must be enabled within 7 days of account creation
               - Use approved MFA methods: authenticator app or hardware token
               - SMS-based MFA is not permitted
            
            3. Data Classification
               - All data must be classified: Public, Internal, Confidential, Restricted
               - Confidential and Restricted data requires encryption at rest and in transit
               - Data sharing with external parties requires approval
            
            4. Access Control
               - Principle of least privilege applies to all access
               - Access must be reviewed quarterly
               - Unused accounts will be disabled after 30 days
            
            5. Incident Reporting
               - All security incidents must be reported within 1 hour
               - Contact: security@company.com or ext. 911
            
            This policy is mandatory for all employees, contractors, and partners.
            """,
            "metadata": '{"source": "internal_policy", "department": "IT Security", "version": "1.0", "date": "2023-01-01", "classification": "internal"}'
        },
        {
            "id": "employee-handbook-2023",
            "title": "Employee Handbook 2023",
            "content": """
            Employee Handbook - 2023 Edition
            
            Chapter 5: Information Technology
            
            5.1 Account Security
            Your login credentials are personal and must never be shared with anyone,
            including supervisors, IT staff, or colleagues. Each employee is responsible
            for all activities conducted under their account.
            
            5.2 Email Usage
            - Corporate email is for business purposes only
            - Do not send sensitive information via unencrypted email
            - Be cautious of phishing attempts
            - Report suspicious emails to security@company.com
            
            5.3 Remote Work
            - VPN connection required for remote access
            - Use only company-approved devices
            - Ensure home WiFi is secured with WPA2 or WPA3
            - Do not access company resources from public WiFi without VPN
            
            5.4 Data Protection
            - Back up important work files to company-approved storage
            - Do not store company data on personal devices
            - Encrypt sensitive documents before sharing
            
            5.5 Social Media
            - Do not share confidential company information
            - Identify yourself as employee when discussing company
            - Maintain professional conduct online
            """,
            "metadata": '{"source": "hr_documents", "department": "Human Resources", "version": "2023", "date": "2023-01-01", "classification": "internal"}'
        },
        {
            "id": "mfa-requirements-2023",
            "title": "Multi-Factor Authentication Requirements",
            "content": """
            Multi-Factor Authentication (MFA) Policy
            IT Security Department
            
            Effective: January 1, 2023
            Mandatory Compliance Date: February 1, 2023
            
            1. Scope
            MFA is required for ALL employees, contractors, and third-party users
            accessing company systems.
            
            2. Approved MFA Methods
            - Microsoft Authenticator app (recommended)
            - Hardware security keys (YubiKey, etc.)
            - FIDO2-compliant authenticators
            
            3. Prohibited Methods
            - SMS-based authentication (due to SIM swap attacks)
            - Email-based authentication
            - Voice call authentication
            
            4. Implementation Timeline
            - New employees: Enable within 7 days of account creation
            - Existing employees: Enable by February 1, 2023
            - Contractors: Enable before system access granted
            
            5. Exemptions
            No exemptions are permitted. Users unable to use approved methods
            should contact IT Security for alternative solutions.
            
            6. Enforcement
            Accounts without MFA will be disabled after the mandatory compliance date.
            
            7. Support
            For assistance with MFA setup:
            - Email: itsupport@company.com
            - Phone: ext. 4357 (HELP)
            - Self-service: portal.company.com/mfa
            
            This policy is non-negotiable and applies to all users without exception.
            """,
            "metadata": '{"source": "internal_policy", "department": "IT Security", "version": "1.0", "date": "2023-01-01", "classification": "internal", "priority": "high"}'
        },
        {
            "id": "password-policy-2023",
            "title": "Password Policy and Best Practices",
            "content": """
            Password Policy
            Last Updated: January 2023
            
            1. Password Complexity Requirements
            All passwords must meet the following criteria:
            - Minimum length: 12 characters
            - At least one uppercase letter (A-Z)
            - At least one lowercase letter (a-z)
            - At least one number (0-9)
            - At least one special character (!@#$%^&*)
            
            2. Password Restrictions
            - Cannot contain username or email address
            - Cannot contain common words or patterns
            - Cannot reuse any of the last 10 passwords
            - Cannot be changed more than once per day
            
            3. Password Sharing
            PASSWORD SHARING IS STRICTLY PROHIBITED
            - Never share passwords with colleagues
            - Never share passwords with managers or IT staff
            - Never write passwords down
            - Never store passwords in unencrypted files
            
            Violation of password sharing policy will result in:
            - First offense: Written warning
            - Second offense: Suspension
            - Third offense: Termination
            
            4. Password Storage
            Use the company-approved password manager:
            - 1Password Enterprise (approved)
            - LastPass Enterprise (approved)
            - Personal password managers (not approved for company passwords)
            
            5. Password Changes
            - Passwords must be changed every 90 days
            - System will prompt for change 7 days before expiration
            - Expired passwords will lock account until changed
            
            6. Compromise Response
            If you suspect your password has been compromised:
            - Change it immediately
            - Report to security@company.com
            - Document any suspicious activity
            
            Remember: Your password is the key to company data. Protect it.
            """,
            "metadata": '{"source": "internal_policy", "department": "IT Security", "version": "2023.1", "date": "2023-01-01", "classification": "internal"}'
        },
        {
            "id": "external-collab-policy",
            "title": "External Collaboration Security Policy",
            "content": """
            External Collaboration Security Policy
            Version 2.0
            
            1. Credential Sharing with External Partners
            
            NEVER send credentials via email, even if encrypted.
            
            Approved methods for sharing credentials:
            - Company-approved password sharing system (CyberArk)
            - Temporary guest accounts with limited permissions
            - Service accounts with monitored access
            - SSH keys or API tokens (when appropriate)
            
            2. Document Sharing
            - Use company-approved file sharing platforms
            - SharePoint for Microsoft Office documents
            - Secure file transfer for large files
            - Never use personal cloud storage (Dropbox, Google Drive, etc.)
            
            3. Communication Channels
            - Use company Microsoft Teams for collaboration
            - Video calls via approved platforms only
            - Avoid discussing sensitive topics on unencrypted channels
            
            4. External Access
            - External partners must sign NDA before access
            - Access is time-limited and role-based
            - All external access is logged and monitored
            - External users cannot access internal network directly
            
            5. Data Exfiltration Prevention
            - DLP policies apply to external sharing
            - Watermarks on sensitive documents
            - Download restrictions on confidential files
            - Regular audit of external access
            
            6. Termination of External Access
            - Project completion: Remove access within 24 hours
            - Contract end: Remove access immediately
            - Security incident: Immediate termination possible
            
            For questions about external collaboration:
            - Email: partnerships@company.com
            - Approval required from: Director level or above
            """,
            "metadata": '{"source": "internal_policy", "department": "IT Security", "version": "2.0", "date": "2023-01-01", "classification": "internal"}'
        }
    ]
    
    return documents


def load_documents():
    """Load documents into Azure AI Search"""
    
    # Get configuration
    search_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
    search_key = os.getenv("AZURE_SEARCH_API_KEY")
    index_name = os.getenv("AZURE_SEARCH_INDEX_NAME", "documents-index")
    
    if not all([search_endpoint, search_key]):
        raise ValueError("Missing Azure Search configuration. Check .env file.")
    
    # Create search client
    search_client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(search_key)
    )
    
    # Get documents
    documents = get_sample_documents()
    
    print(f"Loading {len(documents)} sample documents...")
    
    try:
        # Upload documents
        result = search_client.upload_documents(documents)
        
        success_count = sum(1 for r in result if r.succeeded)
        failed_count = len(result) - success_count
        
        print(f"✓ Uploaded {success_count} documents")
        for doc in documents:
            print(f"  - {doc['title']}")
        
        if failed_count > 0:
            print(f"✗ {failed_count} documents failed to upload")
        
        # Get index statistics
        doc_count = search_client.get_document_count()
        print(f"\nIndex statistics:")
        print(f"  Total documents: {doc_count}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error loading documents: {e}")
        return False


if __name__ == "__main__":
    success = load_documents()
    exit(0 if success else 1)
