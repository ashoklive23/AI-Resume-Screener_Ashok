import re

class SkillsAnalyzer:
    """
    Analyze resume text for procurement, sourcing, and premium skills
    """
    
    def __init__(self):
        # Core procurement and sourcing keywords
        self.procurement_keywords = {
            'procurement': ['procurement', 'purchase', 'purchasing', 'buy', 'buying'],
            'sourcing': ['sourcing', 'strategic sourcing', 'global sourcing', 'supplier sourcing'],
            'vendor_management': ['vendor management', 'supplier management', 'vendor relations', 
                                 'supplier relations', 'supplier development'],
            'negotiation': ['negotiation', 'contract negotiation', 'price negotiation', 
                           'negotiate', 'negotiating'],
            'rfp_rfq': ['rfp', 'rfq', 'rfi', 'request for proposal', 'request for quotation'],
            'cost_reduction': ['cost reduction', 'cost saving', 'cost optimization', 'savings',
                              'cost-effective', 'value engineering'],
            'supply_chain': ['supply chain', 'logistics', 'inventory', 'warehouse'],
            'category_management': ['category management', 'spend analysis', 'spend management'],
            'contract_management': ['contract management', 'contracting', 'contract administration'],
            'erp': ['sap', 'oracle', 'erp', 'enterprise resource planning', 'sap mm', 'sap ariba'],
            'compliance': ['compliance', 'regulatory', 'governance', 'risk management'],
            'quality': ['quality assurance', 'quality control', 'qa', 'qc', 'supplier quality']
        }
        
        # Premium skills that are added advantages
        self.premium_skills_keywords = {
            'excel': ['advanced excel', 'excel', 'vlookup', 'pivot table', 'macro', 'vba',
                     'xlookup', 'power query', 'excel modeling'],
            'powerbi': ['power bi', 'powerbi', 'power-bi', 'dax', 'power bi dashboard'],
            'tableau': ['tableau', 'tableau dashboard', 'tableau visualization'],
            'python': ['python', 'python programming', 'python scripting', 'pandas', 'numpy'],
            'sql': ['sql', 'mysql', 'postgresql', 'sql server', 'sql query'],
            'data_analytics': ['data analytics', 'data analysis', 'business intelligence', 
                              'bi', 'analytics'],
            'automation': ['automation', 'rpa', 'process automation', 'uipath', 'blue prism']
        }
        
        # Advanced procurement concepts (for domain scoring)
        self.advanced_concepts = [
            'total cost of ownership', 'tco', 'target costing', 'should cost',
            'value analysis', 'supplier scorecard', 'supplier audit',
            'make or buy', 'dual sourcing', 'single sourcing',
            'jit', 'just in time', 'lean procurement', 'agile procurement',
            'sustainability', 'green procurement', 'ethical sourcing',
            'e-procurement', 'procure to pay', 'p2p', 'source to pay', 's2p'
        ]
    
    def analyze(self, resume_text):
        """
        Analyze resume text for procurement skills and premium skills
        
        Args:
            resume_text (str): Resume text
            
        Returns:
            dict: Analysis results
        """
        text_lower = resume_text.lower()
        
        # Find procurement skills
        procurement_skills = self._find_procurement_skills(text_lower)
        
        # Find premium skills
        premium_skills = self._find_premium_skills(text_lower)
        
        # Calculate domain score
        domain_score = self._calculate_domain_score(text_lower, procurement_skills, premium_skills)
        
        return {
            'procurement_skills': procurement_skills,
            'premium_skills': premium_skills,
            'domain_score': domain_score
        }
    
    def _find_procurement_skills(self, text):
        """Find procurement and sourcing skills in resume text"""
        found_skills = set()
        
        for category, keywords in self.procurement_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    # Add readable version of the skill
                    skill_name = self._format_skill_name(keyword)
                    found_skills.add(skill_name)
        
        return sorted(list(found_skills))
    
    def _find_premium_skills(self, text):
        """Find premium skills (Excel, Power BI, Tableau, etc.) in resume text"""
        found_skills = set()
        
        for category, keywords in self.premium_skills_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    # Add the category name instead of individual keyword
                    category_name = self._get_premium_category_name(category)
                    found_skills.add(category_name)
                    break  # Only add once per category
        
        return sorted(list(found_skills))
    
    def _calculate_domain_score(self, text, procurement_skills, premium_skills):
        """
        Calculate domain expertise score (0-100)
        
        Scoring breakdown:
        - Base procurement skills: 40 points (max)
        - Advanced concepts: 30 points (max)
        - Premium skills: 20 points (max)
        - Keyword density: 10 points (max)
        """
        score = 0
        
        # 1. Base procurement skills (up to 40 points)
        # Award points for each unique skill category found
        skill_categories_found = set()
        for category, keywords in self.procurement_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    skill_categories_found.add(category)
                    break
        
        # 40 points distributed across 12 categories
        score += min(40, len(skill_categories_found) * 3.33)
        
        # 2. Advanced concepts (up to 30 points)
        advanced_found = sum(1 for concept in self.advanced_concepts if concept in text)
        score += min(30, advanced_found * 2)
        
        # 3. Premium skills (up to 20 points)
        score += min(20, len(premium_skills) * 3)
        
        # 4. Keyword density (up to 10 points)
        # Count total procurement-related keywords
        word_count = len(text.split())
        procurement_word_count = 0
        for keywords in self.procurement_keywords.values():
            for keyword in keywords:
                procurement_word_count += text.count(keyword)
        
        if word_count > 0:
            density = (procurement_word_count / word_count) * 100
            density_score = min(10, density * 2)  # Cap at 10 points
            score += density_score
        
        return min(100, round(score))
    
    def _format_skill_name(self, keyword):
        """Format skill name for display"""
        # Capitalize first letter of each word
        words = keyword.split()
        formatted = ' '.join(word.capitalize() for word in words)
        
        # Special cases
        replacements = {
            'Sap': 'SAP',
            'Erp': 'ERP',
            'Rfp': 'RFP',
            'Rfq': 'RFQ',
            'Rfi': 'RFI',
            'Qa': 'QA',
            'Qc': 'QC',
            'Jit': 'JIT',
            'Tco': 'TCO',
            'P2p': 'P2P',
            'S2p': 'S2P'
        }
        
        for old, new in replacements.items():
            formatted = formatted.replace(old, new)
        
        return formatted
    
    def _get_premium_category_name(self, category):
        """Get display name for premium skill category"""
        category_names = {
            'excel': 'Advanced Excel',
            'powerbi': 'Power BI',
            'tableau': 'Tableau',
            'python': 'Python',
            'sql': 'SQL',
            'data_analytics': 'Data Analytics',
            'automation': 'Process Automation'
        }
        return category_names.get(category, category.capitalize())
