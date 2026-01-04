# 🤝 Contributing to Enterprise RAG

We welcome contributions! Whether it's fixing bugs, improving documentation, or proposing new features, your help is appreciated.

## Development Setup

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/enterprise-rag.git
   ```

2. **Virtual Environment**
   It is recommended to use `venv` or `conda`:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dev Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest black flake8
   ```

## Pull Request Process

1. Create a **Feature Branch** (`git checkout -b feature/amazing-feature`).
2. Commit your changes.
3. Push to the branch.
4. Open a **Pull Request**.

## Coding Standards

- **Python**: We follow PEP8. Please run `black .` before committing.
- **Type Hinting**: Use Python type hints (`def func(a: int) -> str:`) where possible.
- **Documentation**: Update README or docs if you change functionality.

## Reporting Issues

Please use the GitHub Issues tab to report bugs. Include:
- Steps to reproduce.
- Expected vs. Actual behavior.
- Screenshots (if UI related).
