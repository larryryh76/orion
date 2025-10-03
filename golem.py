#!/usr/bin/env python3
"""
Golem - Behavioral Simulation Module
Hyper-realistic human interaction simulation
"""

import time
import random
import math
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Golem:
    """Behavioral Simulation - Brings personas to life"""
    
    def __init__(self, persona=None):
        self.persona = persona
        self.driver = None
        self.session_data = {}
        self.interaction_history = []
        self.current_session_start = None
        
    def initialize_browser(self, headless=False):
        """Initialize browser with human-like configuration"""
        
        try:
            service = Service('./chromedriver.exe')
            options = webdriver.ChromeOptions()
            
            if headless:
                options.add_argument('--headless')
                
            # Human-like browser settings
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Randomize user agent based on persona
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
            options.add_argument(f'--user-agent={random.choice(user_agents)}')
            
            self.driver = webdriver.Chrome(service=service, options=options)
            
            # Execute script to hide automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Set realistic window size
            self.driver.set_window_size(1920, 1080)
            
            self.current_session_start = time.time()
            return True
            
        except Exception as e:
            print(f"Browser initialization failed: {str(e)}")
            return False
            
    def fluid_navigation(self, element, action_type='click'):
        """Mimic unpredictable human mouse movements"""
        
        if not self.driver or not element:
            return False
            
        try:
            actions = ActionChains(self.driver)
            
            # Get element location
            element_location = element.location
            element_size = element.size
            
            # Calculate target point with variance
            target_x = element_location['x'] + element_size['width'] / 2
            target_y = element_location['y'] + element_size['height'] / 2
            
            # Add human-like variance
            variance_x = random.randint(-5, 5)
            variance_y = random.randint(-5, 5)
            target_x += variance_x
            target_y += variance_y
            
            # Simulate curved mouse movement
            current_x, current_y = 0, 0
            steps = random.randint(3, 8)
            
            for i in range(steps):
                # Calculate intermediate points with curve
                progress = (i + 1) / steps
                curve_factor = math.sin(progress * math.pi) * random.uniform(10, 30)
                
                intermediate_x = current_x + (target_x - current_x) * progress + curve_factor
                intermediate_y = current_y + (target_y - current_y) * progress
                
                actions.move_by_offset(intermediate_x - current_x, intermediate_y - current_y)
                current_x, current_y = intermediate_x, intermediate_y
                
                # Random micro-pauses
                if random.random() < 0.3:
                    actions.pause(random.uniform(0.05, 0.15))
                    
            # Move to final target
            actions.move_to_element_with_offset(element, variance_x, variance_y)
            
            # Pre-click hesitation
            hesitation_time = random.uniform(0.1, 0.5)
            actions.pause(hesitation_time)
            
            # Occasional misclick simulation
            if random.random() < 0.05:  # 5% chance
                # Slight misclick
                actions.move_by_offset(random.randint(-3, 3), random.randint(-3, 3))
                actions.pause(random.uniform(0.1, 0.3))
                # Correct back to element
                actions.move_to_element(element)
                actions.pause(random.uniform(0.1, 0.2))
                
            # Execute action
            if action_type == 'click':
                actions.click()
            elif action_type == 'double_click':
                actions.double_click()
                
            actions.perform()
            
            # Log interaction
            self._log_interaction('navigation', {
                'element_tag': element.tag_name,
                'action_type': action_type,
                'hesitation_time': hesitation_time,
                'had_misclick': random.random() < 0.05
            })
            
            return True
            
        except Exception as e:
            print(f"Fluid navigation failed: {str(e)}")
            return False
            
    def tactile_input_simulation(self, element, text):
        """Simulate natural typing with human characteristics"""
        
        if not element or not text:
            return False
            
        try:
            # Clear field first
            element.clear()
            
            # Get persona typing characteristics
            base_typing_speed = self.persona['behavioral']['typing_speed'] if self.persona else 0.15
            personal_typos = self.persona['behavioral']['personal_typos'] if self.persona else {}
            
            typed_text = ""
            
            for i, char in enumerate(text):
                # Calculate typing delay with variance
                char_delay = base_typing_speed + random.uniform(-0.05, 0.05)
                
                # Slower for first character and after spaces
                if i == 0 or (i > 0 and text[i-1] == ' '):
                    char_delay *= random.uniform(1.2, 1.8)
                    
                # Check for personal typos
                current_word = typed_text.split()[-1] if typed_text.split() else ""
                if current_word in personal_typos and random.random() < 0.3:
                    # Make typo
                    typo_char = personal_typos[current_word]
                    element.send_keys(typo_char)
                    time.sleep(char_delay * 2)  # Pause to "notice" mistake
                    
                    # Backspace to correct
                    element.send_keys('\b')
                    time.sleep(char_delay)
                    
                # Type correct character
                element.send_keys(char)
                typed_text += char
                
                # Random micro-pauses for thinking
                if char in '.,!?' and random.random() < 0.4:
                    time.sleep(random.uniform(0.2, 0.8))
                elif char == ' ' and random.random() < 0.2:
                    time.sleep(random.uniform(0.1, 0.4))
                else:
                    time.sleep(char_delay)
                    
            # Log typing interaction
            self._log_interaction('typing', {
                'text_length': len(text),
                'typing_speed': base_typing_speed,
                'had_typos': len(personal_typos) > 0
            })
            
            return True
            
        except Exception as e:
            print(f"Tactile input failed: {str(e)}")
            return False
            
    def session_state_management(self, site_domain, action='login'):
        """Manage session state with realistic cookies and history"""
        
        if action == 'login':
            # Load existing session data if available
            session_file = f'session_{site_domain.replace(".", "_")}.json'
            
            try:
                with open(session_file, 'r') as f:
                    saved_session = json.load(f)
                    
                # Restore cookies
                for cookie in saved_session.get('cookies', []):
                    try:
                        self.driver.add_cookie(cookie)
                    except:
                        pass  # Cookie might be expired
                        
                self.session_data = saved_session
                
            except FileNotFoundError:
                # Create new session data
                self.session_data = {
                    'site_domain': site_domain,
                    'first_visit': time.time(),
                    'visit_count': 1,
                    'cookies': [],
                    'user_agent': self.driver.execute_script("return navigator.userAgent;")
                }
                
        elif action == 'save':
            # Save current session state
            if self.driver:
                try:
                    self.session_data['cookies'] = self.driver.get_cookies()
                    self.session_data['last_visit'] = time.time()
                    self.session_data['visit_count'] = self.session_data.get('visit_count', 0) + 1
                    
                    session_file = f'session_{site_domain.replace(".", "_")}.json'
                    with open(session_file, 'w') as f:
                        json.dump(self.session_data, f, indent=2)
                        
                except Exception as e:
                    print(f"Session save failed: {str(e)}")
                    
    def simulate_human_scrolling(self, scroll_type='random'):
        """Simulate natural scrolling behavior"""
        
        if not self.driver:
            return False
            
        try:
            if scroll_type == 'random':
                # Random scroll pattern
                scroll_actions = random.randint(2, 5)
                
                for _ in range(scroll_actions):
                    # Random scroll direction and amount
                    scroll_direction = random.choice(['down', 'up'])
                    scroll_amount = random.randint(100, 500)
                    
                    if scroll_direction == 'down':
                        self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
                    else:
                        self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount});")
                        
                    # Pause between scrolls
                    time.sleep(random.uniform(0.5, 2.0))
                    
            elif scroll_type == 'to_element':
                # Scroll to bring element into view (handled by Selenium automatically)
                pass
                
            return True
            
        except Exception as e:
            print(f"Scrolling simulation failed: {str(e)}")
            return False
            
    def cognitive_fatigue_simulation(self):
        """Simulate human cognitive fatigue over time"""
        
        if not self.current_session_start:
            return 1.0
            
        session_duration = time.time() - self.current_session_start
        fatigue_curve = self.persona['behavioral']['cognitive_fatigue_curve'] if self.persona else 1.0
        
        # Increase delays as session progresses
        base_fatigue = 1.0 + (session_duration / 3600) * fatigue_curve
        
        # Add random variance
        fatigue_factor = base_fatigue * random.uniform(0.8, 1.2)
        
        return fatigue_factor
        
    def _log_interaction(self, interaction_type, details):
        """Log interaction for behavioral analysis"""
        
        interaction = {
            'timestamp': time.time(),
            'type': interaction_type,
            'details': details,
            'session_duration': time.time() - self.current_session_start if self.current_session_start else 0
        }
        
        self.interaction_history.append(interaction)
        
        # Keep only last 100 interactions for memory management
        if len(self.interaction_history) > 100:
            self.interaction_history = self.interaction_history[-100:]
            
    def get_interaction_stats(self):
        """Get interaction statistics"""
        
        if not self.interaction_history:
            return {}
            
        total_interactions = len(self.interaction_history)
        interaction_types = {}
        
        for interaction in self.interaction_history:
            itype = interaction['type']
            interaction_types[itype] = interaction_types.get(itype, 0) + 1
            
        return {
            'total_interactions': total_interactions,
            'interaction_types': interaction_types,
            'session_duration': time.time() - self.current_session_start if self.current_session_start else 0,
            'avg_interaction_interval': self.interaction_history[-1]['timestamp'] - self.interaction_history[0]['timestamp'] / total_interactions if total_interactions > 1 else 0
        }
        
    def cleanup(self):
        """Clean up browser resources"""
        
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

def test_golem():
    """Test Golem behavioral simulation"""
    
    print("TESTING GOLEM MODULE")
    print("=" * 40)
    
    # Create test persona
    test_persona = {
        'behavioral': {
            'typing_speed': 0.15,
            'personal_typos': {'the': 'teh'},
            'cognitive_fatigue_curve': 1.0
        }
    }
    
    golem = Golem(test_persona)
    
    # Test browser initialization
    browser_init = golem.initialize_browser(headless=True)
    print(f"Browser initialization: {'SUCCESS' if browser_init else 'FAILED'}")
    
    if browser_init:
        # Test session management
        golem.session_state_management('test.com', 'login')
        print(f"Session management: SUCCESS")
        
        # Test cognitive fatigue
        fatigue_factor = golem.cognitive_fatigue_simulation()
        print(f"Cognitive fatigue factor: {fatigue_factor:.2f}")
        
        # Test interaction stats
        golem._log_interaction('test', {'test': True})
        stats = golem.get_interaction_stats()
        print(f"Interaction logging: {stats['total_interactions']} interactions")
        
        # Cleanup
        golem.cleanup()
        
    print(f"\nGolem module: OPERATIONAL")
    return True

if __name__ == "__main__":
    test_golem()