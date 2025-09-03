#!/usr/bin/env python3
"""
Simplified Benchmark Suite - For Paper Data Generation
======================================================
"""

import asyncio
import json
import time
import statistics
from pathlib import Path
from datetime import datetime
import pandas as pd

from deepconf_with_behavior import create_integrated_analyzer

# Embedded test data
test_cases = [
    {
        "prompt": "Create a personalized machine learning learning path for someone with weak foundation but strong learning ability",
        "profile": {
            "name": "Alex Lee",
            "age": 24,
            "major": "Computer Science",
            "current_skills": ["Python basics", "Data structures"],
            "goal": "Become a machine learning engineer",
            "learning_style": "Practice-oriented"
        },
        "domain": "education",
        "expected_confidence": 0.75
    },
    {
        "prompt": "Analyze the feasibility and path for a software engineer transitioning to technical management",
        "profile": {
            "name": "Jordan Smith",
            "age": 32,
            "years_experience": 8,
            "current_position": "Senior Software Engineer",
            "management_experience": "Team Lead for 2 years",
            "goal": "Technical Director"
        },
        "domain": "career",
        "expected_confidence": 0.80
    },
    {
        "prompt": "Develop a comprehensive health improvement plan for sedentary programmers",
        "profile": {
            "name": "Sam Chen",
            "age": 29,
            "occupation": "Software Developer",
            "health_status": {
                "BMI": 26.5,
                "exercise_habits": "Rarely exercises",
                "sleep_quality": "Frequent late nights"
            },
            "goal": "Improve overall health"
        },
        "domain": "lifestyle",
        "expected_confidence": 0.65
    },
    {
        "prompt": "Evaluate the business plan feasibility for tech entrepreneurs entering the SaaS market", 
        "profile": {
            "name": "Taylor Wong",
            "age": 35,
            "background": "Former big tech CTO",
            "product_idea": "Project management SaaS for SMEs",
            "risk_tolerance": "Medium"
        },
        "domain": "business",
        "expected_confidence": 0.55
    },
    {
        "prompt": "Create research direction selection and publication strategy for computer vision PhD students",
        "profile": {
            "name": "Riley Park",
            "age": 26,
            "education": "Master's student",
            "research_interests": ["Object detection", "Image segmentation"],
            "goal": "Top-tier conference publications"
        },
        "domain": "research",
        "expected_confidence": 0.85
    },
    {
        "prompt": "Develop workplace social skills improvement plan for introverted tech professionals",
        "profile": {
            "name": "Casey Kim",
            "age": 27,
            "personality": "Introverted, not good at expression",
            "position": "Backend Developer",
            "goal": "Enhance workplace influence"
        },
        "domain": "social",
        "expected_confidence": 0.70
    }
]

async def run_benchmark():
    """Run benchmark testing"""
    print("🚀 Starting DeepConf-Behavior Benchmark")
    print("=" * 50)
    
    analyzer = create_integrated_analyzer()
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}/{len(test_cases)}: {test_case['domain']}")
        print(f"   User: {test_case['profile'].get('name', 'Unknown')}")
        
        start_time = time.time()
        
        try:
            result = await analyzer.integrated_analysis(
                prompt=test_case['prompt'],
                profile_data=test_case['profile']
            )
            
            execution_time = time.time() - start_time
            
            test_result = {
                'test_id': f"test_{i:03d}",
                'domain': test_case['domain'],
                'integrated_confidence': result.integrated_confidence,
                'analysis_consistency': result.analysis_consistency,
                'recommendation_score': result.recommendation_score,
                'deepconf_confidence': result.deepconf_confidence,
                'behavior_paths_count': len(result.behavior_paths) if result.behavior_paths else 0,
                'execution_time': execution_time,
                'expected_confidence': test_case['expected_confidence'],
                'confidence_error': abs(result.integrated_confidence - test_case['expected_confidence']),
                'status': 'success'
            }
            
            results.append(test_result)
            
            print(f"   ✅ Completed - Confidence: {result.integrated_confidence:.3f} (Expected: {test_case['expected_confidence']:.3f})")
            print(f"   ⏱️ Duration: {execution_time:.1f}s")
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
            results.append({
                'test_id': f"test_{i:03d}",
                'domain': test_case['domain'],
                'error': str(e),
                'execution_time': time.time() - start_time,
                'status': 'failed'
            })
        
        # Avoid too frequent requests
        await asyncio.sleep(2)
    
    # Analyze results
    successful_results = [r for r in results if r['status'] == 'success']
    
    print("\n" + "=" * 50)
    print("📊 Benchmark Results")
    print("=" * 50)
    
    if successful_results:
        # Basic statistics
        confidences = [r['integrated_confidence'] for r in successful_results]
        consistencies = [r['analysis_consistency'] for r in successful_results]
        exec_times = [r['execution_time'] for r in successful_results]
        errors = [r['confidence_error'] for r in successful_results]
        
        print(f"✅ Success Rate: {len(successful_results)}/{len(results)} ({len(successful_results)/len(results)*100:.1f}%)")
        print(f"📈 Average Confidence: {statistics.mean(confidences):.3f} ± {statistics.stdev(confidences) if len(confidences) > 1 else 0:.3f}")
        print(f"🔄 Average Consistency: {statistics.mean(consistencies):.3f} ± {statistics.stdev(consistencies) if len(consistencies) > 1 else 0:.3f}")
        print(f"⏱️ Average Execution Time: {statistics.mean(exec_times):.1f}s ± {statistics.stdev(exec_times) if len(exec_times) > 1 else 0:.1f}s")
        print(f"🎯 Average Prediction Error: {statistics.mean(errors):.3f}")
        
        # Domain statistics
        domain_stats = {}
        for result in successful_results:
            domain = result['domain']
            if domain not in domain_stats:
                domain_stats[domain] = []
            domain_stats[domain].append(result)
        
        print(f"\n📈 Domain Statistics:")
        for domain, domain_results in domain_stats.items():
            domain_confidences = [r['integrated_confidence'] for r in domain_results]
            avg_conf = statistics.mean(domain_confidences)
            print(f"  {domain}: Average confidence {avg_conf:.3f} ({len(domain_results)} tests)")
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path("benchmark_results")
    results_dir.mkdir(exist_ok=True)
    
    # Save raw data
    with open(results_dir / f"benchmark_results_{timestamp}.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    # Save CSV format
    if results:
        df = pd.DataFrame(results)
        df.to_csv(results_dir / f"benchmark_summary_{timestamp}.csv", index=False)
    
    print(f"\n💾 Results saved:")
    print(f"   JSON: benchmark_results/benchmark_results_{timestamp}.json")
    print(f"   CSV: benchmark_results/benchmark_summary_{timestamp}.csv")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_benchmark())