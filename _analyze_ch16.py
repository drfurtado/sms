import pandas as pd
import numpy as np
from scipy import stats
import pingouin as pg
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

ch16 = pd.read_csv('data/core_session_ch16.csv')
N = len(ch16)

# ── PART A ────────────────────────────────────────────────────────────────────
print("=" * 60)
print("PART A: 2×2 Between-Subjects ANOVA  (sex_category × group)")
print("Outcome: strength_post")
print("=" * 60)

print("\nCell counts:")
print(ch16.groupby(['sex_category','group']).size().to_string())

model = smf.ols('strength_post ~ C(sex_category, Sum) * C(group, Sum)', data=ch16).fit()
aov3 = anova_lm(model, typ=3)

SS_err  = aov3.loc['Residual','sum_sq']
df_err  = int(aov3.loc['Residual','df'])
MS_err  = SS_err / df_err

effects = [
    ('sex_category',  'C(sex_category, Sum)'),
    ('group',         'C(group, Sum)'),
    ('interaction',   'C(sex_category, Sum):C(group, Sum)'),
]

rows = []
for label, key in effects:
    ss = aov3.loc[key,'sum_sq']
    df = int(aov3.loc[key,'df'])
    ms = ss / df
    F  = aov3.loc[key,'F']
    p  = aov3.loc[key,'PR(>F)']
    eta2p   = ss / (ss + SS_err)
    omega2p = (ss - df * MS_err) / (ss + (N - df) * MS_err)
    rows.append({'Source': label, 'SS': round(ss,2), 'df': df,
                 'MS': round(ms,2), 'F': round(F,3), 'p': round(p,4),
                 'eta2p': round(eta2p,4), 'omega2p': round(omega2p,4)})

# Intercept row for completeness
int_ss = aov3.loc['Intercept','sum_sq']
int_df = int(aov3.loc['Intercept','df'])
int_F  = aov3.loc['Intercept','F']
int_p  = aov3.loc['Intercept','PR(>F)']
rows.insert(0, {'Source':'Intercept','SS':round(int_ss,2),'df':int_df,
                'MS':round(int_ss/int_df,2),'F':round(int_F,2),'p':round(int_p,4),
                'eta2p':'','omega2p':''})
rows.append({'Source':'Error','SS':round(SS_err,2),'df':df_err,
             'MS':round(MS_err,2),'F':'','p':'','eta2p':'','omega2p':''})

# Model SS
model_ss = sum(aov3.loc[k,'sum_sq'] for _,k in effects)
total_ss = model_ss + SS_err
rows.append({'Source':'Total','SS':round(total_ss,2),'df':N,'MS':'','F':'','p':'','eta2p':'','omega2p':''})

print(pd.DataFrame(rows).to_string(index=False))

# Levene
groups_lev = [g['strength_post'].dropna().values for _, g in ch16.groupby(['sex_category','group'])]
lev_stat, lev_p = stats.levene(*groups_lev)
print(f"\nLevene: F={lev_stat:.3f}, df1=3, df2={N-4}, p={lev_p:.4f}")

print("\nMarginal means (group):")
print(ch16.groupby('group')['strength_post'].agg(['mean','std']).round(2).to_string())
print("\nMarginal means (sex):")
print(ch16.groupby('sex_category')['strength_post'].agg(['mean','std']).round(2).to_string())
print("\nCell means:")
print(ch16.groupby(['sex_category','group'])['strength_post'].agg(['mean','std','count']).round(2).to_string())

# ── PART B ────────────────────────────────────────────────────────────────────
print()
print("=" * 60)
print("PART B: Mixed ANOVA  (Group × Time)")
print("=" * 60)

long = ch16.melt(id_vars=['id','group','sex_category'],
                 value_vars=['strength_pre','strength_mid','strength_post'],
                 var_name='time', value_name='strength')
long['time'] = long['time'].str.replace('strength_','')

aov_b = pg.mixed_anova(data=long, dv='strength', within='time', between='group', subject='id')
print(aov_b[['Source','SS','DF1','DF2','MS','F','p_unc','np2','W_spher','p_spher','eps']].round(4).to_string())

time_row    = aov_b[aov_b['Source']=='time'].iloc[0]
group_row   = aov_b[aov_b['Source']=='group'].iloc[0]
int_row     = aov_b[aov_b['Source']=='Interaction'].iloc[0]

MS_within_error   = time_row['MS'] / time_row['F']
SS_within_error   = MS_within_error * int(time_row['DF2'])
df_within_error   = int(time_row['DF2'])

MS_between_error  = group_row['MS'] / group_row['F']
SS_between_error  = MS_between_error * int(group_row['DF2'])
df_between_error  = int(group_row['DF2'])

print(f"\nWithin-subjects error: SS={SS_within_error:.2f}, df={df_within_error}, MS={MS_within_error:.4f}")
print(f"Between-subjects error: SS={SS_between_error:.2f}, df={df_between_error}, MS={MS_between_error:.4f}")

print(f"\nMauchly's W={time_row['W_spher']:.3f}, p={time_row['p_spher']:.4f}, GG_eps={time_row['eps']:.3f}")

# GG-corrected df
df1_gg = round(int(time_row['DF1']) * time_row['eps'], 2)
df2_gg = round(int(time_row['DF2']) * time_row['eps'], 2)
df1_int_gg = round(int(int_row['DF1']) * time_row['eps'], 2)
df2_int_gg = round(int(int_row['DF2']) * time_row['eps'], 2)
print(f"GG corrected df (Time): {df1_gg}, {df2_gg}")
print(f"GG corrected df (Interaction): {df1_int_gg}, {df2_int_gg}")

# Group means across time
print("\nMeans by group × time:")
print(long.groupby(['group','time'])['strength'].agg(['mean','std']).round(2).to_string())

# Simple effects
train = long[long['group']=='training']
rm_train = pg.rm_anova(data=train, dv='strength', within='time', subject='id', detailed=True)
print("\nSimple effects — Training group:")
print(rm_train[['Source','SS','DF','MS','F','p-unc','np2']].round(4).to_string())

ctrl = long[long['group']=='control']
rm_ctrl = pg.rm_anova(data=ctrl, dv='strength', within='time', subject='id', detailed=True)
print("\nSimple effects — Control group:")
print(rm_ctrl[['Source','SS','DF','MS','F','p-unc','np2']].round(4).to_string())

# Bonferroni pairwise — training
pw = pg.pairwise_tests(data=train, dv='strength', within='time', subject='id', padjust='bonferroni')
print("\nBonferroni pairwise (training):")
print(pw[['A','B','mean(A)','mean(B)','T','dof','p_corr','cohen']].round(3).to_string())
