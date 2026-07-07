"""UI module for desktop and web interface components."""

from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class UIComponent:
    """Base UI component."""
    id: str
    name: str
    component_type: str  # button, input, panel, dialog, etc.
    properties: Dict[str, Any] = None
    children: List['UIComponent'] = None


class InterviewWindow:
    """Main interview window component."""
    
    def __init__(self):
        """Initialize interview window."""
        self.title = "Interview AI - Practice Session"
        self.width = 1200
        self.height = 800
        self.is_fullscreen = False
        
        self.components = {
            "question_panel": self._create_question_panel(),
            "answer_input": self._create_answer_input(),
            "audio_controls": self._create_audio_controls(),
            "feedback_panel": self._create_feedback_panel(),
            "progress_bar": self._create_progress_bar()
        }
    
    def _create_question_panel(self) -> dict:
        """Create question display panel."""
        return {
            "id": "question_panel",
            "type": "panel",
            "title": "Interview Question",
            "properties": {
                "font_size": 16,
                "padding": 20,
                "background_color": "#f5f5f5"
            }
        }
    
    def _create_answer_input(self) -> dict:
        """Create answer input area."""
        return {
            "id": "answer_input",
            "type": "text_area",
            "placeholder": "Type or speak your answer...",
            "properties": {
                "rows": 8,
                "font_size": 14
            }
        }
    
    def _create_audio_controls(self) -> dict:
        """Create audio control buttons."""
        return {
            "id": "audio_controls",
            "type": "button_group",
            "buttons": [
                {"name": "record", "icon": "mic", "tooltip": "Record Answer"},
                {"name": "stop", "icon": "stop", "tooltip": "Stop Recording"},
                {"name": "playback", "icon": "play", "tooltip": "Playback"}
            ]
        }
    
    def _create_feedback_panel(self) -> dict:
        """Create feedback display panel."""
        return {
            "id": "feedback_panel",
            "type": "panel",
            "title": "Feedback",
            "properties": {
                "background_color": "#e8f5e9",
                "border_radius": 8
            }
        }
    
    def _create_progress_bar(self) -> dict:
        """Create progress indicator."""
        return {
            "id": "progress_bar",
            "type": "progress_bar",
            "properties": {
                "min": 0,
                "max": 100,
                "value": 0
            }
        }
    
    def update_question(self, question: str, difficulty: str) -> None:
        """Update displayed question.
        
        Args:
            question: Question text
            difficulty: Difficulty level
        """
        self.components["question_panel"]["content"] = question
        self.components["question_panel"]["difficulty"] = difficulty
    
    def update_feedback(self, feedback: str, score: float) -> None:
        """Update feedback display.
        
        Args:
            feedback: Feedback text
            score: Score value
        """
        self.components["feedback_panel"]["content"] = feedback
        self.components["feedback_panel"]["score"] = score
    
    def update_progress(self, current: int, total: int) -> None:
        """Update progress indicator.
        
        Args:
            current: Current question number
            total: Total questions
        """
        progress = int((current / total) * 100) if total > 0 else 0
        self.components["progress_bar"]["value"] = progress
        self.components["progress_bar"]["text"] = f"{current}/{total}"


class QuestionDisplay:
    """Display interview question with formatting."""
    
    def __init__(self):
        """Initialize question display."""
        self.current_question = None
        self.question_number = 0
        self.total_questions = 0
    
    def display_question(
        self,
        question: str,
        number: int,
        total: int,
        difficulty: str,
        time_limit: int = 300
    ) -> dict:
        """Format question for display.
        
        Args:
            question: Question text
            number: Current question number
            total: Total questions
            difficulty: Difficulty level
            time_limit: Time limit in seconds
            
        Returns:
            Formatted question display data
        """
        self.current_question = question
        self.question_number = number
        self.total_questions = total
        
        return {
            "question": question,
            "number": number,
            "total": total,
            "difficulty": difficulty,
            "time_limit": time_limit,
            "formatted": f"Question {number}/{total} ({difficulty})\n\n{question}"
        }


class FeedbackDisplay:
    """Display interview feedback and scoring."""
    
    def __init__(self):
        """Initialize feedback display."""
        self.feedback_history = []
    
    def display_feedback(
        self,
        score: float,
        strengths: List[str],
        improvements: List[str],
        suggested_answer: str = None
    ) -> dict:
        """Format feedback for display.
        
        Args:
            score: Score (1-10)
            strengths: List of strength points
            improvements: List of improvement areas
            suggested_answer: Suggested better answer
            
        Returns:
            Formatted feedback display data
        """
        feedback_display = {
            "score": score,
            "score_color": self._get_score_color(score),
            "score_text": self._get_score_text(score),
            "strengths": strengths,
            "improvements": improvements,
            "suggested_answer": suggested_answer,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        self.feedback_history.append(feedback_display)
        return feedback_display
    
    @staticmethod
    def _get_score_color(score: float) -> str:
        """Get color for score."""
        if score >= 8:
            return "#4caf50"  # Green
        elif score >= 6:
            return "#2196f3"  # Blue
        elif score >= 4:
            return "#ff9800"  # Orange
        else:
            return "#f44336"  # Red
    
    @staticmethod
    def _get_score_text(score: float) -> str:
        """Get text description for score."""
        if score >= 8:
            return "Excellent"
        elif score >= 6:
            return "Good"
        elif score >= 4:
            return "Fair"
        else:
            return "Needs Improvement"


class SettingsPanel:
    """User settings and preferences."""
    
    def __init__(self):
        """Initialize settings panel."""
        self.settings = {
            "audio": {
                "input_device": "default",
                "output_device": "default",
                "sample_rate": 16000
            },
            "ui": {
                "theme": "light",
                "font_size": 14,
                "language": "en"
            },
            "interview": {
                "difficulty": "medium",
                "time_limit": 300,
                "show_hints": True
            }
        }
    
    def get_setting(self, category: str, key: str):
        """Get a setting value.
        
        Args:
            category: Setting category
            key: Setting key
            
        Returns:
            Setting value
        """
        return self.settings.get(category, {}).get(key)
    
    def set_setting(self, category: str, key: str, value: Any) -> bool:
        """Set a setting value.
        
        Args:
            category: Setting category
            key: Setting key
            value: New value
            
        Returns:
            Success status
        """
        if category in self.settings:
            self.settings[category][key] = value
            return True
        return False
    
    def get_all_settings(self) -> dict:
        """Get all settings.
        
        Returns:
            All settings dictionary
        """
        return self.settings.copy()


class ThemeManager:
    """Manage UI themes."""
    
    LIGHT_THEME = {
        "background": "#ffffff",
        "foreground": "#000000",
        "primary": "#2196f3",
        "secondary": "#757575",
        "success": "#4caf50",
        "warning": "#ff9800",
        "error": "#f44336"
    }
    
    DARK_THEME = {
        "background": "#1e1e1e",
        "foreground": "#ffffff",
        "primary": "#64b5f6",
        "secondary": "#bdbdbd",
        "success": "#81c784",
        "warning": "#ffb74d",
        "error": "#ef5350"
    }
    
    @classmethod
    def get_theme(cls, theme_name: str = "light") -> dict:
        """Get theme colors.
        
        Args:
            theme_name: Theme name (light, dark)
            
        Returns:
            Theme color dictionary
        """
        if theme_name == "dark":
            return cls.DARK_THEME.copy()
        return cls.LIGHT_THEME.copy()
