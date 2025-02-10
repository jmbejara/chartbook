# {{pipeline_specs.pipeline_name}}

Last updated: {sub-ref}`today` 


## Table of Contents

```{toctree}
:maxdepth: 1
:caption: Notebooks 📖
{{ notebook_list | join("\n")}}
```



```{toctree}
:maxdepth: 1
:caption: Pipeline Charts 📈
charts.md
```

```{postlist}
:format: "{title}"
```


```{toctree}
:maxdepth: 1
:caption: Pipeline Dataframes 📊
{{dataframe_file_list | sort | join("\n")}}
```


```{toctree}
:maxdepth: 1
:caption: Appendix 💡
myst_markdown_demos.md
apidocs/index
```


## Pipeline Specs
{% for pipeline_id, pipeline_specs in specs.items() %}
  {% include "_docs_src/_templates/pipeline_specs.md" with context %}
{% endfor %}


{{readme_text}}