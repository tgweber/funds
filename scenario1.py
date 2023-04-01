from funds.report.factory import PDFFundReportFactory

import yaml

with open("data/scenario1.yaml", "r") as f:
    y_funds = yaml.safe_load(f)
funds = []
for y_fund in y_funds:
    funds.append(PDFFundReportFactory.create(y_fund))
