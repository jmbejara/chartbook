# Pipelines 🔌

```{toctree}
:maxdepth: 1
{% for pipeline_id, pipeline_specs in specs|dictsort %}
pipelines/{{pipeline_id}}_README.md
{% endfor %}
```
{% for pipeline_id, pipeline_specs in specs|dictsort %}
  {% set pipeline_page_link = "./pipelines/" ~ pipeline_id ~ "_README.md" %}
  {% set dot_or_dotdot = "." %}

## {{ pipeline_specs.pipeline_name }}

{{pipeline_specs.pipeline_description}}

  {% include "docs_src/_templates/pipeline_specs.md" with context %}


{% endfor %}
