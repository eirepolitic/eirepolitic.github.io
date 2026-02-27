<hr>
<p>title: "AutoDoc Creation Pipeline"</p>
<h2 id="layoutdoc">layout: default</h2>
<h1 id="llmcolumncreator">LLM Column Creator</h1>
<p><strong>Project:</strong> eirepolitic<br><strong>Type:</strong> pipeline<br><strong>Last generated:</strong> 2026-02-26T04:12:34.160412Z</p>
<hr>
<h2 id="overview">Overview</h2>
<h3 id="purpose">Purpose</h3>
<p>The "LLM Column Creator" pipeline adds new columns to CSV or Parquet files using data from existing columns and LLM-generated content, automating tabular data enrichment via LLMs.</p>
<h3 id="scope">Scope</h3>
<p>This pipeline processes CSV files in S3, selects up to five columns as prompt variables, and generates new column content by invoking the OpenAI Responses API. Output is written back to S3 in CSV and Parquet formats, with support for <code>full_table</code> and <code>processed_only</code> write modes, overwrite/resumable behavior, autosaving, validation, and test mode. Implementation uses Python, a YAML configuration, and works with AWS S3 and OpenAI Python client (GPT-4.1-mini and GPT-5 models).</p>
<h2 id="assets">Assets</h2>
<p>The core logic is in the Python script <code>process/llm_table_runner.py</code>, which reads input CSVs from S3, processes them with LLM prompts, and writes results back to S3 in CSV and Parquet formats.</p>
<h3 id="configuration">Configuration</h3>
<p>Configuration is via YAML, supporting options for:</p>
<ul>
<li>S3 bucket, region, and input/output keys</li>
<li>Columns to keep and ID generation (column or hash)</li>
<li>Up to five prompt variables from input columns</li>
<li>Output column and prompt template</li>
<li>LLM model/formulation (model, effort, verbosity, temperature, output tokens)</li>
<li>Web search enablement</li>
<li>Inline citation stripping</li>
<li>Validation: non-empty check, max words, optional regex</li>
<li>Run parameters: test row limit, autosave interval, request delay, retries</li>
<li>Write/overwrite modes</li>
</ul>
<h3 id="exampletaskconfigurations">Example Task Configurations</h3>
<ul>
<li>
<p><code>tasks/llm_task_template.yml</code>: Irish politician data</p>
<ul>
<li>S3: <code>eirepolitic-data</code> (region <code>us-east-2</code>)</li>
<li>Input: <code>processed/members/members_summaries.csv</code></li>
<li>Outputs: <code>processed/members/members_summaries.csv</code> and <code>processed/members/parquets/members_summaries.parquet</code></li>
<li>Columns: <code>member_code</code>, <code>full_name</code>, <code>background</code></li>
<li>ID: <code>member_code</code> (else hash on <code>full_name</code>)</li>
<li>Prompt var: <code>full_name</code></li>
<li>Output: <code>conflicts_of_interest</code></li>
<li>Prompt: Identify conflicts of interest via web search</li>
<li>Model: <code>gpt-4.1-mini</code> + web search, medium reasoning/verbosity, 320 tokens</li>
<li>Write mode: <code>full_table</code></li>
<li>Validation: non-empty, max 2000 words</li>
</ul>
</li>
<li>
<p><code>tasks/Absence_Reasons.yml</code>: Like above, but outputs <code>absence_reason</code> and prompts for TD absence explanations in 2025.</p>
</li>
</ul>
<h3 id="automation">Automation</h3>
<p>GitHub Actions workflows (e.g. <code>.github/workflows/llm_task_controller_template.yml</code>, <code>Absence_Reason_Manual.yml</code>) provide manual triggers, optional test row overrides, and install dependencies including <code>pyarrow</code> and <code>pyyaml</code>.</p>
<h2 id="inputsandoutputs">Inputs and Outputs</h2>
<h3 id="inputs">Inputs</h3>
<ul>
<li>CSV from S3 (bucket, region, and key configurable)</li>
<li>Subset of columns selectable</li>
<li>ID column or SHA-256 hash of specified fallback columns</li>
<li>Up to 5 prompt variable columns</li>
<li>Prompt template leveraging the above columns</li>
<li>LLM configuration: model name, web search toggle, temperature, max tokens, effort, verbosity, citation strip</li>
<li>Run config: retries, delay, autosave, test row limit</li>
<li>Validation: require non-empty, max words, optional regex</li>
</ul>
<h3 id="outputs">Outputs</h3>
<ul>
<li>Results written to S3 as a CSV (configurable key) and Parquet file</li>
<li>Output: retained columns + LLM-generated column (e.g. <code>conflicts_of_interest</code> or <code>absence_reason</code>)</li>
<li>Write modes:
  <ul>
    <li><code>full_table</code>: writes all rows with the new column</li>
    <li><code>processed_only</code>: writes only processed rows</li>
  </ul>
</li>
<li>Overwrite:
  <ul>
    <li><code>true</code>: recompute for all rows</li>
    <li><code>false</code>: fill missing only (default)</li>
  </ul>
</li>
<li>Validation: non-empty, max words, optional regex; repair prompt sent if failed</li>
</ul>
<h2 id="howitworks">How it works</h2>
<p>The pipeline enhances CSV/Parquet files by adding LLM-generated columns using <code>llm_table_runner.py</code>. Input data is read from S3, columns are selected, and up to five prompt variables are built from those columns as specified in a YAML config. Each prompt is rendered, sent to the OpenAI Responses API, and output (with optional web search and citation removal) is validated: non-empty, max words, and optional regex. Repair prompts are used and request retries occur on validation/API failure.</p>
<p>The pipeline chooses between writing all rows (<code>full_table</code>) or just processed rows (<code>processed_only</code>), with overwrite or resumable modes. Progress is autosaved as configured, and unique row IDs are handled by column or hash as needed.</p>
<p>Final results are written to S3 in CSV/Parquet. Run <code>llm_table_runner.py</code> with a YAML config that sets all workflow parameters.</p>
<h2 id="howtorun">How to run</h2>
<p>Run via:</p>
<pre><code class="bash language-bash">python process/llm_table_runner.py &amp;amp;amp;amp;amp;amp;amp;lt;task_config.yml&amp;amp;amp;amp;amp;amp;amp;gt;
</code></pre>
<p>The YAML config specifies S3 bucket/region, input/output keys, kept columns, ID, prompt vars, output column, prompt, LLM settings, run parameters, write mode, and validation.</p>
<ul>
<li>Reads CSV from S3 as per <code>input_key</code></li>
<li>Keeps specified columns</li>
<li>Ensures/creates ID column as configured</li>
<li>Loads any existing output to maintain resumability</li>
<li>Determines rows to process (missing/overwrite)</li>
<li>For each, builds prompt, calls OpenAI, retries/repairs as per config</li>
<li>Validates and, upon success, updates output column</li>
<li>Writes back CSV/Parquet to S3 as specified (<code>full_table</code> or <code>processed_only</code>)</li>
<li>Autosaves at interval; delays between requests</li>
<li>Logs paths, model, rows processed, and summary info</li>
</ul>
<p>Requires <code>OPENAI_API_KEY</code> and AWS credentials in the environment. Can be run manually or in CI (see the Automation section).</p>
<h2 id="dataqualityandvalidation">Data quality and validation</h2>
<p>The pipeline ensures data quality via configurable validation for LLM output: non-empty (require_non_empty), max words (max_words), and optional regex (regex_must_match). Repair prompts are used if validation fails.</p>
<p>ID columns are specified or generated by hash. Previous outputs are preserved unless overwrite is enabled. Citation removal is optional. Retries and request delays are configurable.</p>
<p>Outputs are saved to S3 in both CSV and Parquet formats. Write modes and overwrite behavior match configuration. Autosaving safeguards progress; validation and repair maintain data integrity.</p>
<h2 id="maintenance">Maintenance</h2>
<p>Update and maintain the <code>llm_table_runner.py</code> script and YAML configs with S3 locations, columns, prompt variables, and all operational parameters.</p>
<h3 id="dependencies">Dependencies</h3>
<p>Required Python packages:</p>
<ul>
<li><code>boto3</code></li>
<li><code>pandas</code></li>
<li><code>openai</code></li>
<li><code>pyarrow</code></li>
<li><code>pyyaml</code></li>
</ul>
<h3 id="configuration-1">Configuration</h3>
<ul>
<li>Reads/writes CSV and Parquet with S3</li>
<li>Supports <code>full_table</code> and <code>processed_only</code> write modes</li>
<li>Controls overwrite with <code>overwrite_existing</code></li>
<li>Up to 5 prompt variables from columns</li>
<li>Validation: non-empty, max words, regex (optional)</li>
<li>Citation stripping optional</li>
<li>Configurable autosaves</li>
<li>Row IDs by column or hash</li>
</ul>
<h3 id="executionandlogging">Execution and Logging</h3>
<ul>
<li>Executed via <code>python process/llm_table_runner.py &lt;task_config.yml&gt;</code></li>
<li>Supports test mode row limit</li>
<li>Logs progress, autosaves, and summary</li>
</ul>
<h3 id="integration">Integration</h3>
<ul>
<li>Works with GitHub Actions for manual runs and managing dependencies/environment</li>
</ul>
<h3 id="reliability">Reliability</h3>
<ul>
<li>OpenAI API calls auto-retry per configuration</li>
<li>Web search option for enhanced prompts</li>
</ul>
<p>Keep dependencies updated and monitor logs for stability and maintainability.</p>
<h2 id="orchestration">Orchestration</h2>
<p>Orchestration is handled by <code>process/llm_table_runner.py</code> and a YAML config specifying S3 paths, kept columns, prompt variables, LLM model, and operational settings.</p>
<p>The script reads the input from S3, builds up to five prompt variables, and calls the OpenAI Responses API (optionally with web search). Results are validated and written as CSV and Parquet to S3 using <code>full_table</code> or <code>processed_only</code> modes. Overwrite is controlled by <code>overwrite_existing</code>. Autosaving and validation occur per config, with repair prompts on failed validation. Row IDs are handled by column or hash; the pipeline is resumable.</p>
<p>To run:</p>
<pre><code class="bash language-bash">python process/llm_table_runner.py &amp;amp;amp;amp;amp;amp;amp;lt;task_config.yml&amp;amp;amp;amp;amp;amp;amp;gt;
</code></pre>
<p>Example YAMLs detail all required settings. GitHub Actions workflows automate pipeline setup, dependency install, and execution, using environment variables for necessary keys.</p>
<h2 id="lineage">Lineage</h2>
<p>The pipeline is built in <code>llm_table_runner.py</code> and processes CSV from S3, retaining selected columns as defined in YAML. It creates prompt variables, generates output with the OpenAI API (optional web search), writes CSV and Parquet back to S3 in either <code>full_table</code> or <code>processed_only</code> mode, and handles overwrite as configured. Validation and repair, citation removal, row IDs by column or hash, autosave, retry logic, and test mode are supported. Models include GPT-4.1-mini and GPT-5; env vars are used for credentials. The pipeline is resumable, flexible, and can be executed via command line or GitHub Actions with YAML config. Example YAMLs show real-world use cases; workflow files enable automation with test row overrides.</p>
