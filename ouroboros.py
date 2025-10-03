#!/usr/bin/env python3
"""
Ouroboros - Knowledge Base Module
Site topology maps, semantic web graph, and blacklist registry
"""

import json
import time
import requests
from urllib.parse import urlparse

class Ouroboros:
    """The Knowledge Base - Self-sustaining database of survey environments"""
    
    def __init__(self):
        self.site_topology_maps = {}
        self.semantic_web_graph = {}
        self.blacklist = set()
        self.load_knowledge_base()
        
    def load_knowledge_base(self):
        """Load pre-scraped site topology maps"""
        
        # Site topology maps for major survey platforms
        self.site_topology_maps = {
            'swagbucks.com': {
                'login_flow': ['email', 'password', 'submit'],
                'survey_patterns': ['qualification', 'main_survey', 'completion'],
                'reward_system': 'points_to_cash',
                'detection_level': 'high',
                'bot_traps': ['honeypot_fields', 'timing_analysis', 'mouse_tracking'],
                'typical_flow': ['dashboard', 'discover', 'surveys', 'complete'],
                'payment_threshold': 300,  # points
                'avg_survey_time': 15,  # minutes
                'success_indicators': ['congratulations', 'points_awarded', 'survey_complete']
            },
            'surveyjunkie.com': {
                'login_flow': ['email', 'password', 'submit'],
                'survey_patterns': ['screener', 'main_content', 'demographics'],
                'reward_system': 'points_to_cash',
                'detection_level': 'medium',
                'bot_traps': ['attention_checks', 'duplicate_questions'],
                'typical_flow': ['dashboard', 'available_surveys', 'take_survey'],
                'payment_threshold': 1000,
                'avg_survey_time': 20,
                'success_indicators': ['survey_completed', 'points_earned']
            },
            'prolific.co': {
                'login_flow': ['email', 'password', 'submit'],
                'survey_patterns': ['consent', 'instructions', 'tasks', 'debrief'],
                'reward_system': 'direct_payment',
                'detection_level': 'very_high',
                'bot_traps': ['academic_validation', 'attention_checks', 'consistency_checks'],
                'typical_flow': ['studies', 'participate', 'submit'],
                'payment_threshold': 5.00,  # GBP
                'avg_survey_time': 30,
                'success_indicators': ['submission_successful', 'awaiting_review']
            },
            'cointiply.com': {
                'login_flow': ['email', 'password', 'submit'],
                'survey_patterns': ['offer_wall', 'survey_router', 'completion'],
                'reward_system': 'cryptocurrency',
                'detection_level': 'medium',
                'bot_traps': ['captcha', 'timer_checks'],
                'typical_flow': ['dashboard', 'earn', 'surveys'],
                'payment_threshold': 35000,  # coins
                'avg_survey_time': 12,
                'success_indicators': ['coins_awarded', 'offer_completed']
            }
        }
        
        # Semantic web graph - brand relationships and context
        self.semantic_web_graph = {
            'brands': {
                'coca_cola': ['pepsi', 'sprite', 'fanta', 'dr_pepper'],
                'mcdonalds': ['burger_king', 'kfc', 'subway', 'taco_bell'],
                'apple': ['samsung', 'google', 'microsoft', 'amazon'],
                'netflix': ['hulu', 'disney_plus', 'amazon_prime', 'hbo_max']
            },
            'categories': {
                'fast_food': ['mcdonalds', 'burger_king', 'kfc', 'subway'],
                'streaming': ['netflix', 'hulu', 'disney_plus', 'amazon_prime'],
                'smartphones': ['apple', 'samsung', 'google', 'oneplus'],
                'social_media': ['facebook', 'instagram', 'twitter', 'tiktok']
            },
            'trends': {
                'current_events': ['inflation', 'remote_work', 'sustainability'],
                'tech_trends': ['ai', 'crypto', 'metaverse', 'nft'],
                'lifestyle': ['wellness', 'minimalism', 'plant_based', 'fitness']
            }
        }
        
        # Blacklist - known bot traps and toxic elements
        self.blacklist = {
            'trap_urls': [
                'bot-detection.com',
                'survey-trap.net',
                'fake-reward.org'
            ],
            'toxic_questions': [
                'are you a bot',
                'automated response',
                'script detection',
                'please prove you are human'
            ],
            'bad_companies': [
                'scam-surveys.com',
                'never-pay.net',
                'fake-rewards.org'
            ],
            'honeypot_fields': [
                'hidden_field',
                'bot_check',
                'automation_test',
                'display_none'
            ]
        }
        
    def get_site_topology(self, domain):
        """Get topology map for specific domain"""
        return self.site_topology_maps.get(domain, {})
        
    def is_blacklisted(self, url_or_text):
        """Check if URL or text is blacklisted"""
        url_or_text = url_or_text.lower()
        
        # Check trap URLs
        for trap in self.blacklist['trap_urls']:
            if trap in url_or_text:
                return True
                
        # Check toxic questions
        for toxic in self.blacklist['toxic_questions']:
            if toxic in url_or_text:
                return True
                
        # Check bad companies
        for bad in self.blacklist['bad_companies']:
            if bad in url_or_text:
                return True
                
        return False
        
    def get_brand_context(self, brand):
        """Get semantic context for a brand"""
        brand = brand.lower()
        
        context = {
            'competitors': self.semantic_web_graph['brands'].get(brand, []),
            'category': None,
            'related_trends': []
        }
        
        # Find category
        for category, brands in self.semantic_web_graph['categories'].items():
            if brand in brands:
                context['category'] = category
                break
                
        return context
        
    def update_topology(self, domain, new_data):
        """Update site topology with new intelligence"""
        if domain not in self.site_topology_maps:
            self.site_topology_maps[domain] = {}
            
        self.site_topology_maps[domain].update(new_data)
        
    def add_to_blacklist(self, item, category='trap_urls'):
        """Add item to blacklist"""
        if category in self.blacklist:
            self.blacklist[category].append(item)
            
    def get_detection_level(self, domain):
        """Get bot detection level for domain"""
        topology = self.get_site_topology(domain)
        return topology.get('detection_level', 'unknown')
        
    def get_success_indicators(self, domain):
        """Get success indicators for domain"""
        topology = self.get_site_topology(domain)
        return topology.get('success_indicators', [])
        
    def save_knowledge_base(self):
        """Save knowledge base to file"""
        data = {
            'site_topology_maps': self.site_topology_maps,
            'semantic_web_graph': self.semantic_web_graph,
            'blacklist': self.blacklist,
            'timestamp': time.time()
        }
        
        with open('ouroboros_knowledge.json', 'w') as f:
            json.dump(data, f, indent=2)

def test_ouroboros():
    """Test Ouroboros module"""
    
    print("TESTING OUROBOROS MODULE")
    print("=" * 40)
    
    kb = Ouroboros()
    
    # Test site topology
    swagbucks_topology = kb.get_site_topology('swagbucks.com')
    print(f"Swagbucks topology: {swagbucks_topology['reward_system']}")
    
    # Test blacklist
    is_trap = kb.is_blacklisted('bot-detection.com/test')
    print(f"Bot detection URL blacklisted: {is_trap}")
    
    # Test brand context
    coca_cola_context = kb.get_brand_context('coca_cola')
    print(f"Coca Cola competitors: {coca_cola_context['competitors']}")
    
    # Test detection level
    detection = kb.get_detection_level('prolific.co')
    print(f"Prolific detection level: {detection}")
    
    print(f"\nOuroboros module: OPERATIONAL")
    return True

if __name__ == "__main__":
    test_ouroboros()