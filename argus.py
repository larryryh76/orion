#!/usr/bin/env python3
"""
Argus - Semantic Comprehension Module
Universal content parsing and contextual understanding
"""

import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

class Argus:
    """The Digital Eye - Semantic comprehension of web content"""
    
    def __init__(self, driver=None):
        self.driver = driver
        self.semantic_model = {}
        self.action_priorities = {}
        self.load_semantic_patterns()
        
    def load_semantic_patterns(self):
        """Load semantic understanding patterns"""
        
        # Element classification patterns
        self.element_patterns = {
            'form_fields': {
                'email': ['email', 'e-mail', 'mail', 'login', 'username'],
                'password': ['password', 'pass', 'pwd', 'secret'],
                'name': ['name', 'first', 'last', 'full'],
                'age': ['age', 'birth', 'born', 'old'],
                'gender': ['gender', 'sex', 'male', 'female'],
                'location': ['location', 'city', 'state', 'country', 'zip', 'postal'],
                'income': ['income', 'salary', 'earn', 'money', 'wage'],
                'phone': ['phone', 'mobile', 'cell', 'number', 'tel']
            },
            'action_elements': {
                'submit': ['submit', 'send', 'continue', 'next', 'proceed', 'go'],
                'navigation': ['back', 'previous', 'home', 'menu', 'dashboard'],
                'completion': ['finish', 'complete', 'done', 'end', 'final'],
                'reward': ['redeem', 'claim', 'withdraw', 'cash', 'points', 'reward']
            },
            'question_types': {
                'multiple_choice': ['radio', 'checkbox', 'select', 'option'],
                'text_input': ['text', 'textarea', 'input'],
                'rating': ['scale', 'rating', 'stars', 'score', '1-10'],
                'boolean': ['yes/no', 'true/false', 'agree/disagree']
            }
        }
        
        # Context understanding patterns
        self.context_patterns = {
            'survey_indicators': [
                'survey', 'questionnaire', 'opinion', 'feedback', 'research',
                'study', 'poll', 'interview', 'evaluation'
            ],
            'completion_indicators': [
                'congratulations', 'thank you', 'completed', 'finished',
                'success', 'done', 'submitted', 'received'
            ],
            'error_indicators': [
                'error', 'invalid', 'required', 'missing', 'incorrect',
                'failed', 'problem', 'issue', 'try again'
            ],
            'reward_indicators': [
                'points', 'cash', 'reward', 'earned', 'credited',
                'balance', 'payout', 'redeem', 'withdraw'
            ]
        }
        
        # Action priority mapping
        self.action_priorities = {
            'critical': ['submit', 'continue', 'next', 'proceed'],
            'important': ['save', 'update', 'confirm', 'verify'],
            'optional': ['skip', 'later', 'maybe', 'cancel'],
            'dangerous': ['delete', 'remove', 'clear', 'reset']
        }
        
    def parse_page_semantics(self, url=None):
        """Parse page and create semantic model"""
        
        if not self.driver:
            return {'error': 'No driver available'}
            
        try:
            if url:
                self.driver.get(url)
                time.sleep(2)
                
            # Get page source
            page_source = self.driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Create semantic model
            semantic_model = {
                'url': self.driver.current_url,
                'title': self.driver.title,
                'page_type': self._classify_page_type(soup),
                'forms': self._parse_forms(),
                'actions': self._map_actions(),
                'content_context': self._analyze_content_context(soup),
                'navigation_elements': self._find_navigation_elements(),
                'completion_status': self._check_completion_status(soup)
            }
            
            self.semantic_model = semantic_model
            return semantic_model
            
        except Exception as e:
            return {'error': str(e)}
            
    def _classify_page_type(self, soup):
        """Classify the type of page"""
        
        page_text = soup.get_text().lower()
        
        # Check for survey indicators
        survey_score = sum(1 for indicator in self.context_patterns['survey_indicators'] 
                          if indicator in page_text)
        
        # Check for completion indicators
        completion_score = sum(1 for indicator in self.context_patterns['completion_indicators'] 
                              if indicator in page_text)
        
        # Check for error indicators
        error_score = sum(1 for indicator in self.context_patterns['error_indicators'] 
                         if indicator in page_text)
        
        if error_score > 2:
            return 'error_page'
        elif completion_score > 1:
            return 'completion_page'
        elif survey_score > 2:
            return 'survey_page'
        elif 'login' in page_text or 'sign in' in page_text:
            return 'login_page'
        elif 'dashboard' in page_text or 'account' in page_text:
            return 'dashboard_page'
        else:
            return 'unknown_page'
            
    def _parse_forms(self):
        """Parse all forms on the page"""
        
        forms = []
        
        try:
            form_elements = self.driver.find_elements(By.TAG_NAME, 'form')
            
            for form in form_elements:
                form_data = {
                    'fields': [],
                    'submit_buttons': [],
                    'form_purpose': 'unknown'
                }
                
                # Find input fields
                inputs = form.find_elements(By.TAG_NAME, 'input')
                selects = form.find_elements(By.TAG_NAME, 'select')
                textareas = form.find_elements(By.TAG_NAME, 'textarea')
                
                # Classify input fields
                for input_elem in inputs:
                    field_info = self._classify_input_field(input_elem)
                    if field_info:
                        form_data['fields'].append(field_info)
                        
                # Classify select fields
                for select_elem in selects:
                    field_info = self._classify_select_field(select_elem)
                    if field_info:
                        form_data['fields'].append(field_info)
                        
                # Classify textarea fields
                for textarea_elem in textareas:
                    field_info = self._classify_textarea_field(textarea_elem)
                    if field_info:
                        form_data['fields'].append(field_info)
                        
                # Find submit buttons
                submit_buttons = form.find_elements(By.XPATH, ".//input[@type='submit'] | .//button[@type='submit'] | .//button")
                for button in submit_buttons:
                    button_text = button.get_attribute('value') or button.text or ''
                    form_data['submit_buttons'].append({
                        'element': button,
                        'text': button_text.lower(),
                        'purpose': self._classify_button_purpose(button_text)
                    })
                    
                # Determine form purpose
                form_data['form_purpose'] = self._determine_form_purpose(form_data['fields'])
                forms.append(form_data)
                
        except Exception as e:
            pass
            
        return forms
        
    def _classify_input_field(self, input_elem):
        """Classify input field type and purpose"""
        
        try:
            input_type = input_elem.get_attribute('type') or 'text'
            name = input_elem.get_attribute('name') or ''
            placeholder = input_elem.get_attribute('placeholder') or ''
            id_attr = input_elem.get_attribute('id') or ''
            
            # Combine all text for analysis
            field_text = (name + ' ' + placeholder + ' ' + id_attr).lower()
            
            # Skip hidden fields
            if input_type == 'hidden':
                return None
                
            # Classify field purpose
            field_purpose = 'unknown'
            for purpose, keywords in self.element_patterns['form_fields'].items():
                if any(keyword in field_text for keyword in keywords):
                    field_purpose = purpose
                    break
                    
            return {
                'element': input_elem,
                'type': input_type,
                'purpose': field_purpose,
                'name': name,
                'placeholder': placeholder,
                'required': input_elem.get_attribute('required') is not None
            }
            
        except Exception:
            return None
            
    def _classify_select_field(self, select_elem):
        """Classify select field"""
        
        try:
            name = select_elem.get_attribute('name') or ''
            id_attr = select_elem.get_attribute('id') or ''
            
            field_text = (name + ' ' + id_attr).lower()
            
            # Get options
            select_obj = Select(select_elem)
            options = [option.text for option in select_obj.options]
            
            # Classify purpose
            field_purpose = 'unknown'
            for purpose, keywords in self.element_patterns['form_fields'].items():
                if any(keyword in field_text for keyword in keywords):
                    field_purpose = purpose
                    break
                    
            return {
                'element': select_elem,
                'type': 'select',
                'purpose': field_purpose,
                'name': name,
                'options': options[:10],  # Limit options for performance
                'required': select_elem.get_attribute('required') is not None
            }
            
        except Exception:
            return None
            
    def _classify_textarea_field(self, textarea_elem):
        """Classify textarea field"""
        
        try:
            name = textarea_elem.get_attribute('name') or ''
            placeholder = textarea_elem.get_attribute('placeholder') or ''
            id_attr = textarea_elem.get_attribute('id') or ''
            
            field_text = (name + ' ' + placeholder + ' ' + id_attr).lower()
            
            return {
                'element': textarea_elem,
                'type': 'textarea',
                'purpose': 'text_response',
                'name': name,
                'placeholder': placeholder,
                'required': textarea_elem.get_attribute('required') is not None
            }
            
        except Exception:
            return None
            
    def _classify_button_purpose(self, button_text):
        """Classify button purpose"""
        
        button_text = button_text.lower()
        
        for priority, keywords in self.action_priorities.items():
            if any(keyword in button_text for keyword in keywords):
                return priority
                
        return 'unknown'
        
    def _determine_form_purpose(self, fields):
        """Determine overall form purpose"""
        
        field_purposes = [field['purpose'] for field in fields]
        
        if 'email' in field_purposes and 'password' in field_purposes:
            return 'login_form'
        elif len([p for p in field_purposes if p in ['name', 'email', 'age', 'gender']]) >= 2:
            return 'registration_form'
        elif len(field_purposes) > 5:
            return 'survey_form'
        else:
            return 'unknown_form'
            
    def _map_actions(self):
        """Map and prioritize page actions"""
        
        actions = []
        
        try:
            # Find all clickable elements
            clickable_elements = self.driver.find_elements(By.XPATH, "//button | //input[@type='submit'] | //a[contains(@class, 'btn') or contains(@class, 'button')]")
            
            for element in clickable_elements:
                element_text = element.text or element.get_attribute('value') or ''
                element_text = element_text.lower().strip()
                
                if element_text:
                    action_info = {
                        'element': element,
                        'text': element_text,
                        'priority': self._get_action_priority(element_text),
                        'purpose': self._classify_action_purpose(element_text)
                    }
                    actions.append(action_info)
                    
            # Sort by priority
            priority_order = {'critical': 0, 'important': 1, 'optional': 2, 'dangerous': 3, 'unknown': 4}
            actions.sort(key=lambda x: priority_order.get(x['priority'], 4))
            
        except Exception:
            pass
            
        return actions
        
    def _get_action_priority(self, text):
        """Get action priority level"""
        
        for priority, keywords in self.action_priorities.items():
            if any(keyword in text for keyword in keywords):
                return priority
                
        return 'unknown'
        
    def _classify_action_purpose(self, text):
        """Classify action purpose"""
        
        for purpose, keywords in self.element_patterns['action_elements'].items():
            if any(keyword in text for keyword in keywords):
                return purpose
                
        return 'unknown'
        
    def _analyze_content_context(self, soup):
        """Analyze page content context"""
        
        page_text = soup.get_text().lower()
        
        context = {
            'is_survey': any(indicator in page_text for indicator in self.context_patterns['survey_indicators']),
            'is_completed': any(indicator in page_text for indicator in self.context_patterns['completion_indicators']),
            'has_errors': any(indicator in page_text for indicator in self.context_patterns['error_indicators']),
            'has_rewards': any(indicator in page_text for indicator in self.context_patterns['reward_indicators']),
            'question_count': len(re.findall(r'\?', page_text)),
            'word_count': len(page_text.split())
        }
        
        return context
        
    def _find_navigation_elements(self):
        """Find navigation elements"""
        
        nav_elements = []
        
        try:
            # Common navigation selectors
            nav_selectors = [
                "//nav//a", "//div[contains(@class, 'nav')]//a",
                "//ul[contains(@class, 'menu')]//a", "//a[contains(@class, 'nav')]"
            ]
            
            for selector in nav_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                for elem in elements[:5]:  # Limit for performance
                    text = elem.text.strip()
                    if text:
                        nav_elements.append({
                            'element': elem,
                            'text': text,
                            'href': elem.get_attribute('href')
                        })
                        
        except Exception:
            pass
            
        return nav_elements
        
    def _check_completion_status(self, soup):
        """Check if page indicates completion"""
        
        page_text = soup.get_text().lower()
        
        completion_indicators = self.context_patterns['completion_indicators']
        completion_score = sum(1 for indicator in completion_indicators if indicator in page_text)
        
        return {
            'is_complete': completion_score > 1,
            'completion_score': completion_score,
            'completion_phrases': [phrase for phrase in completion_indicators if phrase in page_text]
        }
        
    def get_next_action(self):
        """Get the next recommended action"""
        
        if not self.semantic_model or 'actions' not in self.semantic_model:
            return None
            
        actions = self.semantic_model['actions']
        
        # Return highest priority action
        if actions:
            return actions[0]
            
        return None
        
    def find_form_field(self, field_purpose):
        """Find form field by purpose"""
        
        if not self.semantic_model or 'forms' not in self.semantic_model:
            return None
            
        for form in self.semantic_model['forms']:
            for field in form['fields']:
                if field['purpose'] == field_purpose:
                    return field
                    
        return None

def test_argus():
    """Test Argus semantic comprehension"""
    
    print("TESTING ARGUS MODULE")
    print("=" * 40)
    
    # Test without driver (pattern matching only)
    argus = Argus()
    
    print(f"Element patterns loaded: {len(argus.element_patterns)}")
    print(f"Context patterns loaded: {len(argus.context_patterns)}")
    print(f"Action priorities loaded: {len(argus.action_priorities)}")
    
    # Test field classification
    test_field_text = "email address input"
    field_purpose = 'unknown'
    for purpose, keywords in argus.element_patterns['form_fields'].items():
        if any(keyword in test_field_text for keyword in keywords):
            field_purpose = purpose
            break
            
    print(f"Field classification test: '{test_field_text}' -> {field_purpose}")
    
    # Test action priority
    test_action = "continue to next page"
    action_priority = argus._get_action_priority(test_action)
    print(f"Action priority test: '{test_action}' -> {action_priority}")
    
    print(f"\nArgus module: OPERATIONAL")
    return True

if __name__ == "__main__":
    test_argus()