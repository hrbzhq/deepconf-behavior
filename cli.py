#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepConf Command Line Interface
===============================

Provides convenient command-line interface for running DeepConf experiments.

Usage Examples:
    # Basic usage
    python cli.py --prompt "Explain quantum computing" --model qwen3:0.6b

    # Custom parameters
    python cli.py --prompt "Solve math problem" --num-paths 8 --keep-ratio 0.8 --mode online

    # Batch testing
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
    """DeepConf Command Line Tool - Integrated Behavioral Analysis"""
    pass

@cli.command()
@click.option('--profile', '-p', required=True, help='User profile JSON file path or JSON string')
@click.option('--model', '-m', default='qwen3:0.6b', help='Model name')
@click.option('--backend', '-b', default='ollama', 
              type=click.Choice(['ollama', 'huggingface']), help='Model backend')
@click.option('--multimodal', help='Multimodal data sources JSON file path')
@click.option('--output', '-o', help='Output file path')
@click.option('--report', '-r', help='Generate report file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def behavior(profile: str, model: str, backend: str, multimodal: Optional[str],
             output: Optional[str], report: Optional[str], verbose: bool):
    """Run behavioral trajectory analysis"""
    import asyncio
    import json
    from pathlib import Path
    
    try:
        from deepconf_with_behavior import create_integrated_analyzer
    except ImportError:
        click.echo("❌ Behavioral analysis functionality unavailable, please check if extensions/behavior_analysis is properly installed", err=True)
        return
    
    if verbose:
        click.echo(f"🎯 Starting behavioral analysis...")
        click.echo(f"   Model: {model}")
        click.echo(f"   Backend: {backend}")
    
    try:
        # Parse user profile
        if profile.startswith('{'):
            profile_data = json.loads(profile)
        else:
            with open(profile, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
        
        # Parse multimodal data sources
        multimodal_data = None
        if multimodal:
            with open(multimodal, 'r', encoding='utf-8') as f:
                multimodal_data = json.load(f)
        
        # Create analyzer
        analyzer = create_integrated_analyzer(
            model_backend=backend,
            model_name=model
        )
        
        # Execute analysis
        async def run_analysis():
            result = await analyzer.analyze_behavior(
                profile_data=profile_data,
                multimodal_sources=multimodal_data
            )
            return result
        
        result = asyncio.run(run_analysis())
        
        # Output results
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            click.echo(f"✅ Results saved to: {output}")
        
        # Generate report
        if report and result.get('status') == 'success':
            report_content = f"""# Behavioral Trajectory Analysis Report

## Analysis Overview
- Analysis Status: {result['status']}
- Path Count: {len(result.get('paths', []))}
- Average Confidence: {result.get('confidence', 0):.3f}

## Detailed Results
{json.dumps(result, ensure_ascii=False, indent=2)}
"""
            with open(report, 'w', encoding='utf-8') as f:
                f.write(report_content)
            click.echo(f"📄 Report saved to: {report}")
        
        if verbose:
            click.echo("📊 Analysis completed")
            click.echo(f"   Status: {result.get('status', 'unknown')}")
            click.echo(f"   Confidence: {result.get('confidence', 0):.3f}")
        
    except Exception as e:
        click.echo(f"❌ Analysis failed: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc())

@cli.command()
@click.option('--prompt', '-p', required=True, help='Analysis prompt')
@click.option('--profile', required=True, help='User profile JSON file path or JSON string')
@click.option('--model', '-m', default='qwen3:0.6b', help='Model name')
@click.option('--backend', '-b', default='ollama', 
              type=click.Choice(['ollama', 'huggingface']), help='Model backend')
@click.option('--multimodal', help='Multimodal data sources JSON file path')
@click.option('--output', '-o', help='Output file path')
@click.option('--report', '-r', help='Generate report file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def integrated(prompt: str, profile: str, model: str, backend: str, 
               multimodal: Optional[str], output: Optional[str], 
               report: Optional[str], verbose: bool):
    """Run integrated analysis (DeepConf + Behavioral Analysis)"""
    import asyncio
    import json
    from pathlib import Path
    
    try:
        from deepconf_with_behavior import create_integrated_analyzer
    except ImportError:
        click.echo("❌ Integrated analysis functionality unavailable, please check related dependencies", err=True)
        return
    
    if verbose:
        click.echo(f"🔄 Starting integrated analysis...")
        click.echo(f"   Prompt: {prompt[:50]}...")
        click.echo(f"   Model: {model}")
        click.echo(f"   Backend: {backend}")
    
    try:
        # Parse user profile
        if profile.startswith('{'):
            profile_data = json.loads(profile)
        else:
            with open(profile, 'r', encoding='utf-8') as f:
                profile_data = json.load(f)
        
        # Parse multimodal data sources
        multimodal_data = None
        if multimodal:
            with open(multimodal, 'r', encoding='utf-8') as f:
                multimodal_data = json.load(f)
        
        # Create analyzer
        analyzer = create_integrated_analyzer(
            model_backend=backend,
            model_name=model
        )
        
        # Execute integrated analysis
        async def run_analysis():
            result = await analyzer.integrated_analysis(
                prompt=prompt,
                profile_data=profile_data,
                multimodal_sources=multimodal_data
            )
            return result
        
        result = asyncio.run(run_analysis())
        
        # Output results
        if output:
            # Convert results to serializable format
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
            click.echo(f"✅ Results saved to: {output}")
        
        # Generate report
        if report:
            report_content = analyzer.generate_integrated_report(result)
            with open(report, 'w', encoding='utf-8') as f:
                f.write(report_content)
            click.echo(f"📄 Report saved to: {report}")
        
        if verbose:
            click.echo("📊 Integrated analysis completed")
            click.echo(f"   Integrated Confidence: {result.integrated_confidence:.3f}")
            click.echo(f"   Analysis Consistency: {result.analysis_consistency:.3f}")
            click.echo(f"   Recommendation Score: {result.recommendation_score:.3f}")
        
    except Exception as e:
        click.echo(f"❌ Integrated analysis failed: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc())

@cli.command()
@click.option('--prompt', '-p', required=True, help='Input prompt')
@click.option('--model', '-m', default='qwen3:0.6b', help='Model name')
@click.option('--backend', '-b', default='ollama', 
              type=click.Choice(['ollama', 'huggingface']), help='Model backend')
@click.option('--num-paths', '-n', default=8, help='Number of paths to generate')
@click.option('--keep-ratio', '-k', default=0.8, help='Path keep ratio')
@click.option('--mode', default='offline', 
              type=click.Choice(['offline', 'online']), help='Execution mode')
@click.option('--output', '-o', help='Output file path')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def run(prompt: str, model: str, backend: str, num_paths: int, 
        keep_ratio: float, mode: str, output: Optional[str], verbose: bool):
    """Run single DeepConf reasoning task"""
    
    if verbose:
        click.echo(f"🚀 Starting DeepConf...")
        click.echo(f"   Prompt: {prompt[:50]}...")
        click.echo(f"   Model: {model}")
        click.echo(f"   Backend: {backend}")
        click.echo(f"   Paths: {num_paths}")
        click.echo(f"   Keep ratio: {keep_ratio}")
        click.echo(f"   Mode: {mode}")
    
    try:
        # Create configuration
        config = DeepConfConfig(
            num_paths=num_paths,
            keep_ratio=keep_ratio
        )
        
        # Create runner
        runner = create_deepconf_runner(
            backend_type=backend,
            model_path=model,
            config=config
        )
        
        # Execute reasoning
        if mode == 'offline':
            result = runner.run_offline(prompt)
        else:
            result = runner.run_online(prompt)
        
        # Output results
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            click.echo(f"✅ Results saved to: {output}")
        
        if verbose:
            click.echo("📊 Reasoning completed")
            click.echo(f"   Final answer: {result['final_answer'][:100]}...")
            click.echo(f"   Generated paths: {len(result['all_paths'])}")
            click.echo(f"   Kept paths: {len(result['kept_paths'])}")
            click.echo(f"   Average confidence: {sum(result['kept_confidences'])/len(result['kept_confidences']):.3f}")
        else:
            click.echo("✅ Reasoning completed")
            click.echo(f"Final answer: {result['final_answer']}")
        
    except Exception as e:
        click.echo(f"❌ Reasoning failed: {e}", err=True)
        if verbose:
            import traceback
            click.echo(traceback.format_exc())

if __name__ == '__main__':
    cli()