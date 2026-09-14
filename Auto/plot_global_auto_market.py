"""根据 Auto/global-auto-market.md 的数据生成图表，输出到 Auto/figures/。"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
OUT = BASE / "figures"
OUT.mkdir(exist_ok=True)

plt.rcParams["font.family"] = "Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 160

YEARS = [2021, 2022, 2023, 2024, 2025]
SALES = {
    "中国": [20.2, 20.55, 21.71, 22.89, 23.74],
    "美国": [14.9, 13.8, 15.46, 15.85, 16.2],
    "欧盟": [9.70, 9.26, 10.55, 10.63, 10.82],
    "印度": [3.07, 3.89, 4.22, 4.30, 4.64],
    "日本": [4.45, 4.20, 4.78, 4.42, 4.57],
}
PARC = {
    "中国": (371.0, "2026H1 汽车"),
    "美国": (298.0, "2024 机动车"),
    "欧盟": (256.0, "2024 乘用车"),
    "日本": (83.09, "2026H1 汽车"),
    "印度": (49.05, "2022 Car/Jeep/Taxi"),
    "巴西": (39.5, "2025 乘用车"),
    "澳大利亚": (22.3, "2025 机动车"),
    "泰国": (12.44, "2025 ≤7座乘用车"),
}

COLORS = {
    "中国": "#d62728",
    "美国": "#1f77b4",
    "欧盟": "#2ca02c",
    "印度": "#ff7f0e",
    "日本": "#9467bd",
    "巴西": "#8c564b",
    "澳大利亚": "#e377c2",
    "泰国": "#7f7f7f",
}
NOTE = "数据：Auto/global-auto-market.md；口径不一，仅比趋势"
END_OFFSETS = {"印度": (7, 7), "日本": (7, -7)}


def finish(ax, title, note=NOTE):
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.figure.text(0.01, 0.01, note, fontsize=8, color="#666666")


def fig_sales_trend():
    fig, ax = plt.subplots(figsize=(9, 5))
    for name, values in SALES.items():
        ax.plot(
            YEARS,
            values,
            marker="o",
            linewidth=2,
            color=COLORS[name],
            label=name,
        )
        ax.annotate(
            f"{values[-1]:.2f}",
            (YEARS[-1], values[-1]),
            xytext=END_OFFSETS.get(name, (6, 0)),
            textcoords="offset points",
            fontsize=9,
            color=COLORS[name],
            va="center",
        )
    ax.set_xticks(YEARS)
    ax.set_ylabel("销量（百万辆）")
    ax.set_xlim(2020.8, 2025.6)
    ax.legend(frameon=False, ncol=5, loc="upper left")
    finish(ax, "主要汽车市场年销量 2021–2025")
    fig.savefig(OUT / "sales_trend.png", bbox_inches="tight")
    plt.close(fig)


def fig_sales_2025():
    items = sorted(((n, v[-1]) for n, v in SALES.items()), key=lambda x: x[1])
    names = [i[0] for i in items]
    values = [i[1] for i in items]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.barh(names, values, color=[COLORS[n] for n in names], alpha=0.85)
    for bar, v in zip(bars, values):
        ax.annotate(
            f"{v:.2f}",
            (v, bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            fontsize=9,
            va="center",
        )
    ax.set_xlabel("销量（百万辆）")
    ax.set_xlim(0, max(values) * 1.15)
    finish(ax, "2025 年销量规模对比")
    fig.savefig(OUT / "sales_2025.png", bbox_inches="tight")
    plt.close(fig)


def fig_parc():
    items = sorted(PARC.items(), key=lambda x: x[1][0])
    names = [i[0] for i in items]
    values = [i[1][0] for i in items]
    fig, ax = plt.subplots(figsize=(8.5, 5))
    bars = ax.barh(names, values, color=[COLORS[n] for n in names], alpha=0.85)
    for bar, (name, (v, label)) in zip(bars, items):
        ax.annotate(
            f"{v:.2f}（{label}）",
            (v, bar.get_y() + bar.get_height() / 2),
            xytext=(4, 0),
            textcoords="offset points",
            fontsize=8.5,
            va="center",
        )
    ax.set_xlabel("保有量（百万辆）")
    ax.set_xlim(0, max(values) * 1.45)
    finish(ax, "各市场汽车保有量（口径与年份不同）")
    fig.savefig(OUT / "parc.png", bbox_inches="tight")
    plt.close(fig)


def fig_replacement_cycle():
    markets = ["中国", "美国", "欧盟", "日本", "印度"]
    cycles = [PARC[m][0] / SALES[m][-1] for m in markets]
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bars = ax.bar(markets, cycles, color=[COLORS[m] for m in markets], alpha=0.85)
    for bar, v in zip(bars, cycles):
        ax.annotate(
            f"{v:.1f} 年",
            (bar.get_x() + bar.get_width() / 2, v),
            xytext=(0, 4),
            textcoords="offset points",
            fontsize=9,
            ha="center",
        )
    ax.set_ylabel("保有量 ÷ 2025 年销量（年）")
    ax.set_ylim(0, max(cycles) * 1.2)
    finish(ax, "整车替换周期概算（存量 ÷ 年销量）", NOTE + "；存量与销量口径不完全对齐")
    fig.savefig(OUT / "replacement_cycle.png", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    fig_sales_trend()
    fig_sales_2025()
    fig_parc()
    fig_replacement_cycle()
    print("saved:", *(p.name for p in sorted(OUT.glob("*.png"))))
