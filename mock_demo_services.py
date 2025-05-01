"""
Mock Demo Services module for integrating with Storylane demos.
This module simulates API interactions with Storylane for demo orchestration.
"""

import time
import json
from typing import Dict, List, Any, Optional
import webbrowser

class StorylaneDemoService:
    """Service for interacting with Storylane demos."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Storylane demo service.
        
        Args:
            api_key: Optional API key for Storylane (not required for mock)
        """
        self.api_key = api_key
        self.current_demo_id = None
        self.current_section_id = None
        
        # Define our cybersecurity demo sections
        self.demo_sections = {
            "prismacloud_demo": [
                {
                    "id": "dashboard",
                    "name": "Dashboard Overview",
                    "description": "Overview of the main Prisma Cloud dashboard and key features",
                    "url": "https://app.storylane.io/share/filcrnbzfr0i?page_id=412f5a03-66bf-4d00-b752-b34b6886908b",
                    "relevant_topics": ["dashboard", "overview", "visibility", "ui", "navigation", "main features"],
                    "addresses_objections": ["complexity", "ease of use", "learning curve"],
                    "answers_questions": ["What does the interface look like?", "How do I navigate the platform?", "What can I see at a glance?"]
                },
                {
                    "id": "security",
                    "name": "Security Settings",
                    "description": "Configuration of security policies and compliance standards",
                    "url": "https://app.storylane.io/share/filcrnbzfr0i?page_id=86c995a2-bf4a-442b-9125-e758be1e0748",
                    "relevant_topics": ["security", "compliance", "configuration", "policies", "standards", "soc2", "gdpr", "hipaa"],
                    "addresses_objections": ["compliance requirements", "security standards", "policy management", "regulatory challenges"],
                    "answers_questions": ["How do I set security policies?", "Can it meet compliance requirements?", "How configurable are the security settings?"]
                },
                {
                    "id": "alerts",
                    "name": "Alerts",
                    "description": "Alert management, notifications, and remediation workflows",
                    "url": "https://app.storylane.io/share/filcrnbzfr0i?page_id=9f19ef20-2c1a-46ca-b85f-740b7d236412",
                    "relevant_topics": ["alerts", "notifications", "incidents", "remediation", "response", "monitoring"],
                    "addresses_objections": ["alert fatigue", "false positives", "incident response time", "prioritization"],
                    "answers_questions": ["How are alerts managed?", "Can we customize alert thresholds?", "What's the incident response workflow?"]
                },
                {
                    "id": "enforcement",
                    "name": "Enforcement",
                    "description": "Policy enforcement and automated remediation capabilities",
                    "url": "https://app.storylane.io/share/filcrnbzfr0i?page_id=d4555711-e77c-494d-bbd2-eece331ac63f",
                    "relevant_topics": ["enforcement", "automation", "remediation", "policy", "actions", "automatic fixes"],
                    "addresses_objections": ["manual workload", "time to remediate", "enforcement consistency"],
                    "answers_questions": ["Can it automatically fix issues?", "How does policy enforcement work?", "What kind of automation is available?"]
                },
                {
                    "id": "inventory",
                    "name": "Inventory",
                    "description": "Asset inventory and resource management across cloud environments",
                    "url": "https://app.storylane.io/share/filcrnbzfr0i?page_id=321f5c3f-4042-4c60-b415-18a0655d4f89",
                    "relevant_topics": ["inventory", "assets", "resources", "discovery", "cloud resources", "tracking"],
                    "addresses_objections": ["visibility", "shadow IT", "asset tracking", "resource management"],
                    "answers_questions": ["How does it track cloud resources?", "Can we see all our assets?", "How is the inventory maintained?"]
                },
                {
                    "id": "api",
                    "name": "API Overview",
                    "description": "API capabilities and integration options with other tools",
                    "url": "https://app.storylane.io/share/filcrnbzfr0i?page_id=86c995a2-bf4a-442b-9125-e758be1e0748",
                    "relevant_topics": ["api", "integrations", "automation", "devops", "cicd", "jenkins", "github", "devsecops"],
                    "addresses_objections": ["integration with existing tools", "ci/cd pipeline", "development workflow"],
                    "answers_questions": ["Can it integrate with our CI/CD tools?", "How does the API work?", "Can we automate workflows?"]
                }
            ]
        }
        
    def get_available_demos(self) -> List[Dict[str, Any]]:
        """
        Get a list of available demos.
        
        Returns:
            List of demo dictionaries with id and name
        """
        return [
            {"id": "prismacloud_demo", "name": "Prisma Cloud Security Demo"}
        ]
    
    def get_demo_sections(self, demo_id: str) -> List[Dict[str, Any]]:
        """
        Get sections for a specific demo.
        
        Args:
            demo_id: ID of the demo
            
        Returns:
            List of section dictionaries
        """
        self.current_demo_id = demo_id
        return self.demo_sections.get(demo_id, [])
    
    def navigate_to_section(self, section_id: str) -> bool:
        """
        Navigate to a specific section within the current demo.
        
        Args:
            section_id: ID of the section to navigate to
            
        Returns:
            Boolean indicating success
        """
        if not self.current_demo_id:
            print("No demo currently loaded")
            return False
        
        sections = self.demo_sections.get(self.current_demo_id, [])
        section = next((s for s in sections if s["id"] == section_id), None)
        
        if not section:
            print(f"Section {section_id} not found")
            return False
        
        # In a real implementation, this would use an API call
        # For our mock, we'll print and potentially open the URL
        print(f"Navigating to section: {section['name']}")
        print(f"URL: {section['url']}")
        
        # Uncomment to actually open the URL in a browser
        # webbrowser.open(section['url'])
        
        self.current_section_id = section_id
        return True
    
    def get_current_section(self) -> Optional[Dict[str, Any]]:
        """
        Get the current active section.
        
        Returns:
            Dictionary representing the current section or None
        """
        if not self.current_demo_id or not self.current_section_id:
            return None
        
        sections = self.demo_sections.get(self.current_demo_id, [])
        return next((s for s in sections if s["id"] == self.current_section_id), None)
