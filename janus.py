#!/usr/bin/env python3
"""
Janus - Persona Engine Module
Generates complete, internally consistent digital personas
"""

import json
import time
import random
import hashlib
from typing import Dict, Any

class Janus:
    """The Persona Engine - Living, evolving digital identities"""
    
    def __init__(self):
        self.active_personas = {}
        self.persona_templates = {}
        self.load_persona_templates()
        
    def load_persona_templates(self):
        """Load persona generation templates"""
        
        self.persona_templates = {
            'demographics': {
                'ages': list(range(18, 65)),
                'locations': [
                    'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX',
                    'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA',
                    'Dallas, TX', 'San Jose, CA', 'Austin, TX', 'Jacksonville, FL',
                    'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC', 'San Francisco, CA',
                    'Indianapolis, IN', 'Seattle, WA', 'Denver, CO', 'Washington, DC'
                ],
                'incomes': [
                    '25000-35000', '35000-50000', '50000-75000', '75000-100000',
                    '100000-150000', '150000-200000', '200000+'
                ],
                'education': [
                    'High School', 'Some College', 'Bachelor\'s Degree', 
                    'Master\'s Degree', 'Professional Degree', 'Doctorate'
                ],
                'employment': [
                    'Full-time', 'Part-time', 'Self-employed', 'Student', 
                    'Retired', 'Unemployed', 'Homemaker'
                ],
                'family_status': [
                    'Single', 'Married', 'Divorced', 'Widowed', 
                    'In a relationship', 'It\'s complicated'
                ]
            },
            'behavioral': {
                'typing_speeds': (0.08, 0.35),  # seconds per character
                'mouse_variance': (2, 15),  # pixels
                'cognitive_fatigue': (0.7, 1.3),  # multiplier over time
                'common_typos': {
                    'the': ['teh', 'hte'],
                    'and': ['adn', 'nad'],
                    'you': ['yuo', 'oyu'],
                    'that': ['taht', 'htat'],
                    'with': ['wiht', 'whit']
                },
                'browser_patterns': [
                    'chrome_windows', 'firefox_windows', 'safari_mac',
                    'edge_windows', 'chrome_mac', 'firefox_mac'
                ]
            },
            'truth_matrix_topics': {
                'political': ['liberal', 'conservative', 'moderate', 'independent'],
                'shopping_habits': ['online_preferred', 'in_store_preferred', 'mixed'],
                'tech_adoption': ['early_adopter', 'mainstream', 'late_adopter'],
                'brand_loyalty': ['high', 'medium', 'low'],
                'privacy_concern': ['high', 'medium', 'low'],
                'environmental_concern': ['high', 'medium', 'low'],
                'health_consciousness': ['very_conscious', 'somewhat_conscious', 'not_conscious'],
                'social_media_usage': ['heavy', 'moderate', 'light', 'none'],
                'financial_risk': ['conservative', 'moderate', 'aggressive'],
                'travel_frequency': ['frequent', 'occasional', 'rare', 'never']
            }
        }
        
    def generate_persona(self, persona_id=None):
        """Generate complete, internally consistent persona"""
        
        if not persona_id:
            persona_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
            
        # Generate demographic profile
        demographics = self._generate_demographics()
        
        # Generate behavioral profile
        behavioral = self._generate_behavioral_profile()
        
        # Generate truth matrix
        truth_matrix = self._generate_truth_matrix()
        
        # Create persona
        persona = {
            'id': persona_id,
            'created_at': time.time(),
            'demographics': demographics,
            'behavioral': behavioral,
            'truth_matrix': truth_matrix,
            'consistency_score': 1.0,
            'usage_count': 0,
            'last_used': None
        }
        
        # Ensure internal consistency
        persona = self._ensure_consistency(persona)
        
        # Store active persona
        self.active_personas[persona_id] = persona
        
        return persona
        
    def _generate_demographics(self):
        """Generate demographic profile"""
        
        age = random.choice(self.persona_templates['demographics']['ages'])
        location = random.choice(self.persona_templates['demographics']['locations'])
        
        # Income correlates with age and education
        if age < 25:
            income_options = self.persona_templates['demographics']['incomes'][:3]
        elif age < 35:
            income_options = self.persona_templates['demographics']['incomes'][:5]
        else:
            income_options = self.persona_templates['demographics']['incomes']
            
        income = random.choice(income_options)
        
        # Education correlates with income
        if '200000+' in income or '150000-200000' in income:
            education_options = ['Master\'s Degree', 'Professional Degree', 'Doctorate']
        elif '75000-' in income:
            education_options = ['Bachelor\'s Degree', 'Master\'s Degree']
        else:
            education_options = ['High School', 'Some College', 'Bachelor\'s Degree']
            
        education = random.choice(education_options)
        
        return {
            'age': age,
            'location': location,
            'income': income,
            'education': education,
            'employment': random.choice(self.persona_templates['demographics']['employment']),
            'family_status': random.choice(self.persona_templates['demographics']['family_status']),
            'gender': random.choice(['Male', 'Female', 'Non-binary'])
        }
        
    def _generate_behavioral_profile(self):
        """Generate behavioral patterns"""
        
        typing_speed = random.uniform(*self.persona_templates['behavioral']['typing_speeds'])
        mouse_variance = random.uniform(*self.persona_templates['behavioral']['mouse_variance'])
        cognitive_fatigue = random.uniform(*self.persona_templates['behavioral']['cognitive_fatigue'])
        
        # Generate personal typo patterns
        personal_typos = {}
        for word, typos in self.persona_templates['behavioral']['common_typos'].items():
            if random.random() < 0.3:  # 30% chance of having this typo pattern
                personal_typos[word] = random.choice(typos)
                
        return {
            'typing_speed': typing_speed,
            'mouse_variance': mouse_variance,
            'cognitive_fatigue_curve': cognitive_fatigue,
            'personal_typos': personal_typos,
            'browser_pattern': random.choice(self.persona_templates['behavioral']['browser_patterns']),
            'session_duration_preference': random.randint(10, 45),  # minutes
            'break_frequency': random.randint(3, 8)  # surveys before break
        }
        
    def _generate_truth_matrix(self):
        """Generate consistent belief system"""
        
        truth_matrix = {}
        
        for topic, options in self.persona_templates['truth_matrix_topics'].items():
            truth_matrix[topic] = random.choice(options)
            
        # Ensure logical consistency
        truth_matrix = self._apply_consistency_rules(truth_matrix)
        
        return truth_matrix
        
    def _apply_consistency_rules(self, truth_matrix):
        """Apply logical consistency rules to truth matrix"""
        
        # High privacy concern correlates with low social media usage
        if truth_matrix['privacy_concern'] == 'high':
            if random.random() < 0.7:
                truth_matrix['social_media_usage'] = random.choice(['light', 'none'])
                
        # Early tech adopters tend to shop online
        if truth_matrix['tech_adoption'] == 'early_adopter':
            if random.random() < 0.8:
                truth_matrix['shopping_habits'] = 'online_preferred'
                
        # Environmental concern correlates with health consciousness
        if truth_matrix['environmental_concern'] == 'high':
            if random.random() < 0.6:
                truth_matrix['health_consciousness'] = random.choice(['very_conscious', 'somewhat_conscious'])
                
        return truth_matrix
        
    def _ensure_consistency(self, persona):
        """Ensure overall persona consistency"""
        
        # Age-based adjustments
        age = persona['demographics']['age']
        
        if age < 30:
            # Younger people tend to be more tech-savvy
            if random.random() < 0.6:
                persona['truth_matrix']['tech_adoption'] = random.choice(['early_adopter', 'mainstream'])
                persona['truth_matrix']['social_media_usage'] = random.choice(['heavy', 'moderate'])
                
        elif age > 50:
            # Older people tend to be more conservative with tech
            if random.random() < 0.5:
                persona['truth_matrix']['tech_adoption'] = random.choice(['late_adopter', 'mainstream'])
                persona['behavioral']['typing_speed'] *= 1.3  # Slower typing
                
        return persona
        
    def get_persona_response(self, persona_id, question_context):
        """Get consistent response based on persona's truth matrix"""
        
        if persona_id not in self.active_personas:
            return None
            
        persona = self.active_personas[persona_id]
        truth_matrix = persona['truth_matrix']
        
        # Analyze question context and return appropriate response
        question_lower = question_context.lower()
        
        # Political questions
        if any(word in question_lower for word in ['political', 'vote', 'government', 'policy']):
            return self._get_political_response(truth_matrix['political'])
            
        # Shopping questions
        elif any(word in question_lower for word in ['shop', 'buy', 'purchase', 'store']):
            return self._get_shopping_response(truth_matrix['shopping_habits'])
            
        # Technology questions
        elif any(word in question_lower for word in ['technology', 'tech', 'digital', 'app']):
            return self._get_tech_response(truth_matrix['tech_adoption'])
            
        # Default response based on personality
        else:
            return self._get_default_response(truth_matrix)
            
    def _get_political_response(self, political_lean):
        """Get political response based on lean"""
        responses = {
            'liberal': ['Strongly agree', 'Somewhat agree'],
            'conservative': ['Strongly disagree', 'Somewhat disagree'],
            'moderate': ['Neutral', 'Somewhat agree', 'Somewhat disagree'],
            'independent': ['Neutral', 'It depends']
        }
        return random.choice(responses.get(political_lean, ['Neutral']))
        
    def _get_shopping_response(self, shopping_habit):
        """Get shopping response based on habits"""
        responses = {
            'online_preferred': ['Online shopping', 'Mostly online', 'Digital purchases'],
            'in_store_preferred': ['In-store shopping', 'Physical stores', 'Traditional shopping'],
            'mixed': ['Both online and in-store', 'Depends on the item', 'Mixed approach']
        }
        return random.choice(responses.get(shopping_habit, ['Mixed approach']))
        
    def _get_tech_response(self, tech_adoption):
        """Get technology response based on adoption level"""
        responses = {
            'early_adopter': ['Very interested', 'Always try new tech', 'Love innovation'],
            'mainstream': ['Somewhat interested', 'Wait for reviews', 'Cautiously optimistic'],
            'late_adopter': ['Not very interested', 'Prefer proven technology', 'Skeptical of new tech']
        }
        return random.choice(responses.get(tech_adoption, ['Somewhat interested']))
        
    def _get_default_response(self, truth_matrix):
        """Get default response based on overall personality"""
        # Use multiple factors to determine response style
        if truth_matrix['brand_loyalty'] == 'high':
            return random.choice(['Strongly agree', 'Yes, definitely'])
        elif truth_matrix['privacy_concern'] == 'high':
            return random.choice(['Prefer not to say', 'Not comfortable sharing'])
        else:
            return random.choice(['Agree', 'Yes', 'Somewhat agree', 'Maybe'])
            
    def update_persona_usage(self, persona_id):
        """Update persona usage statistics"""
        if persona_id in self.active_personas:
            self.active_personas[persona_id]['usage_count'] += 1
            self.active_personas[persona_id]['last_used'] = time.time()
            
    def get_persona_stats(self, persona_id):
        """Get persona statistics"""
        if persona_id in self.active_personas:
            return {
                'usage_count': self.active_personas[persona_id]['usage_count'],
                'consistency_score': self.active_personas[persona_id]['consistency_score'],
                'age': self.active_personas[persona_id]['demographics']['age'],
                'created_days_ago': (time.time() - self.active_personas[persona_id]['created_at']) / 86400
            }
        return None

def test_janus():
    """Test Janus persona engine"""
    
    print("TESTING JANUS MODULE")
    print("=" * 40)
    
    janus = Janus()
    
    # Generate test persona
    persona = janus.generate_persona()
    
    print(f"Generated persona ID: {persona['id']}")
    print(f"Age: {persona['demographics']['age']}")
    print(f"Location: {persona['demographics']['location']}")
    print(f"Income: {persona['demographics']['income']}")
    print(f"Political lean: {persona['truth_matrix']['political']}")
    print(f"Tech adoption: {persona['truth_matrix']['tech_adoption']}")
    print(f"Typing speed: {persona['behavioral']['typing_speed']:.3f}s/char")
    
    # Test response generation
    political_response = janus.get_persona_response(persona['id'], "What is your political opinion?")
    shopping_response = janus.get_persona_response(persona['id'], "How do you prefer to shop?")
    
    print(f"Political response: {political_response}")
    print(f"Shopping response: {shopping_response}")
    
    print(f"\nJanus module: OPERATIONAL")
    return True

if __name__ == "__main__":
    test_janus()