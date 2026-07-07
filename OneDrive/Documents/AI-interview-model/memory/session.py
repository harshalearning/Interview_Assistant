"""Memory module for conversation and session management."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class Message:
    """Single message in conversation."""
    
    def __init__(
        self,
        role: str,  # "user", "assistant", "system"
        content: str,
        timestamp: str = None
    ):
        """Initialize message.
        
        Args:
            role: Message role
            content: Message content
            timestamp: ISO format timestamp
        """
        self.role = role
        self.content = content
        self.timestamp = timestamp or datetime.utcnow().isoformat()
    
    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            "role": self.role,
            "content": self.content,
            "timestamp": self.timestamp
        }


class ConversationMemory:
    """Store and retrieve conversation history."""
    
    def __init__(self, max_history: int = 50):
        """Initialize conversation memory.
        
        Args:
            max_history: Maximum messages to store
        """
        self.messages: List[Message] = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str) -> None:
        """Add message to memory.
        
        Args:
            role: Message role
            content: Message content
        """
        message = Message(role=role, content=content)
        self.messages.append(message)
        
        # Keep only recent messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_messages(self, n: int = None) -> List[dict]:
        """Get recent messages.
        
        Args:
            n: Number of messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        if n:
            return [m.to_dict() for m in self.messages[-n:]]
        return [m.to_dict() for m in self.messages]
    
    def get_context(self, n: int = 5) -> str:
        """Get recent conversation context as string.
        
        Args:
            n: Number of messages to include
            
        Returns:
            Formatted conversation context
        """
        recent = self.messages[-n:]
        context = "\n".join([
            f"{m.role}: {m.content}"
            for m in recent
        ])
        return context
    
    def clear(self) -> None:
        """Clear all messages."""
        self.messages = []
    
    def get_summary(self) -> dict:
        """Get memory summary statistics.
        
        Returns:
            Summary information
        """
        if not self.messages:
            return {"messages": 0}
        
        return {
            "messages": len(self.messages),
            "first_message": self.messages[0].timestamp,
            "last_message": self.messages[-1].timestamp,
            "user_messages": sum(1 for m in self.messages if m.role == "user"),
            "assistant_messages": sum(1 for m in self.messages if m.role == "assistant")
        }


class SessionState:
    """Manage interview session state."""
    
    def __init__(self, session_id: str, user_id: str, topic: str):
        """Initialize session state.
        
        Args:
            session_id: Unique session ID
            user_id: User ID
            topic: Interview topic
        """
        self.session_id = session_id
        self.user_id = user_id
        self.topic = topic
        self.status = "active"  # active, paused, completed
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
        
        self.conversation = ConversationMemory()
        self.metrics = {
            "questions_asked": 0,
            "answers_given": 0,
            "total_score": 0.0,
            "average_confidence": 0.0
        }
        self.custom_data: Dict[str, Any] = {}
    
    def update_metric(self, metric_name: str, value: Any) -> None:
        """Update a metric.
        
        Args:
            metric_name: Metric name
            value: Metric value
        """
        self.metrics[metric_name] = value
        self.updated_at = datetime.utcnow().isoformat()
    
    def increment_metric(self, metric_name: str, delta: float = 1.0) -> None:
        """Increment a numeric metric.
        
        Args:
            metric_name: Metric name
            delta: Amount to increment
        """
        if metric_name in self.metrics:
            self.metrics[metric_name] += delta
        self.updated_at = datetime.utcnow().isoformat()
    
    def set_custom_data(self, key: str, value: Any) -> None:
        """Store custom data.
        
        Args:
            key: Data key
            value: Data value
        """
        self.custom_data[key] = value
        self.updated_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> dict:
        """Convert session to dictionary.
        
        Returns:
            Session state dictionary
        """
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "topic": self.topic,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metrics": self.metrics,
            "conversation_summary": self.conversation.get_summary(),
            "custom_data": self.custom_data
        }


class SessionManager:
    """Manage multiple interview sessions."""
    
    def __init__(self):
        """Initialize session manager."""
        self.sessions: Dict[str, SessionState] = {}
    
    def create_session(
        self,
        session_id: str,
        user_id: str,
        topic: str
    ) -> SessionState:
        """Create new session.
        
        Args:
            session_id: Session ID
            user_id: User ID
            topic: Interview topic
            
        Returns:
            Created session state
        """
        session = SessionState(session_id, user_id, topic)
        self.sessions[session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[SessionState]:
        """Get session by ID.
        
        Args:
            session_id: Session ID
            
        Returns:
            Session state or None
        """
        return self.sessions.get(session_id)
    
    def end_session(self, session_id: str) -> bool:
        """End a session.
        
        Args:
            session_id: Session ID
            
        Returns:
            Success status
        """
        if session_id in self.sessions:
            self.sessions[session_id].status = "completed"
            self.sessions[session_id].updated_at = datetime.utcnow().isoformat()
            return True
        return False
    
    def get_user_sessions(self, user_id: str) -> List[dict]:
        """Get all sessions for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            List of session dictionaries
        """
        return [
            s.to_dict() for s in self.sessions.values()
            if s.user_id == user_id
        ]


class UserProfile:
    """Store user profile and preferences."""
    
    def __init__(self, user_id: str):
        """Initialize user profile.
        
        Args:
            user_id: Unique user ID
        """
        self.user_id = user_id
        self.created_at = datetime.utcnow().isoformat()
        self.updated_at = datetime.utcnow().isoformat()
        
        self.preferences = {
            "difficulty": "medium",
            "question_count": 5,
            "focus_areas": [],
            "preferred_language": "en"
        }
        
        self.performance_history = []
        self.completed_topics = set()
    
    def record_performance(
        self,
        topic: str,
        score: float,
        feedback: str
    ) -> None:
        """Record performance on a topic.
        
        Args:
            topic: Topic practiced
            score: Performance score
            feedback: Feedback text
        """
        self.performance_history.append({
            "topic": topic,
            "score": score,
            "feedback": feedback,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.completed_topics.add(topic)
        self.updated_at = datetime.utcnow().isoformat()
    
    def get_average_score(self, topic: str = None) -> float:
        """Get average score for topic.
        
        Args:
            topic: Optional topic filter
            
        Returns:
            Average score
        """
        if not self.performance_history:
            return 0.0
        
        relevant = [
            p for p in self.performance_history
            if topic is None or p["topic"] == topic
        ]
        
        if not relevant:
            return 0.0
        
        return sum(p["score"] for p in relevant) / len(relevant)
