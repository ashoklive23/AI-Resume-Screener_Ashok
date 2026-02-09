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
    
    def check_suitability(self, text):
        """
        Check if the profile suits specific roles
        
        Args:
            text (str): Resume text
            
        Returns:
            dict: Suitability analysis
        """
        text_lower = text.lower()
        
        # Define specific keywords for each role type
        role_keywords = {
            'Sourcing': self.procurement_keywords['sourcing'] + ['strategic sourcing', 'supplier discovery'],
            'Procurement': self.procurement_keywords['procurement'] + ['purchase order', 'purchasing', 'buying'],
            'Vendor Development': self.procurement_keywords['vendor_management'] + ['supplier development', 'vendor improvement']
        }
        
        suitability = {}
        
        for role, keywords in role_keywords.items():
            matches = [k for k in keywords if k in text_lower]
            unique_matches = list(set(matches))
            
            # Simple scoring: High if > 2 unique keywords, Medium if > 0, Low otherwise
            if len(unique_matches) >= 2:
                fit = "High"
            elif len(unique_matches) > 0:
                fit = "Medium"
            else:
                fit = "Low"
                
            suitability[role] = {
                'fit': fit,
                'matched_keywords': unique_matches
            }
            
        return suitability

    def analyze(self, text, experience_years=0):
        """
        Analyze resume text for key skills and domain knowledge
        
        Args:
            text (str): Resume text
            experience_years (float): Years of experience
            
        Returns:
            dict: Analysis results
        """
        text_lower = text.lower()
        
        # Find procurement skills
        procurement_skills = self._find_procurement_skills(text_lower)
        
        # Find premium skills
        premium_skills = self._find_premium_skills(text_lower)
        
        # Calculate domain score
        score_data = self._calculate_domain_score(text_lower, procurement_skills, premium_skills, experience_years)
        domain_score = score_data['total_score']
        score_breakdown = score_data['breakdown']
        
        # Check role suitability
        suitability = self.check_suitability(text_lower)
        
        # Determine best fit role
        best_fit_role = "General Procurement"
        max_matches = 0
        
        for role, data in suitability.items():
            if len(data['matched_keywords']) > max_matches:
                max_matches = len(data['matched_keywords'])
                best_fit_role = role
            elif len(data['matched_keywords']) == max_matches and max_matches > 0:
                # If tie, append
                if role not in best_fit_role:
                    best_fit_role += f" / {role}"
        
        if max_matches == 0:
            best_fit_role = "General Procurement"
            
        # Generate Pros and Cons
        pros, cons = self._generate_pros_cons(domain_score, premium_skills, suitability, score_breakdown, text_lower, experience_years)
        
        return {
            'procurement_skills': procurement_skills,
            'premium_skills': premium_skills,
            'domain_score': domain_score,
            'score_breakdown': score_breakdown,
            'suitability': suitability,
            'best_fit_role': best_fit_role,
            'pros': pros,
            'cons': cons
        }
        
    def _generate_pros_cons(self, score, premium_skills, suitability, breakdown, text, experience_years):
        """Generate pros and cons based on analysis"""
        pros = []
        cons = []
        import re
        
        # Score based
        if score >= 70:
            pros.append("High domain expertise score")
        elif score < 40:
            cons.append("Low domain expertise score")
            
        # Skills based
        if premium_skills:
            pros.append(f"Possesses premium skills ({len(premium_skills)} detected)")
        else:
            cons.append("No premium skills (Python, PowerBI, etc.) detected")
            
        # Achievement Analysis
        achievement_keywords = [
            'achieved', 'saved', 'increased', 'decreased', 'reduced', 'improved', 
            'delivered', 'awarded', 'accolade', 'revenue', 'budget', 'cost saving',
            'optimization', '%', 'million', 'billion', 'usd', 'inr'
        ]
        achievement_count = sum(1 for word in achievement_keywords if word in text)
        
        if achievement_count >= 5:
            pros.append("Strong track record of quantifiable achievements")
        elif achievement_count >= 2:
            pros.append("Mention of result-oriented achievements")
        else:
            cons.append("Limited mention of quantifiable achievements")

        # Stability/Tenure Analysis (Job Hopping)
        if experience_years > 0:
            # Heuristic: Count date ranges to estimate number of roles
            # Pattern: Month Year - Month Year
            date_pattern = r'(\w+\s+\d{4})\s*[-–—to]+\s*(\w+\s+\d{4}|present|current)'
            matches = re.findall(date_pattern, text)
            num_roles = len(matches)
            
            # If no matches found, fallback isn't possible easily, so skip
            if num_roles > 0:
                avg_tenure = experience_years / num_roles
                
                if experience_years > 2 and avg_tenure < 1.0:
                    cons.append(f"Frequent job changes detected (Approx. {num_roles} roles in {experience_years} years)")
                elif experience_years > 5 and avg_tenure > 3.0:
                    pros.append("Demonstrates long-term stability in roles")

        # Fit based
        high_fits = [role for role, data in suitability.items() if data.get('fit') == 'High']
        if high_fits:
            pros.append(f"Strong alignment with {', '.join(high_fits)} roles")
        else:
            if not any(data.get('fit') == 'Medium' for data in suitability.values()):
                cons.append("Weak alignment with core procurement roles")
                
        # Density based
        if breakdown.get('Keyword Density', 0) < 3:
            cons.append("Low keyword density in resume")
            
        return pros, cons
    
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
                    break 
        
        return sorted(list(found_skills))

    def _calculate_domain_score(self, text, procurement_skills, premium_skills, experience_years=0):
        """
        Calculate domain score based on identified skills and stability
        Total: 100 Points
        - Base Procurement Skills: 30 pts
        - Advanced Concepts: 30 pts
        - Premium Skills: 20 pts
        - Keyword Density (Procurement/Sourcing/Vendor): 10 pts
        - Stability (Avg Tenure > 2 yrs): 10 pts
        """
        score = 0
        
        # 1. Base Procurement Skills (Max 30)
        skill_categories_found = set()
        for skill in procurement_skills:
            root = skill.split()[0].lower()
            skill_categories_found.add(root)
            
        base_score = min(30, len(skill_categories_found) * 3)
        score += base_score
        
        # 2. Advanced Concepts (Max 30)
        # Assuming advanced_concepts is defined in __init__ or we use a local list if not
        # To be safe, I'll define it locally as I did in my logic design, unless simple self.advanced_concepts is reliable.
        # The previous code had it as a list. I will use the list from previous context.
        advanced_concepts = ['tco', 'jit', 'erp', 'mrp', 'kanban', 'six sigma', 'kaizen', 'payable', 'contract', 'negotiation']
        advanced_found = sum(1 for concept in advanced_concepts if concept in text)
        advanced_score = min(30, advanced_found * 3)
        score += advanced_score
        
        # 3. Premium Skills (Max 20)
        premium_score = min(20, len(premium_skills) * 5)
        score += premium_score
        
        # 4. Keyword Density (Procurement/Sourcing/Vendor) (Max 10)
        role_keywords = [
            'sourcing', 'source', 'rfq', 'rfp', 'rfi', 'negotiation', 'supplier', 'bid',
            'procurement', 'purchase', 'buying', 'order', 'po', 'requisition', 'procure',
            'vendor', 'supplier', 'relationship', 'srm', 'performance', 'evaluation', 'onboarding'
        ]
        
        density_count = sum(1 for word in role_keywords if word in text)
        # Simple cap: 10+ matching keywords gives full points
        density_score = min(10, density_count)
        score += density_score
        
        # 5. Stability Check (Max 10)
        stability_score = 0
        if experience_years > 2:
            import re
            date_pattern = r'(\w+\s+\d{4})\s*[-–—to]+\s*(\w+\s+\d{4}|present|current)'
            matches = re.findall(date_pattern, text)
            num_roles = len(matches)
            
            if num_roles > 0:
                avg_tenure = experience_years / num_roles
                if avg_tenure >= 2.0:
                    stability_score = 10
        elif experience_years == 0:
             stability_score = 0
             if len(text.split()) > 100: # Heuristic: if valid resume text but extraction failed, assume neutral/stable
                 stability_score = 5 
        else:
             # For < 2 years experience, default to full points (entry level)
             stability_score = 10
             
        score += stability_score
        
        return {
            'total_score': min(100, round(score)),
            'breakdown': {
                'Base Skills': base_score,
                'Advanced Concepts': advanced_score,
                'Premium Skills': premium_score,
                'Density (Role Keywords)': density_score,
                'Stability (>2yr Avg)': stability_score
            }
        }
    
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
