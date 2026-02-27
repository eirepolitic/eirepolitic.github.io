<hr>
<p>title: "AutoDoc Creation Pipeline"</p>
<h2 id="layoutdoc">layout: default</h2>
<h1 id="memberimagespipeline">Member Images Pipeline</h1>
<p><strong>Project:</strong> eirepolitic<br><strong>Type:</strong> pipeline<br><strong>Last generated:</strong> 2026-02-26T04:31:22.458471Z</p>
<hr>
<h2 id="overview">Overview</h2>
<h3 id="purpose">Purpose</h3>
<p>This pipeline extracts member profile image URLs from the Oireachtas website and builds an Athena table with member codes, names, and corresponding image URLs.</p>
<h3 id="scope">Scope</h3>
<p>The pipeline reads <code>s3://&lt;bucket&gt;/raw/members/oireachtas_members_34th_dail.csv</code> and outputs results as CSV and Parquet to S3. It normalizes member URIs, uses BeautifulSoup to find profile images using configured selectors, and writes found photo URLs. The execution is resumable, updating only missing <code>photo_url</code> fields in the output CSV if it exists. Autosave occurs every 50 rows (default). Configuration uses environment variables for AWS/S3, pipeline parameters, GitHub Actions workflow integration, and dependency management (notably <code>beautifulsoup4</code> and <code>pyarrow</code>). The workflow accepts a <code>test_rows</code> input to limit processing for testing (<code>default: 50</code>).</p>
<h2 id="assets">Assets</h2>
<p>The pipeline extracts photo URLs from Oireachtas profile pages using:</p>
<pre><code>s3://&amp;amp;amp;amp;amp;amp;amp;lt;bucket&amp;amp;amp;amp;amp;amp;amp;gt;/raw/members/oireachtas_members_34th_dail.csv
</code></pre>
<p>Output is written to:</p>
<ul>
<li>CSV: <code>s3://&lt;bucket&gt;/processed/members/members_photo_urls.csv</code></li>
<li>Parquet: <code>s3://&lt;bucket&gt;/processed/members/parquets/members_photo_urls.parquet</code></li>
</ul>
<p>If the output CSV exists, only rows with missing <code>photo_url</code> are processed.</p>
<p>Key environment variables:</p>
<ul>
<li><code>AWS_ACCESS_KEY_ID</code></li>
<li><code>AWS_SECRET_ACCESS_KEY</code></li>
<li><code>AWS_REGION</code></li>
<li><code>S3_BUCKET</code> (default: <code>eirepolitic-data</code>)</li>
<li><code>INPUT_KEY</code> (default: <code>raw/members/oireachtas_members_34th_dail.csv</code>)</li>
<li><code>OUTPUT_CSV_KEY</code> (default: <code>processed/members/members_photo_urls.csv</code>)</li>
<li><code>OUTPUT_PARQUET_KEY</code> (default: <code>processed/members/parquets/members_photo_urls.parquet</code>)</li>
<li><code>REQUEST_TIMEOUT</code> (default: 10)</li>
<li><code>DELAY_BETWEEN_REQUESTS</code> (default: 0.2)</li>
<li><code>AUTOSAVE_INTERVAL</code> (default: 50)</li>
<li><code>TEST_ROWS</code> (default: 0)</li>
</ul>
<p>Profile photo selectors searched:</p>
<ul>
<li><code>img.c-member-about__img</code></li>
<li><code>img.member-profile-photo</code></li>
<li><code>div.member-image img</code></li>
<li>Any <code>img</code> with <code>src</code> containing <code>/media/members/photo/</code></li>
</ul>
<p>Member URIs are normalized to public profile URLs on <code>oireachtas.ie</code>.</p>
<p>The GitHub Actions workflow <strong>Build Member Photo URLs (Manual)</strong> runs the pipeline on <code>ubuntu-latest</code>, installs dependencies, and accepts a <code>test_rows</code> parameter to restrict processing for tests.</p>
<h2 id="inputsandoutputs">Inputs and Outputs</h2>
<h3 id="inputs">Inputs</h3>
<ul>
<li>CSV input: <code>s3://&lt;bucket&gt;/raw/members/oireachtas_members_34th_dail.csv</code></li>
<li>Columns: <code>member_code</code>, <code>full_name</code>, <code>uri</code></li>
<li><code>INPUT_KEY</code> env variable defaults to <code>raw/members/oireachtas_members_34th_dail.csv</code></li>
<li>AWS credentials and region: <code>AWS_ACCESS_KEY_ID</code>, <code>AWS_SECRET_ACCESS_KEY</code>, <code>AWS_REGION</code></li>
<li>Optional <code>TEST_ROWS</code> (default 0) to limit processing</li>
</ul>
<h3 id="outputs">Outputs</h3>
<ul>
<li>CSV: <code>s3://&lt;bucket&gt;/processed/members/members_photo_urls.csv</code></li>
<li>Parquet: <code>s3://&lt;bucket&gt;/processed/members/parquets/members_photo_urls.parquet</code></li>
<li>Env variables: <code>OUTPUT_CSV_KEY</code>, <code>OUTPUT_PARQUET_KEY</code></li>
<li>Columns: <code>member_code</code>, <code>full_name</code>, <code>photo_url</code></li>
<li>Resumable: only processes rows with missing <code>photo_url</code></li>
<li>Configurable <code>AUTOSAVE_INTERVAL</code> (default: 50)</li>
<li>Delay between requests: <code>DELAY_BETWEEN_REQUESTS</code> (default: 0.2s)</li>
<li>Request timeout: <code>REQUEST_TIMEOUT</code> (default: 10s)</li>
</ul>
<h2 id="howitworks">How it works</h2>
<p>The pipeline builds a table of member codes, names, and photo URLs by scraping Oireachtas public profile pages. Input data is loaded from S3 and processed to produce output files.</p>
<p>Member URIs are normalized to public profile URLs. Profile photo URLs are scraped using prioritized selectors, with fallbacks as needed.</p>
<p>Results are written to S3 as CSV and Parquet. The script resumes if the output CSV exists, filling only missing <code>photo_url</code> values. It uses autosave (every 50 rows by default) and configurable delays.</p>
<p>All behavior is controlled via environment variables. Pipeline execution can be triggered manually via the <strong>Build Member Photo URLs (Manual)</strong> workflow, which passes configuration to the Python script and manages job execution.</p>
<h2 id="howtorun">How to run</h2>
<p>Run <code>members_photo_urls.py</code> to extract <code>member_code</code>, <code>full_name</code>, and <code>photo_url</code> by scraping Oireachtas profile pages.</p>
<h3 id="inputandoutput">Input and Output</h3>
<ul>
<li><strong>Input:</strong> <code>s3://&lt;bucket&gt;/raw/members/oireachtas_members_34th_dail.csv</code></li>
<li><strong>Output:</strong>
<ul>
<li>CSV: <code>s3://&lt;bucket&gt;/processed/members/members_photo_urls.csv</code></li>
<li>Parquet: <code>s3://&lt;bucket&gt;/processed/members/parquets/members_photo_urls.parquet</code></li>
</ul>
</li>
</ul>
<h3 id="behavior">Behavior</h3>
<ul>
<li>Checks columns: <code>member_code</code>, <code>full_name</code>, <code>uri</code></li>
<li>If output CSV exists, resumes to fill missing <code>photo_url</code> only</li>
<li>Normalizes URIs to public profiles</li>
<li>Scrapes images via prioritized selectors/fallbacks</li>
<li>Saves progress to both output files on S3</li>
<li>Autosaves every <code>AUTOSAVE_INTERVAL</code> and applies delays (<code>DELAY_BETWEEN_REQUESTS</code>)</li>
</ul>
<h3 id="environmentvariables">Environment Variables</h3>
<p>Relevant variables (defaults shown):</p>
<ul>
<li><code>AWS_ACCESS_KEY_ID</code>, <code>AWS_SECRET_ACCESS_KEY</code>, <code>AWS_REGION</code></li>
<li><code>S3_BUCKET</code> (default: <code>eirepolitic-data</code>)</li>
<li><code>INPUT_KEY</code> (default: <code>raw/members/oireachtas_members_34th_dail.csv</code>)</li>
<li><code>OUTPUT_CSV_KEY</code> (default: <code>processed/members/members_photo_urls.csv</code>)</li>
<li><code>OUTPUT_PARQUET_KEY</code> (default: <code>processed/members/parquets/members_photo_urls.parquet</code>)</li>
<li><code>REQUEST_TIMEOUT</code> (default: 10)</li>
<li><code>DELAY_BETWEEN_REQUESTS</code> (default: 0.2)</li>
<li><code>AUTOSAVE_INTERVAL</code> (default: 50)</li>
<li><code>TEST_ROWS</code> (default: 0)</li>
</ul>
<h3 id="runningthepipeline">Running the Pipeline</h3>
<p>Run manually via the <strong>"Build Member Photo URLs (Manual)"</strong> GitHub Actions workflow, on <code>ubuntu-latest</code>, with required environment variables and dependencies. Accepts optional <code>TEST_ROWS</code> for test-limited runs.</p>
<h2 id="dataqualityandvalidation">Data quality and validation</h2>
<p>Data quality and validation are maintained by requiring <code>member_code</code>, <code>full_name</code>, and <code>uri</code> columns in the source CSV. Member URIs are normalized to ensure valid profile URLs. Only rows with missing <code>photo_url</code> are processed. CSS selector fallback for scraping improves robustness. Missing data (e.g. no profile or image) results in <code>photo_url</code> set as missing (<code>pd.NA</code>).</p>
<p>Requests use a default 0.2s delay and 10s timeout to avoid server overload or timeouts. Autosave writes both output formats to S3 every 50 processed rows, ensuring resumability and minimal data loss risk. If the output CSV exists, only missing <code>photo_url</code> cells are filled.</p>
<p>The pipeline uses pandas, runs on Python 3.11, and supports manual triggering and row limits for controlled, validated execution.</p>
<h2 id="maintenance">Maintenance</h2>
<p>The <code>members_photo_urls.py</code> script extracts and writes <code>member_code</code>, <code>full_name</code>, and <code>photo_url</code> by scraping Oireachtas member profile pages.</p>
<h3 id="datainputsandoutputs">Data Inputs and Outputs</h3>
<ul>
<li><strong>Input:</strong> <code>s3://&lt;bucket&gt;/raw/members/oireachtas_members_34th_dail.csv</code></li>
<li><strong>Outputs:</strong>
<ul>
<li>CSV: <code>s3://&lt;bucket&gt;/processed/members/members_photo_urls.csv</code></li>
<li>Parquet: <code>s3://&lt;bucket&gt;/processed/members/parquets/members_photo_urls.parquet</code></li>
</ul>
</li>
</ul>
<h3 id="resumability">Resumability</h3>
<p>If the output CSV exists, only rows with missing <code>photo_url</code> are reprocessed.</p>
<h3 id="environmentvariables-1">Environment Variables</h3>
<p>Configurable via:</p>
<ul>
<li><code>AWS_ACCESS_KEY_ID</code>, <code>AWS_SECRET_ACCESS_KEY</code>, <code>AWS_REGION</code></li>
<li><code>S3_BUCKET</code> (default: <code>eirepolitic-data</code>)</li>
<li><code>INPUT_KEY</code> (default: <code>raw/members/oireachtas_members_34th_dail.csv</code>)</li>
<li><code>OUTPUT_CSV_KEY</code> (default: <code>processed/members/members_photo_urls.csv</code>)</li>
<li><code>OUTPUT_PARQUET_KEY</code> (default: <code>processed/members/parquets/members_photo_urls.parquet</code>)</li>
<li><code>REQUEST_TIMEOUT</code> (default: 10)</li>
<li><code>DELAY_BETWEEN_REQUESTS</code> (default: 0.2)</li>
<li><code>AUTOSAVE_INTERVAL</code> (default: 50)</li>
<li><code>TEST_ROWS</code> (default: 0)</li>
</ul>
<h3 id="scrapingandprocessing">Scraping and Processing</h3>
<ul>
<li>Normalizes <code>data.oireachtas.ie</code> URIs to public profiles</li>
<li>Scrapes images with BeautifulSoup using prioritized selectors</li>
<li>Handles missing profiles/images and network errors robustly</li>
</ul>
<h3 id="awss3interaction">AWS S3 Interaction</h3>
<ul>
<li>Uses <code>boto3</code> for S3 IO</li>
<li>Autosaves every <code>AUTOSAVE_INTERVAL</code> rows</li>
</ul>
<h3 id="automation">Automation</h3>
<ul>
<li>Manual workflow in GitHub Actions (<code>member_photo_urls.yml</code> with <code>workflow_dispatch</code>)</li>
<li>Workflow sets AWS/S3 env variables, installs dependencies, runs the script</li>
<li>Supports <code>TEST_ROWS</code> for partial/test runs</li>
</ul>
<h2 id="orchestration">Orchestration</h2>
<p>The pipeline builds a member images Athena table by scraping image URLs from Oireachtas profiles, using input CSV data in the S3 bucket <code>eirepolitic-data</code> (default).</p>
<p>Implemented in Python, uses <code>boto3</code>, <code>pandas</code>, <code>requests</code>, <code>BeautifulSoup</code>, and <code>pyarrow</code>. Member URIs are normalized, images extracted with prioritized selectors, and output written to S3 in CSV and Parquet formats.</p>
<p>If the output CSV exists, only missing <code>photo_url</code> rows are processed. Autosave occurs every 50 rows.</p>
<p>Outputs:</p>
<ul>
<li>CSV: <code>processed/members/members_photo_urls.csv</code></li>
<li>Parquet: <code>processed/members/parquets/members_photo_urls.parquet</code></li>
</ul>
<p>Configurable via environment variables, including AWS credentials, S3 paths, timeouts, delays, autosave interval, and test row limit.</p>
<p>Manual execution is via the <strong>Build Member Photo URLs (Manual)</strong> GitHub Actions workflow, which installs dependencies, sets up configuration, and runs the script with row limiting if desired.</p>
<h2 id="lineage">Lineage</h2>
<p>The pipeline constructs a table with <code>member_code</code>, <code>full_name</code>, <code>photo_url</code> by reading <code>s3://&lt;bucket&gt;/raw/members/oireachtas_members_34th_dail.csv</code>. Member URIs are normalized to public profile URLs, and profile HTML is scraped for photo URLs via prioritized CSS selectors.</p>
<p>If output CSV exists, only rows without <code>photo_url</code> are processed. Final data is written as CSV and Parquet to S3:</p>
<ul>
<li><code>s3://&lt;bucket&gt;/processed/members/members_photo_urls.csv</code></li>
<li><code>s3://&lt;bucket&gt;/processed/members/parquets/members_photo_urls.parquet</code></li>
</ul>
<p>Configuration is through environment variables for AWS, S3 bucket, input/output keys, timeout, delay, autosave, and row-limiting.</p>
<p>The pipeline is triggered by the <strong>Build Member Photo URLs (Manual)</strong> workflow on <code>ubuntu-latest</code>, which handles environment setup and dependencies before running the script, with optional row limit (<code>default: 50</code> for tests).</p>
