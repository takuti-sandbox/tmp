```sh
td wf push py-ml
td wf secrets --project py-ml --set apikey=$TD_API_KEY --set endpoint=$TD_API_SERVER
td wf start py-ml py-build-hivemall-compatible-model --session now
```
