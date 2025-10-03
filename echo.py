#!/usr/bin/env python3
"""
Echo - Persona Preservation Engine
Handles cognitive storms and maintains persona consistency
"""

import time
import random
from typing import Dict, Any, Optional

class Echo:
    """Persona Preservation Engine - Handles difficult questions"""
    
    def __init__(self):
        self.cognitive_storm_threshold = 0.3
        self.fallback_responses = [
            "That's a tough one, I'm not sure I've ever thought about it that way",
            "I'd need to look into that more before I gave a definite answer",
            "Hmm, that's interesting. I haven't really considered that before",
            "I'm not entirely sure about that one",
            "That's a good question - I'd have to think about it more"
        ]
        self.pause_history = {}
        
    def wait_and_reflect_protocol(self, question: str, persona_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle cognitive storm with calculated pause"""
        
        # Calculate cognitive difficulty
        difficulty_score = self._assess_question_difficulty(question)
        
        if difficulty_score > self.cognitive_storm_threshold:
            # Initiate pause
            pause_duration = self._calculate_pause_duration(question, persona_data)
            
            # Simulate thinking time
            time.sleep(pause_duration)
            
            # Attempt persona recalibration
            response = self._persona_recalibration(question, persona_data)
            
            if not response:
                # Use human fallback
                response = self._human_fallback_response(question)
                
            # Log pause for adaptive learning
            self._log_pause_event(question, pause_duration, difficulty_score)
            
            return {
                'response': response,
                'pause_duration': pause_duration,
                'cognitive_storm': True
            }
        
        return {'cognitive_storm': False}
        
    def _assess_question_difficulty(self, question: str) -> float:
        """Assess cognitive difficulty of question"""
        
        difficulty_indicators = [
            'philosophy', 'ethics', 'morality', 'religion', 'politics',
            'controversial', 'opinion', 'believe', 'feel about',
            'what do you think', 'how do you feel', 'personal view'
        ]
        
        question_lower = question.lower()
        difficulty_score = 0.0
        
        # Check for difficulty indicators
        for indicator in difficulty_indicators:
            if indicator in question_lower:
                difficulty_score += 0.1
                
        # Check for complex sentence structure
        if len(question.split()) > 20:
            difficulty_score += 0.1
            
        # Check for multiple questions
        if question.count('?') > 1:
            difficulty_score += 0.15
            
        return min(difficulty_score, 1.0)
        
    def _calculate_pause_duration(self, question: str, persona_data: Dict[str, Any]) -> float:
        """Calculate appropriate pause duration"""
        
        base_pause = random.uniform(2.0, 5.0)
        
        # Adjust based on persona characteristics
        if persona_data and 'behavioral' in persona_data:
            cognitive_fatigue = persona_data['behavioral'].get('cognitive_fatigue_curve', 1.0)
            base_pause *= cognitive_fatigue
            
        # Adjust based on question complexity
        question_length = len(question.split())
        if question_length > 15:
            base_pause *= 1.3
            
        # Check pause history for similar questions
        question_type = self._classify_question_type(question)
        if question_type in self.pause_history:
            # Learned hesitation - slightly longer pause
            base_pause *= 1.1
            
        return base_pause
        
    def _persona_recalibration(self, question: str, persona_data: Dict[str, Any]) -> Optional[str]:
        """Attempt to generate response from persona truth matrix"""
        
        if not persona_data or 'truth_matrix' not in persona_data:
            return None
            
        truth_matrix = persona_data['truth_matrix']
        question_lower = question.lower()
        
        # Check for political questions
        if any(word in question_lower for word in ['political', 'vote', 'government']):
            political_lean = truth_matrix.get('political', 'moderate')
            return self._generate_political_response(political_lean, question)
            
        # Check for lifestyle questions
        if any(word in question_lower for word in ['lifestyle', 'hobby', 'free time']):
            return self._generate_lifestyle_response(truth_matrix, question)
            
        # Check for value-based questions
        if any(word in question_lower for word in ['important', 'value', 'priority']):
            return self._generate_value_response(truth_matrix, question)
            
        return None
        
    def _generate_political_response(self, political_lean: str, question: str) -> str:
        """Generate political response based on lean"""
        
        responses = {
            'liberal': [
                "I tend to lean more progressive on most issues",
                "I think we need more social programs and equality",
                "Government should help people more"
            ],
            'conservative': [
                "I believe in traditional values and limited government",
                "Personal responsibility is really important to me",
                "I prefer smaller government and free markets"
            ],
            'moderate': [
                "I try to see both sides of political issues",
                "I think the truth is usually somewhere in the middle",
                "I don't align strongly with either party"
            ]
        }
        
        return random.choice(responses.get(political_lean, responses['moderate']))
        
    def _generate_lifestyle_response(self, truth_matrix: Dict[str, Any], question: str) -> str:
        """Generate lifestyle response"""
        
        social_media_usage = truth_matrix.get('social_media_usage', 'moderate')
        
        if 'social media' in question.lower():
            if social_media_usage == 'heavy':
                return "I'm pretty active on social media - I check it throughout the day"
            elif social_media_usage == 'light':
                return "I don't use social media that much, maybe just to keep in touch"
            else:
                return "I use social media occasionally, nothing too crazy"
                
        return "I try to keep a good work-life balance"
        
    def _generate_value_response(self, truth_matrix: Dict[str, Any], question: str) -> str:
        """Generate value-based response"""
        
        values = []
        
        if truth_matrix.get('family_oriented', True):
            values.append("family")
        if truth_matrix.get('career_focused', True):
            values.append("career success")
        if truth_matrix.get('health_conscious', 'medium') == 'high':
            values.append("health and wellness")
            
        if values:
            return f"I'd say {random.choice(values)} is really important to me"
        else:
            return "I value honesty and treating people well"
            
    def _human_fallback_response(self, question: str) -> str:
        """Generate human-like fallback response"""
        
        # Add slight personalization based on question
        if 'opinion' in question.lower():
            return random.choice([
                "I don't really have a strong opinion on that one",
                "That's not something I've thought much about honestly"
            ])
        elif 'experience' in question.lower():
            return random.choice([
                "I haven't really had that experience myself",
                "That's not something I've dealt with personally"
            ])
        else:
            return random.choice(self.fallback_responses)
            
    def _classify_question_type(self, question: str) -> str:
        """Classify question type for pause history"""
        
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['political', 'vote', 'government']):
            return 'political'
        elif any(word in question_lower for word in ['personal', 'experience', 'feel']):
            return 'personal'
        elif any(word in question_lower for word in ['opinion', 'think', 'believe']):
            return 'opinion'
        else:
            return 'general'
            
    def _log_pause_event(self, question: str, duration: float, difficulty: float):
        """Log pause event for adaptive learning"""
        
        question_type = self._classify_question_type(question)
        
        if question_type not in self.pause_history:
            self.pause_history[question_type] = []
            
        self.pause_history[question_type].append({
            'duration': duration,
            'difficulty': difficulty,
            'timestamp': time.time()
        })
        
        # Keep only recent history
        if len(self.pause_history[question_type]) > 10:
            self.pause_history[question_type] = self.pause_history[question_type][-10:]
            
    def get_adaptive_pause_multiplier(self, question_type: str) -> float:
        """Get learned pause multiplier for question type"""
        
        if question_type not in self.pause_history:
            return 1.0
            
        # Calculate average difficulty for this question type
        history = self.pause_history[question_type]
        if not history:
            return 1.0
            
        avg_difficulty = sum(event['difficulty'] for event in history) / len(history)
        
        # Return multiplier based on learned difficulty
        return 1.0 + (avg_difficulty * 0.5)

def test_echo():
    """Test Echo module"""
    
    print("TESTING ECHO MODULE")
    print("=" * 40)
    
    echo = Echo()
    
    # Test persona data
    test_persona = {
        'truth_matrix': {
            'political': 'liberal',
            'social_media_usage': 'moderate',
            'family_oriented': True
        },
        'behavioral': {
            'cognitive_fatigue_curve': 1.2
        }
    }
    
    # Test difficult question
    difficult_question = "What are your philosophical views on the ethics of artificial intelligence in modern society?"
    
    result = echo.wait_and_reflect_protocol(difficult_question, test_persona)
    
    if result['cognitive_storm']:
        print(f"Cognitive storm detected")
        print(f"Pause duration: {result['pause_duration']:.2f}s")
        print(f"Response: {result['response']}")
    else:
        print("No cognitive storm - question handled normally")
        
    # Test political question
    political_question = "What is your political opinion on government spending?"
    result = echo.wait_and_reflect_protocol(political_question, test_persona)
    
    print(f"Political response: {result.get('response', 'No response')}")
    
    print(f"\nEcho module: OPERATIONAL")
    return True

if __name__ == "__main__":
    test_echo()