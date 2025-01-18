Change this code accordingly to have circular markers on it 

def comma_format(x, pos):
    return f'{x:,.0f}'

# Rename columns for clarity
pjme_all = pjme_all.rename(columns={
    'MW_Prediction': 'Prediction',
    'PJME_MW': 'Actual'
})

# Plot the forecast with the actuals
f, ax = plt.subplots(1)
f.set_figheight(5)
f.set_figwidth(15)

pjme_all[['Prediction', 'Actual']].plot(
    ax=ax,
    style=['-', '-'],
    alpha=0.7,  # Set transparency
    linewidth=3,  # Set thinner line width
    color=['#300FF0', '#F0300F']  # Set custom colors for Prediction and Actual
)

ax.set_xbound(lower='08-08-2016', upper='08-10-2016')
ax.set_ylim(0, 60000)

# Add comma delineation to y-axis
ax.yaxis.set_major_formatter(FuncFormatter(comma_format))

# Add y-axis label
ax.set_ylabel('Energy Usage (Megawatts)')

# Add plot title
plot = plt.suptitle('August 8th - August 10th, Best Prediction Days, Prediction vs Actuals')

plt.show()
