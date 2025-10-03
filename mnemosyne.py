#!/usr/bin/env python3
"""
Mnemosyne - Adaptive Learning Matrix
Self-improving neural network for detection resistance
"""

import json
import time
import random
import re
from typing import Dict, List, Any

class Mnemosyne:
    """Adaptive Learning Matrix - Core resilience system"""
    
    def __init__(self):
        self.behavioral_patterns = {}
        self.success_metrics = {}
        self.failure_analysis = {}
        self.predictive_models = {}
        self.contextual_responses = {}
        self.load_learning_data()
        
    def load_learning_data(self):
        """Load existing learning data"""
        
        try:
            with open('mnemosyne_learning.json', 'r') as f:
                data = json.load(f)
                self.behavioral_patterns = data.get('behavioral_patterns', {})
                self.success_metrics = data.get('success_metrics', {})
                self.failure_analysis = data.get('failure_analysis', {})
                self.predictive_models = data.get('predictive_models', {})
        except FileNotFoundError:
            self._initialize_base_models()
            
    def _initialize_base_models(self):
        """Initialize base learning models"""
        
        self.predictive_models = {
            'survey_completion_time': {
                'short_surveys': {'min': 3, 'max': 8, 'avg': 5},
                'medium_surveys': {'min': 8, 'max': 20, 'avg': 12},
                'long_surveys': {'min': 20, 'max': 45, 'avg': 30}
            },
            'bot_trap_indicators': [
                'please prove you are human',
                'are you a robot',
                'automated response detected',
                'suspicious activity',
                'verification required'
            ],
            'success_indicators': [
                'survey completed',
                'thank you',
                'points awarded',
                'payment processed',
                'congratulations'
            ]
        }
        
        self.contextual_responses = {
            'emotional_tones': {
                'positive': ['excellent', 'great', 'wonderful', 'amazing', 'fantastic'],
                'negative': ['poor', 'bad', 'terrible', 'awful', 'disappointing'],
                'neutral': ['okay', 'fine', 'average', 'decent', 'acceptable']
            },
            'question_types': {
                'satisfaction': ['very satisfied', 'satisfied', 'neutral', 'dissatisfied'],
                'frequency': ['always', 'often', 'sometimes', 'rarely', 'never'],
                'agreement': ['strongly agree', 'agree', 'neutral', 'disagree', 'strongly disagree'],
                'likelihood': ['very likely', 'likely', 'neutral', 'unlikely', 'very unlikely']
            }
        }
        
    def predictive_heuristics_engine(self, initial_questions: List[str]) -> Dict[str, Any]:
        """Analyze initial questions and predict survey path"""
        
        prediction = {
            'estimated_duration': 0,
            'trap_probability': 0.0,
            'completion_likelihood': 0.8,
            'recommended_pace': 'normal',
            'question_types': [],
            'risk_level': 'low'
        }
        
        # Analyze question patterns
        total_questions = len(initial_questions)
        
        if total_questions == 0:
            return prediction
            
        # Estimate duration based on question count and complexity
        avg_time_per_question = 30  # seconds
        complexity_multiplier = 1.0
        
        for question in initial_questions:
            question_lower = question.lower()
            
            # Check for complex question indicators
            if any(indicator in question_lower for indicator in ['explain', 'describe', 'why', 'how']):
                complexity_multiplier += 0.2
                
            # Check for bot trap indicators
            if any(trap in question_lower for trap in self.predictive_models['bot_trap_indicators']):
                prediction['trap_probability'] += 0.3
                prediction['risk_level'] = 'high'
                
            # Classify question type
            if any(word in question_lower for word in ['satisfied', 'satisfaction']):
                prediction['question_types'].append('satisfaction')
            elif any(word in question_lower for word in ['often', 'frequency', 'how many']):
                prediction['question_types'].append('frequency')
            elif any(word in question_lower for word in ['agree', 'opinion']):
                prediction['question_types'].append('agreement')
                
        # Calculate predictions
        prediction['estimated_duration'] = int(total_questions * avg_time_per_question * complexity_multiplier / 60)
        prediction['trap_probability'] = min(prediction['trap_probability'], 1.0)
        
        # Adjust completion likelihood based on trap probability
        prediction['completion_likelihood'] = max(0.3, 0.9 - prediction['trap_probability'])
        
        # Recommend pace based on risk
        if prediction['trap_probability'] > 0.5:
            prediction['recommended_pace'] = 'careful'
        elif prediction['trap_probability'] > 0.3:
            prediction['recommended_pace'] = 'moderate'
        else:
            prediction['recommended_pace'] = 'normal'
            
        return prediction
        
    def situational_analysis_engine(self, page_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze entire webpage for interruptions and alerts"""
        
        analysis = {
            'urgent_notifications': [],
            'popup_modals': [],
            'system_alerts': [],
            'navigation_blockers': [],
            'priority_actions': []
        }
        
        # Analyze for urgent notifications
        if 'notifications' in page_elements:
            for notification in page_elements['notifications']:
                urgency_keywords = ['urgent', 'important', 'alert', 'warning', 'error']
                if any(keyword in notification.lower() for keyword in urgency_keywords):
                    analysis['urgent_notifications'].append(notification)
                    
        # Analyze for popup modals
        if 'modals' in page_elements:
            for modal in page_elements['modals']:
                modal_keywords = ['popup', 'modal', 'dialog', 'overlay']
                if any(keyword in modal.lower() for keyword in modal_keywords):
                    analysis['popup_modals'].append(modal)
                    
        # Analyze for system alerts
        if 'alerts' in page_elements:
            analysis['system_alerts'] = page_elements['alerts']
            
        # Prioritize actions based on analysis
        if analysis['urgent_notifications']:
            analysis['priority_actions'].append('handle_notifications')
        if analysis['popup_modals']:
            analysis['priority_actions'].append('dismiss_popups')
        if analysis['system_alerts']:
            analysis['priority_actions'].append('respond_to_alerts')
            
        return analysis
        
    def behavioral_feedback_loop(self, session_result: Dict[str, Any]):
        """Learn from session outcomes"""
        
        session_id = f"session_{int(time.time())}"
        
        if session_result.get('success', False):
            # Positive reinforcement
            self._log_successful_behavior(session_id, session_result)
        else:
            # Analyze failure and adjust
            self._analyze_failure_patterns(session_id, session_result)
            
        # Update success metrics
        site = session_result.get('site', 'unknown')
        if site not in self.success_metrics:
            self.success_metrics[site] = {'successes': 0, 'attempts': 0, 'success_rate': 0.0}
            
        self.success_metrics[site]['attempts'] += 1
        if session_result.get('success', False):
            self.success_metrics[site]['successes'] += 1
            
        self.success_metrics[site]['success_rate'] = (
            self.success_metrics[site]['successes'] / self.success_metrics[site]['attempts']
        )
        
        # Save learning data
        self.save_learning_data()
        
    def _log_successful_behavior(self, session_id: str, session_result: Dict[str, Any]):
        """Log successful behavioral patterns"""
        
        successful_pattern = {
            'timestamp': time.time(),
            'site': session_result.get('site'),
            'duration': session_result.get('duration', 0),
            'questions_answered': session_result.get('questions_answered', 0),
            'behavioral_metrics': session_result.get('behavioral_metrics', {}),
            'persona_used': session_result.get('persona_used', {}),
            'success_indicators': session_result.get('success_indicators', [])
        }
        
        self.behavioral_patterns[session_id] = successful_pattern
        
    def _analyze_failure_patterns(self, session_id: str, session_result: Dict[str, Any]):
        """Analyze failure patterns for learning"""
        
        failure_pattern = {
            'timestamp': time.time(),
            'site': session_result.get('site'),
            'failure_reason': session_result.get('error', 'unknown'),
            'failure_point': session_result.get('failure_point', 'unknown'),
            'behavioral_metrics': session_result.get('behavioral_metrics', {}),
            'detection_indicators': session_result.get('detection_indicators', [])
        }
        
        self.failure_analysis[session_id] = failure_pattern
        
        # Adjust behavioral parameters based on failure
        self._adjust_behavioral_parameters(failure_pattern)
        
    def _adjust_behavioral_parameters(self, failure_pattern: Dict[str, Any]):
        """Adjust behavioral parameters based on failure analysis"""
        
        failure_reason = failure_pattern.get('failure_reason', '').lower()
        
        # Adjust timing if detected as too fast
        if 'too fast' in failure_reason or 'suspicious timing' in failure_reason:
            if 'timing_adjustments' not in self.behavioral_patterns:
                self.behavioral_patterns['timing_adjustments'] = {}
            self.behavioral_patterns['timing_adjustments']['min_delay_multiplier'] = 1.5
            
        # Adjust mouse patterns if detected as robotic
        if 'robotic' in failure_reason or 'automated' in failure_reason:
            if 'mouse_adjustments' not in self.behavioral_patterns:
                self.behavioral_patterns['mouse_adjustments'] = {}
            self.behavioral_patterns['mouse_adjustments']['variance_multiplier'] = 2.0
            
    def contextual_reasoning_engine(self, question: str, persona: Dict[str, Any]) -> str:
        """Generate contextual response based on question analysis"""
        
        question_lower = question.lower()
        
        # Analyze emotional tone
        emotional_tone = self._analyze_emotional_tone(question)
        
        # Analyze question type
        question_type = self._classify_question_type(question)
        
        # Generate response based on persona and context
        response = self._generate_contextual_response(question_type, emotional_tone, persona)
        
        return response
        
    def _analyze_emotional_tone(self, question: str) -> str:
        """Analyze emotional tone of question"""
        
        question_lower = question.lower()
        
        positive_indicators = ['love', 'enjoy', 'like', 'happy', 'satisfied', 'great', 'excellent']
        negative_indicators = ['hate', 'dislike', 'unhappy', 'dissatisfied', 'poor', 'bad', 'terrible']
        
        positive_score = sum(1 for word in positive_indicators if word in question_lower)
        negative_score = sum(1 for word in negative_indicators if word in question_lower)
        
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
            
    def _classify_question_type(self, question: str) -> str:
        """Classify question type for appropriate response"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['satisfied', 'satisfaction']):
            return 'satisfaction'
        elif any(word in question_lower for word in ['often', 'frequency', 'how many times']):
            return 'frequency'
        elif any(word in question_lower for word in ['agree', 'opinion', 'think']):
            return 'agreement'
        elif any(word in question_lower for word in ['likely', 'probably', 'chance']):
            return 'likelihood'
        else:
            return 'general'
            
    def _generate_contextual_response(self, question_type: str, emotional_tone: str, persona: Dict[str, Any]) -> str:
        """Generate contextual response"""
        
        # Get base responses for question type
        base_responses = self.contextual_responses['question_types'].get(question_type, ['yes', 'no', 'maybe'])
        
        # Adjust based on emotional tone and persona
        if question_type in self.contextual_responses['question_types']:
            responses = self.contextual_responses['question_types'][question_type]
        else:
            responses = ['agree', 'neutral', 'disagree']
            
        # Persona-based adjustments
        if persona and 'truth_matrix' in persona:
            truth_matrix = persona['truth_matrix']
            
            # Adjust based on persona characteristics
            if truth_matrix.get('brand_loyalty') == 'high' and emotional_tone == 'positive':
                # High brand loyalty + positive question = positive response
                positive_responses = [r for r in responses if 'agree' in r or 'satisfied' in r or 'likely' in r]
                if positive_responses:
                    return random.choice(positive_responses)
                    
        # Default response selection
        return random.choice(responses)
        
    def get_behavioral_adjustments(self, site: str) -> Dict[str, float]:
        """Get behavioral adjustments for specific site"""
        
        adjustments = {
            'timing_multiplier': 1.0,
            'mouse_variance_multiplier': 1.0,
            'pause_frequency_multiplier': 1.0
        }
        
        # Apply learned adjustments
        if 'timing_adjustments' in self.behavioral_patterns:
            adjustments['timing_multiplier'] = self.behavioral_patterns['timing_adjustments'].get('min_delay_multiplier', 1.0)
            
        if 'mouse_adjustments' in self.behavioral_patterns:
            adjustments['mouse_variance_multiplier'] = self.behavioral_patterns['mouse_adjustments'].get('variance_multiplier', 1.0)
            
        # Site-specific adjustments based on success rate
        if site in self.success_metrics:
            success_rate = self.success_metrics[site]['success_rate']
            if success_rate < 0.5:  # Low success rate, be more careful
                adjustments['timing_multiplier'] *= 1.5
                adjustments['mouse_variance_multiplier'] *= 1.3
                
        return adjustments
        
    def save_learning_data(self):
        """Save learning data to file"""
        
        data = {
            'behavioral_patterns': self.behavioral_patterns,
            'success_metrics': self.success_metrics,
            'failure_analysis': self.failure_analysis,
            'predictive_models': self.predictive_models,
            'timestamp': time.time()
        }
        
        with open('mnemosyne_learning.json', 'w') as f:
            json.dump(data, f, indent=2)

def test_mnemosyne():
    """Test Mnemosyne adaptive learning"""
    
    print("TESTING MNEMOSYNE MODULE")
    print("=" * 40)
    
    mnemosyne = Mnemosyne()
    
    # Test predictive heuristics
    test_questions = [
        "How satisfied are you with our service?",
        "How often do you shop online?",
        "Please prove you are human"
    ]
    
    prediction = mnemosyne.predictive_heuristics_engine(test_questions)
    print(f"Survey prediction: {prediction['estimated_duration']} min, {prediction['trap_probability']:.2f} trap risk")
    
    # Test contextual reasoning
    test_persona = {
        'truth_matrix': {
            'brand_loyalty': 'high',
            'shopping_habits': 'online_preferred'
        }
    }
    
    response = mnemosyne.contextual_reasoning_engine("How satisfied are you?", test_persona)
    print(f"Contextual response: {response}")
    
    # Test behavioral feedback
    test_result = {
        'success': True,
        'site': 'test.com',
        'duration': 300,
        'questions_answered': 10
    }
    
    mnemosyne.behavioral_feedback_loop(test_result)
    print(f"Behavioral feedback logged")
    
    # Test behavioral adjustments
    adjustments = mnemosyne.get_behavioral_adjustments('test.com')
    print(f"Behavioral adjustments: timing={adjustments['timing_multiplier']:.2f}")
    
    print(f"\nMnemosyne module: OPERATIONAL")
    return True

if __name__ == "__main__":
    test_mnemosyne()