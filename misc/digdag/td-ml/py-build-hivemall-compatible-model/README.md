Build prediction model and create a new table with Hivemall compatible schema on TD:

```sh
# export TD_API_KEY=1/xxxxxx
# export TD_API_SERVER=https://api.treasuredata.com
td wf push py-ml-project-hivemall-model
td wf secrets --project py-ml-project-hivemall-model --set apikey=$TD_API_KEY --set endpoint=$TD_API_SERVER
td wf start py-ml-project-hivemall-model py-build-hivemall-compatible-model --session now
```
