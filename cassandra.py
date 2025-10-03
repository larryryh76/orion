#!/usr/bin/env python3
"""
Cassandra - Predictive Human Empathy Engine
Models human psychology and behavior patterns for enhanced evasion
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple

class Cassandra:
    """Predictive Human Empathy Engine - Psychology modeling system"""
    
    def __init__(self):
        self.human_behavior_models = {}
        self.workday_patterns = {}
        self.curiosity_triggers = {}
        self.detection_psychology = {}
        self.analyst_profiles = {}
        self.load_empathy_data()
        
    def load_empathy_data(self):
        """Load human behavior modeling data"""
        try:
            with open('cassandra_empathy.json', 'r') as f:
                data = json.load(f)
                self.human_behavior_models = data.get('human_behavior_models', {})
                self.workday_patterns = data.get('workday_patterns', {})
                self.analyst_profiles = data.get('analyst_profiles', {})
        except FileNotFoundError:
            self._initialize_empathy_models()
            
    def _initialize_empathy_models(self):
        """Initialize human psychology models"""
        self.workday_patterns = {
            'monday': {'alertness': 0.7, 'scrutiny': 0.8, 'patience': 0.6},
            'tuesday': {'alertness': 0.9, 'scrutiny': 0.9, 'patience': 0.8},
            'wednesday': {'alertness': 0.8, 'scrutiny': 0.8, 'patience': 0.7},
            'thursday': {'alertness': 0.7, 'scrutiny': 0.7, 'patience': 0.6},
            'friday': {'alertness': 0.5, 'scrutiny': 0.4, 'patience': 0.3},
            'weekend': {'alertness': 0.3, 'scrutiny': 0.2, 'patience': 0.9}
        }
        
        self.curiosity_triggers = {
            'perfect_responses': 0.9,  # Too perfect = suspicious
            'inconsistent_timing': 0.7,  # Irregular patterns
            'demographic_mismatch': 0.8,  # Profile doesn't match answers
            'emotional_flatness': 0.6,  # No personality showing
            'technical_precision': 0.8   # Too technically accurate
        }
        
        self.analyst_profiles = {
            'experienced': {
                'detection_skill': 0.9,
                'pattern_recognition': 0.8,
                'curiosity_threshold': 0.3,
                'investigation_depth': 0.9
            },
            'junior': {
                'detection_skill': 0.4,
                'pattern_recognition': 0.3,
                'curiosity_threshold': 0.7,
                'investigation_depth': 0.5
            },
            'automated_system': {
                'detection_skill': 0.7,
                'pattern_recognition': 0.9,
                'curiosity_threshold': 0.1,
                'investigation_depth': 0.3
            }
        }
        
    def behavioral_anomaly_prediction(self, current_time: datetime = None) -> Dict[str, float]:
        """Predict human analyst behavior based on time and workday patterns"""
        if not current_time:
            current_time = datetime.now()
            
        day_of_week = current_time.strftime('%A').lower()
        hour = current_time.hour
        
        # Base patterns by day
        base_pattern = self.workday_patterns.get(day_of_week, self.workday_patterns['tuesday'])
        
        # Time-based adjustments
        time_adjustments = self._calculate_time_adjustments(hour)
        
        # Combine base pattern with time adjustments
        prediction = {
            'alertness': max(0.1, min(1.0, base_pattern['alertness'] * time_adjustments['alertness'])),
            'scrutiny': max(0.1, min(1.0, base_pattern['scrutiny'] * time_adjustments['scrutiny'])),
            'patience': max(0.1, min(1.0, base_pattern['patience'] * time_adjustments['patience'])),
            'audit_intensity': self._calculate_audit_intensity(day_of_week, hour),
            'recommended_approach': self._recommend_approach(base_pattern, time_adjustments)
        }
        
        return prediction
        
    def _calculate_time_adjustments(self, hour: int) -> Dict[str, float]:
        """Calculate time-based behavioral adjustments"""
        adjustments = {'alertness': 1.0, 'scrutiny': 1.0, 'patience': 1.0}
        
        # Early morning (6-9 AM) - Lower alertness
        if 6 <= hour <= 9:
            adjustments['alertness'] *= 0.7
            adjustments['patience'] *= 1.2
            
        # Mid-morning (9-12 PM) - Peak performance
        elif 9 <= hour <= 12:
            adjustments['alertness'] *= 1.0
            adjustments['scrutiny'] *= 1.1
            
        # Lunch time (12-2 PM) - Reduced attention
        elif 12 <= hour <= 14:
            adjustments['alertness'] *= 0.6
            adjustments['scrutiny'] *= 0.7
            adjustments['patience'] *= 0.8
            
        # Afternoon (2-5 PM) - Moderate performance
        elif 14 <= hour <= 17:
            adjustments['alertness'] *= 0.8
            adjustments['scrutiny'] *= 0.9
            
        # Evening (5-8 PM) - Declining performance
        elif 17 <= hour <= 20:
            adjustments['alertness'] *= 0.5
            adjustments['scrutiny'] *= 0.6
            adjustments['patience'] *= 0.4
            
        # Night/Weekend (8 PM+) - Minimal oversight
        else:
            adjustments['alertness'] *= 0.3
            adjustments['scrutiny'] *= 0.2
            adjustments['patience'] *= 1.5
            
        return adjustments
        
    def _calculate_audit_intensity(self, day: str, hour: int) -> float:
        """Calculate expected audit intensity"""
        base_intensity = 0.5
        
        # Day-based adjustments
        day_multipliers = {
            'monday': 1.2,  # Start of week - higher scrutiny
            'tuesday': 1.0,
            'wednesday': 0.9,
            'thursday': 0.8,
            'friday': 0.4,  # End of week - lower scrutiny
            'saturday': 0.2,
            'sunday': 0.1
        }
        
        # Time-based adjustments
        if 9 <= hour <= 11:  # Peak audit time
            time_multiplier = 1.3
        elif 14 <= hour <= 16:  # Afternoon audit
            time_multiplier = 1.1
        elif 12 <= hour <= 14:  # Lunch break
            time_multiplier = 0.3
        elif hour >= 17 or hour <= 8:  # After hours
            time_multiplier = 0.2
        else:
            time_multiplier = 1.0
            
        return min(1.0, base_intensity * day_multipliers.get(day, 1.0) * time_multiplier)
        
    def _recommend_approach(self, base_pattern: Dict, time_adjustments: Dict) -> str:
        """Recommend behavioral approach based on predictions"""
        avg_scrutiny = base_pattern['scrutiny'] * time_adjustments['scrutiny']
        avg_patience = base_pattern['patience'] * time_adjustments['patience']
        
        if avg_scrutiny > 0.8:
            return 'ultra_careful'
        elif avg_scrutiny > 0.6:
            return 'careful'
        elif avg_patience > 0.8:
            return 'relaxed'
        else:
            return 'normal'
            
    def human_curiosity_countermeasure(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Inject human-like imperfections to satisfy analyst curiosity"""
        enhanced_response = response_data.copy()
        
        # Calculate perfection score
        perfection_score = self._calculate_perfection_score(response_data)
        
        if perfection_score > 0.8:  # Too perfect - needs humanization
            enhanced_response = self._inject_human_imperfections(enhanced_response)
            
        return enhanced_response
        
    def _calculate_perfection_score(self, response_data: Dict[str, Any]) -> float:
        """Calculate how 'perfect' a response appears"""
        score = 0.0
        factors = 0
        
        # Check response consistency
        if response_data.get('consistency_score', 0) > 0.9:
            score += 0.3
            factors += 1
            
        # Check timing patterns
        if response_data.get('timing_variance', 1.0) < 0.1:
            score += 0.2
            factors += 1
            
        # Check emotional variance
        if response_data.get('emotional_range', 1.0) < 0.2:
            score += 0.2
            factors += 1
            
        # Check demographic alignment
        if response_data.get('demographic_match', 0.5) > 0.95:
            score += 0.3
            factors += 1
            
        return score / max(1, factors)
        
    def _inject_human_imperfections(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add subtle human-like imperfections"""
        imperfections = [
            self._add_minor_inconsistency,
            self._add_emotional_tangent,
            self._add_timing_variation,
            self._add_demographic_quirk
        ]
        
        # Apply 1-2 random imperfections
        selected_imperfections = random.sample(imperfections, random.randint(1, 2))
        
        for imperfection_func in selected_imperfections:
            response_data = imperfection_func(response_data)
            
        return response_data
        
    def _add_minor_inconsistency(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a minor, believable inconsistency"""
        inconsistencies = [
            "Actually, let me think about that again...",
            "Well, sometimes I feel differently about this",
            "It depends on my mood, really",
            "I'm not always consistent with this"
        ]
        
        if 'additional_comments' not in response_data:
            response_data['additional_comments'] = []
            
        response_data['additional_comments'].append(random.choice(inconsistencies))
        return response_data
        
    def _add_emotional_tangent(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add an emotional, slightly off-topic comment"""
        tangents = [
            "This reminds me of something that happened last week",
            "My friend always says something similar",
            "I had a bad experience with this once",
            "This is actually pretty important to me"
        ]
        
        if 'emotional_context' not in response_data:
            response_data['emotional_context'] = []
            
        response_data['emotional_context'].append(random.choice(tangents))
        return response_data
        
    def _add_timing_variation(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add realistic timing variations"""
        if 'response_timing' in response_data:
            # Add small random delays
            base_time = response_data['response_timing']
            variation = random.uniform(0.8, 1.3)
            response_data['response_timing'] = base_time * variation
            
        return response_data
        
    def _add_demographic_quirk(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add subtle demographic-based response quirks"""
        quirks = [
            "As someone my age would say",
            "In my experience",
            "From where I come from",
            "People like me usually"
        ]
        
        if 'demographic_context' not in response_data:
            response_data['demographic_context'] = []
            
        response_data['demographic_context'].append(random.choice(quirks))
        return response_data
        
    def detection_postmortem_analysis(self, detection_event: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze human thought process behind detection"""
        analysis = {
            'detection_trigger': None,
            'analyst_type': 'unknown',
            'thought_process': [],
            'critical_evidence': [],
            'prevention_strategy': []
        }
        
        # Identify detection trigger
        triggers = detection_event.get('triggers', [])
        for trigger in triggers:
            if trigger in self.curiosity_triggers:
                analysis['detection_trigger'] = trigger
                break
                
        # Model analyst thought process
        analysis['thought_process'] = self._model_analyst_thinking(detection_event)
        
        # Identify critical evidence
        analysis['critical_evidence'] = self._identify_critical_evidence(detection_event)
        
        # Generate prevention strategy
        analysis['prevention_strategy'] = self._generate_prevention_strategy(analysis)
        
        # Learn from detection
        self._learn_from_detection(analysis)
        
        return analysis
        
    def _model_analyst_thinking(self, detection_event: Dict[str, Any]) -> List[str]:
        """Model the human analyst's thought process"""
        thought_process = []
        
        # Initial suspicion
        if detection_event.get('initial_flag'):
            thought_process.append("Something feels off about this response pattern")
            
        # Pattern recognition
        if detection_event.get('pattern_anomaly'):
            thought_process.append("The timing/behavior doesn't match typical users")
            
        # Curiosity investigation
        if detection_event.get('investigation_depth', 0) > 0.5:
            thought_process.append("Let me dig deeper into this user's history")
            
        # Final confirmation
        if detection_event.get('confidence', 0) > 0.8:
            thought_process.append("This is definitely automated behavior")
            
        return thought_process
        
    def _identify_critical_evidence(self, detection_event: Dict[str, Any]) -> List[str]:
        """Identify what evidence convinced the analyst"""
        evidence = []
        
        if detection_event.get('timing_anomaly'):
            evidence.append("Inhuman response timing patterns")
            
        if detection_event.get('consistency_anomaly'):
            evidence.append("Responses too consistent/perfect")
            
        if detection_event.get('behavioral_anomaly'):
            evidence.append("Behavior doesn't match demographic profile")
            
        if detection_event.get('technical_signature'):
            evidence.append("Technical fingerprint detected")
            
        return evidence
        
    def _generate_prevention_strategy(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate strategy to prevent similar detections"""
        strategies = []
        
        trigger = analysis.get('detection_trigger')
        
        if trigger == 'perfect_responses':
            strategies.append("Inject more human imperfections and inconsistencies")
            
        elif trigger == 'inconsistent_timing':
            strategies.append("Improve timing variation algorithms")
            
        elif trigger == 'demographic_mismatch':
            strategies.append("Better align responses with persona demographics")
            
        elif trigger == 'emotional_flatness':
            strategies.append("Enhance emotional expression in responses")
            
        elif trigger == 'technical_precision':
            strategies.append("Add more casual, non-technical language")
            
        return strategies
        
    def _learn_from_detection(self, analysis: Dict[str, Any]):
        """Update models based on detection analysis"""
        trigger = analysis.get('detection_trigger')
        
        if trigger and trigger in self.curiosity_triggers:
            # Increase sensitivity to this trigger
            self.curiosity_triggers[trigger] = min(1.0, self.curiosity_triggers[trigger] + 0.1)
            
        # Save updated models
        self.save_empathy_data()
        
    def save_empathy_data(self):
        """Save empathy modeling data"""
        data = {
            'human_behavior_models': self.human_behavior_models,
            'workday_patterns': self.workday_patterns,
            'analyst_profiles': self.analyst_profiles,
            'curiosity_triggers': self.curiosity_triggers,
            'last_updated': time.time()
        }
        
        with open('cassandra_empathy.json', 'w') as f:
            json.dump(data, f, indent=2)
            
    def get_human_psychology_insight(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get psychological insights for current context"""
        current_time = datetime.now()
        behavior_prediction = self.behavioral_anomaly_prediction(current_time)
        
        insight = {
            'analyst_state': behavior_prediction,
            'recommended_persona_adjustments': self._recommend_persona_adjustments(behavior_prediction),
            'risk_assessment': self._assess_current_risk(behavior_prediction),
            'optimal_timing': self._suggest_optimal_timing(current_time)
        }
        
        return insight
        
    def _recommend_persona_adjustments(self, behavior_prediction: Dict[str, float]) -> Dict[str, Any]:
        """Recommend persona adjustments based on analyst state"""
        adjustments = {}
        
        if behavior_prediction['scrutiny'] > 0.7:
            adjustments['increase_imperfections'] = True
            adjustments['emotional_variance'] = 'high'
            adjustments['response_timing'] = 'varied'
            
        if behavior_prediction['patience'] < 0.5:
            adjustments['response_speed'] = 'faster'
            adjustments['complexity'] = 'reduced'
            
        return adjustments
        
    def _assess_current_risk(self, behavior_prediction: Dict[str, float]) -> str:
        """Assess current detection risk level"""
        risk_score = (
            behavior_prediction['alertness'] * 0.3 +
            behavior_prediction['scrutiny'] * 0.4 +
            behavior_prediction['audit_intensity'] * 0.3
        )
        
        if risk_score > 0.8:
            return 'critical'
        elif risk_score > 0.6:
            return 'high'
        elif risk_score > 0.4:
            return 'moderate'
        else:
            return 'low'
            
    def _suggest_optimal_timing(self, current_time: datetime) -> Dict[str, Any]:
        """Suggest optimal timing for operations"""
        suggestions = {}
        
        # Find lowest risk time in next 24 hours
        lowest_risk_time = None
        lowest_risk_score = 1.0
        
        for hour_offset in range(24):
            test_time = current_time + timedelta(hours=hour_offset)
            prediction = self.behavioral_anomaly_prediction(test_time)
            risk_score = prediction['alertness'] * 0.5 + prediction['scrutiny'] * 0.5
            
            if risk_score < lowest_risk_score:
                lowest_risk_score = risk_score
                lowest_risk_time = test_time
                
        suggestions['optimal_time'] = lowest_risk_time.strftime('%Y-%m-%d %H:%M')
        suggestions['risk_reduction'] = f"{((1.0 - lowest_risk_score) * 100):.1f}%"
        
        return suggestions

# Test the Cassandra module
if __name__ == "__main__":
    cassandra = Cassandra()
    
    # Test behavioral prediction
    prediction = cassandra.behavioral_anomaly_prediction()
    print("Behavioral Prediction:", prediction)
    
    # Test curiosity countermeasure
    test_response = {
        'consistency_score': 0.95,
        'timing_variance': 0.05,
        'emotional_range': 0.1
    }
    enhanced = cassandra.human_curiosity_countermeasure(test_response)
    print("Enhanced Response:", enhanced)
    
    # Test psychology insight
    insight = cassandra.get_human_psychology_insight({})
    print("Psychology Insight:", insight)
    
    print("Cassandra - Predictive Human Empathy Engine: OPERATIONAL")