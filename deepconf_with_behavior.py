#!/usr/bin/env python3
"""
DeepConf-Behavior: Unified Framework for Confidence-Aware Reasoning and Behavioral Analysis
====================================================================================

This module integrates TrajectoryConfidenceAnalyzer behavioral analysis
into the DeepConf framework, providing enhanced confidence analysis and
behavioral trajectory analysis capabilities.

Key Features:
- Inherits all original DeepConf functionality
- Behavioral trajectory generation and analysis
- Multi-modal data fusion
- Anomaly detection and early termination
- Visualization report generation
- Batch behavioral analysis
- Asynchronous processing

Usage Example:
    from deepconf_with_behavior import DeepConfBehaviorAnalyzer
    
    analyzer = DeepConfBehaviorAnalyzer(
        deepconf_config={'model_backend': 'ollama', 'model_name': 'qwen:0.6b'},
        behavior_config={'multimodal_sources': ['text', 'profile']},
        model_backend='ollama',
        model_name='qwen:0.6b'
    )
    
    # Original DeepConf functionality
    result = analyzer.run_deepconf("Analyze quantum computing applications")
    
    # New behavioral analysis functionality
    profile = {"name": "Zhang San", "age": 28, "major": "Computer Science"}
    behavior_result = await analyzer.analyze_behavior(profile)
    
    # Integrated analysis
    integrated_result = await analyzer.integrated_analysis(
        prompt="How to improve programming skills?",
        profile_data=profile,
        multimodal_sources=['user_history', 'preferences']
    )

Author: Qiang Zhang
Affiliation: Beijing Zhicheng Yunhui Technology Co., Ltd. · R&D Center
Contact: hrbzhq@163.com
GitHub: https://github.com/hrbzhq/deepconf-behavior
"""

import asyncio
import logging
import time
import json
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from pathlib import Path

# Import original DeepConf functionality
try:
    from deepconf_complete import (
        DeepConfRunner, DeepConfConfig, GenerationOutput,
        create_deepconf_runner
    )
except ImportError:
    logging.error("DeepConf module not found. Please ensure deepconf_complete.py is available.")
    raise

# Import behavioral analysis extension
try:
    from extensions.behavior_analysis import TrajectoryConfidenceAnalyzer
    BEHAVIOR_ANALYSIS_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Behavioral analysis extension not available: {e}")
    BEHAVIOR_ANALYSIS_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class IntegratedAnalysisResult:
    """Result structure for integrated analysis."""
    # Core metrics
    integrated_confidence: float
    analysis_consistency: float
    recommendation_score: float
    processing_time: float
    
    # Component results
    deepconf_result: Optional[Dict[str, Any]] = None
    behavior_result: Optional[Dict[str, Any]] = None
    
    # Analysis metadata
    timestamp: str = ""
    model_info: Dict[str, str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


class DeepConfBehaviorAnalyzer:
    """
    Unified analyzer combining DeepConf reasoning with behavioral trajectory analysis.
    
    This class integrates multi-path reasoning capabilities from DeepConf with
    behavioral pattern analysis, providing comprehensive AI decision-making support
    with enhanced confidence estimation and interpretability.
    """
    
    def __init__(self,
                 deepconf_config: Optional[Dict[str, Any]] = None,
                 behavior_config: Optional[Dict[str, Any]] = None,
                 model_backend: str = 'ollama',
                 model_name: str = 'qwen:0.6b'):
        """
        Initialize the integrated analyzer.
        
        Args:
            deepconf_config: Configuration for DeepConf reasoning
            behavior_config: Configuration for behavioral analysis
            model_backend: Backend for model inference ('ollama', 'hf', etc.)
            model_name: Name of the language model to use
        """
        self.model_backend = model_backend
        self.model_name = model_name
        
        # Initialize DeepConf runner
        self.deepconf_config = deepconf_config or {
            'model_backend': model_backend,
            'model_name': model_name,
            'num_paths': 8,
            'keep_ratio': 0.8,
            'temperature': 0.7
        }
        
        try:
            self.deepconf_runner = create_deepconf_runner(self.deepconf_config)
            logger.info(f"DeepConf runner initialized with {model_backend}:{model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize DeepConf runner: {e}")
            self.deepconf_runner = None
        
        # Initialize behavioral analyzer
        if BEHAVIOR_ANALYSIS_AVAILABLE:
            self.behavior_config = behavior_config or {
                'multimodal_sources': ['text', 'profile', 'history'],
                'confidence_threshold': 0.7,
                'max_trajectory_length': 10
            }
            
            try:
                self.behavior_analyzer = TrajectoryConfidenceAnalyzer()
                logger.info("Behavioral analysis module initialized")
            except Exception as e:
                logger.error(f"Failed to initialize behavioral analyzer: {e}")
                self.behavior_analyzer = None
        else:
            self.behavior_analyzer = None
            logger.warning("Behavioral analysis not available")
    
    def run_deepconf(self, prompt: str, **kwargs) -> Optional[GenerationOutput]:
        """
        Run DeepConf multi-path reasoning analysis.
        
        Args:
            prompt: Input prompt for reasoning
            **kwargs: Additional arguments for DeepConf
            
        Returns:
            GenerationOutput with reasoning results and confidence scores
        """
        if not self.deepconf_runner:
            logger.error("DeepConf runner not available")
            return None
        
        try:
            start_time = time.time()
            result = self.deepconf_runner.generate(prompt, **kwargs)
            processing_time = time.time() - start_time
            
            logger.info(f"DeepConf analysis completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"DeepConf analysis failed: {e}")
            return None
    
    async def analyze_behavior(self,
                              profile_data: Dict[str, Any],
                              multimodal_sources: Optional[List[str]] = None) -> Optional[Dict[str, Any]]:
        """
        Run behavioral trajectory analysis.
        
        Args:
            profile_data: User profile and behavioral data
            multimodal_sources: List of data sources to analyze
            
        Returns:
            Dictionary containing behavioral analysis results
        """
        if not self.behavior_analyzer:
            logger.error("Behavioral analyzer not available")
            return None
        
        try:
            start_time = time.time()
            
            # Use provided sources or default from config
            sources = multimodal_sources or self.behavior_config.get('multimodal_sources', ['text'])
            
            # Run behavioral analysis
            result = await self.behavior_analyzer.analyze_trajectory(
                profile_data=profile_data,
                multimodal_sources=sources
            )
            
            processing_time = time.time() - start_time
            result['processing_time'] = processing_time
            
            logger.info(f"Behavioral analysis completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Behavioral analysis failed: {e}")
            return None
    
    async def integrated_analysis(self,
                                 prompt: str,
                                 profile_data: Dict[str, Any],
                                 multimodal_sources: Optional[List[str]] = None) -> IntegratedAnalysisResult:
        """
        Run integrated analysis combining DeepConf reasoning and behavioral analysis.
        
        Args:
            prompt: Input prompt for reasoning
            profile_data: User profile and behavioral data
            multimodal_sources: List of data sources to analyze
            
        Returns:
            IntegratedAnalysisResult with comprehensive analysis results
        """
        start_time = time.time()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f"Starting integrated analysis at {timestamp}")
        
        try:
            # Run both analyses concurrently
            deepconf_task = asyncio.to_thread(self.run_deepconf, prompt)
            behavior_task = self.analyze_behavior(profile_data, multimodal_sources)
            
            # Wait for both to complete
            deepconf_result, behavior_result = await asyncio.gather(
                deepconf_task, behavior_task, return_exceptions=True
            )
            
            # Handle exceptions
            if isinstance(deepconf_result, Exception):
                logger.error(f"DeepConf analysis failed: {deepconf_result}")
                deepconf_result = None
            
            if isinstance(behavior_result, Exception):
                logger.error(f"Behavioral analysis failed: {behavior_result}")
                behavior_result = None
            
            # Integrate results and compute metrics
            integrated_result = self._integrate_results(deepconf_result, behavior_result)
            
            processing_time = time.time() - start_time
            
            # Create final result
            result = IntegratedAnalysisResult(
                integrated_confidence=integrated_result['integrated_confidence'],
                analysis_consistency=integrated_result['analysis_consistency'],
                recommendation_score=integrated_result['recommendation_score'],
                processing_time=processing_time,
                deepconf_result=self._serialize_deepconf_result(deepconf_result),
                behavior_result=behavior_result,
                timestamp=timestamp,
                model_info={
                    'backend': self.model_backend,
                    'model': self.model_name
                }
            )
            
            logger.info(f"Integrated analysis completed in {processing_time:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Integrated analysis failed: {e}")
            # Return default result in case of failure
            return IntegratedAnalysisResult(
                integrated_confidence=0.0,
                analysis_consistency=0.0,
                recommendation_score=0.0,
                processing_time=time.time() - start_time,
                timestamp=timestamp,
                model_info={'backend': self.model_backend, 'model': self.model_name}
            )
    
    def _integrate_results(self,
                          deepconf_result: Optional[GenerationOutput],
                          behavior_result: Optional[Dict[str, Any]]) -> Dict[str, float]:
        """
        Integrate results from both DeepConf and behavioral analysis.
        
        Args:
            deepconf_result: Results from DeepConf reasoning
            behavior_result: Results from behavioral analysis
            
        Returns:
            Dictionary with integrated metrics
        """
        # Extract confidence scores
        deepconf_confidence = 0.5  # Default
        behavior_confidence = 0.5  # Default
        
        if deepconf_result and hasattr(deepconf_result, 'average_confidence'):
            deepconf_confidence = deepconf_result.average_confidence
        
        if behavior_result and 'confidence_score' in behavior_result:
            behavior_confidence = behavior_result['confidence_score']
        
        # Compute integrated metrics using weighted combination
        alpha, beta, gamma = 0.4, 0.3, 0.3  # Weights for integration
        
        # Consistency measure (how well the two analyses agree)
        consistency = 1.0 - abs(deepconf_confidence - behavior_confidence)
        
        # Integrated confidence
        integrated_confidence = (
            alpha * deepconf_confidence +
            beta * behavior_confidence +
            gamma * consistency
        )
        
        # Recommendation score (quality of actionable insights)
        recommendation_score = integrated_confidence
        if behavior_result and 'recommendation_quality' in behavior_result:
            recommendation_score = (
                0.6 * integrated_confidence +
                0.4 * behavior_result['recommendation_quality']
            )
        
        return {
            'integrated_confidence': integrated_confidence,
            'analysis_consistency': consistency,
            'recommendation_score': recommendation_score
        }
    
    def _serialize_deepconf_result(self, result: Optional[GenerationOutput]) -> Optional[Dict[str, Any]]:
        """
        Serialize DeepConf result to dictionary format.
        
        Args:
            result: DeepConf GenerationOutput object
            
        Returns:
            Serialized result dictionary
        """
        if not result:
            return None
        
        try:
            return {
                'final_answer': getattr(result, 'final_answer', ''),
                'average_confidence': getattr(result, 'average_confidence', 0.0),
                'reasoning_paths': getattr(result, 'reasoning_paths', []),
                'model_info': getattr(result, 'model_info', {})
            }
        except Exception as e:
            logger.warning(f"Failed to serialize DeepConf result: {e}")
            return {'error': str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the analyzer.
        
        Returns:
            Dictionary with status information
        """
        return {
            'deepconf_available': self.deepconf_runner is not None,
            'behavior_analysis_available': self.behavior_analyzer is not None,
            'model_backend': self.model_backend,
            'model_name': self.model_name,
            'version': '1.0.0'
        }


# Convenience function for quick access
def create_analyzer(model_backend: str = 'ollama', model_name: str = 'qwen:0.6b') -> DeepConfBehaviorAnalyzer:
    """
    Create a DeepConf-Behavior analyzer with default configuration.
    
    Args:
        model_backend: Backend for model inference
        model_name: Name of the language model
        
    Returns:
        Configured DeepConfBehaviorAnalyzer instance
    """
    return DeepConfBehaviorAnalyzer(
        model_backend=model_backend,
        model_name=model_name
    )


if __name__ == "__main__":
    # Example usage
    async def main():
        # Initialize analyzer
        analyzer = create_analyzer()
        
        # Check status
        status = analyzer.get_status()
        print(f"Analyzer Status: {json.dumps(status, indent=2)}")
        
        # Example profile data
        profile = {
            "name": "Test User",
            "age": 28,
            "background": "Computer Science",
            "experience_level": "intermediate",
            "goals": ["career_growth", "skill_development"],
            "preferences": ["hands_on_learning", "project_based"]
        }
        
        # Run integrated analysis
        result = await analyzer.integrated_analysis(
            prompt="How can I improve my programming skills to advance my career?",
            profile_data=profile,
            multimodal_sources=['text', 'profile']
        )
        
        # Display results
        print("\n=== Integrated Analysis Results ===")
        print(f"Integrated Confidence: {result.integrated_confidence:.3f}")
        print(f"Analysis Consistency: {result.analysis_consistency:.3f}")
        print(f"Recommendation Score: {result.recommendation_score:.3f}")
        print(f"Processing Time: {result.processing_time:.2f}s")
        
        # Save results
        with open('integrated_analysis_result.json', 'w', encoding='utf-8') as f:
            f.write(result.to_json())
        
        print("\nResults saved to integrated_analysis_result.json")
    
    # Run the example
    asyncio.run(main())