# Titanic Exploratory Data Analysis — Multivariate Interpretations

## Chart 1 — Survival Rate by Sex and Passenger Class

Survival rates vary jointly by sex and passenger class. In the cleaned dataset, female survival rates were 96.74% for first class, 92.11% for second class, and 50.00% for third class, while male survival rates were 36.89%, 15.74%, and 13.54%, respectively. The chart therefore shows substantial differences across the combined sex-and-class groups.

## Chart 2 — Age, Fare, and Survival

The scatter plot examines age and fare while separating passengers by survival outcome. Fare values are widely dispersed, particularly among higher-fare passengers, while age spans a broad range. The plot provides a multivariate view of where survived and non-survived observations occur across the age and fare dimensions.

## Chart 3 — Survival Rate by Family Relationships

The heatmap examines survival rates jointly across `sibsp` and `parch`. The survival rate varies across different combinations of siblings/spouses and parents/children aboard, although some combinations represent relatively small groups. The visualization is therefore useful for identifying patterns in family-relationship combinations while recognizing that cell sizes should be considered when interpreting extreme rates.

## Chart 4 — Family Size, Fare, and Survival

The scatter plot combines calculated family size, fare, and survival outcome. It shows that passengers with different family sizes occur across a wide range of fares and both survival outcomes. The visualization provides a combined view of family structure and fare rather than evaluating either variable independently.