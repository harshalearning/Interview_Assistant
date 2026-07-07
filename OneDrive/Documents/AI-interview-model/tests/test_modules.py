"""Unit tests for core modules."""

import pytest
from speech.processor import AudioProcessor, SpeechToText
from llm.models import PromptTemplate, InterviewQuestionGenerator, PromptEngineer
from memory.session import ConversationMemory, SessionState, UserProfile
from data.manager import DatasetManager, VectorStoreManager, CacheManager
from rag.retrieval import EmbeddingGenerator, KnowledgeBase


class TestAudioProcessor:
    """Test audio processing."""
    
    def test_normalize_audio(self):
        """Test audio normalization."""
        import numpy as np
        processor = AudioProcessor()
        
        # Test with sample audio
        audio = np.array([0.5, -0.5, 1.0, -1.0])
        normalized = processor.normalize_audio(audio)
        
        assert np.allclose(np.max(np.abs(normalized)), 1.0)


class TestPromptTemplate:
    """Test prompt templating."""
    
    def test_format_prompt(self):
        """Test prompt formatting."""
        template = PromptTemplate(
            "What is {topic}?",
            ["topic"]
        )
        result = template.format(topic="Python")
        assert result == "What is Python?"
    
    def test_format_with_multiple_vars(self):
        """Test formatting with multiple variables."""
        template = PromptTemplate(
            "Explain {concept} in {language}",
            ["concept", "language"]
        )
        result = template.format(concept="OOP", language="Python")
        assert result == "Explain OOP in Python"


class TestInterviewQuestionGenerator:
    """Test question generation."""
    
    def test_generate_easy_question(self):
        """Test easy question generation."""
        generator = InterviewQuestionGenerator()
        question = generator.generate_question("Python", difficulty="easy")
        assert len(question) > 0
        assert "Python" in question
    
    def test_generate_hard_question(self):
        """Test hard question generation."""
        generator = InterviewQuestionGenerator()
        question = generator.generate_question("Python", difficulty="hard")
        assert len(question) > 0
        assert "Python" in question


class TestConversationMemory:
    """Test conversation memory."""
    
    def test_add_message(self):
        """Test adding messages."""
        memory = ConversationMemory()
        memory.add_message("user", "Hello")
        
        messages = memory.get_messages()
        assert len(messages) == 1
        assert messages[0]["content"] == "Hello"
    
    def test_max_history(self):
        """Test max history enforcement."""
        memory = ConversationMemory(max_history=5)
        
        for i in range(10):
            memory.add_message("user", f"Message {i}")
        
        messages = memory.get_messages()
        assert len(messages) == 5


class TestSessionState:
    """Test session state management."""
    
    def test_create_session(self):
        """Test session creation."""
        session = SessionState("sess1", "user1", "Python")
        assert session.session_id == "sess1"
        assert session.status == "active"
    
    def test_update_metric(self):
        """Test metric updates."""
        session = SessionState("sess1", "user1", "Python")
        session.update_metric("questions_asked", 5)
        
        assert session.metrics["questions_asked"] == 5
    
    def test_increment_metric(self):
        """Test metric incrementing."""
        session = SessionState("sess1", "user1", "Python")
        session.increment_metric("questions_asked", 1)
        session.increment_metric("questions_asked", 1)
        
        assert session.metrics["questions_asked"] == 2


class TestUserProfile:
    """Test user profile."""
    
    def test_create_profile(self):
        """Test profile creation."""
        profile = UserProfile("user1")
        assert profile.user_id == "user1"
        assert profile.preferences["difficulty"] == "medium"
    
    def test_record_performance(self):
        """Test recording performance."""
        profile = UserProfile("user1")
        profile.record_performance("Python", 8.5, "Good job!")
        
        assert len(profile.performance_history) == 1
        assert profile.performance_history[0]["score"] == 8.5
    
    def test_average_score(self):
        """Test average score calculation."""
        profile = UserProfile("user1")
        profile.record_performance("Python", 8.0, "Good")
        profile.record_performance("Python", 9.0, "Great")
        
        avg = profile.get_average_score("Python")
        assert avg == 8.5


class TestDatasetManager:
    """Test dataset management."""
    
    def test_create_dataset(self):
        """Test dataset creation."""
        manager = DatasetManager()
        dataset = manager.create_dataset(
            "Python Basics",
            "Basic Python questions",
            "python"
        )
        
        assert dataset["name"] == "Python Basics"
        assert dataset["category"] == "python"
    
    def test_add_question(self):
        """Test adding questions to dataset."""
        manager = DatasetManager()
        dataset = manager.create_dataset(
            "Python Basics",
            "Basic questions",
            "python"
        )
        
        manager.add_question_to_dataset(
            dataset["id"],
            "What is Python?",
            "Python is a programming language",
            "easy"
        )
        
        assert dataset["metadata"]["total_questions"] == 1


class TestCacheManager:
    """Test caching."""
    
    def test_cache_set_get(self):
        """Test cache operations."""
        cache = CacheManager()
        cache.set("key1", "value1")
        
        assert cache.get("key1") == "value1"
    
    def test_cache_remove(self):
        """Test cache removal."""
        cache = CacheManager()
        cache.set("key1", "value1")
        cache.remove("key1")
        
        assert cache.get("key1") is None


class TestPromptEngineer:
    """Test prompt engineering."""
    
    def test_system_prompt(self):
        """Test system prompt creation."""
        engineer = PromptEngineer()
        prompt = engineer.create_system_prompt("interviewer")
        
        assert len(prompt) > 0
        assert "interviewer" in prompt.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
