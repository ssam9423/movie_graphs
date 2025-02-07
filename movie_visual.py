"""Visualize Data: IMBD Stats - Samantha Song - Started 2025.02.05"""

# CSV is from LearnDataSci on Github
# Information in CSV:
#   Rank
#   Genre
#   Description
#   Director
#   Actors
#   Year
#   Runtime (min)
#   Rating
#   Votes
#   Revenue (millions)
#   Metascore
#   Name

# Imports
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import scipy.optimize

imdb = pd.read_csv("https://raw.githubusercontent.com/LearnDataSci/articles/refs/heads/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv", index_col="Title")
rows = imdb.shape[0]        # 1,000 Movies
columns = imdb.shape[1]     # 11 types of information

# Plot
# Determine x and y values for plot
x_axis = 'Rating'
y_axis = 'Votes'
z_colors = 'Metascore'

# Remove any nulls in Runtime & Revenue
run_v_rev = imdb[imdb[x_axis].notna()]
run_v_rev = run_v_rev[run_v_rev[y_axis].notna()]
run_v_rev = run_v_rev[run_v_rev[z_colors].notna()]
run_v_rev = run_v_rev.sort_values(by=x_axis)

# Set X, Y & Color Axis
x_vals = run_v_rev[x_axis]
y_vals = run_v_rev[y_axis]
colors = run_v_rev[z_colors]
colors = colors.astype(int)

# Create Scatter Plot & Label Axis
scatter = plt.scatter(x_vals, y_vals, s=10, c=colors, cmap='RdYlGn')
scatter.set_clim(0)

plt.title(x_axis + ' vs. ' + y_axis)
plt.xlabel(x_axis)
plt.ylabel(y_axis)
plt.xlim(0, 10)
plt.ylim(0)
plt.grid()
color_bar = plt.colorbar()
color_bar.ax.set_ylabel(z_colors, rotation=270)
# color_bar.ax.invert_yaxis()   # For rank (lower is better)

# Create Trendline
top_vals = np.array([[0.0, 0.0]])
for rating in range(0, 10):
    # Get movie data for each rating bucket
    sub_rvr = run_v_rev[(run_v_rev[x_axis].between(rating, rating + 1))]
    # Sort according to y_axis to get top 5 y_values for trend line
    sub_rvr = sub_rvr.sort_values(y_axis).tail(5)
    # Sort according to x_axis for plotting
    sub_rvr = sub_rvr.sort_values(x_axis)
    sub_rvr_x = sub_rvr[x_axis].values.reshape(-1, 1)
    sub_rvr_y = sub_rvr[y_axis].values.reshape(-1, 1)
    sub_rvr_x_y = np.append(sub_rvr_x, sub_rvr_y, axis=1)
    top_vals = np.append(top_vals, sub_rvr_x_y, axis=0)

# Exponential Fit
def exp_fit(x, m, t, b):
    return m * np.exp(t * x) + b

fit_x = top_vals[:, 0]
fit_y = top_vals[:, 1]

p0 = (10000, 2, 0)
params, cv = scipy.optimize.curve_fit(exp_fit, fit_x, fit_y, p0)
fit_m, fit_t, fit_b = params

plt.plot(fit_x, exp_fit(fit_x, fit_m, fit_t, fit_b), "b--", label="Trend Line")

# Find Name from x and y
def find_name(x_point, y_point):
    "Get name of movie from x and y coordinates"
    name = run_v_rev[(run_v_rev[x_axis] == x_point) &
                     (run_v_rev[y_axis] == y_point)]
    name_list = list(name.index)
    return name_list[0]

# Annotating Points
crs = mplcursors.cursor(scatter, hover=True)
crs.connect("add", lambda sel: sel.annotation.set_text(find_name(sel.target[0], sel.target[1])))
crs.connect("add", lambda sel: sel.annotation.get_bbox_patch().set(fc="white"))

# Save Figure
folder = 'Movie Plots/'
file_name = x_axis + '_vs_' + y_axis + ' (' + z_colors + ')' + 'Curve Fit'
# plt.savefig(folder + file_name + '.png', dpi=300)

plt.show()


# Create Massive Subplot
# Create axis & subplot and set text size
axis = ['Year', 'Runtime (Minutes)', 'Rating', 'Votes', 'Revenue (Millions)', 'Metascore']
plt.rc('font', size=5)
plt.rc('figure', titlesize=15)
fig, axs = plt.subplots(4, 4)
plot_num = 0    # Used for keeping track of where each subplot is

# For each permutation of 2 axis, create a new subplot
for x_ind, x_ax in enumerate(axis):
    for y_ind, y_ax in enumerate(axis):
        if y_ind < x_ind:
            x = run_v_rev[x_ax]
            y = run_v_rev[y_ax]
            x_plot = int(plot_num / 4)
            y_plot = plot_num % 4
            axs[x_plot, y_plot].scatter(x, y, s=1, c='grey')
            axs[x_plot, y_plot].set_title(x_ax + ' vs ' + y_ax, size=8)
            plot_num += 1

# Adjust subplot and set title
fig.delaxes(axs[3, 3])
fig.suptitle('IMDB Movie Data Comparisons')
plt.subplots_adjust(wspace=0.2, hspace=0.5)
plt.gcf().set_size_inches(12, 8)

# fig.savefig(folder + 'Movie_Data_Comparisons.png', dpi=300)

# Show Figure
plt.show()
