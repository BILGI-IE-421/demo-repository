"""Produce every figure used on the site from data/taxis_clean.csv.

Run from the repository root after preprocess.py:
    python scripts/figures.py

Static figures go to visuals/*.png, the interactive figure to visuals/*.html.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "taxis_clean.csv"
VISUALS = ROOT / "visuals"
SOURCE = "Source: NYC Taxi & Limousine Commission via seaborn-data, March 2019 sample"

sns.set_theme(style="whitegrid", palette="colorblind", font_scale=1.0)
PALETTE = sns.color_palette("colorblind")


def save(fig: plt.Figure, name: str) -> None:
    fig.text(0.0, -0.03, SOURCE, fontsize=8, color="#555555", ha="left", va="top")
    fig.savefig(VISUALS / name, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", VISUALS / name)


def fig1_fare_distribution(df: pd.DataFrame) -> None:
    """Distribution: a heavy-tailed variable on a log axis."""
    fig, ax = plt.subplots(figsize=(8, 5))
    bins = [2, 3, 4, 5, 7, 10, 15, 20, 30, 50, 75, 100, 150]
    ax.hist(df["fare"], bins=bins, color=PALETTE[0], edgecolor="white")
    ax.set_xscale("log")
    ax.set_xticks([2, 5, 10, 20, 50, 100])
    ax.set_xticklabels(["$2", "$5", "$10", "$20", "$50", "$100"])
    median = df["fare"].median()
    ax.axvline(median, color=PALETTE[3], linestyle="--")
    ax.annotate(f"median \\${median:.0f}", xy=(median, ax.get_ylim()[1] * 0.9),
                xytext=(median * 1.3, ax.get_ylim()[1] * 0.9), color=PALETTE[3])
    ax.set_title(r"Most fares are under \$15, but a long tail runs past \$100", loc="left", fontweight="bold")
    ax.set_xlabel("Fare (US dollars, log scale)")
    ax.set_ylabel("Number of trips")
    save(fig, "fig1_fare_distribution.png")


def fig2_distance_vs_fare(df: pd.DataFrame) -> None:
    """Relationship: two continuous variables, one categorical colour."""
    fig, ax = plt.subplots(figsize=(8, 5))
    sub = df[df["distance"] < 25]
    for i, (payment, grp) in enumerate(sub.groupby("payment")):
        ax.scatter(grp["distance"], grp["fare"], s=10, alpha=0.4, color=PALETTE[i], label=payment)
    flat = sub[sub["fare"] == 52]
    ax.annotate(f"JFK flat fare, \\$52 ({len(flat)} trips)", xy=(flat["distance"].median(), 52),
                xytext=(12, 70), arrowprops={"arrowstyle": "->", "color": "#444444"}, color="#444444")
    ax.set_title("Fare rises almost linearly with distance; cash trips stay short", loc="left", fontweight="bold")
    ax.set_xlabel("Trip distance (miles)")
    ax.set_ylabel("Fare (US dollars)")
    ax.legend(title="Payment", markerscale=2, frameon=False)
    save(fig, "fig2_distance_vs_fare.png")


def fig3_trips_by_day(df: pd.DataFrame) -> None:
    """Trend over time: daily counts, weekends shaded, 7-day rolling mean."""
    march = df[(df["pickup"] >= "2019-03-01") & (df["pickup"] < "2019-04-01")]
    daily = march.groupby(march["pickup"].dt.normalize()).size()
    daily = daily.reindex(pd.date_range("2019-03-01", "2019-03-31"), fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for day in daily.index:
        if day.dayofweek >= 5:
            ax.axvspan(day - pd.Timedelta(hours=12), day + pd.Timedelta(hours=12), color="#dddddd", alpha=0.5, lw=0)
    ax.plot(daily.index, daily.values, color=PALETTE[0], linewidth=1.2, alpha=0.8, label="trips per day")
    ax.plot(daily.index, daily.rolling(7, center=True).mean(), color=PALETTE[3], linewidth=2.5, label="7-day mean")
    ax.set_ylim(0, None)
    ax.set_xlim(daily.index.min() - pd.Timedelta(hours=12), daily.index.max() + pd.Timedelta(hours=12))
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1, 8, 15, 22, 29]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%-d %b"))
    ax.set_title("Trips dip every weekend (shaded); otherwise the sample is flat across March 2019", loc="left", fontweight="bold")
    ax.set_xlabel("Pickup date, 2019")
    ax.set_ylabel("Trips in sample")
    ax.legend(frameon=False, loc="lower left")
    save(fig, "fig3_trips_by_day.png")


def fig4_tip_by_borough(df: pd.DataFrame) -> None:
    """Comparison across categories: zero-based, sorted horizontal bars with sample sizes."""
    card = df[df["payment"] == "credit card"]
    grp = card.groupby("pickup_borough")["tip"]
    no_tip = (grp.apply(lambda s: 100 * (s == 0).mean())).sort_values()
    n = grp.size().reindex(no_tip.index)
    tipped_median = card[card["tip"] > 0].groupby("pickup_borough")["tip_pct"].median().reindex(no_tip.index)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.barh(no_tip.index, no_tip.values, color=PALETTE[2])
    for y, (v, cnt, med) in enumerate(zip(no_tip.values, n.values, tipped_median.values)):
        label = f"{v:.0f}% no tip  (n={cnt}; tippers give {med:.0f}%)"
        if v > 60:  # long bar: label inside, in white
            ax.text(v - 1.5, y, label, va="center", ha="right", fontsize=9, color="white")
        else:
            ax.text(v + 1.5, y, label, va="center", ha="left", fontsize=9)
    ax.set_xlim(0, 100)
    ax.set_title("Outside Manhattan, most card trips record no tip at all", loc="left", fontweight="bold")
    ax.set_xlabel("Share of credit-card trips with a zero tip (%); cash tips are never recorded")
    ax.set_ylabel("")
    save(fig, "fig4_tip_by_borough.png")


def fig5_borough_flows(df: pd.DataFrame) -> None:
    """Annotated heatmap: pickup borough x dropoff borough."""
    flows = pd.crosstab(df["pickup_borough"], df["dropoff_borough"])
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sns.heatmap(flows, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax, linewidths=0.5)
    ax.set_title("Nine in ten trips start and end in Manhattan", loc="left", fontweight="bold")
    ax.set_xlabel("Drop-off borough")
    ax.set_ylabel("Pickup borough")
    save(fig, "fig5_borough_flows.png")


def interactive_hourly(df: pd.DataFrame) -> None:
    """Interactive figure: hover shows exact values; nothing else to click."""
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    hourly = df.groupby(["weekday", "hour"]).size().reset_index(name="trips")
    hourly["weekday"] = pd.Categorical(hourly["weekday"], categories=order, ordered=True)
    hourly = hourly.sort_values(["weekday", "hour"])
    fig = px.line(hourly, x="hour", y="trips", color="weekday",
                  category_orders={"weekday": order},
                  color_discrete_sequence=px.colors.qualitative.Safe,
                  labels={"hour": "Pickup hour", "trips": "Trips in sample", "weekday": "Day"},
                  title="Weekday evenings are the busiest hours; weekends start late")
    fig.update_layout(template="plotly_white", hovermode="x unified", legend_title_text="")
    fig.update_xaxes(dtick=2)
    out = VISUALS / "interactive_hourly.html"
    fig.write_html(out, include_plotlyjs="cdn", full_html=True)
    print("wrote", out)


def main() -> None:
    VISUALS.mkdir(exist_ok=True)
    df = pd.read_csv(DATA, parse_dates=["pickup", "dropoff"])
    fig1_fare_distribution(df)
    fig2_distance_vs_fare(df)
    fig3_trips_by_day(df)
    fig4_tip_by_borough(df)
    fig5_borough_flows(df)
    interactive_hourly(df)


if __name__ == "__main__":
    main()
