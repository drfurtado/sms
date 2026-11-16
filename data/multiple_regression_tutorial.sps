* ==============================================================.
* SPSS Syntax: Multiple Regression Tutorial
* Dataset: core_session.csv
* Outcome (Y):  sprint_20m_s
* Predictor 1 (X1): vo2_mlkgmin
* Predictor 2 (X2): strength_kg
* ==============================================================.

* --- Step 0: Open the dataset and filter to pre-training ---.
* UPDATE THE FILE PATH BELOW to match your local file location.
* Example: '/Users/yourname/path/to/core_session.csv'.

GET DATA
  /TYPE=TXT
  /FILE='/Users/ovandef/webdev/github/sms/data/core_session.csv'
  /DELIMITERS=","
  /QUALIFIER='"'
  /ARRANGEMENT=DELIMITED
  /FIRSTCASE=2
  /VARIABLES=
    id A4
    group A10
    time A4
    vo2_mlkgmin F8.1
    hr_rest_bpm F8.0
    sprint_20m_s F8.3
    strength_kg F8.1
    agility_ttest_s F8.3
    rpe_6_20 F8.0
    pain_0_10 F8.0
    function_0_100 F8.1
    balance_errors_count F8.0
    age_years F8.1
    sex_category A10
    height_cm F8.1
    mass_kg F8.1
    training_age_years F8.2.
EXECUTE.

* Filter to pre-training time point only.
USE ALL.
COMPUTE filter_$=(time = 'pre').
VARIABLE LABELS filter_$ 'time = "pre" (FILTER)'.
VALUE LABELS filter_$ 0 'Not Selected' 1 'Selected'.
FORMATS filter_$ (f1.0).
FILTER BY filter_$.
EXECUTE.


* ==============================================================.
* PART 1: Scatterplot Matrix
* ==============================================================.

GRAPH
  /SCATTERPLOT(MATRIX) = sprint_20m_s vo2_mlkgmin strength_kg.


* ==============================================================.
* PART 2: Correlation Matrix
* ==============================================================.

CORRELATIONS
  /VARIABLES=sprint_20m_s vo2_mlkgmin strength_kg
  /PRINT=TWOTAIL NOSIG
  /MISSING=PAIRWISE.


* ==============================================================.
* PART 3: Multiple Linear Regression
* (with all options from the tutorial)
* ==============================================================.

REGRESSION
  /DESCRIPTIVES MEAN STDDEV CORR SIG N
  /MISSING LISTWISE
  /STATISTICS COEFF OUTS CI(95) R ANOVA ZPP TOL
  /CRITERIA=PIN(.05) POUT(.10)
  /NOORIGIN
  /DEPENDENT sprint_20m_s
  /METHOD=ENTER vo2_mlkgmin strength_kg
  /SCATTERPLOT=(*ZRESID ,*ZPRED)
  /RESIDUALS NORMPROB
  /SAVE PRED ZPRED ZRESID COOK.


* ==============================================================.
* NOTES:
* 
* The REGRESSION command above produces:
*   - Table 1: Descriptive Statistics (DESCRIPTIVES)
*   - Table 2: Model Summary with R, R², Adj R² (R)
*   - Table 3: ANOVA table (ANOVA)
*   - Table 4: Coefficients with B, SE, Beta, t, Sig, 95% CI,
*              Tolerance, and VIF (COEFF, CI, TOL)
*   - Zero-order, Part, and Partial correlations (ZPP)
*   - ZRESID vs ZPRED scatterplot (residual plot)
*   - Normal P-P Plot of residuals (NORMPROB)
*   - Saved variables: PRE_1 (predicted), ZPR_1 (standardized
*     predicted), ZRE_1 (standardized residual), COO_1 (Cook's D)
*
* After running, you should see these tables/charts in the Output:
*   1. Descriptive Statistics table
*   2. Correlations table (from DESCRIPTIVES, redundant with Part 2)
*   3. Model Summary table
*   4. ANOVA table
*   5. Coefficients table (with Collinearity Statistics columns)
*   6. Scatterplot: ZRESID vs ZPRED
*   7. Normal P-P Plot
* ==============================================================.
