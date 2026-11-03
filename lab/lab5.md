***Robin Ghassibeh (231463)***

### Lab 5 pipeline, from git push to a running container

```mermaid
flowchart TD
    classDef human fill:#ffd88a,stroke:#b8860b,color:#000
    classDef auto fill:#a8e6b4,stroke:#2e7d32,color:#000
    classDef store fill:#d5dde2,stroke:#455a64,color:#000

    subgraph CODE["Code"]
        commit["git push, or a pull request"]:::human
        test["test job: ruff + pytest"]:::auto
        smoke["smoke job: docker build + /health with SKIP_MODEL"]:::auto
        merge["merge the pull request once test and smoke are green"]:::human
        publish["push job, main only: build and push the image"]:::auto
        image[("ghcr.io/robin-devlp/mlops-lab-1:commit SHA<br/>CODE VERSION = commit SHA")]:::store
    end

    subgraph MODEL["Model"]
        prep["data.py builds the processed data"]:::human
        validate["validate_data.py checks the data contract, then dvc push"]:::human
        train["train.py trains and logs a run to MLflow"]:::human
        register["register the run as a new food11 version"]:::human
        gate["promote.py: promote only if accuracy >= champion + 2 se"]:::human
        registry[("MLflow registry: food11@champion<br/>MODEL VERSION = champion alias")]:::store
    end

    subgraph RUN["Running"]
        deploy["docker pull the image by its SHA, then docker compose up"]:::human
        serve["inference loads models:/food11@champion at startup"]:::auto
    end

    commit --> test --> smoke
    smoke -- pull request --> merge --> publish
    smoke -- push to main --> publish
    publish --> image
    prep --> validate --> train --> register --> gate --> registry
    image --> deploy --> serve
    registry --> serve

    subgraph LEGEND["Legend"]
        h["needs a human"]:::human
        a["automatic"]:::auto
    end
```

Green steps run by themselves on every push, yellow steps still need me. The code version is fixed when the push job tags the image with the commit SHA, and the model version is fixed when promote.py moves the champion alias, so the two are released independently and only meet when the inference container starts.
