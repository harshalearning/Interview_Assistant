"""Data module for datasets, vectors stores, and assets management."""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

class DataManager:
    """Manage data files and assets."""
    
    def __init__(self, base_path: str = "data"):
        """Initialize data manager.
        
        Args:
            base_path: Base path for data storage
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (self.base_path / "datasets").mkdir(exist_ok=True)
        (self.base_path / "vectors").mkdir(exist_ok=True)
        (self.base_path / "audio").mkdir(exist_ok=True)
        (self.base_path / "cache").mkdir(exist_ok=True)
    
    def save_json(self, filename: str, data: dict, subdir: str = None) -> bool:
        """Save data as JSON.
        
        Args:
            filename: File name
            data: Data to save
            subdir: Subdirectory (datasets, vectors, etc.)
            
        Returns:
            Success status
        """
        try:
            if subdir:
                filepath = self.base_path / subdir / filename
            else:
                filepath = self.base_path / filename
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    def load_json(self, filename: str, subdir: str = None) -> Optional[dict]:
        """Load JSON file.
        
        Args:
            filename: File name
            subdir: Subdirectory
            
        Returns:
            Loaded data or None
        """
        try:
            if subdir:
                filepath = self.base_path / subdir / filename
            else:
                filepath = self.base_path / filename
            
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON: {e}")
            return None


class DatasetManager:
    """Manage interview datasets."""
    
    def __init__(self):
        """Initialize dataset manager."""
        self.datasets: Dict[str, dict] = {}
    
    def create_dataset(
        self,
        name: str,
        description: str,
        category: str
    ) -> dict:
        """Create a new dataset.
        
        Args:
            name: Dataset name
            description: Description
            category: Category (e.g., 'python', 'javascript', 'sql')
            
        Returns:
            Created dataset metadata
        """
        dataset_id = f"{category}_{name}".lower().replace(" ", "_")
        
        dataset = {
            "id": dataset_id,
            "name": name,
            "description": description,
            "category": category,
            "created_at": datetime.utcnow().isoformat(),
            "questions": [],
            "metadata": {
                "total_questions": 0,
                "languages": [],
                "difficulty_distribution": {}
            }
        }
        
        self.datasets[dataset_id] = dataset
        return dataset
    
    def add_question_to_dataset(
        self,
        dataset_id: str,
        question: str,
        answer: str,
        difficulty: str,
        tags: List[str] = None
    ) -> bool:
        """Add question to dataset.
        
        Args:
            dataset_id: Dataset ID
            question: Question text
            answer: Expected answer/explanation
            difficulty: Difficulty level
            tags: Question tags
            
        Returns:
            Success status
        """
        if dataset_id not in self.datasets:
            return False
        
        question_entry = {
            "question": question,
            "answer": answer,
            "difficulty": difficulty,
            "tags": tags or [],
            "added_at": datetime.utcnow().isoformat()
        }
        
        self.datasets[dataset_id]["questions"].append(question_entry)
        self.datasets[dataset_id]["metadata"]["total_questions"] += 1
        
        # Update difficulty distribution
        diff_dist = self.datasets[dataset_id]["metadata"]["difficulty_distribution"]
        diff_dist[difficulty] = diff_dist.get(difficulty, 0) + 1
        
        return True
    
    def get_dataset(self, dataset_id: str) -> Optional[dict]:
        """Get dataset by ID.
        
        Args:
            dataset_id: Dataset ID
            
        Returns:
            Dataset or None
        """
        return self.datasets.get(dataset_id)
    
    def get_questions_by_difficulty(
        self,
        dataset_id: str,
        difficulty: str
    ) -> List[dict]:
        """Get questions by difficulty.
        
        Args:
            dataset_id: Dataset ID
            difficulty: Difficulty level
            
        Returns:
            List of questions
        """
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            return []
        
        return [
            q for q in dataset["questions"]
            if q["difficulty"] == difficulty
        ]


class VectorStoreManager:
    """Manage vector store operations."""
    
    def __init__(self):
        """Initialize vector store manager."""
        self.metadata: Dict[str, dict] = {}
    
    def create_collection(
        self,
        name: str,
        description: str,
        embedding_model: str = "all-MiniLM-L6-v2"
    ) -> dict:
        """Create vector collection.
        
        Args:
            name: Collection name
            description: Description
            embedding_model: Embedding model
            
        Returns:
            Collection metadata
        """
        collection = {
            "name": name,
            "description": description,
            "embedding_model": embedding_model,
            "created_at": datetime.utcnow().isoformat(),
            "vectors": 0,
            "last_updated": datetime.utcnow().isoformat()
        }
        
        self.metadata[name] = collection
        return collection
    
    def update_collection_stats(
        self,
        name: str,
        vector_count: int
    ) -> bool:
        """Update collection statistics.
        
        Args:
            name: Collection name
            vector_count: Number of vectors
            
        Returns:
            Success status
        """
        if name not in self.metadata:
            return False
        
        self.metadata[name]["vectors"] = vector_count
        self.metadata[name]["last_updated"] = datetime.utcnow().isoformat()
        return True
    
    def get_collection_info(self, name: str) -> Optional[dict]:
        """Get collection information.
        
        Args:
            name: Collection name
            
        Returns:
            Collection info or None
        """
        return self.metadata.get(name)


class AudioAssetManager:
    """Manage audio files and metadata."""
    
    def __init__(self):
        """Initialize audio asset manager."""
        self.audio_files: Dict[str, dict] = {}
    
    def register_audio(
        self,
        audio_id: str,
        filename: str,
        duration: float,
        format: str = "wav"
    ) -> dict:
        """Register audio file.
        
        Args:
            audio_id: Unique audio ID
            filename: File name
            duration: Duration in seconds
            format: File format
            
        Returns:
            Audio metadata
        """
        metadata = {
            "id": audio_id,
            "filename": filename,
            "duration": duration,
            "format": format,
            "registered_at": datetime.utcnow().isoformat(),
            "path": f"data/audio/{filename}"
        }
        
        self.audio_files[audio_id] = metadata
        return metadata
    
    def get_audio_info(self, audio_id: str) -> Optional[dict]:
        """Get audio file information.
        
        Args:
            audio_id: Audio ID
            
        Returns:
            Audio metadata or None
        """
        return self.audio_files.get(audio_id)
    
    def list_audio_files(self) -> List[dict]:
        """List all registered audio files.
        
        Returns:
            List of audio metadata
        """
        return list(self.audio_files.values())


class CacheManager:
    """Manage caching of frequently accessed data."""
    
    def __init__(self, ttl: int = 3600):
        """Initialize cache manager.
        
        Args:
            ttl: Time to live in seconds
        """
        self.cache: Dict[str, dict] = {}
        self.ttl = ttl
    
    def set(self, key: str, value: Any) -> None:
        """Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self.cache[key] = {
            "value": value,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None
        """
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        
        # Check TTL
        timestamp = datetime.fromisoformat(entry["timestamp"])
        if (datetime.utcnow() - timestamp).seconds > self.ttl:
            del self.cache[key]
            return None
        
        return entry["value"]
    
    def clear(self) -> None:
        """Clear all cache."""
        self.cache.clear()
    
    def remove(self, key: str) -> bool:
        """Remove specific cache entry.
        
        Args:
            key: Cache key
            
        Returns:
            Success status
        """
        if key in self.cache:
            del self.cache[key]
            return True
        return False
