#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepConf 命令行工具
==================

提供便捷的命令行接口来运行DeepConf实验。

使用示例:
    # 基础使用
    python cli.py --prompt "解释量子计算" --model qwen3:0.6b

    # 自定义参数
    python cli.py --prompt "求解数学题" --num-paths 8 --keep-ratio 0.8 --mode online

    # 批量测试
    python cli.py --input-file prompts.txt --output-dir results/
"""

import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
import click

from deepconf_complete import create_deepconf_runner, DeepConfConfig

@click.group()
def cli():
    """DeepConf 命令行工具 - 集成行为分析功能"""
    pass

@cli.command()
@click.option('--profile', '-p', required=True, help='用户画像JSON文件路径或JSON字符串')
@click.option('--model', '-m', default='qwen3:0.6b', help='模型名称')
@click.option('--backend', '-b', default='ollama', 
              type=click.Choice(['ollama', 'huggingface']), help='模型后端')
@click.option('--multimodal', help='多模态数据源JSON文件路径')
@click.option('--output', '-o', help='输出文件路径')
@click.option('--report', '-r', help='生成报告文件路径')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
def behavior(profile: str, model: str, backend: str, multimodal: Optional[str],
             output: Optional[str], report: Optional[str], verbose: bool):
    """运行行为轨迹分析"""
    import asyncio
    import json
    from pathlib import Path
    
    try:
        from deepconf_with_behavior import create_integrated_analyzer
    except ImportError:
        click.echo("❌ 行为分析功能不可用，请检查extensions/behavior_analysis是否正确安装", err=True)
        return
    
    if verbose:
        click.echo(f"🎯 启动行为分析...")
        click.echo(f"   模型: {model}")
        click.echo(f"   后端: {backend}")
    
    try:
        # 解析用户画像
        if profile.startswith('{'):
            profile_data = json.loads(profile)
        else:
            with open(profile, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
        
        # 解析多模态数据源
        multimodal_data = None
        if multimodal:
            with open(multimodal, 'r', encoding='utf-8') as f:
                multimodal_data = json.load(f)
        
        # 创建分析器
        analyzer = create_integrated_analyzer(
            model_backend=backend,
            model_name=model
        )
        
        # 执行分析
        async def run_analysis():
            result = await analyzer.analyze_behavior(
                profile_data=profile_data,
                multimodal_sources=multimodal_data
            )
            return result
        
        result = asyncio.run(run_analysis())
        
        # 输出结果
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            click.echo(f"✅ 结果已保存到: {output}")
        
        # 生成报告
        if report and result.get('status') == 'success':
            report_content = f"""# 行为轨迹分析报告

## 分析概览
- 分析状态: {result['status']}
- 路径数量: {len(result.get('paths', []))}
- 平均置信度: {result.get('confidence', 0):.3f}

## 详细结果
{json.dumps(result, ensure_ascii=False, indent=2)}
"""
            with open(report, 'w', encoding='utf-8') as f:
                f.write(report_content)
            click.echo(f"📄 报告已保存到: {report}")
        
        if verbose:
            click.echo("📊 分析完成")
            click.echo(f"   状态: {result.get('status', 'unknown')}")
            click.echo(f"   置信度: {result.get('confidence', 0):.3f}")
        
    except Exception as e:
        click.echo(f"❌ 分析失败: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc())

@cli.command()
@click.option('--prompt', '-p', required=True, help='分析提示词')
@click.option('--profile', required=True, help='用户画像JSON文件路径或JSON字符串')
@click.option('--model', '-m', default='qwen3:0.6b', help='模型名称')
@click.option('--backend', '-b', default='ollama', 
              type=click.Choice(['ollama', 'huggingface']), help='模型后端')
@click.option('--multimodal', help='多模态数据源JSON文件路径')
@click.option('--output', '-o', help='输出文件路径')
@click.option('--report', '-r', help='生成报告文件路径')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
def integrated(prompt: str, profile: str, model: str, backend: str, 
               multimodal: Optional[str], output: Optional[str], 
               report: Optional[str], verbose: bool):
    """运行集成分析(DeepConf + 行为分析)"""
    import asyncio
    import json
    from pathlib import Path
    
    try:
        from deepconf_with_behavior import create_integrated_analyzer
    except ImportError:
        click.echo("❌ 集成分析功能不可用，请检查相关依赖", err=True)
        return
    
    if verbose:
        click.echo(f"🔄 启动集成分析...")
        click.echo(f"   提示: {prompt[:50]}...")
        click.echo(f"   模型: {model}")
        click.echo(f"   后端: {backend}")
    
    try:
        # 解析用户画像
        if profile.startswith('{'):
            profile_data = json.loads(profile)
        else:
            with open(profile, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
        
        # 解析多模态数据源
        multimodal_data = None
        if multimodal:
            with open(multimodal, 'r', encoding='utf-8') as f:
                multimodal_data = json.load(f)
        
        # 创建分析器
        analyzer = create_integrated_analyzer(
            model_backend=backend,
            model_name=model
        )
        
        # 执行集成分析
        async def run_analysis():
            result = await analyzer.integrated_analysis(
                prompt=prompt,
                profile_data=profile_data,
                multimodal_sources=multimodal_data
            )
            return result
        
        result = asyncio.run(run_analysis())
        
        # 输出结果
        if output:
            # 将结果转换为可序列化的格式
            serializable_result = {
                'deepconf_result': result.deepconf_result,
                'deepconf_confidence': result.deepconf_confidence,
                'behavior_result': result.behavior_result,
                'integrated_confidence': result.integrated_confidence,
                'analysis_consistency': result.analysis_consistency,
                'recommendation_score': result.recommendation_score
            }
            
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(serializable_result, f, ensure_ascii=False, indent=2)
            click.echo(f"✅ 结果已保存到: {output}")
        
        # 生成报告
        if report:
            report_content = analyzer.generate_integrated_report(result)
            with open(report, 'w', encoding='utf-8') as f:
                f.write(report_content)
            click.echo(f"📄 报告已保存到: {report}")
        
        if verbose:
            click.echo("📊 集成分析完成")
            click.echo(f"   综合置信度: {result.integrated_confidence:.3f}")
            click.echo(f"   分析一致性: {result.analysis_consistency:.3f}")
            click.echo(f"   推荐评分: {result.recommendation_score:.3f}")
        
    except Exception as e:
        click.echo(f"❌ 集成分析失败: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc())

@cli.command()
@click.option('--prompt', '-p', required=True, help='输入提示')
@click.option('--model', '-m', default='qwen3:0.6b', help='模型名称')
@click.option('--backend', '-b', default='ollama', 
              type=click.Choice(['ollama', 'huggingface']), help='模型后端')
@click.option('--num-paths', '-n', default=8, help='生成路径数量')
@click.option('--keep-ratio', '-k', default=0.8, help='保留路径比例')
@click.option('--mode', default='offline', 
              type=click.Choice(['offline', 'online']), help='运行模式')
@click.option('--output', '-o', help='输出文件路径')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
def run(prompt: str, model: str, backend: str, num_paths: int, 
        keep_ratio: float, mode: str, output: Optional[str], verbose: bool):
    """运行单个DeepConf推理任务"""
    
    if verbose:
        click.echo(f"🚀 启动DeepConf...")
        click.echo(f"   提示: {prompt[:50]}...")
        click.echo(f"   模型: {model}")
        click.echo(f"   后端: {backend}")
        click.echo(f"   路径数: {num_paths}")
        click.echo(f"   保留比例: {keep_ratio}")
        click.echo(f"   模式: {mode}")
    
    try:
        # 创建配置
        config = DeepConfConfig(
            num_paths=num_paths,
            keep_ratio=keep_ratio
        )
        
        # 创建运行器
        runner = create_deepconf_runner(
            backend_type=backend,
            model_path=model,
            config=config
        )
        
        # 执行推理
        if mode == 'offline':
            result = runner.run_offline(prompt)
        else:
            result = runner.run_online(prompt)
        
        # 输出结果
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            click.echo(f"✅ 结果已保存到: {output}")
        
        if verbose:
            click.echo("📊 推理完成")
            click.echo(f"   最终答案: {result['final_answer'][:100]}...")
            click.echo(f"   生成路径: {len(result['all_paths'])}")
            click.echo(f"   保留路径: {len(result['kept_paths'])}")
            click.echo(f"   平均置信度: {sum(result['kept_confidences'])/len(result['kept_confidences']):.3f}")
        else:
            click.echo("✅ 推理完成")
            click.echo(f"最终答案: {result['final_answer']}")
        
    except Exception as e:
        click.echo(f"❌ 推理失败: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc())

if __name__ == '__main__':
    cli()