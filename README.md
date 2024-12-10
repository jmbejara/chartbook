Chart Book CLI
==============

```
rm uv.lock && uv sync && uv run chartbook generate --pipeline-theme pipeline ./_docs   
```

```
pip uninstall chartbook
pip install --force-reinstall git+https://github.com/jmbejara/chartbook-cli.git
chartbook generate --pipeline-theme pipeline ./_docs
```
or
```
chartbook generate --pipeline-theme chartbook ./_docs
```

```
uv pip install --force-reinstall git+https://github.com/jmbejara/chartbook-cli.git
chartbook generate --pipeline-theme pipeline ./_docs

uvx --from git+https://github.com/jmbejara/chartbook-cli chartbook generate --pipeline-theme pipeline ./_docs
```
or
```
uv run chartbook generate --pipeline-theme pipeline ./_docs
```

```
ipython --pdb src/chartbook/cli.py -- generate --pipeline-theme chartbook ./_docs
```