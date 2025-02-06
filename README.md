# Movie Graphs
## Description
Simple program that allows the user to compare different imdb movie stats on a graph and hover on each point to see what movie the point represents.
The Movie Data Comparisons subplot allows the user to get a brief overview of the relationships between 2 movie stats and helps determine if there is any sort of interesting relationship to be investigated. 
<p align="center">
  <img src="/Movie_Data_Comparisons.png" width="600" height="400" class="center">
</p>

For example, in the Rating vs Votes graph, there seems to be a parabolic relationship between the maximum rating a movie could recieve based on the number of votes it has.
The color of the dots shows that there is a positive corelation between the rating and the metascore. 
<p align="center">
<img src="/Rating_vs_Votes%20(Metascore).png" width="600" height="400">
</p>

## Adapting the Code
To change which values are on the x and y axis, change the values of `x_axis` and `y_axis` to the column names of the imdb movie stats database.
The `z_colors` can also be changed to add another dimension to the graph.
The limits for both the x and y axis may need to be adjusted depending on the `x_axis` and `y_axis`. This can be done by adjusting `plt.xlim()` and `plt.ylim()`

```
# Determine x and y values for plot
x_axis = 'Rating'
y_axis = 'Votes'
z_colors = 'Metascore'

-----

plt.xlim(0, 10)
plt.ylim(0)
```

## Acknowledgements
The imdb data used is from [LearnDataSci](https://github.com/LearnDataSci/articles/blob/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv)
