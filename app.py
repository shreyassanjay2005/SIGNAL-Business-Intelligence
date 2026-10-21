
from pathlib import Path
from html import escape
import json

import altair as alt
import joblib
import pandas as pd
import streamlit as st

# -----------------------------------------------------------
# SIGNAL | Business analytics portfolio by Shreyas Sanjay
# -----------------------------------------------------------
BASE = Path(__file__).resolve().parent
DATA = BASE / 'superstore.csv'
MODEL = BASE / 'signal_model.joblib'
VALIDATION = BASE / 'signal_validation.csv'
METRICS = BASE / 'signal_metrics.json'

BLUE = '#6FA8FF'
TEAL = '#4DD2B2'
CORAL = '#F18489'
AMBER = '#F1B967'
VIOLET = '#B6A4FF'
MUTED = '#A3AFBD'
GRID = '#2A3848'
CATEGORY_COLORS = ['#B6A4FF', '#4DD2B2', '#F1B967']

st.set_page_config(
    page_title='SIGNAL | Shreyas Sanjay',
    page_icon='📈',
    layout='wide',
    initial_sidebar_state='expanded'
)

# -----------------------------------------------------------
# WEBSITE DESIGN
# -----------------------------------------------------------

st.markdown("""
<style>
:root {
    --bg: #101722;
    --surface: #182331;
    --border: #304052;
    --text: #EEF2F7;
    --muted: #A3AFBD;
}

.stApp, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--text);
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1370px;
    padding: 2rem 2.4rem 3rem;
}

h1, h2, h3 {
    letter-spacing: -.035em;
}

h1 {
    font-size: 2rem !important;
    font-weight: 710 !important;
}

h2 {
    font-size: 1.35rem !important;
}

h3 {
    font-size: 1.08rem !important;
}

[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

section[data-testid="stSidebar"] {
    background: #151F2D;
    border-right: 1px solid #2E3B4B;
}

section[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 8px;
    margin: 3px 0;
    padding: 9px 10px;
}

section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #26374B;
}

section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #202F40;
}

[data-testid="stMetric"] {
    background: #1B2939;
    border: 1px solid #324355;
    border-radius: 11px;
    padding: 18px 19px;
    min-height: 112px;
}

[data-testid="stMetricLabel"] {
    color: #ACB9C8;
    font-size: .83rem;
}

[data-testid="stMetricValue"] {
    color: #F1F4F8;
    font-size: 1.75rem;
    font-weight: 690;
    letter-spacing: -.04em;
}

[data-testid="stMetricDelta"] {
    font-size: .82rem;
}

[data-testid="stVegaLiteChart"] {
    background: #16212F;
    border: 1px solid #2B3C50;
    border-radius: 11px;
    padding: 10px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #334358;
    border-radius: 9px;
    overflow: hidden;
}

div.stButton button,
div.stDownloadButton button {
    background: #25384E;
    color: #ECF3FA;
    border: 1px solid #405A76;
    border-radius: 8px;
    font-weight: 570;
}

div.stButton button:hover,
div.stDownloadButton button:hover {
    background: #304963;
    border-color: #6FA8FF;
    color: white;
}

div.stButton button[kind="primary"] {
    background: #6FA8FF;
    color: #0A1523;
    border-color: #6FA8FF;
    font-weight: 700;
}

button[role="tab"] {
    color: #AABACA;
    font-weight: 550;
}

button[role="tab"][aria-selected="true"] {
    color: #EDF4FF;
}

hr {
    border-color: #2F4051 !important;
}

.brand-title {
    font-size: 1.6rem;
    font-weight: 800;
    letter-spacing: -.075em;
    color: #F2F6FC;
}

.brand-title span {
    color: #6FA8FF;
}

.brand-sub {
    font-size: .67rem;
    letter-spacing: .13em;
    color: #A8B8C9;
    font-weight: 600;
}

.masthead {
    border-bottom: 1px solid #324356;
    padding: 0 0 20px;
    margin: 0 0 20px;
}

.masthead-top {
    color: #B2C1D1;
    font-size: .71rem;
    font-weight: 650;
    letter-spacing: .12em;
}

.masthead-name {
    font-size: 1.13rem;
    letter-spacing: -.02em;
    color: #E8F0FB;
    margin-top: 6px;
}

.masthead-name strong {
    color: #6FA8FF;
}

.strip {
    display: flex;
    height: 4px;
    width: 190px;
    gap: 5px;
    margin: 14px 0 0;
}

.strip i {
    display: block;
    flex: 1;
    border-radius: 3px;
}

.signal-note {
    background: #1A2B3C;
    border: 1px solid #334B63;
    border-left: 3px solid #6FA8FF;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 12px 0 17px;
    line-height: 1.55;
    font-size: .93rem;
}

.signal-note.warn {
    background: #292737;
    border-left-color: #F1B967;
}

.signal-note.loss {
    background: #2D2530;
    border-left-color: #F18489;
}

.signal-footer {
    margin-top: 32px;
    padding: 22px 0 5px;
    border-top: 1px solid #304154;
    display: flex;
    justify-content: space-between;
    gap: 18px;
    align-items: flex-start;
    flex-wrap: wrap;
}

.footer-name {
    color: #EFF4FC;
    font-weight: 700;
    letter-spacing: -.01em;
}

.footer-caption {
    color: #A3B2C1;
    font-size: .79rem;
    margin-top: 4px;
}

.footer-right {
    color: #9CAFC0;
    font-size: .77rem;
    text-align: right;
}

.footer-dots {
    color: #4DD2B2;
}

@media(max-width:800px) {
    .block-container {
        padding: 1.5rem .85rem 2rem;
    }
    .signal-footer {
        flex-direction: column;
    }
    .footer-right {
        text-align: left;
    }
}
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------

def dollars(value):
    return f'${value:,.0f}'


def note(message, kind='info'):
    cls = {
        'warning': 'warn',
        'loss': 'loss'
    }.get(kind, '')

    st.markdown(
        f'<div class="signal-note {cls}">{escape(message)}</div>',
        unsafe_allow_html=True
    )


def title(name, subtitle):
    st.title(name)
    st.caption(subtitle)
    st.write('')


def show(chart):
    chart = (
        chart.configure_view(stroke=None)
        .configure_axis(
            labelColor=MUTED,
            titleColor=MUTED,
            gridColor=GRID,
            domainColor=GRID,
            tickColor=GRID,
            labelFontSize=11
        )
        .configure_legend(
            labelColor=MUTED,
            titleColor=MUTED
        )
    )
    st.altair_chart(chart, use_container_width=True)


def summary(data):
    rev = float(data.Sales.sum())
    profit = float(data.Profit.sum())

    return (
        rev,
        profit,
        int(data['Order ID'].nunique()),
        100 * profit / rev if rev else 0
    )


def file_version(p):
    return p.stat().st_mtime_ns


@st.cache_data
def load_data(path, version):
    d = pd.read_csv(path)

    required = [
        'Order Date', 'Order ID', 'Region',
        'Segment', 'Category', 'Sub-Category',
        'Sales', 'Profit', 'Discount', 'Quantity'
    ]

    missing = sorted(set(required) - set(d.columns))

    if missing:
        raise ValueError('CSV missing: ' + ', '.join(missing))

    d['Order Date'] = pd.to_datetime(
        d['Order Date'],
        format='%d/%m/%y',
        errors='coerce'
    )

    for c in ['Sales', 'Profit', 'Discount', 'Quantity']:
        d[c] = pd.to_numeric(d[c], errors='coerce')

    return d.dropna(subset=required).copy()


@st.cache_resource
def load_model(path, version):
    return joblib.load(path)


@st.cache_data
def load_predictions(path, version):
    return pd.read_csv(path)


# -----------------------------------------------------------
# EXECUTIVE OVERVIEW
# -----------------------------------------------------------

def overview(data):
    title(
        'Executive Overview',
        'Revenue, profit and the signals worth investigating.'
    )

    rev, profit, orders, margin = summary(data)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric('Total revenue', dollars(rev))
    c2.metric('Net profit', dollars(profit))
    c3.metric('Orders', f'{orders:,}')
    c4.metric('Profit margin', f'{margin:.1f}%')

    st.write('')

    left, right = st.columns([1.6, 1])

    with left:
        st.subheader('Revenue trend')

        monthly = (
            data.assign(
                Month=data['Order Date']
                .dt.to_period('M')
                .dt.to_timestamp()
            )
            .groupby('Month', as_index=False)['Sales']
            .sum()
        )

        ch = (
            alt.Chart(monthly)
            .mark_area(
                line={
                    'color': BLUE,
                    'strokeWidth': 2.5
                },
                color=BLUE,
                opacity=.20
            )
            .encode(
                x=alt.X(
                    'Month:T',
                    axis=alt.Axis(
                        format='%b %Y',
                        tickCount=6
                    ),
                    title=None
                ),
                y=alt.Y('Sales:Q', title='Sales ($)'),
                tooltip=[
                    alt.Tooltip('Month:T', format='%b %Y'),
                    alt.Tooltip('Sales:Q', format='$,.0f')
                ]
            )
            .properties(height=320)
        )

        show(ch)

    with right:
        st.subheader('Category contribution')

        categories = (
            data.groupby('Category', as_index=False)['Profit']
            .sum()
        )

        ch = (
            alt.Chart(categories)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X('Profit:Q', title='Profit ($)'),
                y=alt.Y(
                    'Category:N',
                    sort='-x',
                    title=None
                ),
                color=alt.Color(
                    'Category:N',
                    scale=alt.Scale(
                        domain=[
                            'Technology',
                            'Office Supplies',
                            'Furniture'
                        ],
                        range=CATEGORY_COLORS
                    ),
                    legend=None
                ),
                tooltip=[
                    'Category:N',
                    alt.Tooltip('Profit:Q', format='$,.0f')
                ]
            )
            .properties(height=320)
        )

        show(ch)

    st.divider()
    st.subheader('At a glance')

    gp = data.groupby('Sub-Category')['Profit'].sum()

    if not gp.empty:
        loss_rate = float(
            (data.Profit < 0).mean() * 100
        )

        a, b, c = st.columns(3)

        a.metric('Highest profit group', gp.idxmax())
        b.metric('Lowest profit group', gp.idxmin())
        c.metric('Unprofitable sales lines', f'{loss_rate:.1f}%')

        if gp.min() < 0:
            note(
                f'{gp.idxmin()} has a net loss of '
                f'{dollars(abs(gp.min()))}. '
                'Review discounting and costs before changing pricing.',
                'loss'
            )
        else:
            note(
                'Every product group has positive net profit '
                'in this selection.'
            )

    st.caption(
        'Figures are from the historical fictional Sample '
        'Superstore dataset, not current business activity.'
    )


# -----------------------------------------------------------
# PROFIT DETECTIVE
# -----------------------------------------------------------

def detective(data, region):
    title(
        'Profit Detective',
        'Explore where margins deteriorate, and what might explain it.'
    )

    groups = (
        data.groupby('Sub-Category', as_index=False)['Profit']
        .sum()
    )

    chart = (
        alt.Chart(groups)
        .mark_bar(cornerRadiusEnd=3)
        .encode(
            x=alt.X('Profit:Q', title='Net profit ($)'),
            y=alt.Y(
                'Sub-Category:N',
                sort='-x',
                title=None
            ),
            color=alt.condition(
                'datum.Profit < 0',
                alt.value(CORAL),
                alt.value(TEAL)
            ),
            tooltip=[
                'Sub-Category:N',
                alt.Tooltip('Profit:Q', format='$,.0f')
            ]
        )
        .properties(height=475)
    )

    show(chart)

    losers = groups[groups.Profit < 0]

    if not losers.empty:
        note(
            f'{len(losers)} product groups are net loss-making; '
            f'combined group losses: '
            f'{dollars(abs(losers.Profit.sum()))}.',
            'loss'
        )
    else:
        note('No net loss-making product groups in this region.')

    choices = sorted(
        data['Sub-Category']
        .dropna()
        .unique()
        .tolist()
    )

    if not choices:
        return

    chosen = st.selectbox(
        'Investigate product group',
        choices,
        index=(
            choices.index('Tables')
            if 'Tables' in choices else 0
        )
    )

    detail = data[
        data['Sub-Category'] == chosen
    ].copy()

    net = float(detail.Profit.sum())

    gross_losses = float(
        -detail.Profit.clip(upper=0).sum()
    )

    avg_discount = float(detail.Discount.mean() * 100)
    loss_rate = float((detail.Profit < 0).mean() * 100)

    tab1, tab2, tab3 = st.tabs([
        'Investigation',
        'Recovery scenario',
        'Decision brief'
    ])

    # INVESTIGATION

    with tab1:
        st.write('')

        a, b, c = st.columns(3)

        a.metric('Net profit', dollars(net))
        b.metric('Average discount', f'{avg_discount:.1f}%')
        c.metric('Unprofitable lines', f'{loss_rate:.1f}%')

        st.subheader('Profit by discount level')

        labels = [
            'No discount',
            '1–20%',
            '21–40%',
            'Above 40%'
        ]

        detail['Discount Band'] = pd.cut(
            detail.Discount,
            bins=[-.001, .001, .20, .40, 1],
            labels=labels
        )

        bands = (
            detail.groupby(
                'Discount Band',
                observed=True
            )
            .agg(
                Profit=('Profit', 'sum'),
                Lines=('Profit', 'size')
            )
            .reset_index()
        )

        chart = (
            alt.Chart(bands)
            .mark_bar(cornerRadiusEnd=3)
            .encode(
                x=alt.X(
                    'Discount Band:N',
                    sort=labels,
                    title='Discount range'
                ),
                y=alt.Y(
                    'Profit:Q',
                    title='Net profit ($)'
                ),
                color=alt.condition(
                    'datum.Profit < 0',
                    alt.value(CORAL),
                    alt.value(TEAL)
                ),
                tooltip=[
                    'Discount Band:N',
                    alt.Tooltip('Profit:Q', format='$,.0f'),
                    'Lines:Q'
                ]
            )
            .properties(height=300)
        )

        show(chart)

        if not bands.empty:
            worst = bands.loc[bands.Profit.idxmin()]

            if worst.Profit < 0:
                note(
                    f'For {chosen}, the {worst["Discount Band"]} '
                    f'bracket has net losses of '
                    f'{dollars(abs(worst.Profit))}. '
                    'This is correlation, not causal evidence.',
                    'warning'
                )

    # RECOVERY SCENARIO

    with tab2:
        st.write('')
        st.subheader('Recovery scenario')

        rate = st.slider(
            'Assumed share of loss exposure recovered (%)',
            0, 100, 25, 5
        )

        gain = gross_losses * rate / 100
        revised = net + gain

        a, b, c = st.columns(3)

        a.metric('Historical profit', dollars(net))
        b.metric(
            'Scenario profit',
            dollars(revised),
            delta=dollars(gain)
        )
        c.metric('Gross loss exposure', dollars(gross_losses))

        compare = pd.DataFrame({
            'Case': [
                'Historical',
                'Illustrative recovery'
            ],
            'Profit': [net, revised]
        })

        chart = (
            alt.Chart(compare)
            .mark_bar(
                size=70,
                cornerRadiusEnd=3
            )
            .encode(
                x=alt.X('Case:N', title=None),
                y=alt.Y('Profit:Q', title='Net profit ($)'),
                color=alt.Color(
                    'Case:N',
                    scale=alt.Scale(
                        domain=[
                            'Historical',
                            'Illustrative recovery'
                        ],
                        range=[CORAL, TEAL]
                    ),
                    legend=None
                ),
                tooltip=[
                    'Case:N',
                    alt.Tooltip('Profit:Q', format='$,.0f')
                ]
            )
            .properties(height=275)
        )

        show(chart)

        st.subheader('Opportunity ranking')

        d = data.copy()
        d['Gross Loss'] = -d.Profit.clip(upper=0)

        ranking = (
            d.groupby(
                'Sub-Category',
                as_index=False
            )
            .agg(
                Net_Profit=('Profit', 'sum'),
                Gross_Loss=('Gross Loss', 'sum')
            )
        )

        ranking = ranking[
            ranking.Net_Profit < 0
        ].copy()

        ranking['Hypothetical Recovery'] = (
            ranking.Gross_Loss * rate / 100
        )

        ranking = ranking.sort_values(
            'Hypothetical Recovery',
            ascending=False
        )

        if not ranking.empty:
            st.dataframe(
                ranking.rename(
                    columns={
                        'Sub-Category': 'Product Group',
                        'Net_Profit': 'Net Profit',
                        'Gross_Loss': 'Gross Loss Exposure'
                    }
                ).style.format({
                    'Net Profit': '${:,.0f}',
                    'Gross Loss Exposure': '${:,.0f}',
                    'Hypothetical Recovery': '${:,.0f}'
                }),
                hide_index=True,
                use_container_width=True
            )

            top = ranking.iloc[0]

            note(
                f'{top["Sub-Category"]} has the largest '
                f'illustrative recovery opportunity at '
                f'{dollars(top["Hypothetical Recovery"])}.'
            )

        else:
            note('No net loss-making groups to rank.')

        st.caption(
            'Assumes losses can be reduced without additional costs. '
            'This is not a forecast.'
        )

    # DECISION BRIEF

    with tab3:
        st.write('')
        st.subheader('Decision brief')

        low = detail[detail.Discount <= .20]
        high = detail[detail.Discount > .20]

        lr = (
            (low.Profit < 0).mean() * 100
            if len(low) else None
        )

        hr = (
            (high.Profit < 0).mean() * 100
            if len(high) else None
        )

        def rate_label(value):
            return (
                f'{value:.1f}%'
                if value is not None else 'N/A'
            )

        a, b = st.columns(2)

        a.metric(
            'Loss rate · discount ≤20%',
            rate_label(lr)
        )

        b.metric(
            'Loss rate · discount >20%',
            rate_label(hr)
        )

        st.caption(
            f'Sample sizes: {len(low):,} and '
            f'{len(high):,} sales lines.'
        )

        if (
            len(low) >= 10
            and len(high) >= 10
            and hr > lr + 5
        ):
            finding = (
                'Higher discounts are associated with '
                'a greater loss frequency.'
            )

            action = (
                'Review discount approval limits and test '
                'pricing changes before rollout.'
            )

            note(finding, 'warning')

        elif len(low) >= 10 and len(high) >= 10:
            finding = (
                'The screening rule does not identify '
                'a meaningfully higher loss rate at larger discounts.'
            )

            action = (
                'Investigate costs, product mix and regions '
                'before changing discounts.'
            )

            note(finding)

        else:
            finding = (
                'There are not enough observations '
                'in both discount groups.'
            )

            action = (
                'Collect more observations before '
                'drawing pricing conclusions.'
            )

            note(finding)

        st.markdown('**Recommended next step**')
        st.write(action)

        report = (
            f'SIGNAL / Decision Brief\n'
            f'Prepared by Shreyas Sanjay\n\n'
            f'Dataset: Sample Superstore (fictional)\n'
            f'Region: {region}\n'
            f'Product: {chosen}\n'
            f'Net profit: {dollars(net)}\n'
            f'Average discount: {avg_discount:.1f}%\n'
            f'Loss rate: {loss_rate:.1f}%\n'
            f'Low discount loss rate: {rate_label(lr)}\n'
            f'High discount loss rate: {rate_label(hr)}\n\n'
            f'Finding: {finding}\n'
            f'Next step: {action}\n\n'
            f'Associations are not causation. No guaranteed recovery.'
        )

        st.download_button(
            'Download decision brief',
            data=report,
            file_name='SIGNAL_Decision_Brief.txt',
            mime='text/plain'
        )


# -----------------------------------------------------------
# DECISION SIMULATOR
# -----------------------------------------------------------

def simulator(data):
    title(
        'Decision Simulator',
        'Change the assumptions and compare possible financial outcomes.'
    )

    revenue, profit, _, _ = summary(data)
    costs = revenue - profit

    change = st.slider(
        'Assumed revenue change (%)',
        -20, 30, 0
    )

    saving = st.slider(
        'Assumed cost reduction (%)',
        0, 15, 0
    )

    factor = 1 + change / 100

    new_rev = revenue * factor
    new_cost = costs * factor * (1 - saving / 100)
    new_profit = new_rev - new_cost

    a, b, c = st.columns(3)

    a.metric('Scenario revenue', dollars(new_rev))
    b.metric('Scenario profit', dollars(new_profit))
    c.metric(
        'Change in profit',
        dollars(new_profit - profit),
        delta=dollars(new_profit - profit)
    )

    comparison = pd.DataFrame([
        {
            'Metric': m,
            'Scenario': s,
            'Amount': v
        }
        for m, old, new in [
            ('Revenue', revenue, new_rev),
            ('Costs', costs, new_cost),
            ('Profit', profit, new_profit)
        ]
        for s, v in [
            ('Historical', old),
            ('Simulated', new)
        ]
    ])

    ch = (
        alt.Chart(comparison)
        .mark_bar(cornerRadiusEnd=3)
        .encode(
            x=alt.X(
                'Metric:N',
                sort=['Revenue', 'Costs', 'Profit'],
                title=None
            ),
            xOffset='Scenario:N',
            y=alt.Y(
                'Amount:Q',
                title='Amount ($)'
            ),
            color=alt.Color(
                'Scenario:N',
                scale=alt.Scale(
                    domain=[
                        'Historical',
                        'Simulated'
                    ],
                    range=[VIOLET, TEAL]
                )
            ),
            tooltip=[
                'Metric:N',
                'Scenario:N',
                alt.Tooltip('Amount:Q', format='$,.0f')
            ]
        )
        .properties(height=340)
    )

    show(ch)

    note(
        'Illustrative business scenario: costs are assumed '
        'to scale with sales before savings. '
        'This is not a forecast.'
    )


# -----------------------------------------------------------
# PREDICTION LAB
# -----------------------------------------------------------

def predictor(data, preferred_region):
    title(
        'Prediction Lab',
        'Estimate the risk of a loss-making sales line.'
    )

    if not MODEL.exists():
        note(
            'Model missing. Run python3 model.py in your SIGNAL folder.',
            'warning'
        )
        return

    try:
        model = load_model(
            str(MODEL),
            file_version(MODEL)
        )
    except Exception as exc:
        st.error(f'Could not load model: {exc}')
        return

    left, right = st.columns(2)

    with left:
        sales = st.number_input(
            'Sale value after discount ($)',
            min_value=0.01,
            value=250.0,
            step=25.0
        )

        quantity = st.number_input(
            'Quantity',
            min_value=1,
            max_value=50,
            value=2
        )

        discount = st.slider(
            'Discount (%)',
            0, 80, 25, 5
        )

    with right:
        regions = sorted(data.Region.unique().tolist())

        region = st.selectbox(
            'Region',
            regions,
            index=(
                regions.index(preferred_region)
                if preferred_region in regions else 0
            )
        )

        segment = st.selectbox(
            'Customer segment',
            sorted(data.Segment.unique().tolist())
        )

        category = st.selectbox(
            'Category',
            sorted(data.Category.unique().tolist())
        )

        sc = sorted(
            data.loc[
                data.Category == category,
                'Sub-Category'
            ].unique().tolist()
        )

        subcategory = st.selectbox(
            'Product group',
            sc
        )

    if st.button('Assess transaction', type='primary'):
        row = pd.DataFrame([{
            'Sales': sales,
            'Quantity': quantity,
            'Discount': discount / 100,
            'Region': region,
            'Segment': segment,
            'Category': category,
            'Sub-Category': subcategory
        }])

        score = float(
            model.predict_proba(row)[0, 1]
        )

        st.divider()
        st.subheader('Model assessment')

        a, b = st.columns(2)

        a.metric('Loss-risk score', f'{score:.1%}')

        b.metric(
            'Result',
            (
                'Review recommended'
                if score >= .5
                else 'Lower risk'
            )
        )

        st.progress(
            min(1.0, max(0.0, score))
        )

        note(
            'The model flagged this sale for review.'
            if score >= .5
            else 'The model did not flag this sale at the 50% threshold.',
            'warning' if score >= .5 else 'info'
        )

        st.subheader('Discount sensitivity')

        demo = pd.concat(
            [row] * 9,
            ignore_index=True
        )

        demo['Discount'] = [
            i / 10 for i in range(9)
        ]

        demo['Risk'] = model.predict_proba(demo)[:, 1]
        demo['Discount (%)'] = demo.Discount * 100

        ch = (
            alt.Chart(demo)
            .mark_line(
                color=AMBER,
                point=True,
                strokeWidth=2.6
            )
            .encode(
                x=alt.X(
                    'Discount (%):Q',
                    scale=alt.Scale(domain=[0, 80])
                ),
                y=alt.Y(
                    'Risk:Q',
                    axis=alt.Axis(format='.0%'),
                    scale=alt.Scale(domain=[0, 1]),
                    title='Model loss score'
                ),
                tooltip=[
                    alt.Tooltip(
                        'Discount (%):Q',
                        format='.0f'
                    ),
                    alt.Tooltip(
                        'Risk:Q',
                        format='.1%'
                    )
                ]
            )
            .properties(height=300)
        )

        show(ch)

        st.caption(
            'The score is a model estimate, not a guaranteed probability. '
            'Holding sale value constant while varying discounts is a '
            'sensitivity exercise, not causal analysis.'
        )


# -----------------------------------------------------------
# MODEL PERFORMANCE
# -----------------------------------------------------------

def evaluation():
    title(
        'Model Performance',
        'Understand how the classifier performs and where it makes mistakes.'
    )

    if not VALIDATION.exists():
        note(
            'Validation file missing. Run python3 model.py first.',
            'warning'
        )
        return

    val = load_predictions(
        str(VALIDATION),
        file_version(VALIDATION)
    )

    actual = val['Actual Loss'].astype(int)
    probs = val['Loss Probability'].astype(float)

    threshold = st.slider(
        'Classification threshold',
        .10, .90, .50, .05
    )

    pred = (probs >= threshold).astype(int)

    tp = int(
        ((actual == 1) & (pred == 1)).sum()
    )

    tn = int(
        ((actual == 0) & (pred == 0)).sum()
    )

    fp = int(
        ((actual == 0) & (pred == 1)).sum()
    )

    fn = int(
        ((actual == 1) & (pred == 0)).sum()
    )

    acc = (tp + tn) / len(val)

    precision = (
        tp / (tp + fp)
        if tp + fp else 0
    )

    recall = (
        tp / (tp + fn)
        if tp + fn else 0
    )

    brier = float(
        ((probs - actual) ** 2).mean()
    )

    a, b, c, d = st.columns(4)

    a.metric('Accuracy', f'{acc:.2%}')
    b.metric('Precision', f'{precision:.2%}')
    c.metric('Recall', f'{recall:.2%}')
    d.metric('Brier score', f'{brier:.4f}')

    baseline = max(
        float(actual.mean()),
        float(1 - actual.mean())
    )

    st.caption(
        f'{len(val):,} held-out historical records '
        f'• baseline accuracy {baseline:.2%}'
    )

    if METRICS.exists():
        with open(METRICS) as f:
            m = json.load(f)

        if 'roc_auc' in m:
            st.caption(
                f'ROC-AUC: {m["roc_auc"]:.3f} '
                '• not affected by the classification threshold'
            )

    st.divider()
    st.subheader('Confusion matrix')

    matrix = pd.DataFrame([
        {
            'Actual': 'No loss',
            'Predicted': 'No loss',
            'Count': tn,
            'Status': 'Correct'
        },
        {
            'Actual': 'No loss',
            'Predicted': 'Loss',
            'Count': fp,
            'Status': 'Error'
        },
        {
            'Actual': 'Loss',
            'Predicted': 'No loss',
            'Count': fn,
            'Status': 'Error'
        },
        {
            'Actual': 'Loss',
            'Predicted': 'Loss',
            'Count': tp,
            'Status': 'Correct'
        }
    ])

    base = alt.Chart(matrix).encode(
        x=alt.X(
            'Predicted:N',
            sort=['No loss', 'Loss']
        ),
        y=alt.Y(
            'Actual:N',
            sort=['Loss', 'No loss']
        )
    )

    rect = (
        base.mark_rect(cornerRadius=5)
        .encode(
            color=alt.Color(
                'Status:N',
                scale=alt.Scale(
                    domain=['Correct', 'Error'],
                    range=['#276D67', '#8E4855']
                ),
                legend=None
            ),
            tooltip=[
                'Actual:N',
                'Predicted:N',
                'Count:Q'
            ]
        )
    )

    text = (
        base.mark_text(
            fontSize=26,
            fontWeight='bold',
            color='white'
        )
        .encode(text='Count:Q')
    )

    show(
        (rect + text).properties(height=280)
    )

    note(
        f'At a {threshold:.0%} threshold: '
        f'{fn:,} missed losses and '
        f'{fp:,} false alerts.',
        'warning'
    )

    st.subheader('Score distribution')

    distribution = val.copy()

    distribution['Outcome'] = (
        distribution['Actual Loss'].map({
            0: 'No loss',
            1: 'Loss'
        })
    )

    ch = (
        alt.Chart(distribution)
        .mark_bar(opacity=.85)
        .encode(
            x=alt.X(
                'Loss Probability:Q',
                bin=alt.Bin(maxbins=24),
                title='Predicted loss score'
            ),
            y=alt.Y(
                'count()',
                title='Transactions'
            ),
            color=alt.Color(
                'Outcome:N',
                scale=alt.Scale(
                    domain=['No loss', 'Loss'],
                    range=[BLUE, CORAL]
                )
            ),
            tooltip=[
                'Outcome:N',
                alt.Tooltip(
                    'count()',
                    title='Transactions'
                )
            ]
        )
        .properties(height=285)
    )

    show(ch)

    st.subheader('Probability calibration')

    bands = val.copy()

    bands['band'] = pd.cut(
        bands['Loss Probability'],
        bins=[i / 10 for i in range(11)],
        include_lowest=True
    )

    cal = (
        bands.groupby(
            'band',
            observed=True
        )
        .agg(
            Predicted=('Loss Probability', 'mean'),
            Observed=('Actual Loss', 'mean'),
            Count=('Actual Loss', 'size')
        )
        .reset_index(drop=True)
    )

    perfect = pd.DataFrame({
        'Predicted': [0, 1],
        'Observed': [0, 1]
    })

    ref = (
        alt.Chart(perfect)
        .mark_line(
            color=MUTED,
            strokeDash=[5, 5]
        )
        .encode(
            x=alt.X(
                'Predicted:Q',
                scale=alt.Scale(domain=[0, 1])
            ),
            y=alt.Y(
                'Observed:Q',
                scale=alt.Scale(domain=[0, 1])
            )
        )
    )

    pts = (
        alt.Chart(cal)
        .mark_circle(
            color=TEAL,
            size=95
        )
        .encode(
            x=alt.X(
                'Predicted:Q',
                axis=alt.Axis(format='.0%'),
                title='Predicted loss score'
            ),
            y=alt.Y(
                'Observed:Q',
                axis=alt.Axis(format='.0%'),
                title='Observed loss rate'
            ),
            tooltip=[
                alt.Tooltip(
                    'Predicted:Q',
                    format='.1%'
                ),
                alt.Tooltip(
                    'Observed:Q',
                    format='.1%'
                ),
                'Count:Q'
            ]
        )
    )

    show(
        (ref + pts).properties(height=285)
    )

    st.caption(
        'Performance was evaluated on held-out historical data only, '
        'not on a new business or future sales.'
    )


# -----------------------------------------------------------
# APPLICATION SHELL
# -----------------------------------------------------------

if not DATA.exists():
    st.error(
        'Missing superstore.csv. Put it beside app.py.'
    )
    st.stop()

try:
    df = load_data(
        str(DATA),
        file_version(DATA)
    )
except Exception as exc:
    st.error(f'Could not load sales data: {exc}')
    st.stop()

if df.empty:
    st.error('No usable sales records found.')
    st.stop()


# SIDEBAR

st.sidebar.markdown(
    '<div class="brand-title">'
    'SIGNAL<span>.</span></div>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<div class="brand-sub">'
    'RETAIL DECISION INTELLIGENCE</div>',
    unsafe_allow_html=True
)

st.sidebar.divider()

pages = [
    'Executive Overview',
    'Profit Detective',
    'Decision Simulator',
    'Prediction Lab',
    'Model Performance'
]

page = st.sidebar.radio(
    'Sections',
    pages,
    label_visibility='collapsed'
)

st.sidebar.divider()

regions = (
    ['All regions']
    + sorted(df.Region.unique().tolist())
)

region = st.sidebar.selectbox(
    'Business region',
    regions
)

filtered = (
    df
    if region == 'All regions'
    else df[df.Region == region].copy()
)

st.sidebar.caption(
    'Sample Superstore | 2014–2017'
)

st.sidebar.caption(
    'Historical fictional retail case study'
)

st.sidebar.markdown('---')

st.sidebar.markdown(
    '<div style="font-size:.78rem;color:#A3B7CC">'
    'PROJECT BY</div>'
    '<div style="font-weight:650;color:#EDF4FA">'
    'Shreyas Sanjay</div>',
    unsafe_allow_html=True
)


# TOP BRANDING

st.markdown("""
<div class="masthead">
    <div class="masthead-top">
        SIGNAL / CASE STUDY 01
    </div>
    <div class="masthead-name">
        Business analytics,
        <strong>made actionable.</strong>
    </div>
    <div class="strip">
        <i style="background:#6FA8FF"></i>
        <i style="background:#4DD2B2"></i>
        <i style="background:#F1B967"></i>
        <i style="background:#F18489"></i>
    </div>
</div>
""", unsafe_allow_html=True)


# PAGE ROUTING

if page == 'Executive Overview':
    overview(filtered)

elif page == 'Profit Detective':
    detective(filtered, region)

elif page == 'Decision Simulator':
    simulator(filtered)

elif page == 'Prediction Lab':
    predictor(df, region)

elif page == 'Model Performance':
    evaluation()

# -----------------------------------------------------------
# PERSONAL FOOTER
# -----------------------------------------------------------

st.html("""
<div class="signal-footer">
    <div>
        <div class="footer-name">
            Shreyas Sanjay
            <span class="footer-dots">/</span>
            SIGNAL
        </div>
        <div class="footer-caption">
            Designed &amp; developed by Shreyas Sanjay
            · Business Analytics &amp; AI for Business
        </div>
    </div>
    <div class="footer-right">
        © 2026 Shreyas Sanjay
        <div>
            Sample Superstore · Fictional data
            · Portfolio demonstration
        </div>
    </div>
</div>
""")


# -----------------------------------------
# SIGNAL - CLEAN LIGHT THEME
# -----------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #FFFFFF !important;
    color: #1B2635 !important;
}

/* Typography */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] p,
[data-testid="stMain"] label {
    color: #1B2635 !important;
}

[data-testid="stCaptionContainer"] p {
    color: #7A8796 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #F7F9FC !important;
    border-right: 1px solid #E4EAF1 !important;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #293548 !important;
}

section[data-testid="stSidebar"]
[role="radiogroup"] label:has(input:checked) {
    background: #E6EEFF !important;
}

section[data-testid="stSidebar"]
[role="radiogroup"] label:hover {
    background: #EDF2F8 !important;
}

/* Brand */
.brand-title {
    color: #18212D !important;
}

.brand-title span {
    color: #3267D6 !important;
}

.brand-sub {
    color: #7B8798 !important;
}

/* KPI cards */
div[data-testid="stMetric"] {
    background: #F7F9FC !important;
    border: 1px solid #E5EAF0 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

div[data-testid="stMetricLabel"] p {
    color: #718096 !important;
}

div[data-testid="stMetricValue"] {
    color: #1C2B40 !important;
}

/* Charts */
div[data-testid="stVegaLiteChart"] {
    background: #FFFFFF !important;
    border: 1px solid #E5EAF0 !important;
    border-radius: 10px !important;
    box-shadow: none !important;
}

/* Input controls */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #FFFFFF !important;
    color: #243247 !important;
    border-color: #DCE3EC !important;
}

input {
    color: #243247 !important;
}

/* Tabs */
button[role="tab"] {
    color: #718096 !important;
}

button[role="tab"][aria-selected="true"] {
    color: #3267D6 !important;
}

/* Buttons */
div.stButton button,
div.stDownloadButton button {
    background: #FFFFFF !important;
    color: #3267D6 !important;
    border: 1px solid #C9D5E8 !important;
    border-radius: 8px !important;
    box-shadow: none !important;
}

div.stButton button[kind="primary"] {
    background: #3267D6 !important;
    color: #FFFFFF !important;
    border-color: #3267D6 !important;
}

/* Insight cards */
.signal-note {
    background: #F0F6FF !important;
    color: #263A55 !important;
    border: 1px solid #DDE8FA !important;
    border-left: 3px solid #3267D6 !important;
}

.signal-note.warn {
    background: #FFFAED !important;
    color: #6D532B !important;
    border-left-color: #E4A540 !important;
}

.signal-note.loss {
    background: #FFF4F3 !important;
    color: #813C40 !important;
    border-left-color: #DE7279 !important;
}

/* Masthead */
.masthead {
    border-bottom: 1px solid #E6EAF0 !important;
}

.masthead-top {
    color: #7B8798 !important;
}

.masthead-name {
    color: #243247 !important;
}

.masthead-name strong {
    color: #3267D6 !important;
}

/* Footer */
.signal-footer {
    border-top: 1px solid #E6EAF0 !important;
}

.footer-name {
    color: #18212D !important;
}

.footer-caption,
.footer-right {
    color: #738195 !important;
}

.footer-dots {
    color: #3267D6 !important;
}

/* Dividers */
hr {
    border-color: #E8EDF3 !important;
}

/* Clean minimalist spacing */
.block-container {
    max-width: 1380px !important;
    padding-top: 2.4rem !important;
}

</style>
""", unsafe_allow_html=True)
