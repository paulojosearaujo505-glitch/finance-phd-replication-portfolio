# Replicating and Extending Fama & French (1993): Evidence from 60 Years of U.S. Equity Returns

**Author:** Paulo Jose Araujo  
**Affiliation:** University of Macau  
**Date:** October 2025

---

## Abstract

This paper replicates and extends the seminal Fama & French (1993) three-factor asset pricing model using U.S. equity data from July 1963 through December 2025. Using the 25 Size/Book-to-Market portfolios and the market, size (SMB), and value (HML) factors, I first reproduce the original findings for the 1963–1991 sample period. Consistent with the original paper, I find that the CAPM produces significant positive alphas for small-cap portfolios, and that adding SMB and HML eliminates these alphas. I then extend the sample to 1992–2025 and find that the model's performance deteriorates: significant alphas reappear for several portfolios, and the average factor loadings decline. A structural break test confirms that the SMB and HML loadings have statistically changed after 1991. These results suggest that while the Fama-French factors remain relevant, the size and value premiums have weakened substantially in the modern era.

---

## 1. Introduction

The Capital Asset Pricing Model (CAPM) of Sharpe (1964) and Lintner (1965) posits that market risk is the sole determinant of expected returns. However, a large body of empirical evidence has documented anomalies—such as the size effect and the value effect—that the CAPM cannot explain. Fama & French (1993) addressed this by introducing a three-factor model that augments the market factor with a size factor (SMB: Small Minus Big) and a value factor (HML: High Minus Low). Using data from 1963–1991, they showed that this model explains a substantial portion of the cross-section of stock returns.

More than three decades have passed since the publication of that paper. The U.S. equity market has undergone profound changes: the rise of technology firms, the globalization of capital markets, and the 2008 financial crisis. This raises a critical question: **Do the Fama-French factors still work in the modern era?**

This paper addresses this question by replicating the original analysis and extending the sample to December 2025. I find that while the model's explanatory power remains high, its ability to eliminate abnormal returns has weakened, and the factor loadings have structurally changed.

---

## 2. Data and Methodology

**Data.** I use the Fama-French 3-Factor data and the 25 Size/Book-to-Market portfolio returns, both obtained from Kenneth French's Dartmouth data library. The data are monthly and span July 1926 to December 2025. The risk-free rate is the one-month Treasury bill rate.

**Methodology.** For each of the 25 portfolios, I estimate the following time-series regression:

$$R_{i,t} - R_{f,t} = \alpha_i + \beta_1(Mkt\text{-}RF)_t + \beta_2(SMB)_t + \beta_3(HML)_t + \epsilon_{i,t}$$

where \(R_{i,t}\) is the portfolio return, \(R_{f,t}\) is the risk-free rate, and Mkt-RF, SMB, and HML are the factor returns. I estimate this model on three samples: the original period (1963–1991), the post-publication period (1992–2025), and three sub-periods: Original (1963–1991), Post-Publication (1992–2007), and Modern (2008–2025). I also perform a structural break test by interacting the factors with a post-1991 dummy variable.

---

## 3. Results

### 3.1 Replication of the Original Sample (1963–1991)

Table 1 (see output folder) reports the average excess return, standard deviation, and Sharpe ratio for the 25 portfolios over the original sample. Consistent with Fama & French (1993), small-cap portfolios exhibit higher average returns and higher volatility than large-cap portfolios. For example, the SMALL LoBM portfolio has an average monthly excess return of 0.32% with a standard deviation of 7.78%, while the BIG HiBM portfolio has an average excess return of 0.53% with a standard deviation of 4.79%.

Table 2 (Part A) reports the CAPM regression results. I find that small-cap portfolios have significant positive alphas. For instance, the ME1 BM2 portfolio has an alpha of 0.0015 (t-stat = 2.04), and the SMALL HiBM portfolio has an alpha of 0.0054 (t-stat = 2.64). These results confirm that the CAPM fails to explain the returns of small-cap portfolios.

Table 2 (Part B) reports the 3-factor regression results. When SMB and HML are added, the alphas shrink dramatically. The SMALL HiBM alpha falls from 0.0054 to 0.0006 (t-stat = 0.88), and the ME1 BM2 alpha falls from 0.0015 to -0.0010 (t-stat = -1.23). The adjusted R-squared increases from 0.69–0.91 (CAPM) to 0.86–0.97 (FF3). These results replicate the central finding of Fama & French (1993): the size and value factors absorb the abnormal returns that the CAPM cannot explain.

### 3.2 Out-of-Sample Extension (1992–2025)

I re-run the 3-factor model on the post-publication period. The results are striking. Significant alphas reappear for several portfolios. The SMALL LoBM portfolio now has a significantly negative alpha of -0.0058 (t-stat = -4.04), indicating the model over-explains small growth stocks. The ME1 BM4 portfolio has a positive alpha of 0.0020 (t-stat = 2.76), and the BIG LoBM portfolio has a positive alpha of 0.0016 (t-stat = 3.36). 

Figure 1 (alpha_comparison.png) plots the alphas from the original and extended samples side-by-side. The visual contrast is stark: the blue bars (original) cluster around zero, while the orange bars (extended) swing widely. The model's ability to explain returns has clearly deteriorated.

### 3.3 Structural Break Analysis

To test whether the factor loadings have statistically changed, I estimate a regression with interaction terms between the factors and a post-1991 dummy variable, using the SMALL HiBM portfolio as a representative case. The results are presented in Table 3. 

The interaction terms are highly significant: the Dummy_SMB coefficient is -0.3477 (t-stat = -7.19), and the Dummy_HML coefficient is -0.1829 (t-stat = -4.19). Both are significant at the 1% level. This provides formal statistical evidence that the sensitivity of small-cap value stocks to the size and value factors has fundamentally changed after 1991.

Figure 2 (rolling_betas.png) visualizes this break. The rolling 5-year SMB beta declines from an average of 1.5 in the original period to around 1.0 in the modern era, while the HML beta drops from 1.0 to around 0.6. The visual evidence corroborates the statistical test.

### 3.4 Sub-Period Analysis

I split the full sample into three periods: Original (1963–1991), Post-Publication (1992–2007), and Modern (2008–2025). Table 4 reports the average absolute alpha, the number of significant alphas, and the average factor loadings for each period.

The average absolute alpha increases from 0.0009 in the original period to 0.0018 in the post-publication period, then declines slightly to 0.0010 in the modern era. The number of portfolios with significant alphas (|t| > 2) follows a similar hump-shaped pattern. The average SMB loading declines from 0.9 (original) to 0.5 (modern), while the HML loading declines from 0.9 to 0.6. These results suggest that the factor premiums have weakened, and the model's performance is non-monotonic across regimes.

### 3.5 Cumulative Factor Returns

Figure 3 (cumulative_factors.png) plots the cumulative returns of the SMB and HML factors from 1926 to 2025, with shaded regions for each sub-period. The SMB (size) premium grows steadily until 1991, then flattens out completely. An investor who bet on small-cap stocks over the last 30 years would have earned essentially zero excess return. The HML (value) premium continues to grow until 2007, but then experiences massive drawdowns, particularly after 2020. This visual evidence strongly supports the narrative of factor decay.

---

## 4. Conclusion

This paper replicates and extends Fama & French (1993). I confirm that the 3-factor model successfully explains the cross-section of returns in the original 1963–1991 sample. However, when I extend the analysis to 2025, I find that significant alphas reappear, factor loadings decline, and the model's performance deteriorates. A structural break test confirms that these changes are statistically significant.

These findings do not invalidate the Fama-French model, but they suggest that the size and value premiums have weakened over time. This is consistent with recent literature arguing that factor premiums are time-varying and may be arbitraged away as they become widely known. Future research could explore whether alternative factor definitions (e.g., using different breakpoints) or additional factors (e.g., profitability, investment) can restore the model's explanatory power in the modern era.

---

## References

- Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33(1), 3–56.
- Lintner, J. (1965). The valuation of risk assets and the selection of risky investments in stock portfolios and capital budgets. *The Review of Economics and Statistics*, 47(1), 13–37.
- Sharpe, W. F. (1964). Capital asset prices: A theory of market equilibrium under conditions of risk. *The Journal of Finance*, 19(3), 425–442.