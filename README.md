# Long-Term Fund / ETF Analysis Framework

## 概要

このプロジェクトは、CSV や Yahoo Finance、MSCI 形式の価格データを読み込み、対数線形回帰に基づいた長期トレンド分析を実行する Python フレームワークです。

主な機能:
- `Date`, `Price` 形式の CSV 読み込み
- Yahoo Finance からのティッカー価格取得
- MSCI 形式の CSV 読み込み
- 対数価格を用いた線形回帰
- 95% 経験区間の算出
- 複数銘柄の同時比較表示
- 移動平均、ボリンジャーバンド、ドローダウン分析
- PNG 画像および HTML レポート出力

このフレームワークを使えば、オルカン（eMAXIS Slim 全世界株式）だけでなく、2559、ACWI、S&P500、NASDAQ100、個別株なども同じ構成で分析できます。

## ファイル構成

```
analysis/
 ├── main.py
 ├── loader.py
 ├── regression.py
 ├── statistics.py
 ├── plot.py
 ├── indicators.py
 ├── report.py
 ├── data_source.py
 ├── config.py
 ├── requirements.txt
 └── data/
      sample.csv
README.md
```

## 必要環境

- Python 3.10 以上
- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `yfinance`

## セットアップ

```powershell
cd .\analysis
python -m pip install -r requirements.txt
```

## 実行方法

### CSV データを使う場合

```powershell
cd .\analysis
python main.py --source csv --asset data/sample.csv --save-png --save-html
```

### Yahoo Finance データを使う場合

```powershell
python main.py --source yahoo --asset 2559.T --asset ACWI --save-png --save-html
```

### 期間指定を使う例

```powershell
python main.py --source yahoo --asset 2559.T --asset ACWI --start-date 2022-01-01 --end-date 2024-06-30 --save-png --save-html
```

### `period` 指定の例

```powershell
python main.py --source yahoo --asset 2559.T --period 5y --save-png --save-html
```

### S&P500 の例

```powershell
python main.py --source yahoo --asset ^GSPC --start-date 2022-01-01 --save-png --save-html
```

> `2559.T` は日本のオールカントリー型ETFのティッカー例です。
> `^GSPC` は Yahoo Finance での S&P500 のインデックス記号です。

### MSCI 形式 CSV を使う場合

```powershell
python main.py --source msci --asset data/msci_sample.csv --save-png --save-html
```

## 出力ファイル

`analysis/outputs/` に次のファイルが作成されます。

- `analysis_chart.png`
- `analysis_report.html`

## CSV 形式

読み込み対象 CSV は以下の列を含む必要があります。

- `Date`（日付）
- `Price`（基準価額または終値）

## 追加の拡張ポイント

- `analysis/indicators.py` で移動平均、ボリンジャーバンド、ドローダウンを計算
- `analysis/report.py` で HTML レポートを生成
- `analysis/data_source.py` で複数のデータソースに対応

## 注意点

- `python main.py` を実行する場合、`analysis` フォルダ内に移動してから実行してください。
- `--asset` は複数指定できます。
