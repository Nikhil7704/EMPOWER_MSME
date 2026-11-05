from typing import Dict, Any

WEIGHTS = {
    "annualRevenue": 0.20,
    "netProfitMargin": 0.15,
    "cashFlowStability": 0.15,
    "debtToIncome": 0.15,
    "repaymentHistory": 0.20,
    "businessAge": 0.10,
    "gstFilingConsistency": 0.05,
}

LABELS = {
    "annualRevenue": "Annual Revenue",
    "netProfitMargin": "Net Profit Margin",
    "cashFlowStability": "Cash Flow Stability",
    "debtToIncome": "Debt-to-Income Ratio",
    "repaymentHistory": "Repayment History",
    "businessAge": "Business Age",
    "gstFilingConsistency": "GST Filing Consistency",
}

def clamp(val: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    return max(min_val, min(val, max_val))

def normalize(val: float, min_val: float, max_val: float) -> float:
    if max_val == min_val:
        return 0.0
    return clamp((val - min_val) / (max_val - min_val))

def evaluate_credit(data: Dict[str, Any]) -> Dict[str, Any]:
    annual_revenue = float(data.get("annualRevenue", 0.0))
    net_profit_margin = float(data.get("netProfitMargin", 0.0))
    cash_flow_variance = float(data.get("cashFlowVariance", 50.0))
    existing_debt = float(data.get("existingDebt", 0.0))
    repayment_history = float(data.get("repaymentHistory", 50.0))
    business_age = float(data.get("businessAge", 0.0))
    gst_filing_score = float(data.get("gstFilingScore", 50.0))
    industry_risk = str(data.get("industryRiskLevel", "medium")).lower()

    # Factor scores (0.0 to 1.0)
    rev_score = normalize(annual_revenue, 0, 10_000_000)
    profit_score = normalize(net_profit_margin, -20, 40)
    cf_score = 1.0 - normalize(cash_flow_variance, 0, 60)
    debt_ratio = (existing_debt / annual_revenue) if annual_revenue > 0 else 1.0
    debt_score = 1.0 - normalize(debt_ratio, 0, 2.5)
    repay_score = normalize(repayment_history, 0, 100)
    age_score = normalize(business_age, 0, 10)
    gst_score = normalize(gst_filing_score, 0, 100)

    factor_scores = {
        "annualRevenue": rev_score,
        "netProfitMargin": profit_score,
        "cashFlowStability": cf_score,
        "debtToIncome": debt_score,
        "repaymentHistory": repay_score,
        "businessAge": age_score,
        "gstFilingConsistency": gst_score,
    }

    weighted_sum = sum(score * WEIGHTS[k] for k, score in factor_scores.items())

    industry_penalties = {"low": 0.0, "medium": 0.04, "high": 0.12}
    penalty = industry_penalties.get(industry_risk, 0.04)
    weighted_sum = clamp(weighted_sum - penalty)

    credit_score = int(round(300 + weighted_sum * 600))
    risk_ratio = 1.0 - weighted_sum
    risk_category = "Low" if risk_ratio < 0.35 else ("Medium" if risk_ratio < 0.65 else "High")

    if credit_score >= 750:
        eligibility_tier = "Tier 1 - Prime"
        interest_rate = 8.5
        recommended_amount = annual_revenue * 3.0
    elif credit_score >= 650:
        eligibility_tier = "Tier 2 - Standard"
        interest_rate = 11.5
        recommended_amount = annual_revenue * 2.0
    elif credit_score >= 500:
        eligibility_tier = "Tier 3 - Subprime"
        interest_rate = 15.0
        recommended_amount = annual_revenue * 1.0
    else:
        eligibility_tier = "Not Eligible"
        interest_rate = 18.0
        recommended_amount = annual_revenue * 0.3

    total_weighted = sum(score * WEIGHTS[k] for k, score in factor_scores.items()) or 1.0

    factor_contributions = [
        {
            "factor": k,
            "label": LABELS.get(k, k),
            "rawScore": round(score * 100, 1),
            "weight": int(WEIGHTS[k] * 100),
            "weightedContribution": round((score * WEIGHTS[k] / total_weighted) * 100, 1),
            "status": "strong" if score >= 0.7 else ("moderate" if score >= 0.4 else "weak")
        }
        for k, score in factor_scores.items()
    ]

    positives = []
    improvements = []
    if repay_score >= 0.75:
        positives.append("Excellent past loan repayment track record")
    elif repay_score < 0.5:
        improvements.append("Improve on-time repayment consistency on existing facilities")

    if rev_score >= 0.6:
        positives.append("Solid revenue generation scale")
    else:
        improvements.append("Increase annual gross turnover to qualify for higher limits")

    if profit_score >= 0.6:
        positives.append("Healthy net profit margins above peer average")
    elif profit_score < 0.4:
        improvements.append("Work on cost optimization to expand net profit margins")

    if debt_score >= 0.7:
        positives.append("Comfortable debt service ability (low debt-to-income)")
    else:
        improvements.append("Reduce short-term liabilities to lower debt-to-income burden")

    if gst_score >= 0.8:
        positives.append("Impeccable GST compliance and timely filings")
    else:
        improvements.append("Ensure 100% on-time GST filing to boost institutional credibility")

    return {
        "creditScore": credit_score,
        "riskCategory": risk_category,
        "eligibilityTier": eligibility_tier,
        "recommendedLoanAmount": int(recommended_amount),
        "interestRate": interest_rate,
        "factorContributions": factor_contributions,
        "positives": positives[:3],
        "improvements": improvements[:3]
    }
