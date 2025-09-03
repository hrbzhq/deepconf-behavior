# DeepConf-Behavior Examples

This directory contains example configurations and usage demonstrations for the DeepConf-Behavior framework.

## Quick Start Examples

### 1. Basic User Profile (education.json)
```json
{
  "姓名": "李华",
  "年龄": 24,
  "专业": "计算机科学",
  "当前技能": ["Python基础", "数据结构"],
  "目标": "成为机器学习工程师",
  "学习风格": "实践导向"
}
```

### 2. Career Analysis Profile (career.json)
```json
{
  "姓名": "张强",
  "年龄": 32,
  "工作年限": 8,
  "当前职位": "高级软件工程师",
  "管理经验": "团队Lead 2年",
  "目标": "技术总监"
}
```

## CLI Usage Examples

### Run Basic DeepConf Analysis
```bash
python cli.py run --prompt "解释量子计算原理" --model qwen3:0.6b --verbose
```

### Run Behavior Analysis
```bash
python cli.py behavior --profile examples/education.json --output result.json --report report.md
```

### Run Integrated Analysis
```bash
python cli.py integrated --prompt "制定学习计划" --profile examples/education.json --output integrated_result.json
```

## Benchmark Examples

### Run Performance Benchmark
```bash
python benchmark.py
```

This will run comprehensive tests across multiple domains and generate performance metrics.

## Configuration Options

### Model Backends
- `ollama`: Local Ollama models (default)
- `huggingface`: Hugging Face transformers

### Supported Models
- `qwen3:0.6b`: Lightweight Qwen model
- `qwen3:8b`: Standard Qwen model
- Custom models via model path

### Analysis Modes
- `offline`: Batch processing mode
- `online`: Interactive mode with streaming

## Advanced Usage

See the main documentation for detailed API usage and integration examples.