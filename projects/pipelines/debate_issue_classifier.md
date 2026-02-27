<hr>
<p>title: "AutoDoc Creation Pipeline"</p>
<h2 id="layoutdoc">layout: default</h2>
<h1 id="debateissueclassifier">Debate Issue Classifier</h1>
<p><strong>Project:</strong> eirepolitic<br><strong>Type:</strong> pipeline<br><strong>Last generated:</strong> 2026-02-26T04:07:03.392577Z</p>
<hr>
<h2 id="overview">Overview</h2>
<h3 id="purpose">Purpose</h3>
<p>The "Debate Issue Classifier" pipeline in the "eirepolitic" project assigns political issue categories to speech sections from Dáil Éireann debate records, using an OpenAI language model. It processes debate data, extracts and deduplicates speech segments, and classifies each into one of 25 predefined political issue categories or "NONE".</p>
<h3 id="scope">Scope</h3>
<p>The pipeline fetches all Dáil 34 debates without date filtering, downloads raw XML files by date and debate ID, and uploads them to S3 at "raw/debates/xml". It parses XML files (Akoma Ntoso standard) for speech records, deduplicates, and stores results as CSV in S3. Speeches with fewer than 20 words or empty are labeled "NONE". Others are classified into one issue category using an OpenAI model (default "gpt-4o-mini") via recursive prompt refinement. Results are saved as CSV and Parquet in S3 under "processed/debates". The pipeline autosaves progress and runs monthly via GitHub Actions, with manual triggers and configuration through environment variables.</p>
<h2 id="assets">Assets</h2>
<p>The pipeline works with debate data assets stored in the <code>eirepolitic-data</code> S3 bucket:</p>
<ul>
<li>
<p><strong>Raw XML Debate Files:</strong> <code>raw/debates/xml/</code> prefix, named <code>YYYY-MM-DD__&lt;debate_id&gt;.xml</code>, downloaded from the Oireachtas API for Dáil 34, uploaded with content type <code>application/xml</code> (overwriting allowed), with absolute XML URIs.</p>
</li>
<li>
<p><strong>Extracted Debate Speeches CSV:</strong> <code>raw/debates/debate_speeches_extracted.csv</code>, contains parsed speeches with section, speaker, text, and order. Duplicate speeches are removed by date, speaker, and text.</p>
</li>
<li>
<p><strong>Classified Speeches Outputs:</strong> Classified CSV at <code>processed/debates/debate_speeches_classified.csv</code> and Parquet under <code>processed/debates/parquets/</code>; contains speeches classified into one political issue category from the 25-category list (including "NONE").</p>
</li>
</ul>
<p>Additional details:</p>
<ul>
<li>Configuration via environment variables: <code>AWS_ACCESS_KEY_ID</code>, <code>AWS_SECRET_ACCESS_KEY</code>, <code>AWS_REGION</code>, <code>CHAMBER_ID</code>, <code>LANG</code>, <code>API_LIMIT</code>, <code>API_SLEEP</code>, <code>DOWNLOAD_TIMEOUT</code>.</li>
<li>Oireachtas API base: <code>https://api.oireachtas.ie/v1</code>. Data base: <code>https://data.oireachtas.ie</code>.</li>
<li>Workflows in GitHub Actions automate extraction/classification using Python 3.11 and dependencies from <code>requirements.txt</code>.</li>
</ul>
<h2 id="inputsandoutputs">Inputs and Outputs</h2>
<h3 id="inputs">Inputs</h3>
<ul>
<li>Debate records from Oireachtas API <code>/debates</code> (default: <code>/ie/oireachtas/house/dail/34</code>).</li>
<li>Raw XML debate files in S3 at <code>raw/debates/xml/</code>.</li>
<li>Extracted speeches CSV at <code>raw/debates/debate_speeches_extracted.csv</code> in S3.</li>
<li>Environment variables for configuration: AWS credentials, region, chamber ID, language, API limits, OpenAI API key and model, and classification parameters.</li>
<li>Speech text column <code>"Speech Text"</code> from the extracted CSV.</li>
</ul>
<h3 id="outputs">Outputs</h3>
<ul>
<li>Raw debate XML files at <code>s3://eirepolitic-data/raw/debates/xml/YYYY-MM-DD__&lt;debate_id&gt;.xml</code>.</li>
<li>Extracted debate speeches CSV at <code>s3://eirepolitic-data/raw/debates/debate_speeches_extracted.csv</code>.</li>
<li>Classified speeches CSV at <code>s3://eirepolitic-data/processed/debates/debate_speeches_classified.csv</code>.</li>
<li>Classified speeches Parquet at <code>s3://eirepolitic-data/processed/debates/parquets/debate_speeches_classified.parquet</code>.</li>
<li>Classification labels in the <code>"PoliticalIssues"</code> column.</li>
<li>Autosaved partial classification results in CSV and Parquet formats.</li>
</ul>
<h2 id="howitworks">How it works</h2>
<p>For Dáil Éireann debates, the pipeline fetches Dáil 34 debates, downloads and uploads XML files to S3 ("raw/debates/xml/", <code>YYYY-MM-DD__&lt;debate_id&gt;.xml</code>). It uses environment variables for configuration, extracts metadata, normalizes XML URIs, and uploads XML files to S3.</p>
<p>It lists XML files in S3, parses them into speech records using Akoma Ntoso XML, and extracts the debate date, section, speaker, text, and order. Deduplicates speeches by date, speaker, and text, saving as <code>raw/debates/debate_speeches_extracted.csv</code> in S3.</p>
<p>The pipeline classifies each speech into one political issue category via OpenAI LLM, using 25 categories including "NONE". The model is prompted to select one category, with up to five recursive refinements if the output is invalid. Speeches under 20 words or empty are labeled "NONE".</p>
<p>Results are saved as CSV and Parquet to S3 (<code>processed/debates/debate_speeches_classified.csv</code> and <code>processed/debates/parquets/</code>), with deterministic speech IDs (by date, speaker, order, and text). Existing classifications are reused. Autosaving tracks partial progress.</p>
<p>Retries and exponential backoff address API rate limits. Monthly execution is scheduled by GitHub Actions at 09:15 UTC on the 1st; workflow steps include repository checkout, Python setup, dependency installation, XML extract/conversion, and member extraction. A manual workflow triggers the speech classifier for selectable row limits.</p>
<h2 id="howtorun">How to run</h2>
<p>The pipeline uses three main scripts for extracting, processing, and classifying Dáil 34 debates, interacting with AWS S3 and OpenAI GPT models.</p>
<h3 id="1extractionofdebatesxml">1. Extraction of Debates XML</h3>
<p>Run <code>monthly_extract.py</code> to:</p>
<ul>
<li>Paginate through the <code>/debates</code> API for the chamber (default <code>/ie/oireachtas/house/dail/34</code>).</li>
<li>Download XML files as <code>YYYY-MM-DD__&lt;debate_id&gt;.xml</code>.</li>
<li>Normalize XML URIs to full URLs if needed.</li>
<li>Upload files to S3 <code>raw/debates/xml/</code> with content type <code>application/xml</code> (overwriting allowed).</li>
</ul>
<p>Required AWS variables:</p>
<pre><code class="bash language-bash">AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
</code></pre>
<p>Optional variables (defaults):</p>
<pre><code class="bash language-bash">CHAMBER_ID=/ie/oireachtas/house/dail/34
LANG=en
API_LIMIT=200
API_SLEEP=0.2
DOWNLOAD_TIMEOUT=30
</code></pre>
<h3 id="2xmltocsvconversion">2. XML to CSV Conversion</h3>
<p>Run <code>debates_xml_to_csv_s3.py</code> to:</p>
<ul>
<li>List XML files in S3 <code>raw/debates/xml/</code>.</li>
<li>Parse Akoma Ntoso XML files (<code>http://docs.oasis-open.org/legaldocml/ns/akn/3.0/CSD13</code>).</li>
<li>Extract and deduplicate speech records (by <code>Debate Date</code>, <code>Speaker Name</code>, <code>Speech Text</code>).</li>
<li>Save deduplicated CSV to <code>raw/debates/debate_speeches_extracted.csv</code> in S3.</li>
</ul>
<h3 id="3speechissueclassification">3. Speech Issue Classification</h3>
<p>Run <code>speech_issue_classifier.py</code> to classify speeches using OpenAI GPT models:</p>
<ul>
<li>Read extracted CSV from S3 (<code>raw/debates/debate_speeches_extracted.csv</code>).</li>
<li>Generate <code>speech_id</code> for each speech (date, speaker, order, text).</li>
<li>Retry classification up to 5 times if output is invalid, refining prompt as needed.</li>
<li>Classify using a fixed list of political issues including "Macroeconomics", "Health", "Education", "Environment", "NONE", etc.</li>
<li>Write CSV to <code>processed/debates/debate_speeches_classified.csv</code>, and Parquet files under <code>processed/debates/parquets/</code>.</li>
</ul>
<p>Supported environment variables:</p>
<pre><code class="bash language-bash">S3_BUCKET
INPUT_KEY
OUTPUT_KEY
AWS_REGION
OPENAI_MODEL
OPENAI_REASONING_EFFORT
OPENAI_VERBOSITY
MAX_OUTPUT_TOKENS
DELAY_BETWEEN_REQUESTS
MAX_ITERATIONS
AUTOSAVE_INTERVAL
TEST_ROWS
</code></pre>
<h3 id="automationviagithubactions">Automation via GitHub Actions</h3>
<p>Two workflows:</p>
<ul>
<li><code>monthly_extract.yml</code>: Runs monthly on the 1st at 09:15 UTC, extracting, converting XML to CSV, and extracting members.</li>
<li><code>speech_issue_classifier.yml</code>: Manual trigger, runs speech classification, and converts CSV to Parquet.</li>
</ul>
<p>Both use Python 3.11, <code>requirements.txt</code> dependencies, and access AWS/OpenAI credentials from GitHub Secrets.</p>
<h2 id="dataqualityandvalidation">Data quality and validation</h2>
<p>The pipeline ensures reliable outputs through checks at extraction, transformation, and classification stages.</p>
<h3 id="extractionandrawdatahandling">Extraction and Raw Data Handling</h3>
<ul>
<li>Downloads all Dáil 34 debates as XML (<code>raw/debates/xml/</code>) using the strict naming convention <code>YYYY-MM-DD__&lt;debate_id&gt;.xml</code> for traceability.</li>
<li><code>monthly_extract.py</code> uses environment-based AWS config and a <code>safe_get</code> with retries/backoff for reliability. Metadata is extracted with fallbacks and URIs normalized. XMLs are uploaded with <code>application/xml</code> type.</li>
</ul>
<h3 id="xmltocsvconversionandspeechextraction">XML-to-CSV Conversion and Speech Extraction</h3>
<ul>
<li><code>debates_xml_to_csv_s3.py</code> downloads/parses all XMLs and extracts debate date, section ID/name, speaker name (from references or XML), speech text, and order.</li>
<li>Deduplicates speeches (by date, speaker, and text), saves UTF-8 CSV to S3 (<code>raw/debates/debate_speeches_extracted.csv</code>).</li>
</ul>
<h3 id="politicalissueclassificationandvalidation">Political Issue Classification and Validation</h3>
<ul>
<li><code>speech_issue_classifier.py</code> loads speeches CSV, ensures deterministic <code>speech_id</code>, supports incremental processing by loading prior classifications.</li>
<li>Classifies each speech with OpenAI GPT (default <code>gpt-4o-mini</code>) with controllable parameters.</li>
<li>Validates outputs against the 25-category list (including "NONE"); recursively refines invalid outputs.</li>
<li>Saves results to CSV (<code>processed/debates/debate_speeches_classified.csv</code>) and Parquet (<code>processed/debates/parquets/debate_speeches_classified.parquet</code>).</li>
</ul>
<h3 id="workflowautomationandenvironmentconsistency">Workflow Automation and Environment Consistency</h3>
<ul>
<li>GitHub Actions automate monthly extraction and manual classification.</li>
<li>Workflows handle environment setup/dependencies and inject AWS credentials from secrets.</li>
<li>Manual triggers allow specifying number of test rows.</li>
</ul>
<p>These measures maintain data quality, consistent formatting, and validated classifications throughout the pipeline lifecycle.</p>
<h2 id="maintenance">Maintenance</h2>
<p>The pipeline consists of scripts and automated workflows requiring correct environment setup and AWS credentials.</p>
<h3 id="environmentvariables">Environment Variables</h3>
<ul>
<li>
<p><strong>Extraction (<code>monthly_extract.py</code>):</strong><br>Requires <code>AWS_ACCESS_KEY_ID</code>, <code>AWS_SECRET_ACCESS_KEY</code>, <code>AWS_REGION</code>.<br>Optional: <code>CHAMBER_ID</code> (default <code>/ie/oireachtas/house/dail/34</code>), <code>LANG</code> (default <code>en</code>), <code>API_LIMIT</code> (default <code>200</code>), <code>API_SLEEP</code> (default <code>0.2</code>), <code>DOWNLOAD_TIMEOUT</code> (default <code>30</code>).</p>
</li>
<li>
<p><strong>Speech Issue Classification (<code>speech_issue_classifier.py</code>):</strong> Uses: <code>S3_BUCKET</code>, <code>INPUT_KEY</code>, <code>OUTPUT_KEY</code>, <code>OPENAI_MODEL</code>, <code>OPENAI_REASONING_EFFORT</code>, <code>OPENAI_VERBOSITY</code>, <code>MAX_OUTPUT_TOKENS</code>, <code>DELAY_BETWEEN_REQUESTS</code>, <code>MAX_ITERATIONS</code>, <code>AUTOSAVE_INTERVAL</code>, <code>TEST_ROWS</code>.</p>
</li>
</ul>
<h3 id="datahandlingandstorage">Data Handling and Storage</h3>
<ul>
<li>
<p>Debate XMLs are extracted without date filtering to <code>raw/debates/xml/</code> with naming <code>YYYY-MM-DD__&lt;debate_id&gt;.xml</code> (overwriting allowed).</p>
</li>
<li>
<p>Extraction handles retries and backoff, paginates <code>/debates</code> API, normalizes URIs before upload.</p>
</li>
<li>
<p><code>debates_xml_to_csv_s3.py</code> lists/parses all S3 XMLs, extracts/deduplicates speeches, and saves CSV at <code>raw/debates/debate_speeches_extracted.csv</code>.</p>
</li>
<li>
<p><code>speech_issue_classifier.py</code> classifies each speech, saves as CSV/Parquet in S3, generates deterministic <code>speech_id</code>, and validates outputs (retries/refines as needed).</p>
</li>
<li>
<p>Classified Parquet files are placed under <code>processed/debates/parquets/</code>.</p>
</li>
</ul>
<h3 id="automation">Automation</h3>
<ul>
<li>
<p>Automated by GitHub Actions using Python 3.11 and boto3. <code>monthly_extract.yml</code> (monthly at 09:15 UTC) handles extraction/conversion/member extraction; <code>speech_issue_classifier.yml</code> (manual) runs classification/Parquet conversion. AWS credentials/region are injected via secrets.</p>
</li>
</ul>
<p>Monitor environment variables, AWS credentials, and workflow logs for seamless operation and troubleshooting.</p>
<h2 id="orchestration">Orchestration</h2>
<p>The pipeline is orchestrated by GitHub Actions workflows, automating extraction, processing, and classification monthly, with support for manual triggers.</p>
<h3 id="monthlyextractworkflow">Monthly Extract Workflow</h3>
<p>The "Monthly Extract" GitHub Actions workflow runs at 09:15 UTC on the 1st of each month and can be triggered manually. On Ubuntu latest, it executes in sequence:</p>
<ul>
<li>Checks out the repository.</li>
<li>Sets up Python 3.11.</li>
<li>Installs <code>requirements.txt</code> dependencies.</li>
<li>Runs <code>extract/monthly_extract.py</code> to fetch all Dáil 34 debates (XML files at <code>raw/debates/xml/</code>, overwrite enabled).</li>
<li>Runs <code>extract/debates_xml_to_csv_s3.py</code> to parse S3 XML files, extract/deduplicate speeches, and save CSV as <code>raw/debates/debate_speeches_extracted.csv</code>.</li>
<li>Runs <code>extract/monthly_members_extract.py</code> for members data extraction.</li>
</ul>
<h3 id="speechissueclassificationworkflow">Speech Issue Classification Workflow</h3>
<p>Manually triggered in GitHub Actions, with a <code>test_rows</code> parameter to limit processed rows. Runs on Ubuntu latest with steps:</p>
<ul>
<li>Check out repository and set up Python 3.11.</li>
<li>Install dependencies.</li>
<li>Run <code>process/speech_issue_classifier.py</code> using OpenAI API (default "gpt-4.1-mini" or GPT-5), set via environment parameters; supports <code>test_rows</code>.</li>
<li>Convert the classified CSV to Parquet using <code>process/debate_speeches_csv_to_parquet.py</code>.</li>
</ul>
<p>The classifier reads the CSV from S3 (<code>raw/debates/debate_speeches_extracted.csv</code>), classifies each speech (fixed list, including "NONE"), writes CSV/Parquet to <code>processed/debates/debate_speeches_classified.csv</code> and Parquet path, autosaves progress every 50 rows, and retries OpenAI API up to 5 times.</p>
<h3 id="environmentandcredentials">Environment and Credentials</h3>
<p>All workflows use AWS credentials and region for S3, and OpenAI API key for classification.</p>
<h2 id="lineage">Lineage</h2>
<p>The pipeline extracts all Dáil 34 debates, downloading XML records via the Oireachtas API (<code>/debates</code>), extracting debate date, XML URI, and debate ID, and normalizing URIs with <code>https://data.oireachtas.ie</code>. Raw XMLs are named <code>YYYY-MM-DD__&lt;debate_id&gt;.xml</code> and uploaded to S3 <code>raw/debates/xml</code> (overwriting allowed, <code>application/xml</code> type).</p>
<p>A downstream process lists and parses all S3 XMLs (Akoma Ntoso XML), extracting speech records (debate date/section ID/name/speaker/text/order). Speaker names are obtained from references or speech tags. Deduplication uses (date, speaker, text) and stable IDs (hashed from date, speaker, order, text). Deduplicated speeches are saved as <code>raw/debates/debate_speeches_extracted.csv</code> in S3.</p>
<p>Each speech is classified via OpenAI (default <code>gpt-4o-mini</code>) into one predefined political issue category. Classification results are saved as CSV and Parquet at <code>processed/debates/debate_speeches_classified.csv</code> and <code>processed/debates/parquets/debate_speeches_classified.parquet</code>, supporting autosaves and API retries.</p>
<p>Pipeline configuration uses environment variables: AWS credentials/region, chamber ID, language (<code>en</code>), API limit (200), sleep (0.2s), and timeout (30s).</p>
<p>GitHub Actions automate the pipeline: monthly extraction on the 1st at 09:15 UTC (includes extraction, XML-to-CSV, members extract), and a manual classification workflow for missing rows with configurable limits.</p>
