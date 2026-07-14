# Evidência de execução — Sprint 3

Execução realizada em 14/07/2026.

```text
23 passed
Cobertura total: 90,85%
Limite mínimo configurado: 85%
Ruff check: aprovado
Ruff format --check: aprovado
Bandit: aprovado, sem falhas bloqueantes
```

Comando utilizado:

```bash
pytest -q
ruff check app tests
ruff format --check app tests
bandit -r app -q
```
