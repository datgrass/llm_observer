# llm_performance_testing

## Getting Started

To deploy and manage this asset bundle, follow these steps:

### 1. Deployment

- Click the **deployment rocket** 🚀 in the left sidebar to open the **Deployments** panel, then click **Deploy**.

### 2. Running Jobs & Pipelines

- To run a deployed job or pipeline, hover over the resource in the **Deployments** panel and click the **Run** button.

### 3. Managing Resources

- Use the **Add** dropdown to add resources to the asset bundle.
- Click **Schedule** on a notebook within the asset bundle to create a **job definition** that schedules the notebook.

## Documentation

- For information on using **Databricks Asset Bundles in the workspace**, see: [Databricks Asset Bundles in the workspace](https://docs.databricks.com/aws/en/dev-tools/bundles/workspace-bundles)
- For details on the **Databricks Asset Bundles format** used in this asset bundle, see: [Databricks Asset Bundles Configuration reference](https://docs.databricks.com/aws/en/dev-tools/bundles/reference)

-------------

# LLM Performance Testing (Databricks Asset Bundle)

The **LLM Performance Testing** asset bundle automates benchmarking and monitoring of large language models (LLMs) within Databricks. It is designed to measure model performance, compare cost efficiency, and produce standardized results that integrate into the broader **LLM Observer** framework.

This asset bundle defines a multi-task job pipeline through `resources/jobs.yml` that executes a sequence of Databricks notebooks aimed at evaluating both open-source and proprietary models on randomized datasets.

---

## Job Overview

The primary job defined in this bundle is **`run_llm_test`**, which orchestrates the full LLM performance testing workflow. The job is queued for efficient scheduling and includes the following tasks:

### 1. `00_llm_oss`
Runs initial tests for **open-source** LLMs.  
**Notebook:** `./artifacts/00_llm_oss.ipynb`  
**Base parameters:**
- `catalog`: `llm_observer`  
- `schema`: `default`  

### 2. `00_llm_proprietary`
Runs initial tests for **proprietary** or hosted LLMs.  
**Notebook:** `./artifacts/00_llm_proprietary.ipynb`  
**Base parameters:**
- `catalog`: `llm_observer`  
- `schema`: `default`  

### 3. `01_llm_cost_mapping`
Generates cost mappings based on model metadata and usage output from prior tasks.  
**Dependencies:** `00_llm_oss`, `00_llm_proprietary`  
**Notebook:** `./artifacts/01_llm_cost_mapping.ipynb`  
**Base parameters:**
- `catalog`: `llm_observer`  
- `schema`: `default`  
- `mapping_model_endpoint`: `databricks-meta-llama-3-3-70b-instruct`  

### 4. `02_llm_performance_test`
Runs comparative performance benchmarks across multiple model endpoints and sample sizes.  
**Dependencies:** `01_llm_cost_mapping`  
**Notebook:** `./artifacts/02_llm_performance_test.ipynb`  
**Base parameters:**
- `model_endpoints`:  
  `databricks-claude-sonnet-4-5, databricks-claude-opus-4-5, databricks-claude-opus-4-1`  
- `sample_dataset_sizes`:  
  `100,250,500,750,1000,2500,5000,7500,10000`  
- `catalog`: `llm_observer`  
- `schema`: `default`  
- `time_zone`: `America/Detroit`  

---

## Execution Workflow

1. **Open-source and proprietary tests** initialize baseline results.  
2. **Cost mapping** aligns model performance with cost metrics for normalization.  
3. **Performance testing** executes benchmarks across datasets of varying sizes.  
4. **Results** are stored in the `llm_observer` catalog for downstream visualization.

---

## Output and Integration

All job results integrate with the **LLM Usage Dashboard** at the project root level, enabling a consolidated view of model cost and performance trends. The outputs can also feed additional dashboards, experiments, or model-serving evaluation frameworks.

---

## Customization

You can modify the job configuration in `resources/jobs.yml` to:
- Add or remove model endpoints.  
- Adjust dataset sampling ranges.  
- Update default schemas or time zones.  
- Integrate with additional logging or notification systems.

---

## Related Links

- [Databricks Jobs Documentation](https://docs.databricks.com/en/jobs/index.html)  
- [Databricks Asset Bundles Documentation](https://docs.databricks.com/en/dev-tools/bundles/index.html)
