# LLM Observer

The **LLM Observer** project provides monitoring and performance evaluation tools for large language model (LLM) workloads within Databricks. It consists of a high-level usage dashboard and a set of automated performance testing assets designed to track cost, efficiency, and reliability of LLM operations.

---

## Overview

At the top level, the project includes two main components:

1. **LLM Usage Dashboard**  
   A centralized Databricks dashboard summarizing overall cost and usage metrics for LLM activities. This dashboard helps teams monitor trends, identify cost drivers, and optimize model usage across environments.

2. **llm_performance_testing (Databricks Asset Bundle)**  
   A self-contained Databricks asset bundle that automates the benchmarking and evaluation of LLMs across randomized datasets. This component is designed to produce reproducible performance insights that can inform model selection, tuning, and deployment decisions.

---

## Asset Bundle Structure

The `llm_performance_testing` folder includes the following structure:

```
llm_performance_testing/
│
├── databricks.yml # Asset bundle configuration file
├── .gitignore # Exclusion rules for Git tracking
├── README.md # Component-level documentation
│
└── resources/ # Execution resources for the bundle
├──── job_config.yaml # Databricks job configuration
├──── artifacts/ # Notebooks and supporting files for running performance tests
├────── 00_llm_oss # A notebook to web scrape databricks open source llm pricing
├────── 00_llm_proprietary # A notebook to web scrape databricks proprietary llm pricing
├────── 01_llm_cost_mapping # A notebook to combine price datasets and use AI to map model endpoints
├────── 02_llm_performance_test # A notebook to run managed performance tests and log results for different llms
├────── AI Cost Comparisons # A dashboard to analyze the results of different llm performance tests from the 02_llm_performance_test notebook
└────── stress_test.py # A python file for different functions to scrape data, generate datasets, and run performance tests
```


---

## Key Capabilities

- **Usage Monitoring:** Visualizes LLM-related resource consumption and cost distribution.  
- **Performance Testing:** Runs automated evaluation workflows across multiple LLMs and datasets.  
- **Reproducible Benchmarks:** Uses Databricks asset bundle capabilities for consistent re-runs in CI/CD pipelines.  
- **Extendability:** Easily customizable with additional datasets, evaluation metrics, or model endpoints.

---

## Getting Started

1. Import the **`llm_observer`** bundle into your Databricks workspace.  
2. Review and update configuration values in `resources/job_config.yaml`.  
3. Deploy the asset bundle using the `databricks bundle deploy` command.  
4. Access the **LLM Usage Dashboard** for high-level insights.  
5. Run the **Performance Testing Jobs** to evaluate model performance and collect metrics.

---

## Related Documentation

- [Databricks Asset Bundles](https://docs.databricks.com/en/dev-tools/bundles/index.html)  
- [Dashboard Management in Databricks](https://docs.databricks.com/en/dashboards/index.html)
