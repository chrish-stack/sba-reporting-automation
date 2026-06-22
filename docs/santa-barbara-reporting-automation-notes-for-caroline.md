# Santa Barbara Reporting Automation Notes for Caroline

Prepared for: Caroline Purdy
Prepared by: Chris Hicks / Hermes
Date: 2026-06-22

## 1. Executive read

The most important clarification is that the primary pain point is not the team's ability to understand the data once it is pulled. The team has already found a workable path for interpreting/deciphering pulled data with ChatGPT and internal reporting knowledge.

The highest-value first focus is making the data-pulling process cleaner, faster, and more repeatable.

The current workflow loses the most time in getting the right information out of each platform and into a usable structure:

- selecting the right platform views/reports,
- exporting at the right level,
- making sure the export includes the right columns,
- removing unneeded fields,
- splitting naming fields into useful classification columns,
- handling platform-specific quirks,
- and getting the output into the weekly reporting sheet in a clean enough shape that the existing pivot tables and ChatGPT-assisted insight workflow can work.

Long term, the ideal solution is one flow: pull data, normalize it, apply rules, generate the cleaned weekly table, and support insight generation. But the first project phase should prioritize the cleanest possible pull/extract process because that is the bottleneck the team called out.

## 2. Source materials reviewed

### Shared ChatGPT thread

Source: https://chatgpt.com/share/6a39877a-2c14-83ea-8487-3b3b7df2edf4

The thread included:

- cleaned transcript notes from a screen-recording / workflow conversation,
- a meeting summary titled `Streamlining Multi-Platform Data Reporting Process`,
- key points, action items, and open questions,
- and a synthesized project brief titled `Santa Barbara Reporting Automation Brief`.

### Local how-to PDF

Source file: `How To_ Santa Barbara Reports.pdf`

The PDF is a 10-page how-to document covering:

- weekly reports,
- monthly reports,
- quarterly reports,
- platform exports,
- TapClicks report handling,
- pivot-table filtering,
- Meta, YouTube, Meltwater, GA4/organic context, and troubleshooting.

## 3. Notes from the ChatGPT thread / transcript cleanup

### Workflow context from the conversation

The team discussed the current reporting workflow while looking at the Santa Barbara reporting spreadsheet. A major theme was that campaign/ad naming conventions carry important classification data.

For example, different Luxury Drive audiences may have differentiators such as:

- Outdoor,
- Food and Drink,
- Wellness,
- month,
- objective,
- Facebook / Instagram placement,
- and campaign/audience context.

The team noted that some of this information may be clearly listed in the ad name. In those cases, redundant pieces such as Facebook, Instagram, month, or objective may be removed or separated because the useful distinction is already represented elsewhere in the naming structure.

There was also discussion that the audiences are mostly predetermined. They can change, but not without the team knowing. If a new audience is introduced, such as an Air Services campaign with Chicago as an audience, the media buyer or team would usually have visibility. This matters because a rules-based system can maintain a list of known audiences and only flag unfamiliar values for review.

### Key cleaned transcript points

The conversation framed the reporting problem this way:

- The team has been motivated to fix the process, but because the client is billed on actuals, the urgency was previously lower.
- The workflow has become inefficient enough that the team would rather not spend hours manually tracking small pieces of spend and performance across platforms.
- There is a lot of historical reporting logic. The report has evolved over time as the team added new platforms, campaigns, ads, and audiences.
- The current yearly report already has nearly 10,000 rows, and similar files exist for other years.
- Because of that complexity, rebuilding every manual step may not be the right starting point.
- The better starting point is to define the desired output and build toward that.

One important recommendation from the thread was to start with a smaller test environment rather than flooding the system with all historical data immediately.

Suggested first test:

- one platform,
- one campaign family,
- one audience or audience group,
- one straightforward case,
- and one messy edge case.

The discussion specifically referenced starting with something like Facebook / Meta Brand to Luxury Drive as a bite-sized validation case.

### What Chris asked for in the conversation

Chris asked for:

- the current process,
- the desired solution,
- simple and extreme examples,
- training docs,
- screen recordings if available,
- access to the current report,
- and potentially TapClicks API access or a login/API-code walkthrough.

The explicit strategy was:

1. Start with core context.
2. Get one simple case.
3. Get one extreme/messy case.
4. Stress test the workflow.
5. Validate the automation before scaling.

## 4. Meeting summary from the shared thread

Title: Streamlining Multi-Platform Data Reporting Process
Date/time shown in thread: June 22, 2026, 2:36 PM EDT

### Overall summary

The team discussed a manual process of exporting and consolidating advertising data from multiple platforms into Google Sheets. They highlighted challenges with automation due to complex naming conventions, mixed data sources, and Google Analytics data. They explored potential solutions involving TapClicks API integration and AI-assisted automation to streamline data extraction and reporting.

### Key points

- Data is manually exported platform-by-platform and consolidated weekly into Google Sheets for performance analysis by audience.
- Platforms mentioned include Facebook/Meta, Pinterest, YouTube, TikTok, Reddit, and NextDoor.
- TapClicks contains much of the platform data, but it has struggled with audience naming conventions and formula-based metrics.
- Google Analytics data is integrated manually, adding complexity.
- Past automation attempts through TapClicks struggled because ad naming redundancies created mapping confusion.
- Audience naming conventions are a major obstacle. Campaign details and audience identifiers currently need to be separated manually.
- The team plans to start with a smaller case study before scaling to full data sets.

### Action items from the thread

- Provide API access and permissions for TapClicks.
- Share training documents and instructions detailing the current reporting process.
- Conduct a one-on-one session with Taylor to capture detailed workflow steps.
- Begin automation testing with a simple audience and campaign case before expanding.

### Open questions from the thread

- How should audience naming and sorting issues be resolved so TapClicks/API data maps accurately?
- What is the optimal automated output format to match existing reporting needs?
- How should GA4 data be integrated with ad platform metrics in an automated environment?

## 5. How-to PDF notes: weekly reporting

### Weekly report cadence

Estimated time: 2.5 to 3 hours

Delivery timing: every Tuesday, pulling the previous Monday through Sunday.

Primary working resources:

- `SBA - Weekly Reporting 2024/25`
- `SBA x Sparkloft Social Basecamp – Weekly Reporting Thread`
- platform ad managers

Platforms listed:

- Meta,
- Pinterest,
- YouTube,
- TikTok,
- Reddit,
- NextDoor.

The how-to emphasizes pulling exports from the Ads section of each platform, meaning ad-name-level data is required.

### Weekly export requirements

The raw export needs to match the weekly spreadsheet structure, especially columns D through N.

Each export should be prepared so Excel `Text to Columns` can be used.

For every export, the current manual workflow often adds 2 to 3 columns before the Cost column. These added columns split Ad Group Name data into fields such as:

- Audience,
- Objective,
- and potentially other classification fields depending on the platform/export.

The how-to also notes that unnecessary columns should be removed from raw exports when they are not needed for the weekly report filters.

### Meta weekly notes

The current Meta workflow has already improved somewhat:

- Instead of exporting campaign by campaign, the team can use the reporting tab in Ads Manager.
- There is a report template called `SBA - Weekly Reporting 2025`.
- This template includes needed metrics plus an additional campaign-name column.
- The user sets the correct date range and confirms all ads that ran during the week are visible.
- Then they export Meta as a whole.
- In Excel, they add filters to every column to isolate campaigns and order them.

The how-to says this cleaner Meta export saves about one hour compared with campaign-by-campaign export and manual row cleanup.

Meta rules captured:

- Most Meta ads classify as Facebook unless the ad group name specifically says it is IG-only.
- If the ad name contains `FB+IG`, classify it as Facebook.
- Retainer ads on Meta are Monthly Traffic and Direct Response campaigns.
- Meta Brand Traffic is tricky because pillar names must be removed from the audience field while staying included at the ad-name level if they are not already there.
- FB and IG placements need to be separated when relevant.

### Pinterest weekly notes

The how-to lists Pinterest notes as TBD.

### YouTube weekly notes

YouTube exports a lot of extra data even when custom weekly report columns are selected.

The current manual instruction is to clean the YouTube data as soon as possible, keeping only what is needed.

YouTube also requires calculated values for video completion counts. The export provides percentages, so the workflow adds a column behind each completion-percentage column and calculates:

`Views * Views to %`

This applies to values such as:

- Views to 50%,
- Views to 75%,
- Views to 100%.

Those calculated counts then get added to the weekly report sheet.

### Weekly pivot/insight process

The weekly insights use the `Ad per Audience` tab in `SBA - Weekly Reporting 2024/25`.

The user updates the report dates and verifies that the pivot-table data range includes the most recent raw-data rows.

Pivot filters include:

- Platform,
- Status / Date Range,
- Goal,
- Campaign.

Workflow notes:

- Clear filters first.
- Select the Status / Date Range.
- Then sort/filter according to existing insights by platform, campaign, and goal.

### Weekly insight metrics

The how-to says weekly insights primarily look at cost efficiency by campaign objective.

Metrics:

- Awareness campaigns: CPM.
- Traffic campaigns: CPC.
- Video campaigns: CPM Views to 100%.

For Traffic campaigns:

- JLP reviews cost per conversion separately.
- The team notes cost-per-click outliers.
- The team looks for budget hogs in each ad set.
- Budget hogs are ads/ad sets taking spend away from better-performing options.
- There may be recommendations to move budget hogs or stronger ads into the Engaged Audience ad set.

For Video campaigns:

- CPM Views to 100% is the key metric.
- The team generally wants CPM Views to 100% below $30.
- Longer videos naturally produce more expensive completion metrics.

### Month-overlap weekly rule

If a weekly reporting range overlaps two months, prior-month ads need the previous month appended to the ad name.

Example from the how-to:

If the reporting week is `2/24/25 - 3/2/25`, February ads need `- February` added to the ad name so spend and results do not blend together in the weekly pivot table.

### Weekly troubleshooting notes

- Pivot-table data ranges must match or exceed the number of rows in the raw-data export tab.
- If rows disappear, browser back may restore them, or rows can be dragged back into place in the pivot editor.
- At the last week of the month, the team should look back through weekly report insights and platform data to identify patterns for monthly reports.

## 6. How-to PDF notes: monthly reporting

Estimated time: 6 to 7 hours.

The monthly report lives in TapClicks.

Report name:

- `SBA - Visit Santa Barbara (Monthly) 24/25`

Monthly workflow notes:

1. Edit the cover page to the reporting month and adjust the timeframe to the full month.
2. Skip page 2 insights until all paid data is entered and checked.
3. Update YTD totals on page 3 with a custom date range through the current reporting month.
4. Verify each slide by comparing with in-platform data.
5. Make sure all widget filters are correct.
6. Do not delete inactive-campaign slides. Leave a red note saying `delete after export` so the slide does not have to be recreated later.
7. For the Retainer slide, update ad set filters to the reporting month by typing `*MONTH*` and pressing Enter.
8. Many slides with no data only need the current month applied to widget filters.
9. Once paid data and insights are complete, update the Basecamp thread and check off the related To-Dos.

Organic section:

- The Account team owns the Organic section, including smart connectors on the last page.

Export process:

- Export with correct dates.
- Download.
- Open in Preview.
- Delete placeholder slides.
- Save as `SBA - Visit Santa Barbara MONTH Report 24_25.pdf`.

## 7. How-to PDF notes: quarterly reporting

Estimated time: 13 to 15 hours.

TapClicks report names:

- Q1, Q2, Q3: `SBA - Visit Santa Barbara - Q1, Q2, Q3`
- Q4 / EOY: `SBA - Visit Santa Barbara - Q4 Report`

Fiscal-year scope starts in July:

- Q1: July to September
- Q2: October to December
- Q3: January to March
- Q4: April to June

Quarterly paid-media workflow notes:

1. Cover page automatically adjusts to selected reporting dates.
2. Slide 2 needs filters adjusted to a custom YTD range.
3. Slide 3 uses a smart connector from `SBA FY23/24 Goals Tracker + Organic Summary`.
4. Goals require checking both TapClicks and Meltwater.

TapClicks quarterly goal process:

- Open the SBA TapClicks dashboard.
- Adjust date range to the current YTD.
- Add a campaign filter to the Holistic Overview Summary widget for Brand and Episodic.
- Pull total Impressions, Views to 100%, and Landing Page Views.
- Add those values to the Google Sheet.
- Remove the widget filter after pulling numbers.

Meltwater quarterly process:

- Open the SBA Monitor in Meltwater.
- Adjust date range to YTD.
- Apply Custom Categories > Spam > Spam filter.
- Pull positive sentiment for the YTD goals tracker.
- Adjust the date to the quarter and download the sentiment PNG.
- Pull mentions, AI-powered summaries, relevant travel-industry context, top keywords/entities, keyword sentiment, and sentiment trend graph.
- Pull the same period from the previous year for comparison where needed.

Organic quarterly notes:

- Organic totals are partly manual because there is not currently a smart channel set up that perfectly aligns for SBA.
- The team uses `SBA Quarterly Calculations` to total organic values after the account team loads smart connectors.
- Some metrics are intentionally excluded, such as TikTok organic impressions when unavailable.
- Slide 7 is mostly automated but still needs manual totals, Meta Followers update, and Meta video views.
- Slide 8 is mostly smart connectors, but YouTube Monthly Views and TikTok Video Views need careful checking because they may require subtracting paid video views.

Campaign summaries and performance:

- Starting around slide 16, the team identifies top-performing ads from each campaign and writes campaign/creative insights.
- Useful sources include weekly reporting threads, paid media planning threads, and content recommendation threads.
- The right side of the report contains insights that correlate with campaigns listed at the top of the page.
- The left side has two widgets per campaign.
- Each widget needs filters applied to reflect the ad/results cited in the insights.
- For Meta, the team filters by campaign and date range, then sorts by the relevant metric such as link clicks or CPC.
- Slides 21, 22, and 23 require pulling ads with lowest cost per result by audience.

## 8. Updated automation direction based on Chris's clarification

The earlier brief correctly identified naming/classification as a hard problem, but Chris clarified the main operational pain more sharply:

The primary thing taking time is pulling the information.

The team already has a fairly good workflow for deciphering the data after it has been pulled, including using ChatGPT. So the first build phase should focus less on replacing the entire insight process and more on creating the cleanest, most reliable information-pulling process possible.

### Revised priority order

1. Data access and pulling layer.
2. Export schema normalization.
3. Platform-specific pull templates / API requests.
4. Clean staging outputs that match weekly report needs.
5. Deterministic rules for obvious cleanup.
6. Human/ChatGPT-assisted interpretation layer.
7. Later: full one-swoop automation from pull to insight.

### What the first version should do

The first version should help the team reliably answer:

- Did we pull the right date range?
- Did we pull from the right platform/account/report?
- Did we pull at the Ads level?
- Did we include the required columns?
- Did we avoid unnecessary columns?
- Did we preserve campaign/ad set/ad/ad name fields needed for classification?
- Did we produce a clean export that can feed the current weekly sheet and ChatGPT insight workflow?

### What the first version should not over-focus on

The first version should not over-invest in generating final polished insights before the pull process is solved.

It should not try to replace every pivot table or monthly/quarterly narrative workflow immediately.

It should not rely on AI guessing when deterministic export settings, API fields, or report templates can make the input cleaner from the start.

## 9. Proposed build approach

### Phase 1: Pull-process audit

Document exactly how data is pulled today for each weekly platform:

- Meta,
- Pinterest,
- YouTube,
- TikTok,
- Reddit,
- NextDoor,
- GA4/site data if relevant for weekly reporting.

For each platform, capture:

- where the export is pulled from,
- account/report/template name,
- required date range behavior,
- required level of granularity,
- required columns,
- columns to discard,
- export file format,
- any manual post-export step,
- and common failure cases.

### Phase 2: Pull template / API feasibility

For each source, determine whether the cleanest pull should come from:

- native platform export template,
- saved report view,
- TapClicks API,
- platform API,
- Google Sheet connector,
- or a semi-manual export checklist.

The goal is not full automation at any cost. The goal is the cleanest reliable source pull.

### Phase 3: Staging format

Create a normalized staging format for pulled files.

This should be a clean intermediate table that preserves raw identifiers while adding standardized fields.

Potential field groups:

- source platform,
- account/report source,
- date range,
- campaign name,
- ad set / ad group name,
- ad name,
- raw objective,
- raw audience,
- spend/cost,
- impressions,
- clicks/link clicks,
- views/video metrics,
- completion percentages/counts,
- landing page/site metrics where available.

### Phase 4: Weekly-sheet output

Map the staging table to the existing `SBA - Weekly Reporting 2024/25` structure, especially columns D through N and any raw-data columns required by the pivot tables.

### Phase 5: Insight support

Once data pulls are clean, support the existing ChatGPT-assisted interpretation workflow by generating:

- clean CSVs,
- pivot-ready summaries,
- budget-hog flags,
- outlier flags,
- and a concise prompt packet for weekly insights.

## 10. Recommended immediate ask to Taylor / JLP

For the automation test, can you send over a small pull-process package?

We are trying to solve the information-pulling bottleneck first, then layer the interpretation workflow on top.

For each platform you want included in the first test, can you send:

1. The exact report/export location or saved report/template name.
2. The date range used for one normal weekly pull.
3. The required columns for the export.
4. A raw export file from a clean/simple week.
5. A raw export file from a messy week, especially one with month overlap or repeated ad names.
6. The final cleaned sheet output for those same weeks.
7. Any notes on what you manually delete, split, rename, or calculate after export.
8. Screenshots or recording of the pull/export process if available.
9. TapClicks API access or a walkthrough of which TapClicks report/widgets contain the source data.
10. Any current ChatGPT prompts or examples they use after the data has been pulled.

## 11. Clean working hypothesis

The first useful product is probably not a full AI reporting assistant.

The first useful product is a pull-and-staging assistant:

- it knows exactly what to pull,
- it pulls or guides the pull from the cleanest source,
- it validates that the export has the expected fields/date range/granularity,
- it standardizes the file into a weekly-report-ready format,
- and it hands the team a clean table/prompt packet for their existing analysis workflow.

This gets time savings sooner and lowers risk. Once the pulled data is consistent, then the ChatGPT/AI interpretation layer becomes much easier to automate in one flow.
