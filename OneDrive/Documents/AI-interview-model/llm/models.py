"""LLM module for model integration and prompt engineering."""

from typing import Any, List, Dict
import json
from datetime import datetime

from config import settings

class PromptTemplate:
    """Template for generating prompts."""
    
    def __init__(self, template: str, variables: List[str]):
        """Initialize prompt template.
        
        Args:
            template: Template string with {variable} placeholders
            variables: List of required variables
        """
        self.template = template
        self.variables = variables
    
    def format(self, **kwargs) -> str:
        """Format template with provided variables.
        
        Args:
            **kwargs: Variables to fill in template
            
        Returns:
            Formatted prompt string
        """
        return self.template.format(**kwargs)


class InterviewQuestionGenerator:
    """Generate interview questions based on topic and difficulty."""
    
    def __init__(self):
        """Initialize question generator."""
        self.templates = {
            "easy": [
                "What is {topic}?",
                "Can you explain {topic} in simple terms?",
                "What are the basics of {topic}?",
                "Why is {topic} important?",
                "Give an example of {topic}."
            ],
            "medium": [
                "How does {topic} work in practice?",
                "What are the key components of {topic}?",
                "Compare and contrast different approaches to {topic}.",
                "What challenges exist with {topic}?",
                "How would you implement {topic}?"
            ],
            "hard": [
                "Design a system that uses {topic}.",
                "What are the edge cases in {topic}?",
                "How would you optimize {topic} for performance?",
                "Discuss the trade-offs in {topic}.",
                "How does {topic} scale to large datasets?"
            ]
        }
    
    def generate_question(self, topic: str, difficulty: str = "medium") -> str:
        """Generate a question for given topic and difficulty.
        
        Args:
            topic: Interview topic
            difficulty: Question difficulty (easy, medium, hard)
            
        Returns:
            Generated question
        """
        import random
        
        if difficulty not in self.templates:
            difficulty = "medium"
        
        template = random.choice(self.templates[difficulty])
        return template.format(topic=topic)


class OllamaClient:
    """Client for interacting with Ollama LLM."""
    
    def __init__(self, base_url: str = settings.ollama_base_url):
        """Initialize Ollama client.
        
        Args:
            base_url: Base URL of Ollama service
        """
        self.base_url = base_url
        try:
            import ollama
            self.client = ollama.Client(host=base_url)
            self.available = True
        except Exception as e:
            print(f"Ollama client initialization warning: {e}")
            self.client = None
            self.available = False
    
    async def generate_response(
        self,
        prompt: str,
        model: Any = None,
        temperature: Any = None,
        max_tokens: Any = None
    ) -> dict:
        """Generate a response using Ollama.
        
        Args:
            prompt: Input prompt
            model: Model name
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum response length
            
        Returns:
            Generated response and metadata
        """
        if not self.available or not self.client:
            return {
                "error": "Ollama client not available",
                "response": "Using mock response"
            }

        selected_model: str = str(model or settings.ollama_default_model)
        selected_temperature: float = (
            float(temperature)
            if temperature is not None and float(temperature) > 0
            else settings.ollama_default_temperature
        )
        selected_max_tokens: int = (
            int(max_tokens)
            if max_tokens is not None and int(max_tokens) > 0
            else settings.ollama_max_tokens
        )
        
        try:
            response = self.client.generate(
                model=selected_model,
                prompt=prompt,
                stream=False,
                options={
                    "temperature": selected_temperature,
                    "num_predict": selected_max_tokens
                }
            )
            return {
                "response": response['response'],
                "model": selected_model,
                "created_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"error": str(e), "response": "Error generating response"}

    async def list_models(self) -> dict:
        """List available Ollama models."""
        if not self.available or not self.client:
            return {"error": "Ollama client not available", "models": []}

        try:
            response: Any = self.client.list()
            raw_models: List[Any] = []

            if isinstance(response, dict):
                raw_models = response.get("models") or response.get("data") or []
            elif hasattr(response, "models"):
                raw_models = list(getattr(response, "models", []) or [])
            elif isinstance(response, (list, tuple)):
                raw_models = list(response)
            else:
                raw_models = [response]

            model_names: List[str] = []
            for model in raw_models:
                if isinstance(model, dict):
                    model_name = model.get("name") or model.get("model")
                else:
                    model_name = str(model)

                if model_name:
                    model_names.append(str(model_name))

            return {
                "status": "ok",
                "base_url": self.base_url,
                "models": model_names,
                "count": len(model_names)
            }
        except Exception as e:
            return {"status": "error", "error": str(e), "models": []}

    async def health_check(self) -> dict:
        """Check whether Ollama is reachable and running."""
        if not self.available or not self.client:
            return {"status": "error", "error": "Ollama client not available"}

        try:
            model_list = await self.list_models()
            return {
                "status": "ok" if model_list.get("status") == "ok" else "error",
                "base_url": self.base_url,
                "model_count": model_list.get("count", 0),
                "models": model_list.get("models", []),
                "error": model_list.get("error")
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def evaluate_answer(
        self,
        question: str,
        answer: str,
        model: Any = None
    ) -> dict:
        """Evaluate an interview answer.
        
        Args:
            question: Interview question
            answer: User's answer
            model: Model to use for evaluation
            
        Returns:
            Evaluation result with score and feedback
        """
        evaluation_prompt = f"""Evaluate this interview answer on a scale of 1-10:

Question: {question}
Answer: {answer}

Provide:
1. Score (1-10)
2. Strengths (2-3 points)
3. Areas for improvement (2-3 points)
4. Suggested better answer

Format as JSON with keys: score, strengths, improvements, suggested_answer"""
        
        response = await self.generate_response(evaluation_prompt, model=model)
        
        return {
            "evaluation": response.get("response", ""),
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        }


class PromptEngineer:
    """Manage and optimize prompts for LLM."""
    
    def __init__(self):
        """Initialize prompt engineer."""
        self.prompt_history = []
        self.performance_metrics = {}
    
    def create_system_prompt(self, role: str = "interviewer") -> str:
        """Create a system prompt for given role.
        
        Args:
            role: Role type (interviewer, evaluator, etc.)
            
        Returns:
            System prompt
        """
        prompts = {
            "interviewer": """You are an experienced technical interviewer. Your job is to:
1. Ask clear, relevant technical questions
2. Encourage detailed answers
3. Follow up on incomplete responses
4. Assess the candidate's knowledge and communication skills""",
            
            "evaluator": """You are an expert technical evaluator. Assess responses based on:
1. Correctness and accuracy
2. Clarity and communication
3. Problem-solving approach
4. Knowledge depth and breadth""",
            
            "coach": """You are a supportive interview coach. Help candidates by:
1. Explaining concepts clearly
2. Suggesting better ways to answer
3. Highlighting strengths
4. Providing constructive feedback"""
        }
        
        return prompts.get(role, prompts["interviewer"])
    
    def optimize_prompt(self, prompt: str, feedback: str) -> str:
        """Optimize prompt based on feedback.
        
        Args:
            prompt: Original prompt
            feedback: Feedback on performance
            
        Returns:
            Optimized prompt
        """
        # Store for analysis
        self.prompt_history.append({
            "original": prompt,
            "feedback": feedback,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Simple optimization rules
        if "too vague" in feedback.lower():
            return prompt + "\nBe more specific and concise."
        elif "too long" in feedback.lower():
            return "Summarize the following in 1-2 sentences: " + prompt
        else:
            return prompt
