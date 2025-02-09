| Pipeline Name                   | {{pipeline_specs.pipeline_name}}                       |
|---------------------------------|--------------------------------------------------------|
| Pipeline ID                     | [{{pipeline_id}}]({{pipeline_page_link}})              |
| Lead Pipeline Developer         | {{pipeline_specs.lead_pipeline_developer}}             |
| Contributors                    | {{pipeline_specs.contributors | join(', ')}}           |
| Bitbucket Repo URL              | {{pipeline_specs.bitbucket_repo_URL}}                  |
| Production Directory            | <a href="file://{{pipeline_specs.pipeline_production_dir}}">{{pipeline_specs.pipeline_production_dir}}</a>      |
| Pipeline Web Page   | <a href="file://{{pipeline_specs.path_to_pipeline_site}}">{{pipeline_specs.path_to_pipeline_site}}</a>      |
| Date of Last Code Update        | {{pipeline_specs.source_last_modified_date}}           |
| Runs on Linux, Windows? |{{pipeline_specs.runs_on_grid_or_windows_or_other}}|
| Linked Dataframes               | {% for dataframe_id, dataframe_specs in pipeline_specs.dataframes.items() %} [{{pipeline_id}}_{{dataframe_id}}]({{dot_or_dotdot}}/dataframes/{{pipeline_id}}_{{dataframe_id}}.md)<br> {% endfor %} |


In addition to the `requirements.txt` and `r_requirements.txt`, the pipeline code relies
on first loading modules using the following command:
```
{{pipeline_specs.software_modules_command}}
```