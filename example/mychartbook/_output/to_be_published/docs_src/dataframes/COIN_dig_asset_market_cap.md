# `{{pipeline_id}}_{{dataframe_id}}` - {{dataframe_name}}

## Description

Total market capitalization by digital asset category.
Data is from Global Live Cryptocurrency Charts & Market Data: Market Cap Breakdown. https://coinmarketcap.com/charts/

## Data Dictionary

Details on the data fields are below:

- **date**: Day of the week data are reported. 
- **bitcoin**: Reports the market cap of Bitcoin, the largest digital asset in terms of market cap.
- **ethereum**: Reports the market cap of Ethereum, the second largest digital asset in terms of market cap.
- **Stablecoins**: Reports stablecoin market cap which includes the largest stablecoins, Tether and USDC. 
- **Other**: Combined market cap of all other assets that do not fall into the other categories.

## Dataframe Specs

{% include "_docs_src/_templates/dataframe_specs.md" %}

## Pipeline Specs

{% include "_docs_src/_templates/pipeline_specs.md" %}
