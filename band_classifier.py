class BandClassifier:
    """
    Classify candidates into appropriate bands based on experience
    """
    
    def __init__(self):
        self.band_mapping = {
            '5A': {
                'designation': 'Analyst',
                'min_exp': 0,
                'max_exp': 1,
                'description': 'Entry-level procurement analyst'
            },
            '5B': {
                'designation': 'Senior Analyst',
                'min_exp': 2,
                'max_exp': 3,
                'description': 'Senior procurement analyst with moderate experience'
            },
            '4A': {
                'designation': 'Management Trainee',
                'min_exp': 4,
                'max_exp': 7,
                'description': 'Management trainee with significant experience'
            },
            '4B': {
                'designation': 'Assistant Manager',
                'min_exp': 8,
                'max_exp': 11,
                'description': 'Assistant manager with extensive experience'
            },
            '4C': {
                'designation': 'Manager',
                'min_exp': 12,
                'max_exp': 100,  # No upper limit
                'description': 'Manager with 12+ years of experience'
            }
        }
    
    def classify(self, years_of_experience):
        """
        Classify candidate into appropriate band based on experience
        
        Args:
            years_of_experience (float): Years of experience
            
        Returns:
            dict: Band classification information
        """
        for band, info in self.band_mapping.items():
            if info['min_exp'] <= years_of_experience <= info['max_exp']:
                return {
                    'band': band,
                    'designation': info['designation'],
                    'description': info['description'],
                    'experience_range': f"{info['min_exp']}-{info['max_exp'] if info['max_exp'] < 100 else '+'} years"
                }
        
        # Fallback to 5A if experience is 0 or negative
        if years_of_experience < 0:
            years_of_experience = 0
        
        return {
            'band': '5A',
            'designation': 'Analyst',
            'description': 'Entry-level procurement analyst',
            'experience_range': '0-1 years'
        }
    
    def get_all_bands(self):
        """
        Get information about all bands
        
        Returns:
            dict: All band information
        """
        return self.band_mapping
    
    def get_band_requirements(self, band):
        """
        Get requirements for a specific band
        
        Args:
            band (str): Band code (e.g., '5A', '5B')
            
        Returns:
            dict: Band requirements
        """
        return self.band_mapping.get(band, {})
