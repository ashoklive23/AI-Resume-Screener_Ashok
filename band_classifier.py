class BandClassifier:
    """
    Classify candidates into appropriate bands based on experience
    """
    
    def __init__(self):
        # Define upper limits for each band (exclusive)
        # 5A: 0 to < 2 years
        # 5B: 2 to < 4 years
        # 4A: 4 to < 8 years
        # 4B: 8 to < 12 years
        # 4C: 12+ years
        self.band_mapping = [
            {
                'band': '5A',
                'designation': 'Analyst',
                'min_exp': 0,
                'max_exp': 2,
                'description': 'Entry-level procurement analyst',
                'display_range': '0-2 years'
            },
            {
                'band': '5B',
                'designation': 'Senior Analyst',
                'min_exp': 2,
                'max_exp': 4,
                'description': 'Senior procurement analyst with moderate experience',
                'display_range': '2-4 years'
            },
            {
                'band': '4A',
                'designation': 'Management Trainee',
                'min_exp': 4,
                'max_exp': 8,
                'description': 'Management trainee with significant experience',
                'display_range': '4-8 years'
            },
            {
                'band': '4B',
                'designation': 'Assistant Manager',
                'min_exp': 8,
                'max_exp': 12,
                'description': 'Assistant manager with extensive experience',
                'display_range': '8-12 years'
            },
            {
                'band': '4C',
                'designation': 'Manager',
                'min_exp': 12,
                'max_exp': 100,
                'description': 'Manager with 12+ years of experience',
                'display_range': '12+ years'
            }
        ]
    
    def classify(self, years_of_experience):
        """
        Classify candidate into appropriate band based on experience
        
        Args:
            years_of_experience (float): Years of experience
            
        Returns:
            dict: Band classification information
        """
        # Handle invalid input
        if years_of_experience < 0:
            years_of_experience = 0
            
        # Check against bands
        for info in self.band_mapping:
            # For the last band (4C), we just check if it's >= min_exp
            if info['band'] == '4C':
                if years_of_experience >= info['min_exp']:
                    return self._format_result(info)
            # For other bands, check range [min, max)
            elif info['min_exp'] <= years_of_experience < info['max_exp']:
                return self._format_result(info)
        
        # Fallback (should ideally be covered by 4C or 5A, but just in case)
        return self._format_result(self.band_mapping[0])

    def _format_result(self, info):
        return {
            'band': info['band'],
            'designation': info['designation'],
            'description': info['description'],
            'experience_range': info['display_range']
        }
    
    def get_all_bands(self):
        """
        Get information about all bands
        
        Returns:
            dict: All band information (converted to dict for compatibility)
        """
        result = {}
        for item in self.band_mapping:
            result[item['band']] = {
                'designation': item['designation'],
                'min_exp': item['min_exp'],
                'max_exp': item['max_exp'],
                'description': item['description']
            }
        return result
    
    def get_band_requirements(self, band):
        """
        Get requirements for a specific band
        
        Args:
            band (str): Band code (e.g., '5A', '5B')
            
        Returns:
            dict: Band requirements
        """
        for item in self.band_mapping:
            if item['band'] == band:
                return {
                    'designation': item['designation'],
                    'min_exp': item['min_exp'],
                    'max_exp': item['max_exp'],
                    'description': item['description']
                }
        return {}
