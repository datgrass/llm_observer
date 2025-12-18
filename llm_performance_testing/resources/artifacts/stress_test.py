import numpy as np
import uuid
import re
from datetime import datetime as dt, timedelta
from pandas.tseries.holiday import USFederalHolidayCalendar


def create_widgets(dbutils, task_key):
  # Create the widgets
  dbutils.widgets.text('catalog', 'llm_observer', '01. Catalog')
  dbutils.widgets.text('schema', 'default', '02. Schema')
  if task_key == '01_llm_cost_mapping':
    dbutils.widgets.text('mapping_model_endpoint', 'databricks-meta-llama-3-3-70b-instruct', '03. Mapping Model')
  elif task_key == '02_llm_performance_test':
    dbutils.widgets.text('model_endpoints', 'databricks-claude-sonnet-4-5, databricks-claude-opus-4-5', '03. Model Endpoints')
    dbutils.widgets.text('sample_dataset_sizes', '100,200', '04. Sample Dataset Sizes')
    dbutils.widgets.text('time_zone', 'America/Detroit', '05. Time Zone')


def generate_sales_data(
    n_rows: int,
    base_demand: int = 1000,
    day_range: int = 100,
    seed: int = 123456789
):
  # Create empty list to store records
  records = []
  np.random.seed(seed)

  # Generate dates
  date_offsets = np.random.uniform(1, day_range, n_rows)
  dates = [dt.now() - timedelta(days=int(offset)) for offset in date_offsets]
  dates.sort()
  holidays = USFederalHolidayCalendar().holidays(start=dates[0], end=dates[-1])

  # Generate features for each row
  for i in range(n_rows):
    date_val = dates[i]
    record = {
      'date': date_val.date(),
      'average_temperature': round(np.random.uniform(0, 35), 1),
      'rainfall': round(np.random.exponential(5), 1),
      'weekend': date_val.weekday() >= 5,
      'holiday': str(date_val.date()) in holidays,
      'price_per_kg': round(np.random.uniform(0.5, 3), 2),
      'demand': round(np.random.uniform(1, base_demand), 1),
      'month': date_val.month,
    }
    record['total_spend'] = round(record['demand'] * record['price_per_kg'], 2)
    records.append(record)
  
  return records


def run_sample_query(
    spark,
    sql: str, 
    llm_observer_catalog: str, 
    llm_observer_schema: str, 
    llm_observer_table_name: str
  ):
    # Start query execution
    start_time = dt.now()
    llm_observer_sdf = spark.sql(sql)
    llm_observer_sdf.write.mode('overwrite').saveAsTable(f'{llm_observer_catalog}.{llm_observer_schema}.{llm_observer_table_name}')
    end_time = dt.now()
    print('Results written to table:', f'{llm_observer_catalog}.{llm_observer_schema}.{llm_observer_table_name}')

    # Log information about the query's execution
    elapsed_time = (end_time - start_time).total_seconds()
    run_id = uuid.uuid4().hex
    run_log = {
        'run_id': run_id,
        'output_table': f'{llm_observer_catalog}.{llm_observer_schema}.{llm_observer_table_name}',
        'n_rows': llm_observer_sdf.count(),
        'n_columns': len(llm_observer_sdf.columns),
        'start_time': start_time,
        'end_time': end_time,
        'elapsed_time': elapsed_time,
        'sql': sql,
    }
    
    return run_log
  

def to_valid_table_name(
    raw: str, 
    max_length: int = 128
  ):
    if raw is None:
        raw = ''
    # Lowercase
    name = raw.lower()
    # Replace invalid chars with underscore (anything not a-z, 0-9, or _)
    name = re.sub(r'[^a-z0-9_]', '_', name)
    # Collapse multiple underscores
    name = re.sub(r'_+', '_', name)
    # Ensure non-empty
    if not name:
        name = 't'
    # Ensure it does not start with a digit
    if re.match(r'^[0-9]', name):
        name = 't_' + name
    # Enforce max length
    name = name[:max_length]
    # In case trimming leaves trailing underscore
    name = name.strip('_')
    # Ensure non-empty again
    if not name:
        name = 't'
    return name


def get_indices(records, tag: str):
  # define output object and initialize y counter
  output = []
  x_index = 0

  # loop through each record passed
  for record in records:
    y_index = 0
    tagged_records = record.findAll(tag)

    # loop through each record with associated html tag
    for tagged_record in tagged_records:
      
      # add record to our outputs list
      output.append({
        'x_index': x_index, 
        'y_index': y_index, 
        'text': tagged_record.getText()
      })

      # advance to next row and increment counter
      y_index +=1
    
    # advance to next column and increment counter
    x_index += 1

  return output
