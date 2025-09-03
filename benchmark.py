#!/usr/bin/env python3
"""
简化的基准测试 - 用于生成论文数据
==================================
"""

import asyncio
import json
import time
import statistics
from pathlib import Path
from datetime import datetime
import pandas as pd

from deepconf_with_behavior import create_integrated_analyzer

# 内嵌测试数据
test_cases = [
    {
        "prompt": "制定个人化的机器学习学习路径，考虑基础薄弱但学习能力强的情况",
        "profile": {
            "姓名": "李华",
            "年龄": 24,
            "专业": "计算机科学",
            "当前技能": ["Python基础", "数据结构"],
            "目标": "成为机器学习工程师",
            "学习风格": "实践导向"
        },
        "domain": "education",
        "expected_confidence": 0.75
    },
    {
        "prompt": "分析软件工程师向技术管理岗位转型的可行性和路径",
        "profile": {
            "姓名": "张强",
            "年龄": 32,
            "工作年限": 8,
            "当前职位": "高级软件工程师",
            "管理经验": "团队Lead 2年",
            "目标": "技术总监"
        },
        "domain": "career",
        "expected_confidence": 0.80
    },
    {
        "prompt": "为久坐程序员制定全面的健康改善计划",
        "profile": {
            "姓名": "陈晨",
            "年龄": 29,
            "职业": "软件开发工程师",
            "健康状况": {
                "BMI": 26.5,
                "运动习惯": "几乎不运动",
                "睡眠质量": "经常熬夜"
            },
            "目标": "改善整体健康状况"
        },
        "domain": "lifestyle",
        "expected_confidence": 0.65
    },
    {
        "prompt": "评估技术背景创业者进入SaaS市场的商业计划可行性", 
        "profile": {
            "姓名": "周创",
            "年龄": 35,
            "背景": "前大厂技术总监",
            "产品想法": "面向中小企业的项目管理SaaS",
            "风险承受能力": "中等"
        },
        "domain": "business",
        "expected_confidence": 0.55
    },
    {
        "prompt": "制定计算机视觉PhD学生的研究方向选择和论文发表策略",
        "profile": {
            "姓名": "李研",
            "年龄": 26,
            "学历": "硕士在读",
            "研究兴趣": ["目标检测", "图像分割"],
            "目标": "顶会论文发表"
        },
        "domain": "research",
        "expected_confidence": 0.85
    },
    {
        "prompt": "为内向型技术人员制定职场社交能力提升方案",
        "profile": {
            "姓名": "赵静",
            "年龄": 27,
            "性格": "内向，不善表达",
            "职位": "后端开发工程师",
            "目标": "提升职场影响力"
        },
        "domain": "social",
        "expected_confidence": 0.70
    }
]

async def run_benchmark():
    """运行基准测试"""
    print("🚀 开始 DeepConf-Behavior 基准测试")
    print("=" * 50)
    
    analyzer = create_integrated_analyzer()
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 测试 {i}/{len(test_cases)}: {test_case['domain']}")
        print(f"   用户: {test_case['profile'].get('姓名', 'Unknown')}")
        
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
            
            print(f"   ✅ 完成 - 置信度: {result.integrated_confidence:.3f} (预期: {test_case['expected_confidence']:.3f})")
            print(f"   ⏱️ 耗时: {execution_time:.1f}s")
            
        except Exception as e:
            print(f"   ❌ 失败: {str(e)}")
            results.append({
                'test_id': f"test_{i:03d}",
                'domain': test_case['domain'],
                'error': str(e),
                'execution_time': time.time() - start_time,
                'status': 'failed'
            })
        
        # 避免过于频繁的请求
        await asyncio.sleep(2)
    
    # 分析结果
    successful_results = [r for r in results if r['status'] == 'success']
    
    print("\n" + "=" * 50)
    print("📊 基准测试结果")
    print("=" * 50)
    
    if successful_results:
        # 基础统计
        confidences = [r['integrated_confidence'] for r in successful_results]
        consistencies = [r['analysis_consistency'] for r in successful_results]
        exec_times = [r['execution_time'] for r in successful_results]
        errors = [r['confidence_error'] for r in successful_results]
        
        print(f"✅ 成功率: {len(successful_results)}/{len(results)} ({len(successful_results)/len(results)*100:.1f}%)")
        print(f"📈 平均置信度: {statistics.mean(confidences):.3f} ± {statistics.stdev(confidences) if len(confidences) > 1 else 0:.3f}")
        print(f"🔄 平均一致性: {statistics.mean(consistencies):.3f} ± {statistics.stdev(consistencies) if len(consistencies) > 1 else 0:.3f}")
        print(f"⏱️ 平均执行时间: {statistics.mean(exec_times):.1f}s ± {statistics.stdev(exec_times) if len(exec_times) > 1 else 0:.1f}s")
        print(f"🎯 平均预测误差: {statistics.mean(errors):.3f}")
        
        # 按领域统计
        domain_stats = {}
        for result in successful_results:
            domain = result['domain']
            if domain not in domain_stats:
                domain_stats[domain] = []
            domain_stats[domain].append(result)
        
        print(f"\n📈 按领域统计:")
        for domain, domain_results in domain_stats.items():
            domain_confidences = [r['integrated_confidence'] for r in domain_results]
            avg_conf = statistics.mean(domain_confidences)
            print(f"  {domain}: 平均置信度 {avg_conf:.3f} ({len(domain_results)}个测试)")
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path("benchmark_results")
    results_dir.mkdir(exist_ok=True)
    
    # 保存原始数据
    with open(results_dir / f"benchmark_results_{timestamp}.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    
    # 保存CSV格式
    if results:
        df = pd.DataFrame(results)
        df.to_csv(results_dir / f"benchmark_summary_{timestamp}.csv", index=False)
    
    print(f"\n💾 结果已保存:")
    print(f"   JSON: benchmark_results/benchmark_results_{timestamp}.json")
    print(f"   CSV: benchmark_results/benchmark_summary_{timestamp}.csv")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_benchmark())