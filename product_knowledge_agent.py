"""
Product Knowledge Agent for Security Products

This agent provides detailed product knowledge for security products (Prisma Cloud and Carbon Black)
by retrieving and indexing documentation and answering product-specific questions.
"""

import os
import requests
from bs4 import BeautifulSoup
import anthropic
from typing import List, Dict, Any, Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

class ProductKnowledgeAgent:
    """Agent specialized in security product knowledge."""
    
    def __init__(self, anthropic_api_key: str, openai_api_key: Optional[str] = None, product_type: str = "carbon_black"):
        """
        Initialize the Knowledge Agent.
        
        Args:
            anthropic_api_key: API key for Claude
            openai_api_key: Optional API key for OpenAI embeddings
            product_type: Type of product to focus on ('prisma_cloud' or 'carbon_black')
        """
        self.anthropic_api_key = anthropic_api_key
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.product_type = product_type
        
        # For embeddings, we can use different providers
        self.openai_api_key = openai_api_key
        
        # Choose embeddings based on available API keys
        if openai_api_key:
            # Use OpenAI embeddings if key is provided
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        else:
            # Use HuggingFace embeddings as fallback
            from langchain_community.embeddings import HuggingFaceEmbeddings
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Track processed URLs
        self.processed_urls = set()
        
        # Initialize with default product URLs
        self._initialize_with_default_urls()
        
    def _initialize_with_default_urls(self):
        """Initialize with default product URLs based on product type."""
        if self.product_type == "carbon_black":
            # Carbon Black URLs
            urls = [
                "https://www.broadcom.com/products/carbon-black",
                "https://www.broadcom.com/products/carbon-black/threat-prevention",
                "https://www.broadcom.com/products/carbon-black/threat-detection-and-response",
                "https://www.broadcom.com/products/carbon-black/threat-detection-and-response/endpoint-detection-and-response",
                "https://docs.broadcom.com/doc/Carbon-Black-EDR-Datasheet"
            ]
            print("Initializing Product Knowledge Agent with Carbon Black documentation...")
        else:
            # Prisma Cloud URLs
            urls = [
                "https://docs.prismacloud.io/en/enterprise-edition/rn/prisma-cloud-release-info",
                "https://docs.prismacloud.io/en/enterprise-edition/rn/features-introduced-in-2023",
                "https://docs.prismacloud.io/en/enterprise-edition/rn/features-introduced-in-2022"
            ]
            print("Initializing Product Knowledge Agent with Prisma Cloud documentation...")
            
        # Initialize with these URLs
        self.initialize_with_multiple_urls(urls)
        
        # Add fallback product information in case URL scraping fails
        self._add_fallback_product_info()

    def _add_fallback_product_info(self):
        """Add fallback product information based on product type."""
        fallback_text = []
        
        if self.product_type == "carbon_black":
            # Carbon Black fallback information
            fallback_text.append("Carbon Black is a cybersecurity solution now owned by Broadcom (previously VMware).")
            fallback_text.append("Carbon Black provides endpoint protection, detection and response capabilities.")
            fallback_text.append("Key products include Carbon Black EDR (Endpoint Detection and Response), Carbon Black Cloud, and Carbon Black App Control.")
            fallback_text.append("Carbon Black uses behavioral analytics, machine learning, and threat intelligence to detect and prevent attacks.")
            fallback_text.append("Carbon Black EDR provides continuous monitoring, threat hunting, and incident response capabilities.")
            fallback_text.append("Carbon Black Cloud is a cloud-native endpoint protection platform that combines antivirus, EDR, and threat hunting.")
            fallback_text.append("Carbon Black App Control provides application control and critical infrastructure protection.")
            fallback_text.append("Carbon Black integrates with many security tools and SOC platforms.")
        else:
            # Prisma Cloud fallback information
            fallback_text.append("Prisma Cloud is a comprehensive cloud native security platform from Palo Alto Networks.")
            fallback_text.append("It provides visibility and protection across the entire cloud native stack, from infrastructure to applications.")
            fallback_text.append("Key features include CSPM, CWPP, CIEM, and supply chain security.")
            fallback_text.append("Prisma Cloud integrates with CI/CD pipelines for shift-left security.")
            fallback_text.append("Prisma Cloud supports multiple cloud providers including AWS, Azure, and GCP.")
        
        # Add the fallback information to the knowledge base
        if fallback_text:
            combined_text = "\n\n".join(fallback_text)
            try:
                chunks = self.text_splitter.split_text(combined_text)
                if self.vector_store:
                    self.vector_store.add_texts(chunks)
                else:
                    self.vector_store = FAISS.from_texts(texts=chunks, embedding=self.embeddings)
                print(f"Added fallback product information to knowledge base.")
            except Exception as e:
                print(f"Error adding fallback information: {e}")

    def scrape_documentation(self, url: str) -> str:
        """
        Scrape the product documentation.
        
        Args:
            url: URL of the documentation to scrape
            
        Returns:
            Extracted text content
        """
        try:
            print(f"Scraping {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove unnecessary elements
            for element in soup.find_all(['script', 'style', 'nav', 'footer']):
                element.decompose()
                
            # Get the main content
            text = soup.get_text(strip=True)
            print(f"Scraped {len(text)} characters of text from {url}")
            return text
        except Exception as e:
            print(f"Error scraping documentation from {url}: {e}")
            return ""

    def process_documentation(self, text: str):
        """
        Process the documentation and create vector store.
        
        Args:
            text: Text content to process
        """
        try:
            # Split text into chunks
            if not text:
                raise ValueError("No text to process")
                
            chunks = self.text_splitter.split_text(text)
            print(f"Split text into {len(chunks)} chunks")
            
            if not chunks:
                raise ValueError("No chunks created from text")
                
            # Create vector store
            if self.vector_store:
                # Add to existing store
                self.vector_store.add_texts(chunks)
            else:
                # Create new store
                self.vector_store = FAISS.from_texts(
                    texts=chunks,
                    embedding=self.embeddings
                )
            print(f"Processed {len(chunks)} chunks of documentation")
        except Exception as e:
            print(f"Error processing documentation: {e}")

    def add_documentation(self, doc_url: str) -> bool:
        """
        Add additional documentation to the knowledge base.
        
        Args:
            doc_url: URL of the documentation to add
            
        Returns:
            Boolean indicating success
        """
        # Check if URL was already processed
        if doc_url in self.processed_urls:
            print(f"URL {doc_url} was already processed. Skipping.")
            return True
            
        print(f"Scraping additional documentation from {doc_url}...")
        text = self.scrape_documentation(doc_url)
        
        if not text:
            print(f"Failed to scrape documentation from {doc_url}")
            return False
        
        print("Processing additional documentation...")
        try:
            # Process the documentation
            self.process_documentation(text)
            
            # Mark URL as processed
            self.processed_urls.add(doc_url)
            return True
        except Exception as e:
            print(f"Error processing additional documentation: {e}")
            return False

    def initialize_with_multiple_urls(self, urls: List[str]):
        """
        Initialize the agent with multiple documentation URLs.
        
        Args:
            urls: List of documentation URLs to initialize with
        """
        success = False
        
        for url in urls:
            print(f"Processing URL: {url}")
            if not self.vector_store:
                # First URL - use normal initialization
                print("Initializing with first URL...")
                self.initialize(url)
                if self.vector_store:
                    success = True
            else:
                # Additional URLs - add to existing knowledge base
                result = self.add_documentation(url)
                success = success or result
        
        if success:
            print("Agent initialized successfully with multiple documentation sources!")
        else:
            print("Failed to initialize agent with any documentation. Using fallback data...")
            self._add_fallback_product_info()

    def query_knowledge_base(
        self, 
        query: str, 
        k: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Query the knowledge base for relevant context.
        
        Args:
            query: The query to search for
            k: Number of results to return
            
        Returns:
            List of document dictionaries with relevant text
        """
        if not self.vector_store:
            return [{"text": f"Knowledge base for {self.product_type} not initialized."}]
        
        try:
            # Get similar documents
            docs = self.vector_store.similarity_search(query, k=k)
            return [{"text": doc.page_content} for doc in docs]
        except Exception as e:
            print(f"Error querying knowledge base: {e}")
            # Return fallback info based on product type
            if self.product_type == "carbon_black":
                return [{"text": "Carbon Black is a cybersecurity solution from Broadcom providing endpoint detection and response capabilities."}]
            else:
                return [{"text": "Prisma Cloud is a comprehensive cloud native security platform from Palo Alto Networks."}]

    def get_response(self, query: str) -> str:
        """
        Get a response to a product question using the Claude API.
        
        Args:
            query: The product question to answer
            
        Returns:
            Response text answering the question
        """
        try:
            # Get relevant context
            context_docs = self.query_knowledge_base(query)
            
            if not context_docs:
                if self.product_type == "carbon_black":
                    return "I don't have specific information about that aspect of Carbon Black."
                else:
                    return "I don't have specific information about that aspect of Prisma Cloud."
                
            context = "\n\n".join([doc["text"] for doc in context_docs])

            # Create system prompts based on product type
            if self.product_type == "carbon_black":
                system_prompt = """You are a Carbon Black Product Expert. Use the provided context to answer questions accurately. 
                If the information isn't in the context, use your general knowledge about cybersecurity concepts, 
                but make it clear what is from the documentation versus general knowledge.
                Keep answers concise and focus on answering the specific question.
                Carbon Black is a cybersecurity product from Broadcom that provides endpoint detection and response capabilities."""
            else:
                system_prompt = """You are a Prisma Cloud Product Expert. Use the provided context to answer questions accurately. 
                If the information isn't in the context, use your general knowledge about cloud security concepts, 
                but make it clear what is from the documentation versus general knowledge.
                Keep answers concise and focus on answering the specific question.
                Prisma Cloud is a product from Palo Alto Networks that provides cloud security across multiple clouds."""

            # Create the completion using Claude
            message = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",  # Using a more widely available model
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {
                        "role": "user", 
                        "content": f"Context: {context}\n\nQuestion: {query}"
                    }
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            print(f"Detailed error in get_response: {e}")
            if self.product_type == "carbon_black":
                return f"I'm currently having trouble retrieving information about that. Carbon Black provides endpoint detection and response capabilities to detect, investigate, and respond to advanced threats."
            else:
                return f"I'm currently having trouble retrieving information about that. Prisma Cloud provides comprehensive cloud security capabilities including cloud security posture management, cloud workload protection, and cloud infrastructure entitlement management."

    def initialize(self, doc_url: str):
        """
        Initialize the agent with documentation.
        
        Args:
            doc_url: URL of the documentation to initialize with
        """
        print(f"Scraping documentation from {doc_url}...")
        text = self.scrape_documentation(doc_url)
        
        if not text:
            print("Failed to scrape documentation, using fallback information")
            self._add_fallback_product_info()
        else:
            # Mark URL as processed
            self.processed_urls.add(doc_url)
            
            print("Processing documentation...")
            self.process_documentation(text)
            print("Agent initialized successfully!")