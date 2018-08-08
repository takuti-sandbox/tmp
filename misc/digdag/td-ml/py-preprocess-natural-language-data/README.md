Preprocess natural language data in Python before running ML queries on TD:

```sh
# export TD_API_KEY=1/xxxxxx
# export TD_API_SERVER=https://api.treasuredata.com
td wf push py-ml-preprocess
td wf secrets --project py-ml-preprocess --set apikey=$TD_API_KEY --set endpoint=$TD_API_SERVER
td wf start py-ml-preprocess py-preprocess-natural-language-data --session now
```

This workflow is part of our [Salesforce.com Predictive Analytics Workflow Template](https://github.com/treasure-data/workflow-examples/tree/master/machine-learning/sfdc-predictive-analytics).
