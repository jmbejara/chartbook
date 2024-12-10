Chart Book CLI
==============

```
rm uv.lock && uv sync && uv run chartbook generate ./_docs   
```

```
pip uninstall chartbook
pip install --force-reinstall git+https://github.com/jmbejara/chartbook.git
chartbook generate --pipeline-theme pipeline ./_docs
```
or
```
chartbook generate --pipeline-theme chartbook ./_docs
```
